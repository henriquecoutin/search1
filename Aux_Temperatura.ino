#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd (0x27, 16, 2);


int pin = 0; //pino analógico LM35

float temp_c = 0, temp_f=0; 
float medicao[8]; // vetor com medições 
int i;
int inPin = 7; //pino pushbutton
int val;

void setup()
{
  Serial.begin(9600);//Inicializa comunicação serial
  lcd.init();
  lcd.backlight();
  lcd.print("Iniciando");
  delay(1000);
  lcd.clear();
  pinMode(inPin, INPUT); //declarando o pino do push button como input
}

void loop()
{
  lcd.setCursor(0,0);
  lcd.print("Iniciar medicao?");
  lcd.setCursor(0,8);
  lcd.print("Pres. o botao   ");
  
  val = digitalRead(inPin);  
  if(val == 1)
  {
    get_temp();
  }
}

void get_temp()
{
  lcd.clear();
  Serial.print("Medindo valores, aguarde...");
  lcd.setCursor(0,0);
  lcd.print("Medindo valores,");
  lcd.setCursor(0,8);
  lcd.print("aguarde...");
  
  for(i = 0;i <= 9; i++)//Loop que faz a leitura da temperatura 10 vezes a cada 1 segundo
  { 
    medicao[i] = (5.00*analogRead(pin)*100.00)/1024.00; //fazendo a conversão para graus no sensor
    //A cada leitura, incrementa o valor da variavel tempc
    temp_c = temp_c + medicao[i]; 
    delay(1000);
  }

  //Faz a média da temperatura e salva na mesma variável
  temp_c = temp_c/10.00;
   
  //Converte para Fahrenheit e armazena na variável tempf
  temp_f = (temp_c*9.00)/5.00 + 32.00;
  
  //Enviar para o monitor serial e lcd a temperatura em Celsius
  
  Serial.print("Temp.(C): ");
  Serial.print(temp_c, 3);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Temp.(C)");
  lcd.setCursor(0,8);
  lcd.print(temp_c, 3);
  temp_c = 0;
  val = digitalRead(inPin);
  Serial.print(val);
  lcd.setCursor(10,8);
  lcd.print("-> +1?");
  
  int flag = 0; //bandeira de controle do while apenas
  while(flag == 0) //flag para aguardar nova entrada para fazer mais uma medição
  {
    val = digitalRead(inPin);
    if(val == 1) flag = 1;
  }
  lcd.clear();
}
