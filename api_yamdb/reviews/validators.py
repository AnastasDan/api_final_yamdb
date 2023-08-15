from django.db import models
from django.utils import timezone


def validate_year(value):
    current_year = timezone.now().year
    if current_year < value:
        raise models.ValidationError(f"Год выпуска больше {current_year}")
