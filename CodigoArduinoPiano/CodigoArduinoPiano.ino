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

    // Flanco de bajada
    if (estadoAnterior[i] == HIGH && estadoActual == LOW) {
      if (i == indiceBotonEspecial) {
        tiempoPresionado = millis();
        esperandoLargaPresion = true;
      } else {
        Serial.println(i);
      }
    }

    // Si estamos esperando una larga presión del botón especial...
    if (i == indiceBotonEspecial && esperandoLargaPresion) {
      if (estadoActual == LOW) {
        if (millis() - tiempoPresionado >= 3000) {
          Serial.println("A");  // Presionado 3 segundos
          esperandoLargaPresion = false;
        }
      } else {
        // Se soltó antes de los 3 segundos
        if (millis() - tiempoPresionado < 3000) {
          Serial.println(i);  // Enviar número del botón
        }
        esperandoLargaPresion = false;
      }
    }

    estadoAnterior[i] = estadoActual;
  }

  delay(10);
}