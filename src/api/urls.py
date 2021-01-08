from django.urls import path

from src.api import views

urlpatterns = [
    path("rubiks_cubes/", views.RubiksCubeListView.as_view()),
    path("rubiks_cubes/<int:pk>/", views.RubiksCubeDetailView.as_view()),
    path("rating/", views.AddStarRatingView.as_view()),
    path("review/", views.CreateReviewView.as_view()),
    # path('<str:ct_model>/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail')
]
