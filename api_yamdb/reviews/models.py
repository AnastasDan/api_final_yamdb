from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    validate_slug,
)
from django.db import models

from users.models import User

from .constants import MAX_LENGTH_50, MAX_LENGTH_256
from .validators import validate_year


class BaseSlugModel(models.Model):
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LENGTH_50,
        verbose_name="URL",
        validators=[
            validate_slug,
        ],
    )

    class Meta:
        abstract = True


class Category(BaseSlugModel):
    name = models.CharField(
        max_length=MAX_LENGTH_256, verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Genre(BaseSlugModel):
    name = models.CharField(max_length=MAX_LENGTH_256, verbose_name="Жанр")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_256, verbose_name="Произведение"
    )
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
    description = models.TextField(blank=True, verbose_name="Описание")
    year = models.PositiveIntegerField(
        db_index=True, validators=[validate_year]
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("id",)


class Review(models.Model):
    text = models.TextField("Текст отзыва")
    score = models.PositiveSmallIntegerField(
        "Оценка",
        validators=[
            MaxValueValidator(10, "Значение должно быть до 10"),
            MinValueValidator(1, "Значение должно быть от 1"),
        ],
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="uniq_review"
            )
        ]


class Comment(models.Model):
    text = models.TextField("Текст комментария")
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("pub_date",)
