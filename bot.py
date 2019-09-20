import telebot
from telebot import apihelper
from telebot import types

#apihelper.proxy = {'https':'socks5://4009548:mYlbBtTn@orbtl.s5.opennetwork.cc:999'}
apihelper.proxy = {'https':'socks5://cqdFMa:Lkc29c@138.59.204.46:9165'}

TOKEN = '983071785:AAE-4gKtJpp7PA1wLtcXUtdvUz9duTP1BnA'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def command_handler(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    edit_city = types.KeyboardButton('Список городов')

    markup.add(edit_city)

    bot.send_message(message.chat.id, 'Нажми на кнопку', reply_markup=markup)

@bot.message_handler(regexp="Список городов")
@bot.edited_message_handler(regexp="Список городов")
def echo_city(message):
    bot.send_message(message.chat.id, 'Напиши новый список в необходимой последовательности (предыдущий список будет удален!)\nПример написания: <b>Краснодар, Анапа, Крымск</b>', parse_mode='HTML')


def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()