#include <Arduino.h>
#include <AccelStepper.h>
#include <MultiStepper.h>

// //Global Step Perameters
// #define stepsPerRev 4096
// #define stepDelay 450//900 seems to be max

AccelStepper step1(AccelStepper::FULL4WIRE,13,12,14,27);
AccelStepper step2(AccelStepper::FULL4WIRE,15,2,4,16);

MultiStepper myLaser;

long incomingPos[2];
long OutgoingPos[2]; // Array of desired stepper positions
long sequence[4000];

void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
  pinMode(23,OUTPUT);
  digitalWrite(23,LOW);

  step1.setMaxSpeed(500.0);
  step2.setMaxSpeed(500.0);

  bool success = myLaser.addStepper(step1);
  success = myLaser.addStepper(step2);

}

bool status = 0;
void toggleReadingLED(){
  digitalWrite(23, !status);
  status = !status; 
}



bool nowReading = 0;
byte buff[2];
int readCount = 0;
void getPacket(){
  while(!Serial.available()){}
  if(!nowReading){
    toggleReadingLED();
    nowReading = 1;
  }

  while(nowReading){
    Serial.readBytes(buff,2);
    incomingPos[0] = (buff[1] << 8) | buff[0];
    Serial.readBytes(buff,2);
    incomingPos[1] = (buff[1] << 8) | buff[0];

    sequence[readCount*2] = incomingPos[0];
    sequence[readCount*2+1] = incomingPos[1];

    readCount++;


  if(buff[0] == '\n' || buff[1] == '\n'){
    toggleReadingLED();
    nowReading = 0;
    readCount--;
    break;
  }
  

  }
  
  //Need to await serial command
}


long inXLow = 0;
long inXHigh = 3280;
long inYLow = 0;
long inYHigh = 2464;

//Change High Values to get wider range on output
long outXLow = 0;
long outXHigh = 400*3;
long outYLow = 0;
long outYHigh = 300*3;

void processPacket(){
  //Currently Does Linear Mapping
  OutgoingPos[0] = map(incomingPos[0],inXLow,inXHigh,outXLow,outXHigh);
  OutgoingPos[1] = map(incomingPos[1],inYLow,inYHigh,outYLow,outYHigh);
}

void completeMove(){
  for(int i = 0; i < readCount; i++){
    incomingPos[0] = sequence[i*2];
    incomingPos[1] = sequence[i*2+1];
    processPacket();
    myLaser.moveTo(OutgoingPos);
    while(step1.distanceToGo() != 0 && step2.distanceToGo() != 0){
        myLaser.run();
        delay(1);
    }
  }
  
}

long t1;
long t2;

void runTest(){
  t1 = millis();
  //Test Sequence
  for(int i = 1; i < 500; i++){
      incomingPos[0] = map(i,0,500,0,outXHigh);
      incomingPos[1] = map(i,0,500,0,outYHigh);
      processPacket();
      completeMove();
  }
  t2 = millis();
  Serial.print("Time Elapsed: ");
  Serial.println(t2-t1);
}

void loop() {
  // runTest();
  getPacket();
  completeMove();
  readCount = 0;
}