from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import СommentsViewSet, ReviewsViewSet

router = SimpleRouter()
router.register("reviews", ReviewsViewSet, basename="reviews")
router.register("comments", СommentsViewSet, basename="comments")

urlpatterns = [
    path("", include(router.urls)),
]
