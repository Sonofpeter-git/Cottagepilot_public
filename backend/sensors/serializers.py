from rest_framework import serializers
from .models import Sensor, SensorData, SensorAlert
from django.contrib.auth import authenticate
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = [
            'id', 'sensor_id', 'code', 'name', 'type', 'unit', 'location', 'description', 
            'status', 'last_reading', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_reading']
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class SensorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['sensor_id']

class SensorClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['name', 'type', 'unit', 'location', 'description']

class SensorDataSerializer(serializers.ModelSerializer):
    sensor_name = serializers.CharField(source='sensor.name', read_only=True)
    sensor_unit = serializers.CharField(source='sensor.unit', read_only=True)
    
    class Meta:
        model = SensorData
        fields = [
            'id', 'sensor', 'sensor_name', 'sensor_unit', 
            'value', 'timestamp', 'metadata'
        ]  
        read_only_fields = ['id', 'timestamp', 'sensor_name', 'sensor_unit']


class SensorDataCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['value', 'metadata']


class SensorAlertSerializer(serializers.ModelSerializer):
    sensor_name = serializers.CharField(source='sensor.name', read_only=True)
    
    class Meta:
        model = SensorAlert
        fields = [
            'id', 'sensor', 'sensor_name', 'alert_type', 'severity',
            'message', 'threshold_value', 'actual_value', 'is_resolved',
            'created_at', 'resolve_at'
        ]
        read_only_fields = ['id', 'created_at', 'sensor_name']


class SensorStatsSerializer(serializers.Serializer):
    total_sensors = serializers.IntegerField()
    active_sensors = serializers.IntegerField()
    inactive_sensors = serializers.IntegerField()
    error_sensors = serializers.IntegerField()
    total_data_points = serializers.IntegerField()
    recent_alerts = serializers.IntegerField()
