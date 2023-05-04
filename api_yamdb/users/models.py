from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    """Роли пользователей."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """Модель пользователя."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_superuser:
            self.role = UserRole.ADMIN

    email = models.EmailField(verbose_name='Электронная почта',
                              max_length=254,
                              unique=True
                              )
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(verbose_name='Роль пользователя',
                            max_length=9,
                            choices=UserRole.choices,
                            default=UserRole.USER
                            )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == UserRole.USER

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    def __str__(self):
        return self.username
