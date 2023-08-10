from django.db import models

from user.models import User


class Reviews(models.Model):
    text = models.TextField("Текст отзыва")
    score = models.IntegerField()
    titles = models.ForeignKey(
        Titles,
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
