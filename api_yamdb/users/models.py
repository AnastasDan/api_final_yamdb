from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .enums import UserRole
from .constants import USERNAME_REGEX


class User(AbstractUser):
    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(regex=USERNAME_REGEX, message="Недопустимый символ")
        ],
    )
    email = models.EmailField("email", max_length=254, unique=True)
    role = models.CharField(
        "Роль",
        max_length=15,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    bio = models.TextField("Биография", blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_user(self):
        return self.role == UserRole.USER

    def __str__(self):
        return self.username
