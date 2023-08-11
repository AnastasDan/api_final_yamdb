from django.urls import include, path

from rest_framework import routers

from .views import (
    CustomTokenObtainPairView,
    SignupView,
    UserViewSet,
    ReviewsViewSet,
    СommentsViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewsViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/review/(?P<review_id>\d+)/comments",
    СommentsViewSet,
    basename="reviews",
)


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
