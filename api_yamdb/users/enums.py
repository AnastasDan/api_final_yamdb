from enum import Enum


class UserRole(Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    @classmethod
    def choices(cls):
        return [
            (role.value, role.name.replace("_", " ").title()) for role in cls
        ]
