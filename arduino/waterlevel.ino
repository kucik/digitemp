// LAN modul W5500 - web server

#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
// nastavení MAC adresy
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
// Set up ip adress. Must be in range of dhcp

IPAddress ip(192, 168, 1, 1); // TODO change
// ini
EthernetServer server(80);

#define SLEEPTIME 600000 //ms

// pinout for Trig and Echo of ultrasonic module
int pTrig = 4;
int pEcho = 5;
// init vars
double odezva, vzdalenost;
#define pPump 6
#define pPump2 7


//mqtt config.
#define mqtt_server "192.168.1.2" // TODO change mqtt login setup
#define mqtt_user "user"
#define mqtt_password "yourpassword"
#define mqtt_wtopic "yourtopic"
//#define mqtt_send_interval 12000 //ms TODO x50
#define mqtt_send_interval 600000 //ms

#define mqtt_sub_topic_pump "controll/pump"
#define pumpON LOW
#define pumpOFF HIGH

//pump timer
#define pump_max_time 600000 //10 minutes
//const unsigned long pump_max_time = (6000 * 10) //10 minutes
static unsigned long pump_last_impulse = 0;
static int pumpon = false;

//MQtt
EthernetClient ethClient;
PubSubClient client(ethClient);

void setupPump() {
  pinMode(pPump, OUTPUT);
  digitalWrite(pPump, pumpOFF);
}


void setpump(byte* onoff) {
  int ival = atoi(onoff);
  Serial.print("Recvd: ");
  Serial.println(ival);
  if(ival == 1 ) {
    digitalWrite(pPump, pumpON);
    pump_last_impulse = millis();
    pumpon = true;
    Serial.println("Pump on");
  }
  else {
    digitalWrite(pPump, pumpOFF);
    pump_last_impulse = millis();
    pumpon = false;
    Serial.println("Pump off");
  }
}

void checkpump() {
//  Serial.print(millis() - pump_last_impulse);
//  Serial.print(" > ");
//  Serial.println(pump_max_time);
  if(pumpon && (millis() - pump_last_impulse) > pump_max_time) {
    Serial.println("Fallback stop pump!");
    digitalWrite(pPump, pumpOFF);
    pumpon = false;
  }
}

void mqttcallback(char* topic, byte* payload, unsigned int length) {
  //Serial.println(topic);
  if(strcmp(topic, mqtt_sub_topic_pump) == 0) {
    setpump(payload);
  }
}

void setup_hc() {
  // Set up pins of  HC-SR04
  pinMode(pTrig, OUTPUT);
  pinMode(pEcho, INPUT);
}

void reconnect_mqtt() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    // If you do not want to use a username and password, change next line to
    // if (client.connect("ESP8266Client")) {
    if (client.connect("kebule", mqtt_user, mqtt_password)) {
      client.subscribe(mqtt_sub_topic_pump);
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void ipsetup() {
  static int started = false;
  //Serial.println("--Link status: ");
  //Serial.println(Ethernet.linkStatus());
  if(started) {
    Ethernet.maintain();
    if(Ethernet.linkStatus() == LinkON) {
      return;
    }
  }

  Ethernet.begin(mac);
  // Allow hw to sert it out
  delay(1500);
  server.begin();
  // Serial out debug
  Serial.print("Server je na IP adrese: ");
  Serial.println(Ethernet.localIP());
  started = true;
  Serial.print("xLink status: ");
  Serial.println(Ethernet.linkStatus());
  //mqtt
  client.setServer(mqtt_server, 1883);
  client.setCallback(mqttcallback);

  reconnect_mqtt();
}

bool checkBound(float newValue, float prevValue, float maxDiff) {
  return !isnan(newValue) &&
         (newValue < prevValue - maxDiff || newValue > prevValue + maxDiff);
}

void setup() {
  // init serial line 9600 baud
  Serial.begin(9600);
  // Setup ip layer
  //Ethernet.begin(mac, ip);
  ipsetup();
  setup_hc();
  setupPump();
}


double getdistance()
{
  // Set 2us out to GND (for safety)
  // Then set 5us output to HIGH
  // Then LOW again
  digitalWrite(pTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pTrig, HIGH);
  delayMicroseconds(5);
  digitalWrite(pTrig, LOW);
  // By pulseIne get length of pulse in us
  odezva = pulseIn(pEcho, HIGH);
  // Calculate distance from time
  //vzdalenost = odezva / 58.31;
  vzdalenost = odezva * 0.034 / 2.0;
//  Serial.print("Vzdalenost je ");
//  Serial.print(vzdalenost);
//  Serial.println(" cm.");
  return vzdalenost;
}

void send_data() {
  unsigned long currentMillis = millis(); // refresh counter variable
  static unsigned long lastSent = 0 - mqtt_send_interval;

  if(currentMillis - lastSent >= mqtt_send_interval) {
    char c_topic[100];
    double dist = 190.0 - getdistance();
    String topic = mqtt_wtopic;
    topic.toCharArray(c_topic,100);
    client.publish(c_topic, String(dist).c_str(), true);
    lastSent = currentMillis;
    Serial.print("distance sen: ");
    Serial.print(dist);
    Serial.println(" cm.");
  }
}


void loop() {
  ipsetup();
  reconnect_mqtt();
  // Send data
  send_data();
  //delay(3000);
  client.loop();
  checkpump();
  delay(500);
}
