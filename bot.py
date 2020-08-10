import telebot

print('lol')
print('main')
from pyowm.commons.exceptions import APIRequestError, NotFoundError
from pyowm.owm import OWM

from config import TELEGRAM_TOKEN, PYOWM_TOKEN

token = TELEGRAM_TOKEN

bot = telebot.TeleBot(token)
owm = OWM(PYOWM_TOKEN)

weather_mgr = owm.weather_manager()

keyboard_help = telebot.types.ReplyKeyboardMarkup()
keyboard_start = telebot.types.ReplyKeyboardMarkup()

keyboard_remove = telebot.types.ReplyKeyboardRemove()

keyboard_start.row('/help')
keyboard_help.row('/weather_help')


@bot.message_handler(commands=['start'])
def send_info(message):
    bot.send_message(message.chat.id, 'больше информации в /help', reply_markup=keyboard_start)


@bot.message_handler(commands=['help'])
def send_info(message):
    bot.send_message(message.chat.id, '/weather_help информация о выдаче погоды по названию города',
                     reply_markup=keyboard_help)


@bot.message_handler(commands=['weather_help'])
def send_info(message):
    bot.send_message(message.chat.id,
                     'Напиши город в формате(Погода Москва) и будет выдана информация о погоде:3',
                     reply_markup=keyboard_remove)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text[:6].lower() == 'погода':

        try:
            print(message)
            weather = weather_mgr.weather_at_place(message.text[7:]).weather
            temp = weather.temperature('celsius')
            bot.send_message(message.chat.id,
                             'Температура в городе ' + message.text[7:] + ' ' + str(temp['temp']) + str('°'))
        except APIRequestError:
            bot.send_message(message.chat.id, 'Город не найден:(')
        except NotFoundError:
            bot.send_message(message.chat.id, 'Город не найден:(')
    else:
        bot.send_message(message.chat.id, 'Неизвестная команда')


bot.polling()
