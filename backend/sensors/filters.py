import django_filters
from django.utils import timezone
from datetime import timedelta
from .models import Sensor, SensorData


class SensorFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Sensor.STATUS_CHOICES)
    type = django_filters.ChoiceFilter(choices=Sensor.SENSOR_TYPES)
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Sensor
        fields = ['status', 'type', 'created_after', 'created_before']


class SensorDataFilter(django_filters.FilterSet):
    sensor = django_filters.UUIDFilter(field_name='sensor__id')
    value_min = django_filters.NumberFilter(field_name='value', lookup_expr='gte')
    value_max = django_filters.NumberFilter(field_name='value', lookup_expr='lte')
    timestamp_after = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    timestamp_before = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    time_range = django_filters.CharFilter(method='filter_time_range')
    
    def filter_time_range(self, queryset, name, value):
        """Filter by predefined time ranges"""
        time_deltas = {
            '1h': timedelta(hours=1),
            '24h': timedelta(hours=24),
            '7d': timedelta(days=7),
            '30d': timedelta(days=30),
        }
        
        delta = time_deltas.get(value)
        if delta:
            start_time = timezone.now() - delta
            return queryset.filter(timestamp__gte=start_time)
        
        return queryset
    
    class Meta:
        model = SensorData
        fields = ['sensor', 'value_min', 'value_max', 'timestamp_after', 'timestamp_before', 'time_range']