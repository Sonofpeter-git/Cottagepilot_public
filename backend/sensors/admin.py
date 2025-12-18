from django.contrib import admin
from .models import Sensor, SensorData, SensorAlert


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'unit', 'location', 'status', 'last_reading', 'owner', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'location', 'owner__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'value', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['sensor__name']
    readonly_fields = ['id', 'timestamp']
    ordering = ['-timestamp']


@admin.register(SensorAlert)
class SensorAlertAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'alert_type', 'severity', 'is_resolved', 'created_at']
    list_filter = ['alert_type', 'severity', 'is_resolved', 'created_at']
    search_fields = ['sensor__name', 'message']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']