from django.contrib import admin
from .models import Task


@admin.register(Task)
class SensorAdmin(admin.ModelAdmin):
    list_display =  [
                    'name', 'description', 'additional_info', 
                    'location', 'status', 'Responsible_for_the_task', 'owner', 'sensor', 'limit_value',
                    'month_correlation', 'time_correlation', 'created_at', 'updated_at'
                ] 
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'location', 'owner__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
