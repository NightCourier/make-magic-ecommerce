from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.models import RubiksCube
from src.api.serializers.rubiks_cube import RubiksCubeListSerializer, RubiksCubeDetailSerializer


class RubiksCubeListView(APIView):
    """Вывод списка Кубиков Рубика"""

    def get(self, request):
        cubes = RubiksCube.objects.all()
        serializer = RubiksCubeListSerializer(cubes, many=True)
        return Response(serializer.data)


class RubiksCubeDetailView(APIView):
    """Вывод отдельного Кубика Рубика"""

    def get(self, request, pk):
        cubes = RubiksCube.objects.get(id=pk)
        serializer = RubiksCubeDetailSerializer(cubes)
        return Response(serializer.data)
