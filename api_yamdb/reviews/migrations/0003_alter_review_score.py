# Generated by Django 3.2 on 2023-08-13 11:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0002_alter_review_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="score",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MaxValueValidator(
                        10, "Значение должно быть до 10"
                    ),
                    django.core.validators.MinValueValidator(
                        1, "Значение должно быть от 1"
                    ),
                ],
                verbose_name="Оценка",
            ),
        ),
    ]
