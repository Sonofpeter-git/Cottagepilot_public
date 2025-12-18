from django.contrib import admin
from .models import AnalyticsReport, SensorInsight


@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'start_date', 'end_date', 'created_at']
    list_filter = ['report_type', 'created_at']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at']


@admin.register(SensorInsight)
class SensorInsightAdmin(admin.ModelAdmin):
    list_display = ['sensor', 'insight_type', 'title', 'confidence_score', 'created_at']
    list_filter = ['insight_type', 'created_at']
    search_fields = ['sensor__name', 'title']
    readonly_fields = ['id', 'created_at']