#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiManager.h>
#include <PubSubClient.h> 
#include <EEPROM.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_AHTX0.h>

// ==========================================
// CONFIGURATION
// ==========================================
// TODO: UPDATE THIS IP TO YOUR MQTT BROKER ADDRESS
const char* mqtt_server = "192.168.1.100"; 
const int mqtt_port = 1883;

const char* deviceTempID = "ESP8266_12F_005_PROD_Temp";
const char* deviceHumID = "ESP8266_12F_005_PROD_Hum";

const char* topic_data = "sensors/data";

const int EEPROM_SIZE = 512;
const int CODE_ADDR = 0;

WiFiClient espClient;
PubSubClient client(espClient);

// ==========================================
// EEPROM HELPERS
// ==========================================
void saveCodeToEEPROM(const char* code) {
  Serial.print("Saving code to EEPROM: ");
  Serial.println(code);

  int len = strlen(code);
  if (len > EEPROM_SIZE - 1) {
    Serial.println("Code length exceeds EEPROM size limit!");
    return;
  }

  for (int i = 0; i < len; i++) {
    EEPROM.write(CODE_ADDR + i, code[i]);
  }
  EEPROM.write(CODE_ADDR + len, '\0');
  EEPROM.commit();
  Serial.println("Code saved to EEPROM successfully.");
}

bool readCodeFromEEPROM(char* buffer, size_t bufferSize) {
  int i = 0;
  while (i < bufferSize - 1) {
    char c = EEPROM.read(CODE_ADDR + i);
    if (c == '\0') break;
    if ((uint8_t)c == 0xFF) {
      buffer[0] = '\0';
      return false;
    }
    buffer[i] = c;
    i++;
  }
  buffer[i] = '\0';
  return (i > 0);
}

// ==========================================
// MQTT CALLBACK
// ==========================================
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received [");
  Serial.print(topic);
  Serial.print("] ");

  // Allocate a buffer for the payload + null terminator
  char msg[length + 1];
  for (unsigned int i = 0; i < length; i++) {
    msg[i] = (char)payload[i];
  }
  msg[length] = '\0';
  Serial.println(msg);

  // Parse JSON
  DynamicJsonDocument doc(1024);
  DeserializationError error = deserializeJson(doc, msg);

  if (!error) {
    // Check for provisioning message
    if (doc.containsKey("code")) {
      const char* newCode = doc["code"];
      saveCodeToEEPROM(newCode);
      Serial.println("PROVISIONING SUCCESS: Code updated.");
    }
  } else {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
  }
}

// ==========================================
// CONNECT
// ==========================================
void reconnect() {
  // Loop until we're reconnected (try 3 times then fail to sleep)
  int retries = 0;
  while (!client.connected() && retries < 3) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      
      // Subscribe to provisioning topics for BOTH sensors
      String topicTemp = "sensors/provision/" + String(deviceTempID);
      String topicHum = "sensors/provision/" + String(deviceHumID);
      
      client.subscribe(topicTemp.c_str());
      client.subscribe(topicHum.c_str());
      Serial.println("Subscribed to provisioning topics");
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 2 seconds");
      delay(2000);
      retries++;
    }
  }
}

void publishSensorData(const char* sensorId, float value, const char* code) {
  if (!client.connected()) return;

  DynamicJsonDocument doc(512);
  
  JsonObject sensorObj = doc.createNestedArray("sensors").createNestedObject();
  sensorObj["sensor_id"] = sensorId;
  sensorObj["sensor_data"] = value;
  
  if (strlen(code) > 0) {
    doc["code"] = code;
  } else {
    doc["code"] = "nan";
  }

  char buffer[512];
  serializeJson(doc, buffer);
  
  Serial.print("Publishing to ");
  Serial.print(topic_data);
  Serial.print(": ");
  Serial.println(buffer);

  client.publish(topic_data, buffer);
}

// ==========================================
// MAIN LOOP
// ==========================================
void setup() {
  Serial.begin(74880);
  Serial.println("\n--- Wake Up ---");

  // Init EEPROM
  EEPROM.begin(EEPROM_SIZE);

  // Init Sensor
  Adafruit_AHTX0 aht;
  if (!aht.begin()) {
    Serial.println("AHT10 not found!");
    // Wait a bit, then sleep. If hardware fails, no point draining battery.
    delay(2000); 
    ESP.deepSleep(60e6);
    return;
  }

  // Read Data
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);
  float temperature = temp.temperature;
  float humidityValue = humidity.relative_humidity;

  // Connect WiFi
  WiFiManager wifiManager;
  wifiManager.setConfigPortalTimeout(180);
  if (!wifiManager.autoConnect("CottagePilot-Sensor")) {
    Serial.println("WiFi failed to connect. Sleeping.");
    ESP.deepSleep(600e6); // 10 mins
    return;
  }

  // Setup MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);

  if (!client.connected()) {
    reconnect();
  }

  if (client.connected()) {
    // Read auth code
    char codeBuffer[512];
    bool hasCode = readCodeFromEEPROM(codeBuffer, sizeof(codeBuffer));
    if (!hasCode) {
        strcpy(codeBuffer, "nan");
    }

    // Publish Temperature
    publishSensorData(deviceTempID, temperature, codeBuffer);
    delay(250); // Small delay between publishes
    
    // Publish Humidity
    publishSensorData(deviceHumID, humidityValue, codeBuffer);

    // Wait for incoming messages (Provisioning)
    // We stay awake for 5 seconds to listen for a response
    Serial.println("Listening for provisioning...");
    unsigned long start = millis();
    while (millis() - start < 5000) {
      client.loop();
      delay(10);
    }
  }

  Serial.println("Going to deep sleep...");
  client.disconnect();
  ESP.deepSleep(600e6); // 10 minutes
}

void loop() {
  // Not used due to deep sleep
}