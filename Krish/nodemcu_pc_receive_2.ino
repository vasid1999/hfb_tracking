#include<ESP8266WiFi.h>

#define MOTOR_L_1 D0
#define MOTOR_L_2 D1
#define MOTOR_R_1 D2
#define MOTOR_R_2 D3

const char* ssid="CFI_WIFI";
const char* passwd="SPIRITOFENGG";
IPAddress serverip(10,21,67,213);
IPAddress clientip(10,21,67,212);
IPAddress gateway(10,21,67,254);
IPAddress subnet(255,255,252,0);
WiFiClient client1;
WiFiServer server1(3000);
ESP8266WiFiClass w1;

void moveForward(){
digitalWrite(MOTOR_L_1,HIGH);
digitalWrite(MOTOR_L_2,LOW);
digitalWrite(MOTOR_R_1,HIGH);
digitalWrite(MOTOR_R_2,LOW);
}

void moveBackward(){
digitalWrite(MOTOR_L_2,HIGH);
digitalWrite(MOTOR_L_1,LOW);
digitalWrite(MOTOR_R_2,HIGH);
digitalWrite(MOTOR_R_1,LOW);
}

void stopMotion(){
digitalWrite(MOTOR_L_1,LOW);
digitalWrite(MOTOR_L_2,LOW);
digitalWrite(MOTOR_R_1,LOW);
digitalWrite(MOTOR_R_2,LOW);
}

void setup() {
  // put your setup code here, to run once:
  pinMode(MOTOR_L_1,OUTPUT);
  pinMode(MOTOR_L_2,OUTPUT);
  pinMode(MOTOR_R_1,OUTPUT);
  pinMode(MOTOR_R_2,OUTPUT);
  stopMotion();

  w1.config(serverip,gateway,subnet);
  w1.begin(ssid,passwd);
  while(w1.status()!=WL_CONNECTED){delay(500);}
  server1.begin();
  client1=server1.available();
}

void loop() {
  // put your main code here, to run repeatedly:
  
  //receive signals from pc
  while(!client1){delay(500);client1=server1.available();}
  while(client1.connected())
  {
    if(client1.available())
    {
      switch(client1.read())
      {
        //send signals to motor driver module
        case 'w':moveForward();break;
        case 'z':moveBackward();break;
        case 's':stopMotion();break;
      }
    }
  }
  client1.stop();
}
