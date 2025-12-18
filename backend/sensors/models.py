
from django.db import models
import uuid
from datetime import timedelta
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils import decorators

class Sensor(models.Model):
    SENSOR_TYPES = [
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('pressure', 'Pressure'),
        ('light', 'Light'),
        ('motion', 'Motion'),
        ('air_quality', 'Air Quality'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor_id = models.CharField(max_length=255)
    #to validate sensor posts
    code = models.CharField(max_length=100) 
    name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(choices=SENSOR_TYPES, blank=True, null=True, max_length=100)
    unit = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    last_reading = models.FloatField(null=True, blank=True)
    owner = models.ForeignKey('cottageInstance.CottageInstanceModel', on_delete=models.CASCADE, related_name='sensors', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.location})"
    
    def update_last_reading(self, value):
        """Update the last reading value"""     
        self.last_reading = value
        self.updated_at = now()
        self.save(update_fields=['last_reading', 'updated_at'])

    @property
    def is_sensor_claimed(self) -> bool:
        if self.owner == None:
            return False
        else:
            return True


    @property
    def sensor_status(self) -> str:
        if self.updated_at < now() - timedelta(hours=2):
            return 'inactive'
        else:
            self.status = 'active'
            self.save()
            return 'active'

class SensorData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='data_points')
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['sensor', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.sensor.name}: {self.value} at {self.timestamp}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the sensor's last reading
        self.sensor.update_last_reading(self.value)

    def __clean__(self):
        if not self.sensor:
            raise ValidationError("Sensor_data must have a valid sensor")
        
        if not self.value:
            raise ValidationError("Sensor_data muste have a valid value")

class SensorAlert(models.Model):
    ALERT_TYPES = [
        ('threshold', 'Threshold'),
        ('offline', 'Offline'),
        ('anomaly', 'Anomaly'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    message = models.TextField()
    threshold_value = models.FloatField(null=True, blank=True)
    actual_value = models.FloatField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sensor', 'is_resolved']),
            models.Index(fields=['severity', 'is_resolved']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.sensor.name} - {self.alert_type} ({self.severity})"
