const int botones[] = {2, 3, 4, 5, 6, 7, 8, 9, 10}; // Pines conectados a botones
const int numBotones = 9;
bool estadoAnterior[numBotones];

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < numBotones; i++) {
    pinMode(botones[i], INPUT_PULLUP);
    estadoAnterior[i] = HIGH;
  }
}

void loop() {
  for (int i = 0; i < numBotones; i++) {
    bool estadoActual = digitalRead(botones[i]);

    // Detectar flanco de bajada: cuando se presiona el botón
    if (estadoAnterior[i] == HIGH && estadoActual == LOW) {
      Serial.println(i);  // Envía el número del botón
    }

    estadoAnterior[i] = estadoActual;
  }

  delay(10); // Pequeño delay para evitar rebotes
}