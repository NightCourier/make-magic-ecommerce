from django_filters import rest_framework as filters
from src.api.models import RubiksCube


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ProductFilter(filters.FilterSet):
    category = filters.BaseInFilter(lookup_expr='in')
    price = filters.RangeFilter()

    class Meta:
        model = RubiksCube
        fields = ['category', 'price']
