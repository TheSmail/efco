# -*- coding: utf-8 -*-

from enum import Enum

TOKEN = '983071785:AAE-4gKtJpp7PA1wLtcXUtdvUz9duTP1BnA'
db_file = "config/database.vdb"

data = {'xLogin': 'evgen28rus@mail.ru', 'xPassword': 'had2911'}

f = open('config/bet_num.txt', 'r')
sumBet = int(f.read())
f.close()#кол-во необходимых заявок

price = '9.9'

class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_CITY = "1"