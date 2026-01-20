# celery_tasks.py
import secrets
from celery import shared_task
from .models import Sensor, SensorData
from django.utils.timezone import now
import redis
import json
from django.conf import settings
from .utils import send_mqtt_provisioning_success
redis_client = redis.Redis.from_url(settings.REDIS_URL)
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task(name="sensors.celery_tasks.process_sensor_queue")
def process_sensor_queue():
    # 1. Pull everything from Redis at once (Batching)
    pipe = redis_client.pipeline()
    pipe.lrange("sensor_data_queue", 0, -1) # Get all items in the list
    pipe.delete("sensor_data_queue")         # Clear the list
    results = pipe.execute()
    
    raw_payloads = results[0]
    if not raw_payloads:
        return "No data in queue"

    data_points_to_save = []
    
    for raw_data in raw_payloads:
        data = json.loads(raw_data)
        sensor_list = data.get('sensors', [])
        received_code = data.get('code', 'nan')

        for s in sensor_list:
            sensor_id = s.get('sensor_id')
            
            # Handle Provisioning (Individual DB hits are okay here, 
            # as provisioning happens once per sensor)
            if received_code == "nan":
                new_code = format(secrets.randbits(32), '08x')
                sensor_obj, created = Sensor.objects.get_or_create(
                    sensor_id=sensor_id,
                    defaults={'code': new_code, 'status': 'active'}
                )
                send_mqtt_provisioning_success(sensor_id, sensor_obj.code)
                continue # Skip data saving for the provisioning packet

            # Normal Data Processing (Collect for bulk save)
            try:
                sensor_obj = Sensor.objects.get(sensor_id=sensor_id, code=received_code)
                data_points_to_save.append(SensorData(
                    sensor=sensor_obj,
                    value=s.get('sensor_data'),
                    timestamp=now()
                ))
            except Sensor.DoesNotExist:
                print(f"Auth failed for sensor {sensor_id}")

    # 2. Perform ONE database transaction for the whole batch
    if data_points_to_save:
        with transaction.atomic():
            saved_data = SensorData.objects.bulk_create(data_points_to_save)
            # Add alert logic here later
        
        # 3. Real-time Broadcast via Channels
        channel_layer = get_channel_layer()
        

        for dp in saved_data:
            sensor = dp.sensor
            # Only broadcast if the sensor is claimed (has an owner)
            if sensor.owner:
                # Frontend expects 'sensor_id' to match the selectedSensorId (UUID)
                # payload matches SensorData structure
                payload = {
                    "id": str(dp.id),
                    "sensor": str(sensor.id),
                    "sensor_id": str(sensor.id),
                    "sensor_name": sensor.name,
                    "sensor_unit": sensor.unit,
                    "value": dp.value,
                    "timestamp": str(dp.timestamp),
                    "metadata": dp.metadata
                }
                
                cottage_id = sensor.owner.id
                group_name = f"sensors_group_{cottage_id}"
                
                try:
                    async_to_sync(channel_layer.group_send)(
                        group_name,
                        {
                            "type": "sensor.message",
                            "data": payload
                        }
                    )
                except Exception as e:
                    print(f"Failed to broadcast sensor data: {e}")
            
    return f"Processed {len(raw_payloads)} payloads, saved {len(data_points_to_save)} readings."

