from django.urls import include, path

from rest_framework import routers

from .views import (
    CustomTokenObtainPairView,
    SignupView,
    UserViewSet,
    ReviewsViewSet,
    СommentsViewSet,
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewsViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    СommentsViewSet,
    basename="reviews",
)
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"titles", TitleViewSet, basename="titles")


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
