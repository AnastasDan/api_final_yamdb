from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User

from .permissions import IsAdminUser, IsReviewAuthorOrModeratorOrAdmin
from .serializers import (
    SignupSerializer,
    TokenSerializer,
    UserSerializer,
    ReviewsSerializer,
    СommentsSerializer,
)
from .utils import send_confirmation_email
from reviews.models import Reviews, Сomments


class SignupView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = SignupSerializer(data=request.data)

        if not serializer.is_valid() and not User.objects.filter(
            username=request.data.get("username"),
            email=request.data.get("email"),
        ):
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        user, _ = User.objects.get_or_create(**serializer.data)
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_email(
            email=user.email, confirmation_code=confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")

        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {"Ошибка": "Неверные данные"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        access_token = str(AccessToken.for_user(user))
        return Response(
            {"token": access_token}, status=status.HTTP_201_CREATED
        )


class UserViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def get_self_account(self, request):
        user = request.user
        if request.method == "PATCH":
            if "role" in request.data and user.role != "admin":
                return Response(
                    {"detail": "У вас недостаточно прав для изменения роли."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get", "patch", "delete"],
        url_path=r"(?P<username>[\w.@+-]+)",
    )
    def get_username(self, request, username=None):
        user = get_object_or_404(User, username=username)
        if request.method == "PATCH":
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            user.delete()
            return Response(
                {"Сообщение": "Пользователь успешно удален"},
                status=status.HTTP_204_NO_CONTENT,
            )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class СommentsViewSet(viewsets.ModelViewSet):
    queryset = Сomments.objects.all()
    serializer_class = СommentsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsReviewAuthorOrModeratorOrAdmin,
    )


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsReviewAuthorOrModeratorOrAdmin,
    )
