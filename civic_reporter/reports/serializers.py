from rest_framework import serializers

from .models import Area, Category


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ["id", "name", "location"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "type"]
