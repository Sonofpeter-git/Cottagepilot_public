import django_filters
from django.utils import timezone
from datetime import timedelta
from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    month_correlation = django_filters.ChoiceFilter(choices=Task.MONTH_CHOICES)
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Task
        fields = ['status', 'month_correlation', 'created_after', 'created_before']
