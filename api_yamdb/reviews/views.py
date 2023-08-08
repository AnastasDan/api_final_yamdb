from rest_framework import viewsets

from .models import Reviews, Сomments
from .serializers import СommentsSerializer, ReviewsSerializer


class СommentsViewSet(viewsets.ModelViewSet):
    queryset = Сomments.objects.all()
    serializer_class = СommentsSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
