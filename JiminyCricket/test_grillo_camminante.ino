#include <Wire.h>
#include <SparkFun_APDS9960.h>
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

int ENA = 3;
int IN1 = 4;
int IN2 = 9;
int ENB = 5;
int IN3 = 7;
int IN4 = 8;
int ENC = 6;
int IN5 = 13;
int IN6 = 12;

SoftwareSerial mySoftwareSerial(10, 11); // RX, TX
DFRobotDFPlayerMini myDFPlayer;

void printDetail(uint8_t type, int value);

// Pin
#define APDS9960_INT 2 // Must be an interrupt pin
int redOut = A2;
int greenOut = A1;
int blueOut = A0;

// Global variables
SparkFun_APDS9960 apds = SparkFun_APDS9960();
int isr_flag = 0;

void interruptRoutine() {
  isr_flag = 1;
}
void setColor(int red, int green, int blue) {
  analogWrite(redOut, red);
  analogWrite(greenOut, green);
  analogWrite(blueOut, blue);
}
void handleGesture() {
  while (!apds.isGestureAvailable()) {
    Serial.println("Sensore di gesti non disponibile, riprovo...");
    setColor(255,0,0);
    delay(500); // Aggiungi un ritardo prima di riprovare
  }
  setColor(0,0,0);
  
  while (true) {
    switch (apds.readGesture()) {
      case DIR_UP:
        Serial.println("SU");
        setColor(0,255,0); //Verde
        myDFPlayer.play(3);
        delay(3000);
        setColor(0,0,0);
        myDFPlayer.stop();
        Serial.println("No, it's your turn");
        break;
      case DIR_DOWN:
        Serial.println("GIÙ");
        setColor(255,0,255); //Rosa
        delay(500);
        setColor(0,0,0);
        break;
      case DIR_LEFT:
        Serial.println("SINISTRA");
        setColor(0,0,255);  //BLU
        myDFPlayer.play(2);
        delay(3000);
        setColor(0,0,0);
        myDFPlayer.stop();
        Serial.println("No, you have to do it");
        break;
      case DIR_RIGHT:
        Serial.println("DESTRA");
        setColor(255,255,0);  //Giallo
        //directionControl(6000);  
        turnAround(7000);                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        setColor(0,0,0);
        //return; // Esci dalla funzione quando viene rilevato un movimento verso destra
      case DIR_NEAR:
        Serial.println("VICINO");
        break;
      case DIR_FAR:
        Serial.println("LONTANO");
        break;
      default:
        Serial.println("NESSUNO");
    }
    delay(200);
  }
}


void setup() {
  mySoftwareSerial.begin(9600);
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(ENC, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(IN5, OUTPUT);
  pinMode(IN6, OUTPUT);
  // Spegne i motori - Initial State
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  digitalWrite(IN5, LOW);
  digitalWrite(IN6, LOW);
  
  pinMode(redOut, OUTPUT);
  pinMode(greenOut, OUTPUT);
  pinMode(blueOut, OUTPUT);
  
  Serial.println();
  Serial.println(F("DFRobot DFPlayer Mini Demo"));
  Serial.println(F("Initializing DFPlayer... (May take 3~5 seconds)"));

  if (!myDFPlayer.begin(mySoftwareSerial)) { // Use softwareSerial to communicate with the MP3 module.
    Serial.println(F("Unable to begin:"));
    Serial.println(F("1. Please recheck the connection!"));
    Serial.println(F("2. Please insert the SD card!"));
    while (true)
      ;
  }
  Serial.println(F("DFPlayer Mini online."));

  // Set the interrupt pin as input
  pinMode(APDS9960_INT, INPUT);

  // Initialize the serial port
  Serial.begin(9600);
  Serial.println();
  Serial.println(F("--------------------------------"));
  Serial.println(F("SparkFun APDS-9960 - Gesture Test"));
  Serial.println(F("--------------------------------"));

  // Initialize the interrupt service routine
  attachInterrupt(0, interruptRoutine, FALLING);

  // Initialize APDS-9960 (configure I2C and initial values)
  if (apds.init()) {
    Serial.println("APDS-9960 initialization complete");
  } else {
    Serial.println("Something went wrong during APDS-9960 initialization!");
  }

  // Start the gesture sensor engine
  if (apds.enableGestureSensor(true)) {
    setColor(255,0,0);
    delay(500);
    Serial.println(F("Gesture sensor is now active"));
    setColor(0,0,0);
  } else {
    Serial.println(F("Something went wrong during gesture sensor initialization!"));
  }

  myDFPlayer.volume(30);
  //handleGesture();
  directionControl(10000);
}

void loop() {
   // Call the handleGesture function to detect right gesture
}


void turnAround(int time){
  // Imposta la potenza massima dei motori
  analogWrite(ENA, 255);
  analogWrite(ENB, 255);
  analogWrite(ENC, 255);

  // Aziona i motori A, B e C in avanti
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  digitalWrite(IN5, LOW);
  digitalWrite(IN6, HIGH);
  
  // Aspetta per il tempo specificato
  delay(time);
  
  // Ferma i motori
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  analogWrite(ENC, 0);
}

void directionControl(int time){
 // Imposta la potenza massima dei motori
  analogWrite(ENA, 255); //sinistra da davanti
  analogWrite(ENB, 255); //destra
  analogWrite(ENC, 0);

  // Aziona i motori A, B e C in avanti
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  digitalWrite(IN5, LOW);
  digitalWrite(IN6, HIGH);
  
  // Aspetta per il tempo specificato
  delay(time);
  
  // Ferma i motori
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  analogWrite(ENC, 0);
}
