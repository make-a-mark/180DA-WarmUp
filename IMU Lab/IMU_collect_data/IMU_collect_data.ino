#include <Arduino_LSM9DS1.h>

void setup() 
{
  Serial.begin(9600);
  // initialize the IMU
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // print out the samples rates of the IMUs
  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");

  Serial.println();
}

void loop() 
{
  float aX, aY, aZ, gX, gY, gZ;
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) 
  {
      // read the acceleration and gyroscope data
      IMU.readAcceleration(aX, aY, aZ);
      IMU.readGyroscope(gX, gY, gZ);

      Serial.print(aX);
      Serial.print('\t');
      Serial.print(aY);
      Serial.print('\t');
      Serial.print(aZ);
      Serial.print('\t');
      Serial.print(gX);
      Serial.print('\t');
      Serial.print(gY);
      Serial.print('\t');
      Serial.println(gZ);
  }
  

}
