const int rxPin = 4;
uint8_t binary = 0b0000000;
bool inRead = false;
int count = 0;
int parityCount = 0;
int timeWait = 1667;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(rxPin, INPUT);
}

void wait(int clocks = timeWait) {
  for (int n = 0; n < clocks ; n++) {
    asm("nop");
  }
}

void loop() {
  uint8_t rx;
  // put your main code here, to run repeatedly:
  if (!inRead) { 
    inRead = digitalRead(rxPin) == LOW;
    if (inRead) {
      wait(timeWait*1.5);
    }
    
  } else if (count < 8) {
    rx = digitalRead(rxPin);
    binary |= rx << count;
    if (rx == HIGH) parityCount++;
    count++;
    wait();

  } else {
    // Serial.println();
    rx = digitalRead(rxPin);
    bool parity = ((parityCount%2 == 0 && rx == LOW) || (parityCount%2 != 0 && rx == HIGH));
    wait();
    
    rx = digitalRead(rxPin);
    if (rx == HIGH) Serial.println("End");
    if (parity) Serial.println("Ok"); else Serial.println("Fail");
    Serial.println(binary, BIN);
    Serial.println();

    binary = 0b000000000;
    count = 0;
    parityCount = 0;
    inRead = false;
  }
}
