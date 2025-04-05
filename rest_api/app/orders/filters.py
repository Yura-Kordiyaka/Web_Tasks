import django_filters
from .models import Order
from django_filters.rest_framework import FilterSet, OrderingFilter


class OrderFilter(FilterSet):
    delivery_time = django_filters.DateTimeFilter(field_name='delivery_time', lookup_expr='gte',
                                                  label='Delivery Time (Greater Than or Equal)')
    is_delivered = django_filters.BooleanFilter(field_name='is_delivered', label='Delivered')
    ordering = OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
        ),
        label='Ordering',
    )

    class Meta:
        model = Order
        fields = ['delivery_time', 'created_at', 'is_delivered']
