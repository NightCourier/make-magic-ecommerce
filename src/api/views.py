from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import models
from src.api.models import RubiksCube
from src.api.serializers.rating import CreateRatingSerializer
from src.api.serializers.rubiks_cube import RubiksCubeListSerializer, RubiksCubeDetailSerializer
from src.api.service import get_client_ip


class RubiksCubeListView(APIView):
    """Вывод списка Кубиков Рубика"""

    def get(self, request):
        cubes = RubiksCube.objects.all().annotate(
            rating_user=models.Count("rating", filter=models.Q(rating__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Sum(models.F('rating__star')) / models.Count(models.F('rating'))
        )
        serializer = RubiksCubeListSerializer(cubes, many=True)
        return Response(serializer.data)


class RubiksCubeDetailView(APIView):
    """Вывод отдельного Кубика Рубика"""

    def get(self, request, pk):
        cubes = RubiksCube.objects.get(id=pk)
        serializer = RubiksCubeDetailSerializer(cubes)
        return Response(serializer.data)


class AddStarRatingView(APIView):
    """Adding rating for film"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)  # из JSON в QuerySet и в базу данных вот эту
        # data=request.data
        if serializer.is_valid():  # если валидно отработал
            serializer.save(ip=get_client_ip(request))  # предаем ip, полученный с помощью get_client_ip
            return Response(status=201)
        else:
            return Response(status=400)
