import values
import datetime

#get int representing the day of the week between 0 and 6. Monday is 0.
def getDayOfWeek(now):
    x = (datetime.datetime.weekday(now))
    print("Today is day %.0f of the week." % x)
    return x

#check if the current day of the week is on the light schedule. Expects an int.
def checkLightDay(intDay):
    if intDay in values.lightDays:
        print("Day %.0f is on the schedule." % intDay)
        return True
    else:
        print("No light scheduled for today.")
        return False

#see if the current time is within the user-defined light activation window. Expects datetime value.
def checkLightTime(now):
    if values.lightStartTime < now.time() < values.lightEndTime:
        return True
    else:
        return False

#turn the light on or off. Expects a bool of whether the day and time are appropriate to activate the light.
def checkLight(boolDay, boolTime):
    if boolDay == True and boolTime == True:
        print("Light should be on.")
        return True
    elif boolDay == False or boolTime == False:
        print("Light should be off.")
        return False
    else:
        RuntimeError("boolDay or boolTime has an unexpected value. The light will not operate correctly.")
        return None

#expects bools for the required light state and the current light state
def setLight(reqL):
    if reqL != values.lightPin.state and values.lightOverride == False:
        return values.Pin.setPin(values.lightPin, reqL)
    else:
        if values.lightOverride == True:
            values.logReading("Override", values.lightPin.name, "lightOverride is " + str(values.lightOverride) + ".")
        return values.lightPin.state

def doLight():
    #print ("There are {} days where the light is active.".format(len(values.lightDays)))
    dateTimeNow = datetime.datetime.now()
    dayOfWeek = getDayOfWeek(dateTimeNow)
    isLightDay = checkLightDay(dayOfWeek)
    isLightTime = checkLightTime(dateTimeNow)
    requiredLightState = checkLight(isLightDay, isLightTime)
    setLight(requiredLightState)