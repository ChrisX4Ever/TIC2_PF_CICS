const int botones[] = {2, 3, 4, 5, 6, 7, 8, 9, 10}; // Pines conectados a botones
const int numBotones = sizeof(botones) / sizeof(botones[0]);
bool estadoAnterior[numBotones];

unsigned long tiempoPresionado = 0;
bool esperandoLargaPresion = false;
const int indiceBotonEspecial = 7; // botón 8 (pin 9)

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

    // Flanco de bajada (botón presionado)
    if (estadoAnterior[i] == HIGH && estadoActual == LOW) {
      if (i == indiceBotonEspecial) {
        // Inicia contador para detección de larga presión
        tiempoPresionado = millis();
        esperandoLargaPresion = true;
      } else {
        Serial.println(i); // Botón normal
      }
    }

    // Si estamos esperando larga presión...
    if (i == indiceBotonEspecial && esperandoLargaPresion) {
      // Si el botón sigue presionado
      if (estadoActual == LOW) {
        if (millis() - tiempoPresionado >= 3000) {
          Serial.println("A");  // Enviar señal especial
          esperandoLargaPresion = false; // Ya se procesó
        }
      } else {
        // Se soltó antes de los 3 segundos, cancelar
        esperandoLargaPresion = false;
      }
    }

    estadoAnterior[i] = estadoActual;
  }

  delay(10); // Anti-rebote
}