from django.db import models
from sensors.models import Sensor
import uuid


class AnalyticsReport(models.Model):
    REPORT_TYPES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    sensors = models.ManyToManyField(Sensor, related_name='analytics_reports')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.report_type})"


class SensorInsight(models.Model):
    INSIGHT_TYPES = [
        ('trend', 'Trend Analysis'),
        ('anomaly', 'Anomaly Detection'),
        ('prediction', 'Prediction'),
        ('correlation', 'Correlation'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='insights')
    insight_type = models.CharField(max_length=20, choices=INSIGHT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    confidence_score = models.FloatField()  # 0.0 to 1.0
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sensor.name} - {self.title}"