#include <Wire.h> 
#include <OneWire.h>
#include <DallasTemperature.h>
#include <avr/eeprom.h>

// PH Sensors
#define PHSensorPin       A2           //pH meter Analog output to Arduino Analog Input 2
#define Offset            0.0         //deviation compensate
#define samplingInterval  20
#define printInterval     2000
#define ArrayLenth        40           //times of collection
int pHArray[ArrayLenth];               //Store the average value of the sensor feedback
int pHArrayIndex=0;    

// Turbid
#define TUBSensorPin      A1

// GPIO Pin define
#define ONE_WIRE_BUS      12

// parameter for temperture sensor
OneWire oneWire(ONE_WIRE_BUS);// Setup a oneWire instance to communicate with any OneWire devices
DallasTemperature sensors(&oneWire);// Pass our oneWire reference to Dallas Temperature.

unsigned long oldTime;

//** Parameters for EC sensor **//
float K = 1.66;    // default K for calibreation
int R1 = 670;     // <*************resistance 
float Ra = 0.5;    //Resistance of powering Pins
int ECPin = A4;   // Signal pin
int ECGround = A5; // Ground pin
int ECPower = A3; // Power pin
int ppm =0;
float PPMconversion=0.7;
float TemperatureCoef = 0.019; //this changes depending on what chemical we are measuring
float Temperature=10;
float EC=0;
float EC25 =0;
float raw= 0;
float Vin= 5;
float Vdrop= 0;
float Rc= 0;
float buffer=0;

// EEPROM structur
struct settings_t {
  float K;
} settings;

//** EC Calibration **//
float CalibrationEC=2.5;   // default EC for calibration
float TemperatureStart=0;
float TemperatureFinish=0;
//**//

void setup() {
  Serial.begin(9600);
  sensors.begin();

  // EC setup
  pinMode(ECPin,INPUT);
  pinMode(ECPower,OUTPUT);                //Setting pin for sourcing current
  pinMode(ECGround,OUTPUT);               //setting pin for sinking current
  digitalWrite(ECGround,LOW);             //We can leave the ground connected permanantly

  // load data from EEPROM
  eeprom_read_block((void*)&settings, (void*)0, sizeof(settings));   // read eeprom 
  K=settings.K;
}

void loop() {
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue,voltage;
  
  if(millis()-samplingTime > samplingInterval) {
      pHArray[pHArrayIndex++]=analogRead(PHSensorPin);
      if(pHArrayIndex==ArrayLenth)pHArrayIndex=0;
      voltage = avergearray(pHArray, ArrayLenth)*5.0/1024;
      pHValue = 3.5*voltage + Offset;
      samplingTime=millis();
  }

  if(millis() - printTime > printInterval) {
    // Water Temperature
    sensors.requestTemperatures();
    float t_water = sensors.getTempCByIndex(0); 

    // EC sensor
    GetEC();                 

    // Turbid
    float turbidity = analogRead(TUBSensorPin) * (5.0 / 1024.0); // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  
    // send data to raspbery pi
    Serial.print(t_water);
    Serial.print(',');
    Serial.print(EC25);
    Serial.print(',');
    Serial.print(turbidity);  
    Serial.print(',');
    Serial.println(pHValue,2);
    printTime=millis();
  }

 if (Serial.available()){
     String message = Serial.readString();
     String cmd = message.substring(0,1);
     String val = message.substring(1);
     if (cmd == "1") { // EC Calibration
        CalibrationEC = val.toFloat();
        doCalibration();
      }     
  }
}


void GetEC(){
  //*********Reading Temperature Of Solution *******************//
  sensors.requestTemperatures();// Send the command to get temperatures
  Temperature=sensors.getTempCByIndex(0); //Stores Value in Variable
   
  //************Estimates Resistance of Liquid ****************//
  digitalWrite(ECPower,HIGH);
  raw= analogRead(ECPin);
  raw= analogRead(ECPin);// This is not a mistake, First reading will be low beause if charged a capacitor
  digitalWrite(ECPower,LOW);
   
  //***************** Converts to EC **************************//
  Vdrop= (Vin*raw)/1024.0;
  Rc=(Vdrop*R1)/(Vin-Vdrop);
  Rc=Rc-Ra; //acounting for Digital Pin Resitance
  EC = 1000/(Rc*K);
   
  //*************Compensating For Temperaure********************//
  EC25  =  EC/ (1+ TemperatureCoef*(Temperature-25.0));
  ppm=(EC25)*(PPMconversion*1000);
}
//************************** End OF EC Function ***************************//

//***===Function: do Calibraion ===============================//
void doCalibration() {
  Serial.print("Cal EC=");
  Serial.println(CalibrationEC);
  while (1) {
      int i=1;
      buffer=0;
   
      sensors.requestTemperatures();                        // Send the command to get temperatures
      TemperatureStart=sensors.getTempCByIndex(0);          //Stores Value in Variable
      Serial.print("Temp Start = ");
      Serial.println(TemperatureStart);
      delay(1000);
      //******Estimates Resistance of Liquid ***************//
      while(i<=10){
        digitalWrite(ECPower,HIGH);
        raw= analogRead(ECPin);
        raw= analogRead(ECPin);                              // This is not a mistake, First reading will be low
        digitalWrite(ECPower,LOW);
        buffer=buffer+raw;
        Serial.print("Raw ");Serial.print(i);
        Serial.print(" = ");Serial.println(raw);        
        i++;
        delay(5000);
      }
      
      raw=(buffer/10);                              // cal average raw
      sensors.requestTemperatures();                // get finish temperatures
      TemperatureFinish=sensors.getTempCByIndex(0); //Stores Value in Variable
      Serial.print("Temp Finish=");Serial.println(TemperatureFinish);
 
      //*************Compensating For Temperaure********************//
      EC =CalibrationEC*(1+(TemperatureCoef*(TemperatureFinish-25.0))) ;
       
      //***************** Calculates R relating to Calibration fluid **************************//
      Vdrop= (((Vin)*(raw))/1024.0);
      Rc=(Vdrop*R1)/(Vin-Vdrop);
      Rc=Rc-Ra;
      K= 1000/(Rc*EC);
      if (TemperatureStart == TemperatureFinish){
        Serial.print("Result is OK -->");
        Serial.print(" K = ");Serial.println(K); 
        settings.K=K;
        eeprom_write_block((const void*)&settings, (void*)0, sizeof(settings)); //save all configuration to eeprom
        delay(1000);
        Serial.println("Save to EEPROM.");
        return;
      }
      else{
        delay(2000);
        Serial.println("Err-Temp not settle, calibrate again.");
      }
  }
}

double avergearray(int* arr, int number){
  int i;
  int max,min;
  double avg;
  long amount=0;
  if(number<=0){
    Serial.println("Error number for the array to avraging!/n");
    return 0;
  }
  if(number<5){   //less than 5, calculated directly statistics
    for(i=0;i<number;i++){
      amount+=arr[i];
    }
    avg = amount/number;
    return avg;
  }else{
    if(arr[0]<arr[1]){
      min = arr[0];max=arr[1];
    }
    else{
      min=arr[1];max=arr[0];
    }
    for(i=2;i<number;i++){
      if(arr[i]<min){
        amount+=min;        //arr<min
        min=arr[i];
      }else {
        if(arr[i]>max){
          amount+=max;    //arr>max
          max=arr[i];
        }else{
          amount+=arr[i]; //min<=arr<=max
        }
      }//if
    }//for
    avg = (double)amount/(number-2);
  }
  return avg;
}

