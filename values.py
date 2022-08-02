#from sense_hat import SenseHat
import datetime
import csv
import RPi.GPIO as GPIO

#Sense Hat variables
#sense = SenseHat() #configure sensor
#scrollSpeed = .025 #speed at which Sense Hat scrolls. Lower is faster.

#Global Variables
GPIO.setmode(GPIO.BCM)
csvFileName = '/home/pi/Documents/milsboss/logs/' + datetime.datetime.today().strftime("%Y%m%d" + ".csv")
logFileName = datetime.datetime.today().strftime("%Y%m%d" + ".log")

#User Defined Settings
#--Program Settings--
runInterval = 10 #how often the plantMinder.main() function runs, in minutes
summaryInterval = 24 #how often the plantMinder.summary() function runs, in hours
#--Humidity--
minHumidity = 70 #threshhold, below which the humidifier will turn on
maxHumidity = 85 #threshhold, above which the humidifier will turn off
humidifierRunsSummary = 0 # long term counter to track total runs per summary function
humidifierRunsConsec = 0 # short term counter to track if the humidifier has been on too long
humidifierSkipsRemaining = 0 # the number of times a humidifier run has been called for and skipped to keep moisture down
humidifierRunsList = [] #list of the times the humidifier has run
humidifierOverride = False #changed via telegram to manually control humidifier
recentHumidity = None #most recent humidity reading, output as part of the "/status" Telegram command
recentTemperature = None #most recent temperature reading, output as part of the "/status" Telegram command
#--Light--
#days of the week in which the lights come on. Monday is 0.
lightDays = [0, 1, 2, 3, 4, 5, 6]
#hours on lightDays in which the lights are active
lightStartTime = datetime.time(7, 0)
lightEndTime = datetime.time(21, 0)
lightOverride = False #changed via telegram to manually control lights
#--Fan--
#between what minute numbers each hour will the fans run
fanStartMinute = 0
fanEndMinute = 10

#Class representing an I/O pin on the Raspberry Pi for controlling the power relay.
class Pin:
    def __init__(self, name, pin, state):
        self.name = name
        self.pin = pin
        self.state = state
    
    #set a pin on the Raspbery Pi to low (True) or high (False). Expects an object from the Pin class and a bool state.
    def setPin(self, state):
        if state == True:
            GPIO.output(self.pin, GPIO.LOW)
        elif state == False:
            GPIO.output(self.pin, GPIO.HIGH)
        self.state = state
        logReading("Change", self.name, self.state)
        return state

#Pins to control power relays
lightPin = Pin("light", 17, False)
GPIO.setup(lightPin.pin, GPIO.OUT)
fanPin = Pin("fan", 23, False)
GPIO.setup(fanPin.pin, GPIO.OUT)
humidifierPin = Pin("humidifier", 22, False)
GPIO.setup(humidifierPin.pin, GPIO.OUT)
temperaturePin = Pin("temperature", 24, False)
GPIO.setup(temperaturePin.pin, GPIO.OUT)

#List of all pins controlling power relays. Used to iterate through all pins for status report.
pinsList = [
    humidifierPin, 
    temperaturePin,
    lightPin,
    fanPin,
    ]

#get a datetime object of the current time
def getDateTime():
    return datetime.datetime.now()

#get a string of the current time
def getTimeStringNow():
    t = datetime.datetime.today().strftime("%H:%M:%S")
    return t

#get a string of the current date
def getDateStringNow():
    d = datetime.datetime.today().strftime("%Y-%m-%d")
    return d

#log a reading to the log file with relevant information
def logReading(alertType, area, message):
    ds = getDateStringNow()
    ts = getTimeStringNow()    
    file = open(csvFileName,"a")
    print(ds + " " + ts + " "+ alertType + " - " + area + " :: " + str(message))
    csvWriter = csv.writer(file)
    csvWriter.writerow([ds, ts, alertType, area, message])
    file.close()

#enter user parameters in the log file so they are on record
def reportParameters(f, ds, ts):
    file = open(f,"a")
    csvWriter = csv.writer(file)
    csvWriter.writerow([ds, ts, "Summary", lightPin.name, datetime.datetime.weekday(getDateTime()), lightDays]) #today's day number and days when light is active
    csvWriter.writerow([ds, ts, "Summary", lightPin.name, lightStartTime, lightEndTime]) #light start and end time
    csvWriter.writerow([ds, ts, "Summary", humidifierPin.name, minHumidity, maxHumidity]) #humidifier acceptable range
    file.close()

#configure elements of the program once on startup
def initialize(fileName):
    #initialize log file
    file = open(fileName,"a")
    csvWriter = csv.writer(file)    
    csvWriter.writerow(["Date", "Time", "Type", "Area", "Field1", "Field2"]) #title row of log
    file.close()
    #set all pins to a uniform state in case the program did not exit cleanly last time
    for x in pinsList:
        Pin.setPin(x, False)    
    #check user entered values for errors
    if minHumidity >= maxHumidity:
        raise RuntimeError('Minimum humidity must be less than maximum humidity. Check user-entered values.')
    if lightStartTime >= lightEndTime:
        raise RuntimeError('Light start time must be earlier than the light end time. Check user-entered values.')
    return fileName



