from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):

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
