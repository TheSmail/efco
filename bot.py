import telebot
from telebot import apihelper
from telebot import types

#apihelper.proxy = {'https':'socks5://4009548:mYlbBtTn@orbtl.s5.opennetwork.cc:999'}
apihelper.proxy = {'https':'socks5://cqdFMa:Lkc29c@138.59.204.46:9165'}

TOKEN = '983071785:AAE-4gKtJpp7PA1wLtcXUtdvUz9duTP1BnA'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
@bot.message_handler(regexp="Назад")
def command_handler(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    edit_city = types.KeyboardButton('Список городов')
    what = types.KeyboardButton('Что взял?')

    markup.add(edit_city, what)

    bot.send_message(message.chat.id, 'Выбери функцию⬇️', reply_markup=markup)

@bot.message_handler(regexp="Список городов")
@bot.edited_message_handler(regexp="Список городов")
def echo_city(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    exit = types.KeyboardButton('Назад')

    markup.add(exit)

    bot.send_message(message.chat.id, 'Напиши новый список в необходимой последовательности (предыдущий список будет удален!)\nПример написания: <b>Краснодар, Анапа, Крымск</b>\nЕсли напишешь без запятых или с маленькой буквы - все сломаешь', parse_mode='HTML')

    @bot.message_handler(content_types=['text'])
    @bot.edited_message_handler(content_types=['text'])
    def echo_edit(message):
        if message.text:
            f = open('city.txt', 'w')
            f.write(message.text)
            f.close()
        bot.send_message(message.chat.id, 'Запомнил: ' + message.text, reply_markup=markup)


@bot.message_handler(regexp="Что взял?")
@bot.edited_message_handler(regexp="Что взял?")
def echo_what(message):
    f = open('/logs/GOOD_bet.txt', 'r')
    msg = f.read()
    f.close()

    markup = types.ReplyKeyboardMarkup(row_width=2)
    exit = types.KeyboardButton('Назад')

    markup.add(exit)

    bot.send_message(message.chat.id, msg, parse_mode='HTML', reply_markup=markup)

def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()