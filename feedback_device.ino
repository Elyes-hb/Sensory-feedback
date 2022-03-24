int vib1 =3;
int vib2 =5; 
int vib3 =6; 
int vib4 =9; 
int vib5 =10; 
int vib6 =11; 

char val ;

void setup() {
  pinMode(2,OUTPUT);
  digitalWrite(13, LOW);
  pinMode(8, OUTPUT);
  pinMode(vib1, OUTPUT);
  pinMode(vib2, OUTPUT);
  pinMode(vib3, OUTPUT);
  pinMode(vib4, OUTPUT);
  pinMode(vib5, OUTPUT);
  pinMode(vib6, OUTPUT);
   
  
Serial.begin(38400);
  // put your setup code here, to run once:

}

void loop() {

  if(Serial.available() > 0)
  {
    val=Serial.read();
//    Serial.println(val);

  }
if(val== '1'){
STOP();}

if(val== '0'){
sharp_object();
delay(1000);}

if(val== '2'){
blunt_object();
delay(1000);}

if(val== '3'){
hard_object();
delay(1000);}

if(val== '4'){
soft_object();
delay(1000);}


if(val== '5'){    //heat feedback
digitalWrite(8,HIGH);
delay(3000);}
if(val== '6'){    //power off heat feedback
digitalWrite(8,LOW);
delay(3000);}
}

void STOP(){
    analogWrite(vib1, 0);
     analogWrite(vib2,0);
     analogWrite(vib3, 0);
     analogWrite(vib4,0);
     analogWrite(vib5, 0);
     analogWrite(vib6, 0);
}
void soft_object(){
    analogWrite(vib1, 100);
     analogWrite(vib2,100);
     analogWrite(vib3, 100);
     analogWrite(vib4,0);
     analogWrite(vib5, 0);
     analogWrite(vib6,0);
}
void hard_object(){
    analogWrite(vib1, 255);
     analogWrite(vib2,255);
     analogWrite(vib3, 255);
     analogWrite(vib4,0);
     analogWrite(vib5, 0);
     analogWrite(vib6, 0);
}
void blunt_object(){
    analogWrite(vib1, 0);
     analogWrite(vib2,0);
     analogWrite(vib3, 0);
     analogWrite(vib4,100);
     analogWrite(vib5, 100);
     analogWrite(vib6, 100);
}
void sharp_object(){
    analogWrite(vib1, 0);
     analogWrite(vib2,0);
     analogWrite(vib3, 0);
     analogWrite(vib4,255);
     analogWrite(vib5, 255);
     analogWrite(vib6, 255);
}
