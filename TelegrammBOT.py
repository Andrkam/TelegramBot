import requests
import telebot
from telebot import types
from TelegramBotConfig import TOKEN


bot = telebot.TeleBot(TOKEN)

currency_dict = {'доллар': 'USD',
                 'рубль': 'RUB',
                 'евро': 'EUR',
                 'бат': 'THB',
                 'юсдт': 'USDT',
                 'вон' : 'KRW',
                 'юань': 'CNY',
                 'иена': 'JPY'
                 }

@bot.message_handler(commands=["start", "help"])
def start(m, res=False):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = types.KeyboardButton('/Валюты')
        markup.add(key_1)
        bot.send_message(m.chat.id, f'Привет {m.from_user.first_name} !\n'
                                    f'Чтоб получить актуальный курс валюты введи в одну строку:\n'
                                    f'Валюту которую надо конвертирвать, Валюта в которую надо конвертировать, Количество\n'
                                    f'Нажимай ВВОД и кайфуй :)', reply_markup=markup)


@bot.message_handler(commands=['Валюты','values'])
def list_of_currency(m):
    for i in currency_dict:
        bot.send_message(m.chat.id, i)



@bot.message_handler(content_types=['text'])
def convertation(message):
    try:
        first, second, value = message.text.lower().split()
        x = requests.get(f'https://min-api.cryptocompare.com/data/price?&fsym={currency_dict[first]}&tsyms={currency_dict[second]}')
        bot.send_message(message.chat.id, f'Вообщем так: {value} {currency_dict[first]} в валюте {currency_dict[second]} '
                                          f'будет равно: {float(x.json()[currency_dict[second]]) * float(value)} {currency_dict[second]}')
    except KeyError:
        bot.send_message(message.chat.id, f'Нет такой валюты. Нажмите на кнопку Валюты, чтоб получить список всех валют')
    except ValueError:
        bot.send_message(message.chat.id, f'Неверный ввод ! Правильно так: доллар рубль 100')
    bot.send_message(message.chat.id, f'Может еще что нибудь посчитаем ?')


bot.polling(none_stop=True)