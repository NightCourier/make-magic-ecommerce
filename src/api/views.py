from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from django.db import models
from src.api.models import RubiksCube
from src.api.serializers.rating import CreateRatingSerializer
from src.api.serializers.review import CreateReviewSerializer
from src.api.serializers.rubiks_cube import RubiksCubeListSerializer, RubiksCubeDetailSerializer
from src.api.service import get_client_ip, ProductFilter


# class ProductDetailView(generics.RetrieveAPIView):
#
#     CT_MODEL_MODEL_CLASS = {
#         'rubiks_cube': [RubiksCube, RubiksCubeDetailSerializer]
#     }
#
#     def dispatch(self, request, *args, **kwargs):
#         self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']][0]
#         self.queryset = self.model._base_manager.all()
#         self.serializer_class = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']][1]
#
#     context_object_name = 'product'
#     slug_url_kwarg = 'url'


class RubiksCubeListView(generics.ListAPIView):
    """List of Rubiks Cubes"""
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


class RubiksCubeDetailView(generics.RetrieveAPIView):
    """Detail for single Rubiks Cube"""

    queryset = RubiksCube.objects.all()
    serializer_class = RubiksCubeDetailSerializer


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
