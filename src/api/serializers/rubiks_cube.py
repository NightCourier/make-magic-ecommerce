from rest_framework import serializers

from src.api.models import Category, RubiksCube, Cart, CartProduct

"""Сериалайзеры нужны для того, чтобы преобразовывать типы данных Python в JSON и наоборот.
К примеру: забирая фильмы из базы данных мы получаем QuerySet, далее мы представляем это в виде JSON и 
отрпавляем на клиентскую сторону. Для этого на помощь приходят сериализаторы. Они очень похожи на djangoForms,
мы также выбираем модель и поля"""


# class FilterReviewListSeializer(serializers.ListSerializer):
#     """Filter for comments, only parents"""
#     def to_representation(self, data):
#         data = data.filter(parent=None)
#         return super().to_representation(data)


# class RecursiveSerializer(serializers.Serializer):
#     """Recursive output for children"""
#     def to_representation(self, value):
#         serializer = self.parent.parent.__class__(value, context=self.context)
#         return serializer.data


class RubiksCubeListSerializer(serializers.ModelSerializer):
    """List of Rubik's Cubes"""

    class Meta:
        model = RubiksCube
        fields = ("title", "price", "category")


class RubiksCubeDetailSerializer(serializers.ModelSerializer):
    """Full info for product"""

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    # reviews = ReviewSerializer(many=True)

    class Meta:
        model = RubiksCube
        fields = "__all__"




# class ReviewCreateSerializer(serializers.ModelSerializer):
#     """Добавление отзыва"""
#
#     class Meta:
#         model = Review
#         fields = "__all__"  # поля, которые хотим сериализовать. - __all__ - все поля!


# class ReviewSerializer(serializers.ModelSerializer):
#     """Output отзыва"""
#
#     children = RecursiveSerializer(many=True)
#
#     class Meta:
#         list_serializer_class = FilterReviewListSeializer
#         model = Review
#         fields = ("name", "text", "children")




