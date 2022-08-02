import logging
from adafruit_blinka.board.pyboard import X10
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.job import Job
import values
import light
import fan
import humidity
import temperature
import notify
import datetime

logging.basicConfig(filename = '~/Documents/plantProject/' + values.logFileName, filemode='a', level = logging.DEBUG)

#append all lines to single message, then call output in Telegram.
def summary():
    pendingMessage = "**Summary**\n"
    summaryList = [
        ["Summary", "lightOverride", str(values.lightOverride)],
        ["Summary", "humidifierOverride", str(values.humidifierOverride)]
    ]
    values.reportParameters(values.csvFileName,values.getDateStringNow(),values.getTimeStringNow()) #print important program variables to the log
    #iterate through all Pin objects and output their status to the summary
    for x in values.pinsList:
        print (x,x.name,x.state)
        values.logReading("Summary", x.name, x.state)
        formattedLogReading = notify.formatLogForTelegram("Summary", x.name, x.state)
        pendingMessage += formattedLogReading
    #iterate through the supplemental summary list of interesting variables
    for y in summaryList:
        values.logReading(y[0], y[1], y[2])
        formattedLogReading = notify.formatLogForTelegram(y[0], y[1], y[2])
        pendingMessage += formattedLogReading
    pendingMessage += humidity.humidifierStats()
    notify.sendTelegram(pendingMessage)

def main():
    logging.debug("main() has started.")
    humidity.doHumidity()
    temperature.doTemperature()
    light.doLight()
    fan.doFan()
    values.logReading("State", values.humidifierPin.name, values.humidifierPin.state)
    values.logReading("State", values.lightPin.name, values.lightPin.state)
    values.logReading("State", values.temperaturePin.name, values.temperaturePin.state)
    values.logReading("State", values.fanPin.name, values.fanPin.state)
        #TODO append reading to yet-to-be-created list, for use in graph output and Telegram bot

#--BEGIN PROGRAM--
logging.debug("Program initialized.")
values.initialize(values.csvFileName) #check user-entered variables for values which would cause malfunctions
values.Pin.setPin(values.temperaturePin, True) #only run once because it is always on
notify.updater.start_polling() #start the telegram bot

if __name__ == "__main__":
    try:
        scheduler = BlockingScheduler()
        scheduler.add_job(main, 'interval', minutes = values.runInterval)
        scheduler.add_job(summary, 'interval', hours = values.summaryInterval)
        scheduler.start()
    except Exception as e:
        logging.exception("Main crashed. Error: %s", e)

# Testing Code

# for i in range(5):
#     main()
#     time.sleep(10)
# updater.stop() #ends the telegram watcher

# TODO
# Summary message every 24 hours is not working
# Logging to file is not working
# - Logging is configured twice (plantMinder and notify). Only allowed once.
# - Logging is not called in notify. Called elsewhere?
# Implement start at round time (ex. 7:00am instead of 7:06am)
# Summary graph to Telegram


# Future Feature Ideas
# simulate weather from another part of the globe with light and heat pad
# tabulate lux received by sensor over time
# calculate difference between target lux and received lux
# track lux added by grow light
# turn off light when light time is exceeded or lux target is achieved
# log error if not enough lux was received
# consider local sunrise/sunset for hours lights are on
# simulate light from a certain part of the globe