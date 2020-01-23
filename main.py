# -*- coding: utf-8 -*-
import requests
from config import config
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime, time
from time import sleep
import os

script_dir = os.path.dirname(__file__)

session = requests.Session()

def parser():

    #url = "http://y91805lt.beget.tech/2020.html"
    url = "http://taman.trans.efko.ru/trade/2"
    urlAuth = "http://taman.trans.efko.ru/login.php"
    urlLogout = "http://taman.trans.efko.ru/logout.php"
    urlBet = "http://taman.trans.efko.ru"

    betTask = []
    i=0

    session.post(urlAuth, config.data, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

    html = session.get(url, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
    soup = BeautifulSoup(html.content, 'lxml')

    while soup.find('table') == None:
          html = session.get(url, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
          soup = BeautifulSoup(html.content, 'lxml')
          i += 1
          print(i)

    for rows in soup.find_all('tr')[1:]:
        cols = rows.find_all('td')

        links = rows.find_all('button', text=re.compile("10"), class_='newbet')
        for link in links:
            linkBet = urlBet + link.get('href')

        betTask.append({
            'num': cols[0].strong.text,
            'phone': cols[8].strong.text,
            'cityOut': cols[9].strong.text + ' ' + cols[10].strong.text + ' | ' + cols[20].strong.text,
            'cityIn': cols[11].strong.text + ' | ' + cols[24].strong.text,
            'urlBet10': linkBet
        })
        linkBet = urlBet
    print("Парсинг окончен\n")
    print(betTask)

    count = 0

    f = open(os.path.join(script_dir, 'config/city.txt'), 'r')
    city = f.read().split(', ')
    f.close()

    f = open(os.path.join(script_dir, 'logs/GOOD_bet.txt'), 'w')
    f.write('Взятые заявки на \n<b>' + datetime.today().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3] + '</b>\n\n')
    f.close()
    print(city)
    for j in range(len(city)):
        cityRe = r"%s\b" % city[j]
        for i in range(len(betTask)):
            if (re.findall(cityRe, str(betTask[i].get('cityOut'))) == [city[j]]) or (re.findall(cityRe, str(betTask[i].get('cityIn'))) == [city[j]]):
                if count < config.sumBet:
                    urlBet = str(betTask[i].get('urlBet10'))

                    session.get(urlBet, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

                    msg = '✅ <b>' + betTask[i].get('num') + '</b>\n⏺ ' + betTask[i].get('cityOut') + '\n➡️ ' + betTask[i].get('cityIn') + '\n☎️ ' + betTask[i].get('phone') + '\n\n'

                    f = open(os.path.join(script_dir, 'logs/GOOD_bet.txt'), 'a')
                    f.write(msg)
                    f.close()

                    count += 1


    session.get(urlLogout, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

    f = open(os.path.join(script_dir, 'logs/log_bet.txt'), 'w')
    for i in range(len(betTask)):
        for key, value in betTask[i].items():
            f.write("{0}: {1}".format(key, value) + "\n")
        f.write("\n")
    f.close()

# def act(x):
#     return x+10
#
# def wait_start(runTime, action):
#     startTime = time(*(map(int, runTime.split(':'))))
#     while startTime > datetime.today().time():
#         sleep(1)
#     return action

def main():
    #wait_start('15:30:00', lambda: act(100))
    parser()

if __name__ == '__main__':
    main()
