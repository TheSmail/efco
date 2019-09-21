import telebot
from telebot import apihelper
from telebot import types
from config import config
from config import bdworker

#apihelper.proxy = {'https':'socks5://4009548:mYlbBtTn@orbtl.s5.opennetwork.cc:999'}
apihelper.proxy = {'https':'socks5://cqdFMa:Lkc29c@138.59.204.46:9165'}

TOKEN = '983071785:AAE-4gKtJpp7PA1wLtcXUtdvUz9duTP1BnA'

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
@bot.message_handler(regexp="Назад")
def command_handler(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    edit_city = types.KeyboardButton('Список городов')
    bet = types.KeyboardButton('Кол-во заявок')
    what = types.KeyboardButton('Что взял?')

    markup.add(edit_city, bet, what)

    bot.send_message(message.chat.id, 'Выбери функцию ⬇️', reply_markup=markup)


@bot.message_handler(regexp="Что взял?")
@bot.edited_message_handler(regexp="Что взял?")
def echo_what(message):
    f = open('logs/GOOD_bet.txt', 'r')
    msg = f.read()
    f.close()

    bot.send_message(message.chat.id, msg, parse_mode='HTML')
    command_handler(message)

@bot.message_handler(regexp="Кол-во заявок")
@bot.edited_message_handler(regexp="Кол-во заявок")
def echo_bet(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)

    one = types.KeyboardButton('1')
    two = types.KeyboardButton('2')
    three = types.KeyboardButton('3')
    four = types.KeyboardButton('4')
    exit = types.KeyboardButton('Назад')

    markup.add(one, two, three, four, exit)

    f = open('config/bet_num.txt', 'r')
    msg = f.read()
    f.close()

    bot.send_message(message.chat.id, 'Выбери сколько заявок брать ⬇️ (только кнопками снизу)', parse_mode='HTML', reply_markup=markup)
    bot.send_message(message.chat.id, 'Текущее кол-во заявок: <b>' + msg + '</b>', parse_mode='HTML')

    @bot.message_handler(regexp="1")
    @bot.message_handler(regexp="2")
    @bot.message_handler(regexp="3")
    @bot.message_handler(regexp="4")
    def echo_bet_num(message):
        f = open('config/bet_num.txt', 'w')
        f.write(message.text)
        f.close()

        bot.send_message(message.chat.id, 'Новое кол-во заявок: <b>' + message.text + '</b>. Постараюсь взять, если столько будет', parse_mode='HTML')
        command_handler(message)

@bot.message_handler(regexp="Список городов")
@bot.edited_message_handler(regexp="Список городов")
def echo_city(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    exit = types.KeyboardButton('Назад')

    markup.add(exit)

    f = open('config/city.txt', 'r')
    city = f.read()
    f.close()

    bot.send_message(message.chat.id, 'Напиши новый список в необходимой последовательности (предыдущий список будет удален!)\nПример написания: <b>Краснодар, Анапа, Крымск, Томск</b>\nЕсли напишешь без запятых или с маленькой буквы - все сломаешь', parse_mode='HTML')
    bot.send_message(message.chat.id, 'Текущий список: <b>' + city + '</b>', reply_markup=markup, parse_mode='HTML')
    bdworker.set_state(message.chat.id, config.States.S_CITY.value)

@bot.message_handler(func=lambda message: bdworker.get_current_state(message.chat.id) == config.States.S_CITY.value)
def echo_edit(message):
    if message.text:
        f = open('config/city.txt', 'w')
        f.write(message.text)
        f.close()
    bot.send_message(message.chat.id, 'Запомнил: <b>' + message.text + '</b>', parse_mode='HTML')
    command_handler(message)
    bdworker.set_state(message.chat.id, config.States.S_START.value)



def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()