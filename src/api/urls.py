from django.urls import path

from src.api import views

urlpatterns = [
    path("rubiks_cubes/", views.RubiksCubeListView.as_view()),
    path("rubiks_cubes/<int:pk>/", views.RubiksCubeDetailView.as_view()),
    path("rating/", views.AddStarRatingView.as_view()),
]
