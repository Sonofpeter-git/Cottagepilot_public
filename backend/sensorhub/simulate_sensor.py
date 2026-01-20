import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion # New import
import json
import time
import random
import os

# CONFIGURATION
# Inside Docker, use the service name 'mqtt_broker'. Outside, use 'localhost'.
MQTT_BROKER = os.getenv('MQTT_BROKER_HOST', 'localhost') 
MQTT_PORT = 1883
TOPIC_DATA = "sensors/data"

# Define sensors
SENSORS = {
    "ESP8266_12F_005_PROD_Temp": {"type": "temp", "code": "nan"},
    "ESP8266_12F_005_PROD_Hum":  {"type": "hum",  "code": "nan"}
}

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✅ Connected to MQTT Broker at {MQTT_BROKER}")
        # Subscribe to provisioning topic for EACH sensor
        for sensor_id in SENSORS:
            topic = f"sensors/provision/{sensor_id}"
            client.subscribe(topic)
            print(f"📥 Subscribed to {topic}")
    else:
        print(f"❌ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"📩 Message received on {msg.topic}: {payload}")
        
        # Extract sensor_id from topic: sensors/provision/<sensor_id>
        topic_parts = msg.topic.split('/')
        if len(topic_parts) == 3 and topic_parts[1] == "provision":
            sensor_id = topic_parts[2]
            
            if sensor_id in SENSORS and "code" in payload:
                SENSORS[sensor_id]["code"] = payload["code"]
                print(f"💾 EEPROM UPDATED: New persistent code for {sensor_id} is '{payload['code']}'")
                
    except Exception as e:
        print(f"⚠️ Error parsing message: {e}")

def simulate_device_cycle(client):
    # Iterate through all sensors and send data individually
    for sensor_id, sensor_info in SENSORS.items():
        
        # 1. Simulate hardware sensor reading
        if sensor_info["type"] == "temp":
            val = round(22.0 + random.uniform(-0.5, 0.5), 2)
        else:
            val = round(45.0 + random.uniform(-1.0, 1.0), 2)

        # 2. Construct the payload for a SINGLE sensor
        # The backend expects a list under "sensors", but we will send one at a time
        # to ensure the correct "code" is associated with the correct sensor ID.
        payload = {
            "sensors": [
                {"sensor_id": sensor_id, "sensor_data": val}
            ],
            "code": sensor_info["code"]
        }

        # 3. Publish to the MQTT Bridge
        print(f"📡 Publishing for {sensor_id}: {json.dumps(payload)}")
        client.publish(TOPIC_DATA, json.dumps(payload), qos=1)

if __name__ == "__main__":
    # Specify the API version explicitly
    client = mqtt.Client(CallbackAPIVersion.VERSION2) 
    
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect and loop
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        print("🚀 MQTT Simulator Started with API v2...")
        
        while True:
            simulate_device_cycle(client)
            time.sleep(30)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()