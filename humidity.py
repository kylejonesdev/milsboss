import logging
import values
import datetime
#imports for HTU21D humidity sensor
#import time
import board
from adafruit_htu21d import HTU21D
# imports for Telegram
import notify

log = logging.getLogger(__name__)

#create sensor object
i2c = board.I2C() #uses board.SCL and board.SDA
sensor = HTU21D(i2c)
startDate = datetime.date.today()

#get a reading of the current humidity from the humidity sensor
def getHumidity():
    humidity = sensor.relative_humidity 
    humidity = round(humidity, 1)
    values.logReading("Reading", values.humidifierPin.name, str(humidity) + "%")
    return humidity

#check to see whether the state of the humidifier needs changed and return required state.
def checkHumidity(h):
    if h < values.minHumidity:
        print("Humidity: Max-{}, Current-{}, Min-{} :: Humidity is low.".format(values.maxHumidity, h, values.minHumidity))
        return True
    elif h > values.maxHumidity:
        print("Humidity: Max-{}, Current-{}, Min-{} :: Humidity is high.".format(values.maxHumidity, h, values.minHumidity))
        return False
    else:
        return values.humidifierPin.state

#set that state of the humidifier. Expects a bool of the required state of the humidifier and a bool of the current state of the humidifier.
def setHumidifier(reqH, currH):
    if values.humidifierOverride == False:
        if reqH == True and values.humidifierSkipsRemaining > 0:
            values.humidifierSkipsRemaining -= 1
            values.logReading("Override", values.humidifierPin.name, "humidifierSkipsRemaining is " + values.humidifierSkipsRemaining + ".")
            return False
        if reqH != currH:
            r = values.Pin.setPin(values.humidifierPin, reqH)
            return r
    else:
        if values.humidifierOverride == True:
            values.logReading("Override", values.humidifierPin.name, "humidifierOverride is " + str(values.humidifierOverride) + ".")
        return currH

#watches out for the humidifier running too many times without a break and sends a Telegram warning if needed.
def tabulateRuns(hs):
    #TODO expand this code. Show number of times humidifier ran compared to past days. Lights behaved as expected?
    if hs == True:
        values.humidifierRunsSummary += 1
        values.humidifierRunsConsec += 1
        if values.humidifierRunsConsec >= 2:
            telegramMessage = notify.formatLogForTelegram("Summary", "humidifier", "Humidifier has run " + str(values.humidifierRunsConsec) + " times consecutively.")
            notify.sendTelegram(telegramMessage)
            log.debug("The humidifier has run %s times consecutively.", values.humidifierRunsConsec)
            values.humidifierSkipsRemaining = 3
    elif hs == False:
        values.humidifierRunsConsec = 0        
    log.debug("tabulateRuns() completed.")

#Compile humidifier runs over time into a list
def humidifierStats():
    hr = values.humidifierRunsSummary
    hm1 = "Since the last summary, the humidifier ran {} times".format(hr)
    values.logReading("Summary", "humidifier", hm1)
    humidifierTelegram = notify.formatLogForTelegram("Summary", "humidifier", hm1)
    values.humidifierRunsList.append(hr)
    values.humidifierRunsSummary = 0 #reset counter of humidifier runs
    #initialize and clear variables
    hNumerator = 0
    hm2 = None
    for x in values.humidifierRunsList:
        hNumerator += x
    if hNumerator > 0:
        hAverage = hNumerator / values.humidifierRunsList.count()
        hm2 = "Since the program started on {}, the humidifier runs {} times on average in a {} hour period".format(startDate, hAverage, values.summaryInterval)
    else:
        hm2 = "Since the program started on {}, the humidifier has run zero times".format(startDate)
    values.logReading("Summary", "humidifier", hm2)
    humidifierTelegram += notify.formatLogForTelegram("Summary", "humidifier", hm2)
    return humidifierTelegram


#run humidity functions
def doHumidity():
    h = getHumidity()
    values.recentHumidity = h
    requiredHumidifierState = checkHumidity(h)
    hState = setHumidifier(requiredHumidifierState, values.humidifierPin.state)
    tabulateRuns(hState)
    log.debug("doHumidity() completed. hState is %s.", hState)
