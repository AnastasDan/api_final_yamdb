from django.urls import include, path

from rest_framework import routers

from .views import (
    CategoryViewSet,
    CommentsViewSet,
    CustomTokenObtainPairView,
    GenreViewSet,
    ReviewsViewSet,
    SignupView,
    TitleViewSet,
    UserViewSet
)

router_v1 = routers.DefaultRouter()
router_v1.register(r"users", UserViewSet, basename="users")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewsViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentsViewSet,
    basename="reviews",
)
router_v1.register(r"categories", CategoryViewSet, basename="categories")
router_v1.register(r"genres", GenreViewSet, basename="genres")
router_v1.register(r"titles", TitleViewSet, basename="titles")


auth_urls = [
    path("signup/", SignupView.as_view(), name="signup"),
    path(
        "token/",
        CustomTokenObtainPairView.as_view({"post": "create"}),
        name="token",
    ),
]

urlpatterns = [
    path("v1/auth/", include(auth_urls)),
    path("v1/", include(router_v1.urls)),
]
