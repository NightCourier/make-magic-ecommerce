from rest_framework import serializers

from src.api.models import Rating


class CreateRatingSerializer(serializers.ModelSerializer):
    """Adding rating by user"""

    class Meta:
        model = Rating
        fields = ("star", "content_type", "object_id", "content_object")

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get("ip", None),
            content_type=validated_data.get("content_type", None),
            object_id=validated_data.get("object_id", None),
            defaults={'star': validated_data.get("star")}
        )
        return rating