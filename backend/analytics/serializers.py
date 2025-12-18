from rest_framework import serializers
from .models import AnalyticsReport, SensorInsight


class AnalyticsReportSerializer(serializers.ModelSerializer):
    sensor_names = serializers.SerializerMethodField()
    
    class Meta:
        model = AnalyticsReport
        fields = [
            'id', 'name', 'report_type', 'sensors', 'sensor_names',
            'start_date', 'end_date', 'data', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_sensor_names(self, obj):
        return [sensor.name for sensor in obj.sensors.all()]


class SensorInsightSerializer(serializers.ModelSerializer):
    sensor_name = serializers.CharField(source='sensor.name', read_only=True)
    
    class Meta:
        model = SensorInsight
        fields = [
            'id', 'sensor', 'sensor_name', 'insight_type', 'title',
            'description', 'confidence_score', 'data', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'sensor_name']