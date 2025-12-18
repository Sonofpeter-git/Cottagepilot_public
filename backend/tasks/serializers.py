from rest_framework import serializers
from .models import Task
from django.contrib.auth import authenticate
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    sensor_name = serializers.CharField(source='sensor.name', read_only=True)
    sensor_unit = serializers.CharField(source='sensor.unit', read_only=True)

    class Meta:
        model = Task

        fields = [
                    'id', 'name', 'group', 'description', 'additional_info', 
                    'location', 'status', 'sensor', 'sensor_name', 'sensor_unit', 'limit_value',
                    'month_correlation', 'time_correlation'
                ]  
        read_only_fields = ['id', 'sensor_unit', 'sensor_name']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'group', 'description', 'additional_info', 'location',
                  'status', 'created_at', 'updated_at', 'sensor', 'limit_value', 'month_correlation', 'time_correlation']