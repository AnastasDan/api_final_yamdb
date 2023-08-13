from rest_framework import serializers

from reviews.models import Category, Genre, Review, Title, Сomment
from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "email",
            "username",
        )
        model = User

    def validate(self, data):
        username = data.get("username")
        if username == "me":
            raise serializers.ValidationError("Использовать имя me запрещено.")
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User

    def validate(self, data):
        username = data.get("username")
        if username == "me":
            raise serializers.ValidationError("Использовать имя me запрещено.")
        return data


class СommentsSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field="text",
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = "__all__"
        model = Сomment


class ReviewsSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = "__all__"
        model = Review

    def validate(self, data):
        if not self.context.get("request").method == "POST":
            return data
        author = self.context.get("request").user
        title_id = self.context.get("view").kwargs.get("title_id")
        existing_reviews = Review.objects.filter(author=author, title=title_id)
        if existing_reviews.exists():
            raise serializers.ValidationError(
                "Пользователь уже оставил отзыв на это произведение."
            )
        return data


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)

    class Meta:
        fields = (
            "name",
            "slug",
        )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)

    class Meta:
        exclude = ("id",)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, queryset=Genre.objects.all(), slug_field="slug"
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class TitleGETSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title
