# -*- coding: utf-8 -*-
import requests
from config import config
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
import os
script_dir = os.path.dirname(__file__)

session = requests.Session()

def parser():
    f = open(os.path.join(script_dir, 'logs/GOOD_bet.txt'), 'w')
    f.write('Взятые заявки на <b>\n' + datetime.today().strftime('%d.%m.%Y %H:%M:%S') + '</b>\n\n')
    f.close()

    #url = "http://y91805lt.beget.tech"
    url = "http://taman.trans.efko.ru/trade/2"
    urlAuth = "http://taman.trans.efko.ru/login.php"
    urlLogout = "http://taman.trans.efko.ru/logout.php"
    urlBet = "http://taman.trans.efko.ru"

    betTask = []

    session.post(urlAuth, config.data, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

    html = session.get(url, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
    soup = BeautifulSoup(html.content, 'lxml')

    if soup.find('table') != None:
        for rows in soup.find_all('tr')[1:]:
            cols = rows.find_all('td')
            btnBet = rows.find('button', class_='newbet')

            if config.price in btnBet.text:
                btnBet = urlBet + btnBet.attrs['href']
            else: btnBet = 'http://fake.ru'

            betTask.append({
                'num': cols[0].strong.text,
                'date': cols[9].strong.text,
                'cityOut': cols[20].strong.text,
                'cityIn': cols[24].strong.text,
                'urlBet10': btnBet
            })
        print("Парсинг окончен\n")
    else:
        print("Нет торгов")
        session.get(urlLogout, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
        betTask = None

    count = 0

    f = open(os.path.join(script_dir, 'config/city.txt'), 'r')
    city = f.read().split(', ')
    f.close()

    for j in range(len(city)):
        cityRe = r"%s\b" % city[j]
        if count < config.sumBet:
            for i in range(len(betTask)):
                if (re.findall(cityRe, str(betTask[i].get('cityOut'))) == [city[j]]) or (re.findall(cityRe, str(betTask[i].get('cityIn'))) == [city[j]]):
                    urlBet = str(betTask[i].get('urlBet10'))
                    session.get(urlBet, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

                    msg = 'Номер заявки: <b>' + betTask[i].get('num') + '</b>\nДата: ' + betTask[i].get('date') + '\nИз: ' + betTask[i].get('cityOut') + '\nВ: ' + betTask[i].get('cityIn') + '\n\n'

                    f = open(os.path.join(script_dir, 'logs/GOOD_bet.txt'), 'a')
                    f.write(msg)
                    f.close()

                    count += 1
                    break

    session.get(urlLogout, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

    f = open(os.path.join(script_dir, 'logs/log_bet.txt'), 'w')
    for i in range(len(betTask)):
        for key, value in betTask[i].items():
            f.write("{0}: {1}".format(key, value) + "\n")
        f.write("\n")
    f.close()

def main():
    parser()

if __name__ == '__main__':
    main()