from django.db import models
from django.utils import timezone
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)

from users.models import User


def validate_year(value):
    current_year = timezone.now().year
    if current_year < value:
        raise models.ValidationError(f"Год выпуска больше {current_year}")


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name="Категория")
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name="URL",
        validators=[
            RegexValidator(
                regex="^[-a-zA-Z0-9_]+$",
                message=(
                    "Slug может содержать только латинские буквы, "
                    "цифры, дефисы и подчеркивания."
                ),
            )
        ],
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name="Жанр")
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name="URL",
        validators=[
            RegexValidator(
                regex="^[-a-zA-Z0-9_]+$",
                message=(
                    "Slug может содержать только латинские буквы, "
                    "цифры, дефисы и подчеркивания."
                ),
            )
        ],
    )


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name="Произведение")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="categories",
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="Жанр",
    )
    description = models.TextField(
        blank=True, verbose_name="Описание"
    )
    year = models.PositiveIntegerField(validators=[validate_year])


class Review(models.Model):
    text = models.TextField("Текст отзыва")
    score = models.IntegerField("Оценка",
        validators=[
            MaxValueValidator(10, 'Значение должно быть до 10'),
            MinValueValidator(1, 'Значение должно быть от 1')
        ]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="uniq_review"
            )
        ]


class Сomment(models.Model):
    text = models.TextField("Текст коментария")
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("pub_date",)
