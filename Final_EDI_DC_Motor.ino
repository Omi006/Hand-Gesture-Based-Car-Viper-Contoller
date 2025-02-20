#include<cvzone.h> 
SerialData datacom(1,2);//(number recivers from python, digitspervalues)
int enA=9;
int in1=8;
int in2=7;

int valRec[1];
int speedLevel = 0; 
void setup() {
  // put your setup code here, to run once:
  datacom.begin(9600);
  pinMode(enA,OUTPUT);
  pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);

  digitalWrite(in1,LOW);
  digitalWrite(in2,LOW);
 
  
}

void loop() {
 datacom.Get(valRec);
  moveWiper(speedLevel);
 if(valRec==1){
  speedLevel = 1;  // Low speed
 }
 if(valRec==2){
  speedLevel = 2;  // Medium speed
 }
 if(valRec==3){
  speedLevel = 3;  // High speed
 }

 else{
  digitalWrite(in1,LOW);
  digitalWrite(in2,LOW);
 }
 

}

void moveWiper(int speed) {
    int delayTime;

    if (speed == 1) {
        delayTime = 1000;  // Slow speed
    } else if (speed == 2) {
        delayTime = 500;  // Medium speed
    } else if (speed == 3) {
        delayTime = 250;  // Fast speed
    } else {
        return;  // Do nothing if speed is invalid
    }

    // Move wiper back and forth
    wiper.write(0);
    delay(delayTime);
    wiper.write(180);
    delay(delayTime);
}
