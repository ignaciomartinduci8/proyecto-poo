int ledRojo = 11;    // Pin para el LED rojo
int ledVerde = 9;   // Pin para el LED verde
int ledAmarillo = 10; // Pin para el LED amarillo

void setup() {
  pinMode(ledRojo, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledAmarillo, OUTPUT);
  Serial.begin(9600); // Iniciar la comunicación serie a 9600 bps
}

void loop() {
  // Verificar si hay datos disponibles en el puerto serie
  if (Serial.available() > 0) {
    digitalWrite(ledRojo, LOW);    // Apagar el LED rojo
    digitalWrite(ledVerde, HIGH);   // Encender el LED verde
    digitalWrite(ledAmarillo, HIGH); // Encender el LED amarillo
  } else {
    digitalWrite(ledRojo, HIGH);    // Encender el LED rojo
    digitalWrite(ledVerde, LOW);     // Apagar el LED verde
    digitalWrite(ledAmarillo, LOW);  // Apagar el LED amarillo
  }
  delay(1000); // Esperar 1 segundo antes de volver a verificar
}