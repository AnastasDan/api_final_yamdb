from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Категория')
    slug = models.SlugField(unique=True, verbose_name='URL')


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Жанр')
    slug = models.SlugField(unique=True, verbose_name='URL')


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='Произведение')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Категория')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='Жанр')
    year = models.PositiveIntegerField()




