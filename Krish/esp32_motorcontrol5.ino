//This is the new code
#include<WiFi.h>

//15 1 14 27
/*original
#define MOTOR_L_1 19
#define MOTOR_L_2 21
#define MOTOR_R_1 27
#define MOTOR_R_2 14
#define MOTOR_F_1 4
#define MOTOR_F_2 2*/

#define MOTOR_R_1 21
#define MOTOR_R_2 19
#define MOTOR_F_1 27
#define MOTOR_F_2 14
#define MOTOR_F_E 22
#define MOTOR_L_1 2
#define MOTOR_L_2 4

const char* ssid="Krish";
const char* passwd="zxcvbnm1";
IPAddress serverip(192,168,43,11);
//IPAddress clientip(10,21,67,213);
IPAddress gateway(192,168,43,1);
IPAddress subnet(255,255,255,0);
WiFiClient client1;
WiFiServer server1(3000);
WiFiClass w1;
//PWM definitions
const int freq = 3000;
const int pwmChannel = 0;
const int resolution = 8;
int dutyCycle=0;
char ch='s';

void moveForward(){
digitalWrite(MOTOR_L_1,HIGH);
digitalWrite(MOTOR_L_2,LOW);
digitalWrite(MOTOR_R_1,HIGH);
digitalWrite(MOTOR_R_2,LOW);
digitalWrite(MOTOR_F_1,LOW);
digitalWrite(MOTOR_F_2,LOW);
}

void moveBackward(){
digitalWrite(MOTOR_L_2,HIGH);
digitalWrite(MOTOR_L_1,LOW);
digitalWrite(MOTOR_R_2,HIGH);
digitalWrite(MOTOR_R_1,LOW);
digitalWrite(MOTOR_F_1,LOW);
digitalWrite(MOTOR_F_2,LOW);

}

void stopMotion(){
digitalWrite(MOTOR_L_1,LOW);
digitalWrite(MOTOR_L_2,LOW);
digitalWrite(MOTOR_R_1,LOW);
digitalWrite(MOTOR_R_2,LOW);
digitalWrite(MOTOR_F_1,LOW);
digitalWrite(MOTOR_F_2,LOW);

}

/*
 * backup
 * void moveLeft(){
digitalWrite(MOTOR_L_1,HIGH);
digitalWrite(MOTOR_L_2,LOW);
digitalWrite(MOTOR_R_1,HIGH);
digitalWrite(MOTOR_R_2,LOW);
digitalWrite(MOTOR_F_1,HIGH);
digitalWrite(MOTOR_F_2,LOW);

}

void moveRight(){
digitalWrite(MOTOR_L_1,HIGH);
digitalWrite(MOTOR_L_2,LOW);
digitalWrite(MOTOR_R_1,HIGH);
digitalWrite(MOTOR_R_2,LOW);
digitalWrite(MOTOR_F_1,LOW);
digitalWrite(MOTOR_F_2,HIGH);

}*/

void moveLeft(){
digitalWrite(MOTOR_L_1,LOW);
digitalWrite(MOTOR_L_2,LOW);
digitalWrite(MOTOR_R_1,LOW);
digitalWrite(MOTOR_R_2,LOW);
digitalWrite(MOTOR_F_1,HIGH);
digitalWrite(MOTOR_F_2,LOW);

}

void moveRight(){
digitalWrite(MOTOR_L_1,LOW);
digitalWrite(MOTOR_L_2,LOW);
digitalWrite(MOTOR_R_1,LOW);
digitalWrite(MOTOR_R_2,LOW);
digitalWrite(MOTOR_F_1,LOW);
digitalWrite(MOTOR_F_2,HIGH);

}

void setup() {
  // put your setup code here, to run once:
  pinMode(MOTOR_L_1,OUTPUT);
  pinMode(MOTOR_L_2,OUTPUT);
  pinMode(MOTOR_R_1,OUTPUT);
  pinMode(MOTOR_R_2,OUTPUT);
  pinMode(MOTOR_F_1,OUTPUT);
  pinMode(MOTOR_F_2,OUTPUT);
  pinMode(MOTOR_F_E,OUTPUT);
  stopMotion();
  
  ledcSetup(pwmChannel,freq,resolution);
  ledcAttachPin(MOTOR_F_E,pwmChannel);
  ledcWrite(pwmChannel,dutyCycle);
  //digitalWrite(MOTOR_F_E,LOW);
  
  Serial.begin(115200);
  w1.config(serverip,gateway,subnet);
  w1.begin(ssid,passwd);
  while(w1.status()!=WL_CONNECTED){}
  Serial.println(w1.localIP());
  server1.begin();
  client1=server1.available();
}

void loop() {
  // put your main code here, to run repeatedly:
  
  //receive signals from pc
  while(!client1){
    switch(ch)
      {
        //send signals to motor driver module
        case 'w':moveForward();Serial.println("Forward");break;
        case 'z':moveBackward();Serial.println("Backward");break;
        case 'a':moveLeft();Serial.println("Left");delay(100);stopMotion();delay(500);break;
        case 'd':moveRight();Serial.println("Right");delay(100);stopMotion();delay(500);break;
        case 's':stopMotion();Serial.println("Stay");break;
      }
    client1=server1.available();
    }
  while(client1.connected())
  {
    if(client1.available()) ch=client1.read();client1.stop();
  }
}
//try adding macro functions for Serial printing
