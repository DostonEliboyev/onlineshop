import django_filters
from django.db import models
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search_filter', label='Search')
    category = django_filters.CharFilter(method='category_filter', label='Category')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')
    material = django_filters.ChoiceFilter(choices=Product.MATERIAL_CHOICES)
    color = django_filters.ChoiceFilter(choices=Product.COLOR_CHOICES)
    sort = django_filters.CharFilter(method='sort_filter', label='Sort')

    class Meta:
        model = Product
        fields = []

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            models.Q(name__icontains=value) |
            models.Q(description__icontains=value)
        )

    def category_filter(self, queryset, name, value):
        return queryset.filter(
            models.Q(category__slug=value) |
            models.Q(category__parent__slug=value)
        )

    def sort_filter(self, queryset, name, value):
        sort_options = {
            'price_asc': 'price',
            'price_desc': '-price',
            'newest': '-created_at',
            'name': 'name',
        }
        return queryset.order_by(sort_options.get(value, '-created_at'))
