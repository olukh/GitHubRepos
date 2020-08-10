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


@bot.message_handler(commands=['start', 'help'])
def send_info(message):
    bot.send_message(message.chat.id, 'Напиши город в формате(Город Москва) и будет выдана информация о погоде:3')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text[:6].lower() == 'город ':

        try:
            print(message)
            weather = weather_mgr.weather_at_place(message.text[6:]).weather
            temp = weather.temperature('celsius')
            bot.send_message(message.chat.id,
                             'Температура в городе ' + message.text[6:] + ' ' + str(temp['temp']) + str('°'))
        except APIRequestError:
            bot.send_message(message.chat.id, 'Город не найден:(')
        except NotFoundError:
            bot.send_message(message.chat.id, 'Город не найден:(')
    else:
        bot.send_message(message.chat.id, 'Неизвестная команда')


bot.polling()
