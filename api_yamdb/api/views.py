from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, Сomment
from users.models import User

from .filters import TitleFilter
from .permissions import (
    IsAdminOrReadOnly,
    IsAdminUser,
    IsReviewAuthorOrModeratorOrAdmin
)
from .serializers import (
    CategorySerializer,
    CommentsSerializer,
    GenreSerializer,
    ReviewsSerializer,
    SignupSerializer,
    TitleGETSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer
)
from .utils import send_confirmation_email


class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        username = request.data.get("username")

        existing_user = User.objects.filter(
            email=email, username=username
        ).first()
        if existing_user:
            confirmation_code = default_token_generator.make_token(
                existing_user
            )
            send_confirmation_email(
                email=existing_user.email, confirmation_code=confirmation_code
            )
            return Response(
                {"detail": "Код подтверждения отправлен заново."},
                status=status.HTTP_200_OK,
            )

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
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
        return Response({"token": access_token}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = "username"
    search_fields = ("username",)
    http_method_names = ("get", "post", "delete", "patch")

    @action(
        detail=False,
        methods=("get", "patch"),
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def users_profile(self, request):
        user = request.user
        if request.method == "PATCH":
            if "role" in request.data and not request.user.is_admin:
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


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Сomment.objects.all()
    serializer_class = CommentsSerializer
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
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).order_by(
        "-rating"
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return TitleSerializer
        return TitleGETSerializer
