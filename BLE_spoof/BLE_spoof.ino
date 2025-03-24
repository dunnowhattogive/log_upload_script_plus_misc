#include <BLE2902.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

BLEAdvertising *pAdvertising;

// User selectable variables
int deviceType = 1;//1=smart_eye_mini,2=smart_snap,3=smart_sense_mini etc.
int delaySeconds = 2; // delay in seconds
// int advType = 2; 
//   // 0 - ADV_TYPE_IND
//   // 1 - ADV_TYPE_DIRECT_IND_HIGH (directed advertisement with high duty cycle)
//   // 2 - ADV_TYPE_SCAN_IND
//   // 3 - ADV_NONCONN_IND
//   // 4 - ADV_TYPE_DIRECT_IND_LOW (directed advertisement with low duty cycle)


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Starting ESP32 BLE");

  BLEDevice::init("");

  // Create the BLE Server
  BLEServer *pServer = BLEDevice::createServer();

  pAdvertising = pServer->getAdvertising();
  BLEAdvertisementData oAdvertisementData = BLEAdvertisementData();

  uint8_t smart_eye_mini[31] = {0x04,0x3e,0x39,0x0d,0x01,0x13,0x00,0x00,0x8c,0x60,0xf0,0x9c,0xbc,0x80,0x01,0x00,0xff,0x7f,0xad,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}; //043e390d011300008c60f09cbc800100ff7fad0000000000000000001f02010603038afd17ff0f06140000f0810000020000434d0000000000000000
  uint8_t smart_snap[31] = {};
  uint8_t smart_sense_mini[31] = {};
  uint8_t smart_clima[31] = {};
  uint8_t smart_catch_mini[31] = {};
  uint8_t smart_eye_mini_old[31] = {};
  uint8_t smart_snap_old[31] = {};
  uint8_t smart_sense_mini_old[31] = {};

  // uint8_t* data = {}; fill this at a later date 

  // Select the appropriate data based on the device type
  uint8_t* data;
  switch(deviceType) {
    case 1:
      data = smart_eye_mini;
      break;
    case 2:
      data = smart_snap;
      break;
    case 3:
      data = smart_sense_mini;
      break;
    case 4:
      data = smart_clima;
      break;
    case 5:
      data = smart_catch_mini;
      break;
    case 6:
      data = smart_eye_mini_old;
      break;
    case 7:
      data = smart_snap_old;
      break;
    case 8:
      data = smart_sense_mini_old;
      break;
    default:
    data = smart_eye_mini; // default to smart_eye_mini if no valid deviceType is provided
    break;
  }

  // // Set the advertisement data type
  // switch(advType) {
  //   case 0:
  //     pAdvertising->setAdvertisementType(ADV_TYPE_IND);
  //     break;
  //   case 1:
  //     pAdvertising->setAdvertisementType(ADV_TYPE_DIRECT_IND_HIGH);
  //     break;
  //   case 2:
  //     pAdvertising->setAdvertisementType(ADV_TYPE_SCAN_IND);
  //     break;
  //   case 3:
  //     pAdvertising->setAdvertisementType(ADV_TYPE_NONCONN_IND);
  //     break;
  //   case 4:
  //     pAdvertising->setAdvertisementType(ADV_TYPE_DIRECT_IND_LOW);
  //     break;
  // }
  
  // Set up the advertisement data
  oAdvertisementData.addData(std::string((char*)data, sizeof(smart_eye_mini)));
  pAdvertising->setAdvertisementData(oAdvertisementData);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Start advertising
  Serial.println("Sending Advertisement...");
  pAdvertising->start();
  delay(delaySeconds * 1000); // delay for delaySeconds seconds
  pAdvertising->stop();
}
