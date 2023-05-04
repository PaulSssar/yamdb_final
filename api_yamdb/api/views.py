from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly
                                        )
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title

from api.permissions import (IsSuperUserOrIsAdmin,
                             IsSuperUserOrIsAdminOrReadOnly,
                             IsAuthOrSuperUserOrModOrAdminOrReadOnly
                             )
from api.serializers import (AuthUserSerializer, CategoriesSerializer,
                             CommentsSerializer, GenresSerializer,
                             ReviewsSerializer, TitlesGetSerializer,
                             TitlesSerializer, TokenUserSerializer,
                             UserSerializer)
from api.utils import send_confirmation_code

from users.models import User

from .filters import TitleFilter
from .pagination import PagePaginations


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsSuperUserOrIsAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)'
    )
    def get_user_by_username(self, request, username):
        """Метод получает/редактирует данные пользователя по его username."""
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            message = f'Пользователь {user} удален.'
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def get_profile(self, request):
        """Метод получает/редактирует данные своей учетной записи."""
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    """Функция регистрации пользователя."""
    serializer = AuthUserSerializer(data=request.data)
    if User.objects.filter(username=request.data.get('username'),
                           email=request.data.get('email')).exists():
        existing_user = User.objects.get(email=request.data.get('email'))
        send_confirmation_code(existing_user)
        return Response(request.data, status=status.HTTP_200_OK)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token_for_user(request):
    """Функция получения токена."""
    serializer = TokenUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        message = 'не правильный код подтверждения'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    access_token = AccessToken.for_user(user)
    message = {'token': str(access_token)}
    return Response(message, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Title."""
    queryset = Title.objects.all()
    search_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrIsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, )
    filterset_class = TitleFilter

    def get_queryset(self):
        queryset = (Title.objects.annotate(rating=Avg('title__score')).
                    order_by('-rating'))
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesGetSerializer
        return TitlesSerializer


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin):
    """Вьюсет модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrIsAdminOrReadOnly, )
    lookup_field = 'slug'


class GenreViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin):
    """Вьюсет модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsSuperUserOrIsAdminOrReadOnly, )
    lookup_field = 'slug'


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Review."""
    serializer_class = ReviewsSerializer
    pagination_class = PagePaginations
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthOrSuperUserOrModOrAdminOrReadOnly, )

    def select_objects(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        titles = self.select_objects()
        return titles.title.all()

    def perform_create(self, serializer):
        new = self.select_objects()
        serializer.save(author=self.request.user, title=new)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Comment."""
    serializer_class = CommentsSerializer
    pagination_class = PagePaginations
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthOrSuperUserOrModOrAdminOrReadOnly, )

    def select_objects(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        rev = self.select_objects()
        return rev.review.all()

    def perform_create(self, serializer):
        new = self.select_objects()
        serializer.save(author=self.request.user, review=new)
