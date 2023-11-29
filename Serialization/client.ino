int paridade = 0;
int8_t s = 0b11100001;
int8_t um = 0b00000001;
boolean enviado = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(5, OUTPUT);
}

void wait(int n){
  for (int i=0; i < n; i++){
    asm("nop");
  }
}

void loop(){
  if (!enviado){
    digitalWrite(5, LOW);
    wait(1667);
    for(int i = 0; i <= 7; i++) {
      int v = (s & um);
      s = s >> 1;
      if (v == 1){
        digitalWrite(5, HIGH);
        wait(1667);
        paridade += 1;
      } else {
        digitalWrite(5, LOW);
        wait(1667);
      }
    };
    if (paridade % 2 != 0) {
      digitalWrite(5, HIGH);
      wait(1667);
    }else{
      digitalWrite(5, LOW);
      wait(1667);
    }
    digitalWrite(5, HIGH);
    wait(1667);
    enviado = true;
  }
}