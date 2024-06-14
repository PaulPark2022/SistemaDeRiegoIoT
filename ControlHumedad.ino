const int pinLed = 13;

void setup() {
  Serial.begin(9600);
  pinMode(pinLed, OUTPUT);
  
}



void loop() {
  if (Serial.available()>0)
  {
    char option = Serial.read();
    if (option == 'A'){
      digitalWrite(pinLed,HIGH);

    }
    else if (option == 'a'){
      digitalWrite(pinLed,LOW);  
    }
  }
}