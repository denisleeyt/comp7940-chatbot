from pymongo import MongoClient
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from telegram.ext import CallbackQueryHandler
import json
import re
# The messageHandler is used for all message updates
import logging
import tabulate
import os
import base64


ACCESS_TOKEN = base64.b64decode(os.environ["ACCESS_TOKEN_BASE64"]).decode()
CONNECTION_STRING = base64.b64decode(os.environ["CONNECTION_STRING_BASE64"]).decode()
DB = base64.b64decode(os.environ["DB_BASE64"]).decode()
COLLECTION = base64.b64decode(os.environ["COLLECTION_BASE64"]).decode()

global cluster
cluster = MongoClient(CONNECTION_STRING)
global db
db = cluster[DB]
global collection
collection = db[COLLECTION]
LOCATION, SELECT_CAR_PARK, SELECT_INFO = range(3)

def start(update, context):
    """Handler function for the /start command"""
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text='講輸入想泊車的地區')
    return LOCATION

# Save as a parameter while user made the input
def input_location(update, context):
    location = update.message.text
    print(location)
    global collection
    # result = list(collection.find({'carpark_address': re.compile(fr"{location}")}))
    result = list(collection.find({'carpark_address': re.compile(fr"{location}")}))  #Select * from db where carpark_address = input
    # print(carpark_names)
    if len(result) == 0:
        # no car parks found
        update.message.reply_text('沒有找到相應的泊車場所，請重新輸入')
        return LOCATION

    # number_of_result = collection.count_documents({'carpark_address': re.compile(fr"{location}")})
    # print(number_of_result)
    buttons=[]
    for i in range(len(result)):
        button = InlineKeyboardButton(text=result[i]['carpark_name'], callback_data=result[i]['carpark_name'])
        buttons.append([button])

    # create an InlineKeyboardMarkup object with the list of buttons
    keyboard = InlineKeyboardMarkup(buttons)

    # send the list of carpark names as a message with the keyboard
    update.message.reply_text('請選擇想要停泊的停車場\U0001F17F\U0001F697\U0001F698:', reply_markup=keyboard)
    return SELECT_CAR_PARK

# define a function to handle the button presses
def carpark_name_callback(update, context):
    query = update.callback_query
    carpark_name = query.data
    query.answer()

    # save the search result as context.user_data for use in later stages of the conversation
    context.user_data['carpark_name'] = carpark_name

    options = [[InlineKeyboardButton(text='停車場地址', callback_data='停車場地址')],
    [InlineKeyboardButton(text='Google 地圖連結\U0001F5FA', callback_data='Google 地圖連結')],
    [InlineKeyboardButton(text='時租收費\U0001F4B5', callback_data='時租收費')]]

     # create an InlineKeyboardMarkup object with the list of options
    keyboard1 = InlineKeyboardMarkup(options)

    # send the list of carpark names as a message with the keyboard
    query.message.reply_text('請選擇資訊:', reply_markup=keyboard1)
    return SELECT_INFO

def content_callback(update, context):
    query = update.callback_query
    query.answer()
    option = query.data
    carpark_name = context.user_data['carpark_name']
    global collection
    document = collection.find_one({'carpark_name': carpark_name})

    print(document)
    # Display selected carpark detail
    if query.data == '停車場地址':    
        carpark_address = document['carpark_address']
        print(carpark_address)
        query.message.reply_text(text=f"您選擇的停車場是: {carpark_name} \n停車場地址: {carpark_address}")
    elif query.data == 'Google 地圖連結':
        google_map_url = document['google_map_url']
        button = InlineKeyboardButton(text="Google 地圖連結", url=google_map_url)
        keyboard = InlineKeyboardMarkup([[button]])
        if google_map_url != "N/A":
            query.message.reply_text(text=f"您選擇的停車場是: {carpark_name} \n點擊下面的按鈕前往 Google 地圖 \U0001F5FA", reply_markup=keyboard)
        else:
            query.message.reply_text(text=f"您選擇的停車場是: {carpark_name} \n抱歉未能提供Google 地圖連結 \U0001F615")
    elif query.data == '時租收費':
        fee = document['時租']
        print(fee)
        keys = []
        for row in fee:
            # for t in row["時租"]:
            for key in row.keys():
                if key not in keys:
                    keys.append(key)
        table_content_list =[]
        for t in fee:
            table_content_list.append(list(t.values())[0])
        t_r = [0]
        for i in range(1,100):
            if i*(len(fee)/len(keys))<len(fee):
                t_r.append(int(i*(len(fee)/len(keys))))
            elif i*(len(fee)/len(keys))==len(fee):
                t_r.append(int(i*(len(fee)/len(keys))))
            else:
                break
        rows=[]
        if len(t_r)==7:
            for i in range(1):
                rows=(list(zip(table_content_list[t_r[i]:t_r[i+1]-1],table_content_list[t_r[i+1]:t_r[i+2]-1],table_content_list[t_r[i+2]:t_r[i+3]-1],table_content_list[t_r[i+3]:t_r[i+4]-1],table_content_list[t_r[i+4]:t_r[i+5]-1],table_content_list[t_r[i+5]:t_r[i+6]-1])))
        if len(t_r)==6:
            for i in range(1):
                rows=(list(zip(table_content_list[t_r[i]:t_r[i+1]-1],table_content_list[t_r[i+1]:t_r[i+2]-1],table_content_list[t_r[i+2]:t_r[i+3]-1],table_content_list[t_r[i+3]:t_r[i+4]-1],table_content_list[t_r[i+4]:t_r[i+5]-1])))
        elif len(t_r)==5:
            for i in range(1):
                rows=(list(zip(table_content_list[t_r[i]:t_r[i+1]-1],table_content_list[t_r[i+1]:t_r[i+2]-1],table_content_list[t_r[i+2]:t_r[i+3]-1],table_content_list[t_r[i+3]:t_r[i+4]-1])))
        elif len(t_r)==4:
            for i in range(1):
                rows=(list(zip(table_content_list[t_r[i]:t_r[i+1]-1],table_content_list[t_r[i+1]:t_r[i+2]-1],table_content_list[t_r[i+2]:t_r[i+3]-1])))  
        elif len(t_r)==3:
            for i in range(1):
                rows=(list(zip(table_content_list[t_r[i]:t_r[i+1]-1],table_content_list[t_r[i+1]:t_r[i+2]-1])))
        else:
            rows=[]
        header = list(keys)
        table_str = tabulate.tabulate(rows, headers=header)
            # query.message.reply_text(text=f"您選擇的停車場是: {carpark_name} \n時租收費\U0001F4B5:{fee}")
        query.message.reply_text(text=f"您選擇的停車場是: {carpark_name} \n {table_str}", parse_mode='HTML')

# def error(update, context):
#     """Log Errors caused by Updates."""
#     logging.warning('Update "%s" caused error "%s"', update, context.error)



def main():
# Load your token and create an Updater for your Bot
    updater = Updater(token=(ACCESS_TOKEN), use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        LOCATION: [MessageHandler(Filters.text & ~Filters.command, input_location)],
        SELECT_CAR_PARK: [CallbackQueryHandler(carpark_name_callback)],
        SELECT_INFO: [CallbackQueryHandler(content_callback)]
    },
    fallbacks=[CommandHandler('start', start)]
)
    dispatcher.add_handler(conv_handler)

# # Add the command handler for the /start command
#     dispatcher.add_handler(CommandHandler('start', start))
# # Set up a message handler to call the save_location function
#     message_handler = MessageHandler(Filters.text & ~Filters.command, input_location)
#     dispatcher.add_handler(message_handler)
#     dispatcher.add_handler(CallbackQueryHandler(carpark_name_callback))
#     dispatcher.add_handler(CallbackQueryHandler(content_callback))

    # add the error handler to the dispatcher
    # dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()




