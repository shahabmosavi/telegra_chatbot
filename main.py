import requests
from telegram.ext import Updater, CallbackContext, CommandHandler, Filters, MessageHandler
from telegram import Update, ReplyKeyboardMarkup


bot_token = '5219839927:AAFLfCMGx31PchGg6-eUqpedYIoVS5_dlsE'

current_order = ''
about_text = 'در این ربات میتونی با زدن کلید فال حافظ فالت رو بگیری'
api_token = '893694:61f10c4722b828.51196936'
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
keyboard_options = [['کمک'], ["فال حافظ"], ]


def start(update: Update, context: CallbackContext):
    global current_order
    current_order = ''
    update.message.reply_text('سلام به ربات فال حافظ خوش اومدید 🙋‍♀️\n لطفا یکی از گزینه های زیر را انتخاب کنید',
                              reply_markup=ReplyKeyboardMarkup(keyboard_options))


def parse_input(update: Update, context: CallbackContext):
    global current_order
    message = update.message["text"]
    if current_order == '':
        if message == 'کمک':
            update.message.reply_text(about_text)
        elif message == 'فال حافظ':
            current_order = 'فال حافظ'
            fal_options = [['فال دوباره'], ["بازگشت"], ]
            update.message.reply_text(get_hafez_fal(),
                                      reply_markup=ReplyKeyboardMarkup(fal_options))
        else:
            update.message.reply_text('سلام لطفا از بین گزینه ها یکی رو انتخاب کنید',
                                      reply_markup=ReplyKeyboardMarkup(keyboard_options))
    elif current_order == 'فال حافظ':
        if message == "فال دوباره":

            update.message.reply_text(get_hafez_fal())
        else:
            current_order=''
            update.message.reply_text(' لطفا از بین گزینه ها یکی رو انتخاب کنید',
                                      reply_markup=ReplyKeyboardMarkup(keyboard_options))
    else:
        current_order = ''
        print('dasdasdaasdsdsadada')
        update.message.reply_text(' لطفا از بین گزینه ها یکی رو انتخاب کنید',
                                  reply_markup=ReplyKeyboardMarkup(keyboard_options))


def get_hafez_fal():
    res = requests.get('https://one-api.ir/hafez/?token='+api_token)
    res = res.json()
    if res['status'] == 200:
        return 'شعر : \n' + res['result']['RHYME'] + '\n معنی : \n' + res['result']['MEANING']
    else:
        return 'مشکلی پیش آمد لطفا بعدا تست کنید'


input_handler = MessageHandler(Filters.text, parse_input)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(input_handler)

updater.start_polling()
