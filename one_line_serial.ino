#include <Wire.h>
int SLAVE_ADDRESS = 0x08;
int fsrReading = 0;
int fsrReading1 = 0;
int fsr_index = 0;
int fftread = 0;
int i = 0;
int j = 0;
int cnt = 0;
char state;
int s1 = 0;
int s2 = 0;
int s3 = 0;
int s4 = 0;
int s5 = 0;
int s6 = 0;
int s7 = 0;
int s8 = 0;
int s9 = 0;
int s_Temp1 = 0;
int s_Temp2 = 0;
int s_Temp3 = 0;
int s_currrent1;
int s_currrent2;
int s_currrent3;
int s_currrent4;

void setup() {
Serial1.begin(38400);
 Serial.begin(115200);
   pinMode(31,OUTPUT);
digitalWrite(31,LOW);
  pinMode(33,OUTPUT);
digitalWrite(33,LOW);
  pinMode(35,OUTPUT);
digitalWrite(35,LOW);
  pinMode(39,OUTPUT);
digitalWrite(39,LOW);
  pinMode(41,OUTPUT);
digitalWrite(41,LOW);
  pinMode(43,OUTPUT);
digitalWrite(43,LOW);
}

void loop() {
  fsrReading = analogRead(A0);
//if ( j < 1000){
j = millis();
fsrReading = analogRead(A0);

s1 = map(analogRead(A1), 0, 1024, 0, 5000);
s2 = map(analogRead(A0), 0, 1024, 0, 5000); 
s3 = map(analogRead(A2), 0, 1024, 0, 5000);
s4 = map(analogRead(A3), 0, 1024, 0, 5000);
s5 = map(analogRead(A4), 0, 1024, 0, 5000); 
s6 = map(analogRead(A5), 0, 1024, 0, 5000);
s7 = map(analogRead(A1), 0, 1024, 0, 5000);
s8 = map(analogRead(A1), 0, 1024, 0, 5000);
s9 = s9+1;

s_Temp1 = analogRead(A1);
s_Temp2 = analogRead(A1);
s_Temp3 = analogRead(A1);
s_currrent1 = analogRead(A1);
s_currrent2 = analogRead(A1);
s_currrent3 = analogRead(A1);
s_currrent4 = analogRead(A1);

Serial.println((String)s1+","+s2+","+s3+","+s4+","+s5+","+s6+","+s7+","+s8+","+s_Temp1+","+s_Temp2+","+s_Temp3+","+s_currrent1+","+s_currrent2+","+s_currrent3+","+s_currrent4+","+s9);
  if(Serial.available() > 0){
  // digitalWrite(ledPin, LOW); // Checks whether data is comming from the serial port
      state = Serial.read();
   }
  if (state == '0'){
  Serial1.write('0'); // Sends '1' to the slave
  }
  if (state == '1'){
  Serial1.write('1');
  }
  if (state == '2'){
  Serial1.write('2'); // Sends '2' to the slave
  }
  if (state == '3'){
  Serial1.write('3');
  }
  if (state == '4'){
  Serial1.write('4');
  }
  
  
}
