from rest_framework import serializers

from users.models import User
from reviews.models import Review, Сomment, Category, Genre, Title


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


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.RegexField(regex="^[-a-zA-Z0-9_]+$", max_length=50)

    class Meta:
        fields = (
            "name",
            "slug",
        )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.RegexField(regex="^[-a-zA-Z0-9_]+$", max_length=50)

    class Meta:
        fields = "__all__"
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
