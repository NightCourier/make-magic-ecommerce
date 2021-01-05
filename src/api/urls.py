from django.urls import include, path

from src.api.views import HealthView, Authentication

urlpatterns = [
    path('login/', Authentication.as_view(), name='login'),
    path('health/', HealthView.as_view(), name='health'),
    path('', include('src.api.mag.urls')),
]
