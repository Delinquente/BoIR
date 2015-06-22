
#include <LiquidCrystal.h>
String msg = "  ";
char character;
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  // set up the LCD's number of columns and rows: 
  lcd.begin(16, 2);
  // Print a message to the LCD.
  Serial.begin(9600);
  Serial.print("Program Initiated\n"); 
}

void loop() {
      while (Serial.available()>0){   
        character=Serial.read();
        msg.concat(character);
       delay(10);   
    }
    
  lcd.setCursor(0, 0);
  //Serial.println(msg);
  for (int i = 0; i < 16; i++){
    lcd.setCursor(i, 0);
    lcd.print(msg[i]);
  }
  delay(1000);
  msg="";
}

