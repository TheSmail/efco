import requests
import city
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

session = requests.Session()

def parser():
    #url = "http://y91805lt.beget.tech"
    url = "http://taman.trans.efko.ru/trade/2"
    url_auth = "http://taman.trans.efko.ru/login.php"
    urlLogout = "http://taman.trans.efko.ru/logout.php"

    betTask = []
    data = {'xLogin': 'evgen28rus@mail.ru', 'xPassword': 'had2911'}

    session.post(url_auth, data, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

    html = session.get(url, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
    soup = BeautifulSoup(html.content, 'lxml')

    if soup.find('table') != None:
        for rows in soup.find_all('tr')[1:]:
            cols = rows.find_all('td')
            btnBet = rows.find('button', class_='newbet')

            url = "http://taman.trans.efko.ru"

            if '11' in btnBet.text:
                btnBet = url + btnBet.attrs['href']
            else: btnBet = None

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
    for j in range(len(city.C)):
        cityRe = r"%s\b" % city.C[j]
        if count < 3:
            for i in range(len(betTask)):
                if (re.findall(cityRe, str(betTask[i].get('cityOut'))) == [city.C[j]]) or (re.findall(cityRe, str(betTask[i].get('cityIn'))) == [city.C[j]]):
                    urlBet = str(betTask[i].get('urlBet10'))
                    #session.get(urlBet, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
                    msg = 'Заявка выбрана!' + '\n\n' + 'Номер заявки: ' + betTask[i].get('num') + '\n Из: ' + betTask[i].get('cityOut') + '\n В: ' + betTask[i].get('cityIn')
                    count += 1
                    print(msg)
                    break

    session.get(urlLogout, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

    f = open('logs/log_bet.txt', 'w')
    for i in range(len(betTask)):
        for key, value in betTask[i].items():
            f.write("{0}: {1}".format(key, value) + "\n")
        f.write("\n")
    f.close()

def main():
    parser()

if __name__ == '__main__':
    main()