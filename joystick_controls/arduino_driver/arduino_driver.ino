int x;

const int x_in = A0;
const int y_in = A1;

int xIn, yIn;

void setup() {
   // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(1);
}

void loop() {
//   while (!Serial.available());
//   x = Serial.readString().toInt();
   Serial.println("35,50");
//  readJoystick();
}

void readJoystick() {
  xIn = analogRead(x_in);
  yIn = analogRead(y_in);
  Serial.print(xIn);
}
