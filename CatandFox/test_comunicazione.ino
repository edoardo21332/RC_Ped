// Includi le librerie necessarie
#include <Ultrasonic.h>
#include <SoftwareSerial.h>

// Definisci i pin utilizzati
#define TRIGGER_PIN 10
#define ECHO_PIN 6
const int RXPin = 2;  // da collegare su TX di HC05
const int TXPin = 4;  // da collegare su RX di HC05

// Definisci variabili globali
int distance2;  // Distanza calcolata dal sensore ad ultrasuoni
unsigned long tempo;  // Variabile di tempo
long distance = 150;  // Distanza massima di lettura del sensore ad ultrasuoni
const int ritardo = 200;  // Tempo necessario tra un comando ed il successivo
String msgIn;  // Messaggio ricevuto dall'HC05
String msgOut;  // Messaggio da inviare all'HC05
String msgOut2;  // Messaggio di risposta
char a[100];  // Buffer per la trasmissione seriale

// Definisci i pin utilizzati per i motori
int ENA = 9;
int IN1 = 8;
int IN2 = 7;
int ENB = 11;
int IN3 = 3;
int IN4 = 5;

// Crea un'istanza del sensore ad ultrasuoni
Ultrasonic ultrasonic(TRIGGER_PIN, ECHO_PIN);

// Crea un'istanza della porta seriale per l'HC05
SoftwareSerial BTSerial(RXPin, TXPin); // RX, TX

void setup() {
  // Inizializza la porta seriale per la comunicazione con il PC
  Serial.begin(38400);
  Serial.println("Gatto e la Volpe begin");
  // Inizializza la porta seriale per la comunicazione con l'HC05
  BTSerial.begin(38400);
  // Imposta i pin per 0i motori come output
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  // Spegne i motori - Initial State
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  // Ricevi il primo comando dall'HC05
  receiver();
  // Leggi la distanza dal sensore ad ul0trasuoni
  sensorRead();
  // Gira a sinistra
  aSinistra(6000);
  // Muovi avanti
  directionControl(6000);
}

void loop() {
  // Il loop è vuoto perché l'esecuzione viene gestita dalle funzioni
}

void receiver(){
  // Ciclo finché non viene ricevuto il messaggio di conferma "$ACK#"
  while(msgOut!="$ACK#"){
    // Aspetta finché non è disponibile nessun dato sulla seriale Bluetooth
    while (!BTSerial.available()) {}
    
    // Legge i dati in arrivo e li memorizza nella variabile msgIn
    msgIn = "";
    while (BTSerial.available()) {
       char c = BTSerial.read();
       msgIn = msgIn + c;
    }      
    Serial.println(msgIn);

    // Invia un segnale ACK a Pinocchio
    if (msgIn == "$VAI#") {
       msgOut = "ACK";
       int len = strlen(msgOut.c_str());
       char a[len+2];
       a[0] = '$';
       for (int i=1; i <= len; i++) {
         a[i] = msgOut.charAt(i-1);  
       }
       a[len+1] = '#';
       msgOut = "";
       for (int i=0; i <= len+1; i++) {
         msgOut = msgOut + a[i]; 
         BTSerial.println(a[i]);
         delay(200); 
       }

       Serial.println(msgOut);
    }
  }
}

void sensorRead() {
  // Memorizza il tempo di inizio
  unsigned long startTime = millis();
  // Legge il sensore ad ultrasuoni finché la distanza è maggiore di 50 cm e il tempo passato è minore di 4 secondi
  while ((distance > 120) && (millis() - startTime < 5000)) {
    distance = ultrasonic.read();
    distance2 = int(distance);
    BTSerial.print(distance2);
    BTSerial.print("!");
    Serial.print("Distance: ");
    Serial.print(distance2);
    Serial.println(" cm");
    delay(500);
  }
}

void directionControl(int time){
  // Imposta la potenza massima dei motori
  analogWrite(ENA, 117);
  analogWrite(ENB, 255);

  // Aziona i motori A e B in avanti
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  
  // Aspetta per il tempo specificato
  delay(time);
  
  // Ferma i motori
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void aSinistra(int time){
  // Imposta la potenza del motore A
  analogWrite(ENA, 125);

  // Aziona i motori A e B in modo da girare a sinistra
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  
  // Aspetta per il tempo specificato
  delay(time);
  
  // Ferma i motori
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void aDestra(int time){
  // Imposta la potenza del motore A
  analogWrite(ENB, 255);

  // Aziona i motori A e B in modo da girare a sinistra
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  // Aspetta per il tempo specificato
  delay(time);

  // Ferma il motore A
  analogWrite(ENB, 0);
}
