// Throttle potentiometer pin, its value, and its calculated GEOFS value
int throttlePin = 1;
int throttlePinVal = 0;
int throttleVal = 0;
int oldThrottleVal = throttleVal;

// Pitch potentiometer pin, its value, and its calculated GEOFS value
int pitchPin = 2;
double pitchPinVal = 0.00;
double pitchVal = 0.00;
double oldPitchVal = pitchVal;

// Pitch potentiometer pin, its value, and its calculated GEOFS value
int rollPin = 3;
double rollPinVal = 0.00;
double rollVal = 0.00;
double oldRollVal = rollVal;

// the amount of bytes recieved
int recieved = 0;

// Calculation constants
const int MIN = 300;
const int MAX = 700;

const int THROTTLE_DIVISOR = 44;

const int JOYSTICK_SUBTRAHEND = 200;
const int JOYSTICK_DIVISOR = 200;

// experimentals
boolean doneSend = false;
int sendCount = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(100);

  // get all values initially and send them
  // getValues();
  // resetAndSend();
  readAndFlush();

}

void loop() {
  // put your main code here, to run repeatedly:
  // calculate GEOFS values from potentiometers
  getValues();

  // in case values change(significantly) reset them and send them
  if((oldThrottleVal != throttleVal) || !(pitchVal + .01 >= oldPitchVal && oldPitchVal >= pitchVal - .01) || !(rollVal + .01 >= oldRollVal && oldRollVal >= rollVal - .01)){
    resetAndSend();
  };
}

// calculate GEOFS values from potentiometers
void getValues(){
  throttlePinVal = analogRead(throttlePin);
  pitchPinVal = analogRead(pitchPin);
  rollPinVal = analogRead(rollPin);

  // make sure values lie between MIN/MAX
  if(throttlePinVal < MIN) throttlePinVal = MIN;
  if(throttlePinVal > MAX) throttlePinVal = MAX;
  
  if(pitchPinVal < MIN) pitchPinVal = MIN;
  if(pitchPinVal > MAX) pitchPinVal = MAX;

  if(rollPinVal < MIN) rollPinVal = MIN;
  if(rollPinVal > MAX) rollPinVal = MAX;

  // calculate GEOFS values
  throttleVal = round((throttlePinVal - MIN) / THROTTLE_DIVISOR);
  pitchVal = (pitchPinVal - MIN - JOYSTICK_SUBTRAHEND) / JOYSTICK_DIVISOR;
  rollVal = (rollPinVal - MIN - JOYSTICK_SUBTRAHEND) / JOYSTICK_DIVISOR;
}

void resetAndSend(){
  // reset all values
  oldThrottleVal = throttleVal;
  oldPitchVal = pitchVal;
  oldRollVal = rollVal;
 
  // send all values
  Serial.print(throttleVal);
  Serial.print(',');
  Serial.print(pitchVal);
  Serial.print(',');
  Serial.print(rollVal);
  Serial.print('o');

  // wait to recieve resolution
  readAndFlush();
}

void readAndFlush(){
  // wait to recieve something
  while(Serial.available() == 0);
  
  // amount of bytes recieved
  recieved = Serial.available();

  // while buffer still full, read until cleared
  while(recieved > 0){
    Serial.read();
    recieved = Serial.available();
  };
}
