from django.urls import path

from src.api import views

urlpatterns = [
    path("rubiks_cubes/", views.RubiksCubeListView.as_view()),
]
