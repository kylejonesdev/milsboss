import values

values.GPIO.cleanup()
#values.Pin.setPin(values.lightPin,False)
#values.Pin.setPin(values.humidifierPin,False)

#--UNUSED SENSE HAT FUNCTIONS--

#configure SenseHat humidity sensor
#sense = SenseHat()

#output reading to screen in desired color. Default is blue.
#def showMessage(text, colorString):
    #colors = {'red': [255, 0, 0], 'yellow': [255, 255, 0], 'green': [0, 255, 0]}
    #sense.show_message(text, scrollSpeed, text_colour=colors.get(colorString, [0, 0, 255]))

#get current humidity value from sensor
#def getHumidity():
    #sense.clear()
    #humidity = sense.get_humidity() 
    #humidity = round(humidity, 1)
    #values.logReading("Notify", "Humidity", "Minimum: {}% Current: {}% Maximum: {}%".format(values.minHumidity, humidity, values.maxHumidity))
    #return humidity

# print message to UI device
# def humidityToGUI(h):
#     humidityString = "H: %.1f %%rh"
#     minH = values.minHumidity
#     maxH = values.maxHumidity    
#     if h < minH:
#         values.showMessage(humidityString % h, 'red')
#     elif h > minH and h < maxH:
#         values.showMessage(humidityString % h, 'green')
#     elif h > maxH:
#         values.showMessage(humidityString % h, 'yellow')