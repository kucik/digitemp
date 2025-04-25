#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "config.h"

//#define mqtt_send_interval 300000 //ms
#define mqtt_send_interval 6000 //ms
#define TRIGGER_WIDTH 30 //ms length of transmitted signal. Original 5
#define CHANGE_TRESHOLD 0.5
#define LOOP_SLEEP 500

// pinout for Trig and Echo of ultrasonic module
int pTrig = 12;
int pEcho = 14;
// init vars
double trg_echo;


/*
#ifndef STASSID
#define STASSID "ssid"
#define STAPSK "your-password"
#endif
*/

WiFiClient espClient;
PubSubClient client(espClient);

const char* ssid = STASSID;
const char* password = STAPSK;

const char* mqtt_server = MQTT_SERVER;
const char* mqtt_user = MQTT_USER;
const char* mqtt_password = MQTT_PASSWORD;
const char* mqtt_wtopic = MQTT_TOPIC;

char c_topic[100];
String topic = mqtt_wtopic;

void blink(int cnt, int fast) {
  int i;
  for(i = 0; i < cnt; i++) {
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(300 - 200 * fast);
  }
}

void setup_hc() {
  // Set up pins of  HC-SR04
  pinMode(pTrig, OUTPUT);
  pinMode(pEcho, INPUT);
  topic.toCharArray(c_topic,100);
}


void setupWifi() {

  while (WiFi.status() != WL_CONNECTED) {
    delay(5000);
    blink(1,0);
  }
  randomSeed(micros());

}

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
  setup_hc();
  client.setServer(mqtt_server, 1883);
  blink(2, true);
}

void reconnect_mqtt() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    // If you do not want to use a username and password, change next line to
    // if (client.connect("ESP8266Client")) {
    if (client.connect("kebule", mqtt_user, mqtt_password)) {
//      client.subscribe(mqtt_sub_topic_pump);
      Serial.println("connected");
      blink(3, true);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

double getdistance()
{
  double measure_distance = 0.0;
  // Set 2us out to GND (for safety)
  // Then set 5us output to HIGH
  // Then LOW again
  digitalWrite(pTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pTrig, HIGH);
  delayMicroseconds(TRIGGER_WIDTH); //TODO Try 10 / 12 or 30 signal width
  digitalWrite(pTrig, LOW);
  // By pulseIne get length of pulse in us
  trg_echo = pulseIn(pEcho, HIGH);
  // Calculate distance from time
  //vzdalenost = trg_echo / 58.31;
  measure_distance = trg_echo * 0.034 / 2.0;
//  Serial.print("Vzdalenost je ");
/*  Serial.print(vzdalenost);
  Serial.println(" cm.");*/
  return measure_distance;
}

void send_data() {
//  unsigned long currentMillis = millis(); // refresh counter variable
  static double last_sent_dist = -1.0;

  double dist = 190.0 - getdistance();
  /* Filter out invalid value */
  if (dist < 0.0) {
    return;
  }
  /* Filter out minor changes */
  if (abs(dist - last_sent_dist) > CHANGE_TRESHOLD) {

/*    char c_topic[100];
    String topic = mqtt_wtopic;
    topic.toCharArray(c_topic,100);
*/
    reconnect_mqtt();
    client.publish(c_topic, String(dist).c_str(), true);
//    lastSent = currentMillis;
    Serial.print("distance sent:   ");
    Serial.print(dist);
    Serial.println(" cm.");
    last_sent_dist = dist;
    blink(1, false);
  }
}


void loop() {
//  reconnect_mqtt();
  // Send data
  send_data();
  //delay(3000);
  //client.loop();
  delay(LOOP_SLEEP);
}
