from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(
        max_length=256,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("-name",)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("-name",)

    def __str__(self):
        return self.name


def validate_year(value):
    """Валидация года."""
    if value > datetime.now().year:
        raise ValidationError('Мы ещё не в будущем!')
    elif value < 0:
        raise ValidationError('Запрещены отрицательные значения!')


class Title(models.Model):
    """Модель произведений."""
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='titles',
    )
    name = models.CharField(max_length=256)
    year = models.IntegerField(
        verbose_name='Год создания',
        validators=[validate_year]
    )
    description = models.TextField(verbose_name='Описание', )
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведении"
        ordering = ("-year",)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель обзоров."""
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews_author',
        verbose_name="Автор"
    )
    score = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(10)],
                                verbose_name="Оценка"
                                )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title',
        verbose_name="Произведение"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("-pub_date",)
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        )

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Модель комментариев."""
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment_author',
        verbose_name="Автор"
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name="Отзыв", related_name='review',
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text
