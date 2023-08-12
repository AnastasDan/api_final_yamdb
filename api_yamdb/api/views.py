from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Avg

from users.models import User

from .permissions import (
    IsAdminUser,
    IsReviewAuthorOrModeratorOrAdmin,
    IsAdminOrReadOnly,
)
from .serializers import (
    SignupSerializer,
    TokenSerializer,
    UserSerializer,
    ReviewsSerializer,
    СommentsSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)
from .utils import send_confirmation_email
from reviews.models import Review, Сomment, Category, Genre, Title


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
    queryset = Сomment.objects.all()
    serializer_class = СommentsSerializer
    permission_classes = (IsReviewAuthorOrModeratorOrAdmin,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        author = self.request.user
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=author, review=review)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (IsReviewAuthorOrModeratorOrAdmin,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        author = self.request.user
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=author, title=title)


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "titles_id"
