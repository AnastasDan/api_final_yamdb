# from enum import Enum
from django.db import models


# class UserRole(Enum):
#     USER = "user"
#     MODERATOR = "moderator"
#     ADMIN = "admin"

#     @classmethod
#     def choices(cls):
#         return [
#             (role.value, role.name.replace("_", " ").title()) for role in cls
#         ]

class UserRole(models.TextChoices):
    USER = "user", "User"
    MODERATOR = "moderator", "Moderator"
    ADMIN = "admin", "Admin"
