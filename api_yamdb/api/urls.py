from django.urls import include, path

from rest_framework import routers

from .views import CustomTokenObtainPairView, SignupView, UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)


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
    path("v1/", include(router.urls)),
]
