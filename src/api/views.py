from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.models import RubiksCube
from src.api.serializers import RubiksCubeListSerializer


class RubiksCubeListView(APIView):
    """Вывод списка Кубиков Рубика"""

    def get(self, request):
        cubes = RubiksCube.objects.all()
        serializer = RubiksCubeListSerializer(cubes, many=True)
        return Response(serializer.data)
