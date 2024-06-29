int phValue;
float voltage;

int phValue;
float phVoltage;
const int phSensorPin = 34;
float ph;
float ph4 = 3.30; // voltase pada larutan 4.00
float ph7 = 2.60; // voltase pada larutan 6.86

void setup() {
  Serial.begin(115200);
}

void loop() {
  phValue = analogRead(phSensorPin);
  phVoltage = phValue * (3.3 / 4095.0); 
  float phStep = (ph4 - ph7) / 2.86;
  ph = 6.86 + ((ph7 - phVoltage) / phStep);

  Serial.print("PH          : ");
  Serial.println(ph);
  Serial.print("PH Voltage : ");
  Serial.println(phVoltage);
}