from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from src.api.models import RubiksCube
from src.api.mag.serializers.rating import CreateRatingSerializer
from src.api.mag.serializers.review import CreateReviewSerializer
from src.api.mag.serializers.rubiks_cube import RubiksCubeListSerializer, RubiksCubeDetailSerializer
from src.api.service import get_client_ip, ProductFilter


class RubiksCubeListView(generics.ListAPIView):
    """Вывод списка Кубиков Рубика"""
    serializer_class = RubiksCubeListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self):
        cubes = RubiksCube.objects.all().annotate(
            rating_user=models.Count("rating", filter=models.Q(rating__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('rating__star')) / models.Count(models.F('rating'))
        )
        return cubes


class RubiksCubeDetailView(APIView):
    """Вывод отдельного Кубика Рубика"""

    def get(self, request, pk):
        cubes = RubiksCube.objects.get(id=pk)
        serializer = RubiksCubeDetailSerializer(cubes)
        return Response(serializer.data)


class CreateReviewView(generics.CreateAPIView):
    """Adding rating for product"""

    serializer_class = CreateReviewSerializer


class AddStarRatingView(APIView):
    """Adding rating for product"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
