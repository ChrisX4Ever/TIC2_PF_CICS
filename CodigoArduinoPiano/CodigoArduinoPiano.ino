const int botones[] = {2,3,4,5,6,7,8,9,10}; // Pines de los botones

void setup() {
  for (int i = 0; i < 9; i++) { 
    pinMode(botones[i], INPUT_PULLUP); // Activa resistencias internas pull-up
  }
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < 9; i++) { 
    if (digitalRead(botones[i]) == LOW) {
      Serial.print(i); // 
      delay(150);
    }
  }
}