import paho.mqtt.client as mqtt
import json
from django.conf import settings

def send_mqtt_provisioning_success(sensor_id, new_code):
    """
    Connects to the MQTT broker and publishes the new code 
    to a sensor-specific provisioning topic.
    """
    # Use environment variables for broker details
    broker = settings.MQTT_BROKER_HOST
    port = int(settings.MQTT_PORT)
    user = settings.MQTT_USER
    password = settings.MQTT_PASSWORD

    client = mqtt.Client()
    
    if user and password:
        client.username_pw_set(user, password)

    try:
        client.connect(broker, port, 60)
        
        # The topic matches what the ESP8266 is listening to
        topic = f"sensors/provision/{sensor_id}"
        payload = json.dumps({
            "status": "provisioned",
            "code": new_code
        })
        
        client.publish(topic, payload, qos=1)
        client.disconnect()
        print(f"Successfully published new code to {topic}")
        
    except Exception as e:
        print(f"Failed to send MQTT provisioning message: {e}")