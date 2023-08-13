from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUser(BasePermission):
    """Пользователь с правами администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff
            or request.user.role == "admin"
            or request.user.is_superuser
        )


class IsReviewAuthorOrModeratorOrAdmin(BasePermission):
    """
    Право доступа, позволяющее автору отзыва, модератору или администратору
    выполнять операции.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.role == "moderator"
            or request.user.role == "admin"
            or obj.author == request.user
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Право доступа, позволяющее только администраторам редактировать объекты.
    Остальным предоставляется только доступ на чтение.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.role == "admin"
                or request.user.is_superuser
            )
        )
