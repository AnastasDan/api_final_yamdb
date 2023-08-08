from rest_framework import serializers

from .models import Reviews, Сomments


class СommentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Сomments


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Reviews
