import requests
import auth_data
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

session = requests.Session()
urlLogout = "http://taman.trans.efko.ru/logout.php"
betTask = []

def auth():
    url = 'http://taman.trans.efko.ru/login.php'
    session.post(url, data=auth_data.get_pass())

def parser():
    url = "http://y91805lt.beget.tech"
    url = "http://taman.trans.efko.ru/trade/2"

    html = session.get(url, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
    soup = BeautifulSoup(html.content, 'lxml')

    if soup.find('table') != None:
        for rows in soup.find_all('tr')[1:]:
            cols = rows.find_all('td')
            btnBet = rows.find('button', class_='newbet')

            if '10' in btnBet.text:
                btnBet = url + btnBet.attrs['href']
            else: btnBet = None

            betTask.append({
                'num': cols[0].strong.text,
                'date': cols[9].strong.text,
                'cityOut': cols[20].strong.text,
                'cityIn': cols[24].strong.text,
                'urlBet10': btnBet
            })

        print("Парсинг окончен")
    else:
        print("Нет торгов")
        session.get(urlLogout)

    return betTask

def find(betTask):
    city = "Анапа"
    cityRe = r"%s\b" % city
    for i in range(len(betTask)):
        if re.findall(cityRe, str(betTask[i].get('cityOut'))) == [city]:
            urlBet = str(betTask[i].get('urlBet10'))
            session.post()
            break

    session.get(urlLogout)

def main():
    auth()
    parser()
    find(betTask)

if __name__ == '__main__':
    main()