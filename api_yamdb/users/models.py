from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    ROLE_CHOICES = [
        ("user", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Администратор"),
    ]

    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(regex=r"^[\w.@+-]+$", message="Недопустимый символ")
        ],
    )
    email = models.EmailField("email", max_length=254, unique=True)
    role = models.CharField(
        "Роль",
        max_length=15,
        choices=ROLE_CHOICES,
        default="user",
    )
    bio = models.TextField("Биография", blank=True)

    def __str__(self):
        return self.username
