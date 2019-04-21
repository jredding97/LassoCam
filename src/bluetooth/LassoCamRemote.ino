//Bluetooth setup
#include <SoftwareSerial.h>  

int bluetoothTx = 3;  // TX-O pin of bluetooth mate, Arduino D3
int bluetoothRx = 2;  // RX-I pin of bluetooth mate, Arduino D2

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

//Pin setup
const int lsoLsrPin = 5;
const int lsrPin = 6;
const int homeButtonPin = 7;
const int lsrOutputPin = 4;

int lsoLsrState = 0;
int lsrState = 0;
int homeState = 0;

void setup() {
  // put your setup code here, to run once:

  //Serial.begin(9600);  // Begin the serial monitor at 9600bps
  
  bluetooth.begin(115200);  // The Bluetooth Mate defaults to 115200bps
  
  delay(100);
  
  bluetooth.print("$");  // Print three times individually
  bluetooth.print("$");
  bluetooth.print("$");  // Enter command mode
  
  delay(100);  // Short delay, wait for the Mate to send back CMD
  
  bluetooth.println("U,9600,N");  // Temporarily Change the baudrate to 9600, no parity
  // 115200 can be too fast at times for NewSoftSerial to relay the data reliably
  
  bluetooth.begin(9600);  // Start bluetooth serial at 9600*/

  pinMode(lsoLsrPin, INPUT);
  pinMode(lsrPin, INPUT);
  pinMode(homeButtonPin, INPUT);
  pinMode(lsrOutputPin, OUTPUT);

  digitalWrite(lsrOutputPin, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:

  // delay(1000) = wait for roughly 16 seconds
  // Therefore, delay(63) waits for one second

  int lsoLsr = 0;

  lsoLsrState = digitalRead(lsoLsrPin);
  lsrState = digitalRead(lsrPin);
  homeState = digitalRead(homeButtonPin);

  if (lsoLsrState == HIGH)
  {
    bluetooth.println(1);
    lsoLsr = 1;
    digitalWrite(lsrOutputPin, HIGH);
  }
 
  else
  {
    //bluetooth.println("");
    //digitalWrite(lsrOutputPin, LOW);
  }

  if(lsrState == HIGH)
  {
    //bluetooth.println(2);
    digitalWrite(lsrOutputPin, HIGH);
  }
  else
  {
    //bluetooth.println("");
    //digitalWrite(lsrOutputPin, LOW);
  }

  if(homeState == HIGH)
  {
    bluetooth.println(2);
  }
  else
  {
    //bluetooth.println("");
  }

  while(lsoLsrState == HIGH || lsrState == HIGH || homeState == HIGH)
  {
    lsoLsrState = digitalRead(lsoLsrPin);
    lsrState = digitalRead(lsrPin);
    homeState = digitalRead(homeButtonPin);
    
    delay(10);
  }

  digitalWrite(lsrOutputPin, LOW);

  if(lsoLsr == 1)
  {
    bluetooth.println(3);
  }
 
}
