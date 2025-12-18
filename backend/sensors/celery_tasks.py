from celery import shared_task
from .models import Sensor, SensorData
from .serializers import SensorDataCreateSerializer

@shared_task
def save_sensor_data(sensor_id, data):
    try:
        sensor = Sensor.objects.get(id=sensor_id)
    except Sensor.DoesNotExist:
        return {'error': 'Sensor not found'}

    serializer = SensorDataCreateSerializer(data=data)
    if serializer.is_valid():
        serializer.save(sensor=sensor)
        return {'status': 'success'}
    else:
        return {'error': serializer.errors}
