#include <Arduino.h>
#if defined(ESP32)
#include <WiFi.h>
#include <FirebaseESP32.h>
#elif defined(ESP8266)
#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>
#include <HCSR04.h>
#endif

// Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>
#include <SoftwareSerial.h>
//Pinos de comunicacao serial com a ST Núcleo
#define Pin_ST_NUCLEO_RX    5  //Pino D1 da placa Node MCU
#define Pin_ST_NUCLEO_TX    4  //Pino D2 da placa Node MCU
SoftwareSerial SSerial(Pin_ST_NUCLEO_RX, Pin_ST_NUCLEO_TX);

/* 1. Define the WiFi credentials */
#define WIFI_SSID "Jorge"
#define WIFI_PASSWORD "0123456789"

/* 2. If work with RTDB, define the RTDB URL and database secret */
#define DATABASE_URL "https://projeto-pluviometro-default-rtdb.firebaseio.com/"; //<databaseName>.firebaseio.com or <databaseName>.<region>.firebasedatabase.app
#define DATABASE_SECRET "UvOHsKEIvIanQybbKJRGb6w3ET5zBEytm7ESt1dq"

/* 3. Define the Firebase Data object */
FirebaseData fbdo;

/* 4, Define the FirebaseAuth data for authentication data */
FirebaseAuth auth;

/* Define the FirebaseConfig data for config data */
FirebaseConfig config;

/* Define the names for ESP8266 pin for HC-SR04 */
#define TRIGGER_PIN 12
#define ECHO_PIN 14

/* initialize variables to store the calculation metrics */
long duration;
int distance;
int precipitation;


unsigned long dataMillis = 0;
int count = 0;
void setup()
{
    // put your setup code here, to run once:

    Serial.begin(9600);
    SSerial.begin(115200);
    pinMode(TRIGGER_PIN, OUTPUT); // configure Trigger pin(D6) as output
    pinMode(ECHO_PIN, INPUT); // configure Echo pin(D5) as input


    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to Wi-Fi");
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(300);
    }
    Serial.println();
    Serial.print("Connected with IP: ");
    Serial.println(WiFi.localIP());
    Serial.println();

    Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);

    /* Assign the certificate file (optional) */
    // config.cert.file = "/cert.cer";
    // config.cert.file_storage = StorageType::FLASH;

    /* Assign the database URL and database secret(required) */
    config.database_url = DATABASE_URL;
    config.signer.tokens.legacy_token = DATABASE_SECRET;

    Firebase.reconnectWiFi(true);

    /* Initialize the library with the Firebase authen and config */
    Firebase.begin(&config, &auth);

    // Or use legacy authenticate method
    // Firebase.begin(DATABASE_URL, DATABASE_SECRET);
}

void loop()
{
// put your main code here, to run repeatedly:

    digitalWrite(TRIGGER_PIN, LOW); //set trigger signal low for 2us
    delayMicroseconds(2);

    /*send 10 microsecond pulse to trigger pin of HC-SR04 */
    digitalWrite(TRIGGER_PIN, HIGH);  // make trigger pin active high
    delayMicroseconds(10);            // wait for 10 microseconds
    digitalWrite(TRIGGER_PIN, LOW);   // make trigger pin active low

    /*Measure the Echo output signal duration or pulss width */
    duration = pulseIn(ECHO_PIN, HIGH); // save time duration value in "duration variable
    distance = (duration*0.034/2)*10; // Convert pulse duration into distance in mm

    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" mm");

    // limit the distance value between 0 to 200 mm
    distance = constrain(distance, 0, 200);

    // covenrt distance from water surface to precipitation
    precipitation = 200 - distance;

    Serial.print("Precipitacao: ");
    Serial.print(precipitation);
    Serial.println(" mm de chuva");

    if (SSerial.available() > 0)
    {
        Serial.println("Recebido alerta do pluviômetro");
        SSerial.readString();
    }
    // Serial.print("Buffer da Serial: ");
    // Serial.println(SSerial.available());
    // Serial.print("Estado da Serial: ");
    // Serial.println(digitalRead(Pin_ST_NUCLEO_RX)); // ler o estado do pino 5

    if (millis() - dataMillis > 1000) // after 1 second
    {
        dataMillis = millis();
        Serial.printf("Measure Distance... %s\n", Firebase.setInt(fbdo, "/test/int", count++) ? "ok" : fbdo.errorReason().c_str());
        Firebase.setInt(fbdo, "/PRECIP", precipitation);
        Firebase.getInt(fbdo, "/PRECIP");
        Serial.print("PRECIP = ");
        Serial.println(fbdo.intData());
    }
    delay(1000); // wait for 1 second
}