import os
from dotenv import load_dotenv
import values
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler, 
    Filters,
    ConversationHandler,
    CallbackContext
)
from telegram import Bot

#--Telegram Bot Setup--
load_dotenv()
token = os.getenv('TELEGRAM_BOT_KEY')
bot = Bot(token)
bot.send_message(chat_id = -426679140, text = "Program started.")
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher

TYPING_MANAGE, TYPING_MANAGE_CHOICE, TYPING_TAKE_ACTION = range(3)

#--Text Management Functions--

#Format the provided log message to be sent via Telegram
def formatLogForTelegram(alertType, area, logValue):
    newMessage = alertType + ' - ' + str(area) + ' :: ' + str(logValue) + '.\n'
    return newMessage

#Send the provided text in a telegram message
def sendTelegram(m):
    bot.send_message(chat_id = -426679140,text = m)

#Logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Convert bool values to on/off values for text logs
def convertBool(bool):
    if bool == True:
        return "on"
    elif bool == False:
        return "off"
    else:
        return None

#--Bot Conversation Tree--

#Initial greeting
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=
        "Hello. My name is Plant Minder. I provide information about your greenhouse cabinet.\n\n"
        'Commands:\n'
        '/status - returns the current status of the devices in the cabinet.\n'
        '/manage - allows you to select a component to manage.\n'
        '/cancel - ends our conversation.')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#Get a summary of the status of all devices in the cabinet
def status(update: Update, context: CallbackContext):
    update.message.reply_text(
        
        'The temperature is ' + str(values.recentTemperature) + '.\n'
        'The humidity is ' + str(values.recentHumidity) + '.\n'
        'The humidifier is currently ' + convertBool(values.humidifierPin.state) + '.\n'
        'The light is currently ' + convertBool(values.lightPin.state) + '.\n'
        'The fan is currently ' + convertBool(values.fanPin.state) + '.\n'
        
    )

status_handler = CommandHandler('status', status)
dispatcher.add_handler(status_handler)

#Turn individual items in the cabinet on or off
def manage(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Lights','Humidifier']]
    update.message.reply_text(
        'Ok, what would you like to manage?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return TYPING_MANAGE

def manageChoice(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text == 'Lights':
        if values.lightPin.state == True:
            update.message.reply_text(
                'The lights are currently ' + convertBool(values.lightPin.state) + '. Do you want to turn them off?',
            reply_markup=ReplyKeyboardMarkup([['ON','OFF']], one_time_keyboard=True)
            )
        elif values.lightPin.state == False:
            update.message.reply_text(
                'The lights are currently ' + convertBool(values.lightPin.state) + '. Do you want to turn them on?',
            reply_markup=ReplyKeyboardMarkup([['ON','OFF']], one_time_keyboard=True)
            )
    if text == 'Humidifier':
        if values.humidifierOverride == False:
            update.message.reply_text(
                'The humidifier is currently enabled. Do you want to disable it?',
            reply_markup=ReplyKeyboardMarkup([['Leave humidifier','Humidifier OFF']], one_time_keyboard=True)
            )
        if values.humidifierOverride == True:
            update.message.reply_text(
                'The humidifier is currently disabled. Do you want to enable it?',
            reply_markup=ReplyKeyboardMarkup([['Leave humidifier','Humidifier ON']], one_time_keyboard=True)
            )
    return TYPING_MANAGE_CHOICE

def takeAction(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text == 'ON':
        values.Pin.setPin(values.lightPin, True)
        values.lightOverride = False
        lightState = convertBool(values.lightPin.state)
        update.message.reply_text(            
            'The lights are now ' + lightState + '. They will follow the normal light schedule.'
        )
        values.logReading('User_Change', values.lightPin.name, 'The light is now ' + lightState + '.')
    if text == 'OFF':
        values.Pin.setPin(values.lightPin, False)
        values.lightOverride = True
        lightState = convertBool(values.lightPin.state)
        update.message.reply_text(            
            'The lights are now ' + lightState + '. They will remain ' + lightState + ' until you turn them back on.'
        )
        values.logReading('User_Change', values.lightPin.name, 'The light is now ' + lightState + '.')    
    if text == 'Humidifier OFF':
        values.Pin.setPin(values.humidifierPin, False)
        values.humidifierOverride = True
        humidifierState = convertBool(values.humidifierPin.state)
        update.message.reply_text(            
            'The humidifier is now disabled. It will remain '+ humidifierState + ' until you enable it.'
        )
        values.logReading('User_Change', values.humidifierPin.name, 'The humidifier is now disabled.')
    if text == 'Humidifier ON':
        values.Pin.setPin(values.humidifierPin, True)
        values.humidifierOverride = False
        humidifierState = convertBool(values.humidifierPin.state)
        update.message.reply_text(            
            'The humidifier is now enabled. It will now opperate normally.'
        )
        values.logReading('User_Change', values.humidifierPin.name, 'The humidifier is now enabled.')
    #else:
    #TODO continue here with handling no action taken on humidifier

    return TYPING_TAKE_ACTION
    #Script successfully reaches this point
    #TODO add pin controls for humidifier to stay off for 24 hours. May require a new 'humidifierPin.modified' bool attribute in the class.

    # update.message.reply_text(
    #     'Oops. We haven\'t gotten this far with the coding yet. Things aren\'t going to work until the program is reset.'
    # )


#status_handler = CommandHandler('manage', manage)
#dispatcher.add_handler(status_handler)

def done(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Ok. All done.')
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('manage', manage)],
    states={
        TYPING_MANAGE: [
            MessageHandler(
                Filters.regex('^(Lights|Humidifier)$'), manageChoice
            ),
        ],
        TYPING_MANAGE_CHOICE: [
            MessageHandler(
                Filters.regex('^(ON|OFF|Humidifier ON|Humidifier OFF|Leave humidifier)$'), takeAction
            ),
        ],
        #TODO this block has an error that runs start no matter what the user types. It probably needs to be looking for a command.
        TYPING_TAKE_ACTION: [
            MessageHandler(
                Filters.update,manage
            ),
        ],
    },
    fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
)

dispatcher.add_handler(conv_handler)


#old
#def echo(update, context):
    #context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

#echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
#dispatcher.add_handler(echo_handler)