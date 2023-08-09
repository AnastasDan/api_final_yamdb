from django.urls import path
from .views import SignupView, CustomTokenObtainPairView

urlpatterns = [
    path(
        "v1/auth/signup/",
        SignupView.as_view({"post": "create"}),
        name="signup",
    ),
    path(
        "v1/auth/token/",
        CustomTokenObtainPairView.as_view({"post": "create"}),
        name="token",
    ),
]
