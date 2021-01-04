from rest_framework import serializers

from src.api.models import RubiksCube
from src.api.serializers.review import ReviewSerializer

"""Сериалайзеры нужны для того, чтобы преобразовывать типы данных Python в JSON и наоборот.
К примеру: забирая фильмы из базы данных мы получаем QuerySet, далее мы представляем это в виде JSON и 
отрпавляем на клиентскую сторону. Для этого на помощь приходят сериализаторы. Они очень похожи на djangoForms,
мы также выбираем модель и поля"""


class RubiksCubeListSerializer(serializers.ModelSerializer):
    """List of Rubik's Cubes"""

    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = RubiksCube
        fields = ("id", "title", "price", "category", "rating_user", "middle_star")


class RubiksCubeDetailSerializer(serializers.ModelSerializer):
    """Full info for product"""

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    review = ReviewSerializer(many=True)

    class Meta:
        model = RubiksCube
        fields = "__all__"

