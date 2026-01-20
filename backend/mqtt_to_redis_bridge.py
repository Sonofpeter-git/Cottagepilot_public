import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import redis
import json
import os

# Connection to Redis
r = redis.Redis.from_url(os.getenv("REDIS_URL"))
MQTT_BROKER = os.getenv('MQTT_BROKER_HOST', 'mqtt_broker')

def on_message(client, userdata, msg):
    try:
        r.lpush("sensor_data_queue", msg.payload.decode())
    except Exception as e:
        print(f"Error buffering MQTT: {e}")


# Update the connection callback signature for v2
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Bridge connected to MQTT Broker. Result: {rc}")
    client.subscribe("sensors/data")

client = mqtt.Client(CallbackAPIVersion.VERSION2) # Set version here
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)
client.loop_forever()