from PiicoDev_Unified import sleep_ms # Cross-platform compatible sleep function
from PiicoDev_BME280 import PiicoDev_BME280 # Sensor library
from PiicoDev_SSD1306 import * # Display library

### Main ###
sensor = PiicoDev_BME280() # initialise the sensor
zeroAlt = sensor.altitude() # take an initial altitude reading

while True:
    # Print data
    tempC, presPa, humRH = sensor.values() # read all data from the sensor
    pres_hPa = presPa / 100 # convert air pressurr Pascals -> hPa (or mbar, if you prefer)
    print("\r"+str(tempC)+" degrees C  " + str(pres_hPa)+" hPa  " + str(humRH)+" %RH   ", end="")