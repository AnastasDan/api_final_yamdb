from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Reviews(models.Model):
    text = models.TextField("Текст отзыва")
    mark = models.IntegerField()
    titles = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("created_at",)


class Сomments(models.Model):
    text = models.TextField("Текст коментария")
    reviews = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ("created_at",)
