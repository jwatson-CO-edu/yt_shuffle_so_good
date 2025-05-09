////////// INIT ////////////////////////////////////////////////////////////////////////////////////
///// Includes ////////////////////////////////////////////////////////////
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

///// Button Setup ////////////////////////////////////////////////////////
const int     CENTER/*------*/ = D1;
const int     RIGHT /*------*/ = D2;
const int     LEFT /*-------*/ = D3;
const int     UP /*---------*/ = D4;
const int     DOWN /*-------*/ = D5;
unsigned long lastDebounceTime =   0;
unsigned long debounceDelay    = 200;

///// BLE Setup ///////////////////////////////////////////////////////////
BLEServer* /*---*/ pServer /*------*/ = NULL;
BLECharacteristic* pCharacteristic    = NULL;
bool /*---------*/ deviceConnected    = false;
bool /*---------*/ oldDeviceConnected = false;

// Define UUIDs for service and characteristic
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"



////////// BLE SERVICE /////////////////////////////////////////////////////////////////////////////


class MyServerCallbacks: public BLEServerCallbacks {
  // Class to handle server callbacks (connections/disconnections)
  void onConnect( BLEServer* pServer ){
    deviceConnected = true;
    Serial.println( "Device connected" );
  };

  void onDisconnect( BLEServer* pServer ){
    deviceConnected = false;
    Serial.println( "Device disconnected" );
  }
};


////////// SETUP ///////////////////////////////////////////////////////////////////////////////////

void setup() {
  ///// Set the digital pins connected to the button inputs ///////////////
  pinMode( CENTER, INPUT_PULLDOWN );
  pinMode( RIGHT , INPUT_PULLDOWN );
  pinMode( LEFT  , INPUT_PULLDOWN );
  pinMode( UP    , INPUT_PULLDOWN );
  pinMode( DOWN  , INPUT_PULLDOWN );

  ///// Setup serial printing /////////////////////////////////////////////
  Serial.begin();
  delay( 1000 );      // 1 second delay should be sufficient
  Serial.println( "Setup complete" );
  Serial.println( "Bluetooth Mouse Button - ESP32-C3" );

  ///// Setup BLE /////////////////////////////////////////////////////////
  BLEDevice::init( "ESP32-C3 Mouse Control" ); // Initialize BLE device
  // Create BLE server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks( new MyServerCallbacks() );
  // Create BLE service
  BLEService *pService = pServer->createService( SERVICE_UUID );

  // Create BLE characteristic
  pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ   |
    BLECharacteristic::PROPERTY_WRITE  |
    BLECharacteristic::PROPERTY_NOTIFY
  );
  
  // Add a descriptor to the characteristic
  pCharacteristic->addDescriptor( new BLE2902() );
  
  // Start the service
  pService->start();
  
  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID( SERVICE_UUID );
  pAdvertising->setScanResponse( true );
  pAdvertising->setMinPreferred( 0x06 );  // Functions that help with iPhone connections
  pAdvertising->setMinPreferred( 0x12 );
  BLEDevice::startAdvertising();
  
  Serial.println( "BLE device ready. Waiting for connections..." );
}

////////// MAIN ////////////////////////////////////////////////////////////////////////////////////

void send( const char* msg ){
  pCharacteristic->setValue( msg );
  pCharacteristic->notify();
  Serial.printf( "%s signal sent!\n", msg );
}

void loop() {
  // put your main code here, to run repeatedly:
  int cn, rt, lf, shift, dn, cnLst = 0, rtLst = 0, lfLst = 0, shiftLst = 0, dnLst = 0;
  const char* clickSignal   = "CLICK";
  const char* forwardSignal = "FWD";
  const char* backSignal    = "BCK";
  const char* nextSignal    = "NEXT";
  const char* volUpSignal   = "VOLUP";
  const char* volDnSignal   = "VOLDN";

  cn    = digitalRead( CENTER );
  rt    = digitalRead( RIGHT  );
  lf    = digitalRead( LEFT   );
  shift = digitalRead( UP     );
  dn    = digitalRead( DOWN   );

  

  // If the button state has been stable for the debounce period
  if( (millis() - lastDebounceTime) > debounceDelay){
    // If a device is connected, send the "CLICK" signal
    if( deviceConnected ){
      
      if( cn ){
        send( clickSignal );
      }else if( rt ){
        if( shift ){  send( volUpSignal );  }else{  send( forwardSignal );  }
      }else if( lf ){
        if( shift ){  send( volDnSignal );  }else{  send( backSignal );  }
      }else if( dn ){
        send( nextSignal );
      }
      
    }else{
      Serial.println( "No device connected, signal not sent" );
    }
    if( (cn != cnLst) || (rt != rtLst) || (lf != lfLst) || (shift != shiftLst) || (dn != dnLst) ){  lastDebounceTime = millis();  }
    cnLst    = cn;
    rtLst    = rt;
    lfLst    = lf;
    shiftLst = shift;
    dnLst    = dn;
  }

  // Handle connection changes
  if( !deviceConnected ){
    delay( 500 ); // Give time for the BLE stack to get things ready
    pServer->startAdvertising(); // Restart advertising
    Serial.println( "Restarting advertising" );
    oldDeviceConnected = deviceConnected;
  }

  // If just connected
  if( deviceConnected && (!oldDeviceConnected) ){  oldDeviceConnected = deviceConnected;  }
  
  // Serial.printf( "CENTER %d, RIGHT %d, LEFT %d, UP %d, DOWN %d, \n", cn, rt, lf, up, dn );
}
