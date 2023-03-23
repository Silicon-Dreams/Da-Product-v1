import django_filters
from .models import Products

# define listing filter class
class ListingFilter(django_filters.FilterSet):
    name__icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    price = django_filters.RangeFilter()

    class Meta:
        model = Products
        fields = {'price': ['exact']}