from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from users.constants import (LIMIT_EMAIL, LIMIT_NAME, LIMIT_PASSWORD,
                             LIMIT_USERNAME)
from users.validators import username_validation


class User(AbstractUser):
    email = models.EmailField(
        max_length=LIMIT_EMAIL,
        unique=True,
        blank=False,
        verbose_name='Электронная почта'
    )
    username = models.CharField(
        max_length=LIMIT_USERNAME,
        blank=False,
        unique=True,
        verbose_name='Логин',
        validators=[
            username_validation
        ]
    )
    first_name = models.CharField(
        max_length=LIMIT_NAME,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=LIMIT_NAME,
        blank=False,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=LIMIT_PASSWORD,
        blank=False,
        verbose_name='Пароль'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        verbose_name='Аватар'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'last_name', 'first_name']


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def clean(self):
        if self.user == self.following:
            raise ValidationError('Нельзя подписаться на самого себя')

    def __str__(self):
        return 'Подписки'
