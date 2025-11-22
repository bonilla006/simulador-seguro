/*#include <ESP32Servo.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>
#include <Password.h>
#include "mbedtls/md.h"
#include <WiFi.h>
#include <PubSubClient.h>
#define ServoPin 15

Servo servo;

LiquidCrystal_I2C lcd(0x27, 16, 2);

const byte ROWS = 4;
const byte COLS = 4;

char keys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'c'},
  {'*', '0', '#', 'D'},
};
byte rowPins[ROWS] = {23, 19, 18, 5};
byte colPins[COLS] = {17, 16, 4, 2};

///////////////////////////////////
//variables de control
bool isDoorLocked = true;
Password password = Password("1234");
String localpssw = ""; //para poder visualizar y hash
String hashpssw = "";
bool pssw_correcto = false;
byte max_len_passw = 6;
byte current_len_passw = 0;
//creacion del objeto Keypad
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

//credenciales para wifi
const char* SSID = "Wokwi-GUEST";
const char* PASSW = "";

//credenciales para comunicacion con mqtt
const char* SERV_MQTT = "broker.hivemq.com";
const int PORT_MQTT =  1883;
const char* ASUNTO_MQTT = "/smartlock/mqtt/";

//objeto cliente
WiFiClient smartlock;
PubSubClient cliente(smartlock);
///////////////////////////////////


void setup() {
  Serial.begin(115200);
  Serial.println("Conectandoce a internet...");
  //conectarse a internet
  WiFi.begin(SSID, PASSW);
  while(WiFi.status() != WL_CONNECTED){
    Serial.println(WiFi.status());
    delay(2000);
  }
  Serial.println("Conectado al WiFi!");

  //set mqtt
  cliente.setServer(SERV_MQTT, PORT_MQTT);
  conexionMQTT();

  //mandar mensaje de presentacion
  String payload = "{\"acc\":\"ack\",\"iot_id\":\"AAAA-0000\",\"estado\":\"bloqueado\"}";
  cliente.publish(ASUNTO_MQTT, payload.c_str());

  //conectar el mecanismo con el microprocesador
  servo.attach(ServoPin);
  //pocision inicial de la palanca del sistema de bloqueo
  servo.write(90); 

  lcd.init();
  lcd.backlight();
  //en que seccion de la pantalla comenzara a escribir
  lcd.setCursor(0,0);
  lcd.print("Inicio de Sim");
  delay(2000);
  lcd.clear();
}

void loop() {
  //validar que no se haya cortado la comunicacion
  if(!cliente.connected()){
    conexionMQTT();
  }
  
  lcd.setCursor(0,0);
  isDoorLocked ? lcd.print("Contraseña:") : lcd.print("Bienvenido!");

  //devuelve el digito que se ingreso en el keypad
  char digito = keypad.getKey();

  //siempre que no sea nulo
  if(digito != NO_KEY){
    delay(100);
    if(digito != '*'){
      Serial.println(digito);
      //procesar el codigo ingresado
      procesarDigito(digito);
    }else{
      lcd.clear();
      
      //hash la contraseña
      hashpssw = computeSHA256(localpssw);

      //enviar la data hacia el servidor
      String payload = "{\"acc\":\"passw\",\"iot_id\":\"AAAA-0000\",\"pssw\":\"" + hashpssw + "\"}";
      cliente.publish(ASUNTO_MQTT, payload.c_str());

      if(password.evaluate()){
        servo.write(180); //simula que se abrio la cerradura
        isDoorLocked = false;
      } else {
        lcd.clear();
        displayMessage("No contraseña ", "Trate de nuevo");
        reset();
      }
    }
  }
}


void conexionMQTT(){
  //si el dispositivo no esta conectado
  while(!cliente.connected()){
    Serial.println("Iniciando conexion con broker-mqtt...");
    if(cliente.connect("wokwi_smartlock")){
      Serial.println("conexion con broker-mqtt exitosa!");
    }else{
      Serial.print(" failed, rc=");
      Serial.print(cliente.state());
      Serial.println("intentar en 5 segundos...");
      delay(5000);
    }
  }
}

String computeSHA256(const String& data) {
    uint8_t hash[32];
    mbedtls_md_context_t ctx;
    mbedtls_md_type_t md_type = MBEDTLS_MD_SHA256;

    mbedtls_md_init(&ctx);
    mbedtls_md_setup(&ctx, mbedtls_md_info_from_type(md_type), 0);
    mbedtls_md_starts(&ctx);
    mbedtls_md_update(&ctx, (const unsigned char*)data.c_str(), data.length());
    mbedtls_md_finish(&ctx, hash);
    mbedtls_md_free(&ctx);

    // Convertir a String hexadecimal
    String hashStr = "";
    for(int i = 0; i < 32; i++) {
        char buf[3];
        sprintf(buf, "%02x", hash[i]);
        hashStr += buf;
    }
    return hashStr;
}

void procesarDigito(char digito){
  //llenar el posible passw con los digitos ingresados
  if(current_len_passw < max_len_passw){
    //mover el cursor segun ingresado
    lcd.setCursor(current_len_passw, 1);
    lcd.print("*");
    password.append(digito);
    localpssw += digito;
    current_len_passw++;
  }
}

void reset(){
  password.reset();
  current_len_passw = 0;
  lcd.clear();
  lcd.setCursor(0, 0);
}

void displayMessage(const char *line1, const char *line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
  delay(3000);
  lcd.clear();
}
*/