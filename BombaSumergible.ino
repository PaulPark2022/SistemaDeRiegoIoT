// Primera prueba de código, originalmente planeada para un Arduino

#define pin_led 2

void setup() {
  pinMode(2, OUTPUT);
}

void loop() {
  digitalWrite(2, HIGH);
  delay(5000);
  digitalWrite(2, LOW);
  delay(10000)
}
