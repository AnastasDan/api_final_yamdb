from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Категория")
    slug = models.SlugField(unique=True, verbose_name="URL")


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name="Жанр")
    slug = models.SlugField(unique=True, verbose_name="URL")


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name="Произведение")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Категория",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="genres",
        verbose_name="Жанр",
    )
    year = models.PositiveIntegerField()


class Reviews(models.Model):
    text = models.TextField("Текст отзыва")
    score = models.IntegerField()
    titles = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("pub_date",)


class Сomments(models.Model):
    text = models.TextField("Текст коментария")
    reviews = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("pub_date",)
