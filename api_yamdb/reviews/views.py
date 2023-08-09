from rest_framework import viewsets, permissions

from .models import Reviews, Сomments
from .serializers import СommentsSerializer, ReviewsSerializer


class СommentsViewSet(viewsets.ModelViewSet):
    queryset = Сomments.objects.all()
    serializer_class = СommentsSerializer
    permission_classes = permissions.IsAuthenticatedOrReadOnly


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = permissions.IsAuthenticatedOrReadOnly
