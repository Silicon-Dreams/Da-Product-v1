import django_filters
from .models import Products

# define listing filter class
class ListingFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()
    
    class Meta:
        model = Products
        fields = {'filterField': ['exact'], 'name': ['icontains']}