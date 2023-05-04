from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework import serializers

from reviews.models import Category, Comments, Genre, Review, Title

from users.models import User


class AuthUserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            message = "Использовать имя 'me' запрещено"
            raise serializers.ValidationError(message)
        return data


class TokenUserSerializer(serializers.ModelSerializer):
    """Сериализатор получиения токена JWT."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role'
                  )


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        exclude = ('id', )
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title, POST."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=False
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        many=False,
        slug_field='slug',
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category'
                  )
        model = Title

    def validate_year(self, data):
        """Валидация года."""
        if data > datetime.now().year:
            raise serializers.ValidationError('Мы ещё не в будущем!')
        elif data < 0:
            raise serializers.ValidationError('Запрещены отрицательные',
                                              'значения!'
                                              )
        return data


class TitlesGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title, GET."""
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()
    rating = serializers.IntegerField(required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title
        read_only_fields = ('id', 'name', 'year', 'rating', 'description',
                            'genre', 'category')


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        """Валидация на уникальность и оценки."""
        if 'POST' in self.context.get('request').method:
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            author = self.context.get('request').user
            if Review.objects.filter(author=author, title=title).exists():
                raise serializers.ValidationError(
                    'Один пользователь, один отзыв!'
                )
        if data['score'] > 11 or data['score'] < 0:
            raise serializers.ValidationError(
                'Оценка только от 1 до 10!'
            )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
