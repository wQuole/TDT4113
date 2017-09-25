// this constant won't change:
const int  buttonPin = 3;    // the pin that the pushbutton is attached to
const int ledpin_green = 12;       // the pin that the LED is attached to
const int ledpin_red = 13;     //OG

// Variables will change:
int buttonPushCounter = 0;   // counter for the number of button presses
int buttonState = 0;         // current state of the button
int lastButtonState = 0;     // previous state of the button

// Timevariables
long prev_millis = 0;
long pressedTime = 0;
long pausedTime = 0;
long releaseTime = 0;


void setup() {
  // initialize the button pin as a input:
  pinMode(buttonPin, INPUT);
  // initialize the LED as an output:
  pinMode(ledpin_green, OUTPUT);
  // initialize the LED as an output:
  pinMode(ledpin_red, OUTPUT);
  // initialize serial communication:
  Serial.begin(9600);
}

void howLongPause(long pausedTime){
  if(pausedTime != 0){
    if(pausedTime >= 600 && pausedTime < 1200){
      Serial.print('2');
    }
    else if(pausedTime >= 1200){
      Serial.print('3');
    }
  }
}

void howLongPressed(long pressedTime){
    if(pressedTime != 0){
       if(pressedTime <= 400){
      Serial.print('0');
      digitalWrite(ledpin_green, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(400);                       // wait for a second
      digitalWrite(ledpin_green, LOW);    // turn the LED off by making the voltage LOW 
    }
    else{
       Serial.print('1');
       digitalWrite(ledpin_red, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(400);                       // wait for a second
        digitalWrite(ledpin_red, LOW);    // turn the LED off by making the voltage LOW 
    }
  }
}

void loop() {
  // read the pushbutton input pin:
  //buttonState = digitalRead(buttonPin);
  pausedTime = millis() - releaseTime;
  prev_millis = millis();
  
  
  while(digitalRead(buttonPin) == LOW){
    if(pausedTime > 0){
      howLongPause(pausedTime);
      pausedTime = 0;   
    }
    pressedTime = millis() - prev_millis;
    releaseTime = millis();
  }
  if(pressedTime > 50){
     howLongPressed(pressedTime);
     pressedTime = 0;
  }  
}
