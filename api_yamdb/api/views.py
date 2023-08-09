from rest_framework import mixins, viewsets
from django.contrib.auth.tokens import default_token_generator
from users.models import User
from .utils import send_confirmation_email
from .serializers import (
    TokenSerializer,
    UserSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny


class SignupView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid() and not User.objects.filter(
            username=serializer.data['username'],
            email=serializer.data['email']
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

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(username=serializer.validated_data["username"])
        confirmation_code = serializer.validated_data["confirmation_code"]

        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {"Ошибка": "Неверные данные"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        access_token = str(AccessToken.for_user(user))
        return Response(
            {"token": access_token}, status=status.HTTP_201_CREATED
        )
