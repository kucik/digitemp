/*
 *  This sketch sends data via HTTP GET requests to 'host' service, reads
 *  reply and sets RELAY pins respectively.
 *  Fill configuration bellow.
 *
 */

#include <ESP8266WiFi.h>
#include <DHT.h>

#define DHTPIN 2 //DHT GPio pin
#define DHTTYPE DHT11
#define RELAY_PIN 12  // Relay 1 pin
#define RELAY_PIN2 14 // Relay 2(backup) pin
#define SLEEPTIME 30000

const char* ssid     = "wifi_ssid";
const char* password = "wifi_passd";

const char* host = "Server host adress";
const char* hosturl = "called script url"

const char* device = "this_device_name";
const char* privateKey = "this_device_auth_key";

void blink(int cnt, int fast) {
  int i;
  for(i = 0; i < cnt; i++) {
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(300 - 200 * fast);
  }
}

void setupWifi() {

  while (WiFi.status() != WL_CONNECTED) {
    delay(5000);
    blink(1,0);
  }

}

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  delay(10);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  setupWifi();

  dht.begin();

  // Relay
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
  pinMode(RELAY_PIN2, OUTPUT);
  digitalWrite(RELAY_PIN2, LOW);
}

int value = 0;

void setrelay(int val) {

  digitalWrite(RELAY_PIN, val);
  digitalWrite(RELAY_PIN2, val);

}

void loop() {
  boolean connection = 0;

  setupWifi();
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    connection = 0;
  }
  else {
    connection = 1;
  }


  float humidity = dht.readHumidity();
  Serial.println("Hum:" + String(humidity));
  float temp = dht.readTemperature();
  Serial.println("temp: " + String(temp));

  // We now create a URI for the request
  String url = hosturl;
  url += "?dev=";
  url += device;
  url += "&k=";
  url += privateKey;


  url += "&v=";
  url += humidity;
  url += "&v2=";
  url += temp;

  //Serial.print("Requesting URL: ");
  //Serial.println(url);

  int cmd = 0;
  if (connection == 1) {
    // This will send the request to the server
     client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n\r\n");
    unsigned long timeout = millis();
    while (client.available() == 0) {
      if (millis() - timeout > 5000) {
        Serial.println(">>> Client Timeout !");
        client.stop();
        return;
      }
    }

    // Read all the lines of the reply from server and print them to Serial
    while(client.available()){

      String line = client.readStringUntil('\r');
      if (line.startsWith("CMD: ")) {

        String sub = line.substring(5,10);
        if(sub == "START") {
          cmd = 1;
        }
        else if ( sub == "STOPX") {
          cmd = 2;
        }
        else if ( sub == "STAYX") {
          cmd = 3;
        }
      }
    }

    if(cmd > 0) {
      if(cmd == 1) {
        setrelay(HIGH);
      }
      else if(cmd == 2) {
      setrelay(LOW);
      }
    }
    delay(SLEEPTIME);
    return;
  }

  /* Fallback if server did not responded correctly */
  if(humidity > 70.0) {
    setrelay(HIGH);
  }
  else if(humidity < 45.0) {
    setrelay( LOW);
  }

  delay(SLEEPTIME);
}
