#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiManager.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>
#include <EEPROM.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_AHTX0.h>

const char* serverUrl = "";
const char* deviceTempID = "";
const char* deviceHumID = "";

const int EEPROM_SIZE = 512;
const int CODE_ADDR = 0;

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
    if (c == '\0') {
      break;
    }
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

void setup() {
  Serial.begin(74880);
  Serial.println("Setup start");
  
  // Initialize AHT sensor
  Adafruit_AHTX0 aht;
  if (!aht.begin()) {
    Serial.println("AHT10 not found!");
    WiFi.mode(WIFI_OFF);
    delay(100);
    ESP.deepSleep(60e6);
    return;
  }

  // Read sensor data
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);
  
  // Store values before sensor object goes out of scope
  float temperature = temp.temperature;
  float humidityValue = humidity.relative_humidity;
  
  Serial.print("Temperature: ");
  Serial.println(temperature);
  Serial.print("Humidity: ");
  Serial.println(humidityValue);

  EEPROM.begin(EEPROM_SIZE);

  // Connect WiFi
  WiFiManager wifiManager;
  wifiManager.setConfigPortalTimeout(180); // 3 minute timeout
  
  if (!wifiManager.autoConnect("Cottapilot-sensor")) {
    Serial.println("Failed to connect - going to sleep");
    EEPROM.end();
    WiFi.mode(WIFI_OFF);
    delay(100);
    ESP.deepSleep(600e5);
    return;
  }

  Serial.println("WiFi connected");

  // Send data to server
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClientSecure* client = new WiFiClientSecure();
    if (!client) {
      Serial.println("Failed to create WiFiClientSecure");
      EEPROM.end();
      WiFi.disconnect();
      WiFi.mode(WIFI_OFF);
      delay(100);
      ESP.deepSleep(600e5);
      return;
    }
    
    client->setInsecure();
    HTTPClient http;
    
    String url = String(serverUrl) + "create_sensor/";
    
    if (!http.begin(*client, url)) {
      Serial.println("HTTP begin failed");
      delete client;
      EEPROM.end();
      WiFi.disconnect();
      WiFi.mode(WIFI_OFF);
      delay(100);
      ESP.deepSleep(600e6);
      return;
    }
    
    http.addHeader("Content-Type", "application/json");

    // Construct payload
    String postData = "{\"sensors\":[";
    postData += "{\"sensor_id\":\"" + String(deviceTempID) + "\",";
    postData += "\"sensor_data\":" + String(temperature, 2) + "},";
    postData += "{\"sensor_id\":\"" + String(deviceHumID) + "\",";
    postData += "\"sensor_data\":" + String(humidityValue, 2) + "}],";
    
    // Get code from EEPROM
    char codeBuffer[512];
    bool hasCode = readCodeFromEEPROM(codeBuffer, sizeof(codeBuffer));
    
    if (hasCode) {
      postData += "\"code\":\"" + String(codeBuffer) + "\"}";
    } else {
      postData += "\"code\":\"nan\"}";
    }

    Serial.println("Sending: " + postData);
    
    int httpResponseCode = http.POST(postData);
    String responseBody = http.getString();
    
    Serial.print("Response code: ");
    Serial.println(httpResponseCode);
    Serial.print("Response body: ");
    Serial.println(responseBody);

    if (httpResponseCode == 201 || httpResponseCode == 200) {
      // Parse JSON response
      DynamicJsonDocument doc(1024);
      DeserializationError error = deserializeJson(doc, responseBody);
      
      if (!error) {
        const char* code = doc["code"];
        if (code != nullptr) {
          saveCodeToEEPROM(code);
          Serial.println("Data sent successfully");
        } else {
          Serial.println("Code field not found in response");
        }
      } else {
        Serial.print("JSON deserialization failed: ");
        Serial.println(error.c_str());
      }
    } else {
      Serial.println("Failed to post data");
    }
    
    // Cleanup
    http.end();
    delete client;
  } else {
    Serial.println("WiFi not connected");
  }

  // Cleanup before deep sleep
  EEPROM.end();
  //WiFi.disconnect(); would wipe saved credentials
  //WiFi.mode(WIFI_OFF); would wipe saved credentials
  delay(100);

  Serial.println("Going to deep sleep for 1 minutes...");
  Serial.flush();

  ESP.deepSleep(300e6); //minuutti
}

void loop() {
  // Should never reach here due to deep sleep
}