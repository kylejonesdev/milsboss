import values
import datetime

#old fan.py. Works for always on fan.
# def doFan():
#     f = values.Pin.setPin(values.fanPin, True)
#     return f

#turn the fan on or off. Expects the minute number as an int from the current time hh:mm:ss.
def checkFan(t):
    if values.fanEndMinute > t >= values.fanStartMinute:
        print("Fan: Stop-{}, Now-{}, Start-{} :: Fan should be on.".format(values.fanEndMinute, t, values.fanStartMinute))
        return True
    else:
        print("Fan: Stop-{}, Now-{}, Start-{} :: Fan should be off.".format(values.fanEndMinute, t, values.fanStartMinute))
        return False

#expects bools for the required light state and the current light state
def setFan(reqF):
    if reqF != values.fanPin.state:
        return values.Pin.setPin(values.fanPin, reqF)

def doFan():
    timeNowMinute = datetime.datetime.now().minute
    isFanTime = checkFan(timeNowMinute)
    setFan(isFanTime)