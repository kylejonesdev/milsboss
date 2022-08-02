
import logging
import values
#imports for HTU21D humidity sensor
import time
import board
from adafruit_htu21d import HTU21D
# imports for Telegram
import notify

#create sensor object
i2c = board.I2C() #uses board.SCL and board.SDA
sensor = HTU21D(i2c)

def getTemperature():
    tempC = sensor.temperature
    tempF = tempC * (9/5) + 32
    temperature = round(tempF, 1)
    values.logReading("Reading", values.temperaturePin.name, str(temperature) + "F")
    return temperature

def doTemperature():
    #Placeholder as no heater is currently installed, so pin is always true, as set on plantMinder.py main().
    #values.Pin.setPin(values.temperaturePin, True)
    currentTemperature = getTemperature()
    values.recentTemperature = currentTemperature
    return currentTemperature