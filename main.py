import requests
import auth_data
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

    session.post(url_auth, data=auth_data.get_pass(), verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

    html = session.get(url, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
    soup = BeautifulSoup(html.content, 'lxml')

    if soup.find('table') != None:
        for rows in soup.find_all('tr')[1:]:
            cols = rows.find_all('td')
            btnBet = rows.find('button', class_='newbet')

            url = "http://taman.trans.efko.ru"

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
        session.get(urlLogout, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
        betTask = None

    city = "Краснодар"
    cityRe = r"%s\b" % city
    for i in range(len(betTask)):
        if (re.findall(cityRe, str(betTask[i].get('cityOut'))) == [city]) or (re.findall(cityRe, str(betTask[i].get('cityIn'))) == [city]):
            urlBet = str(betTask[i].get('urlBet10'))
            session.get(urlBet, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
            print(urlBet)
            break
    session.get(urlLogout, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

def main():
    parser()

if __name__ == '__main__':
    main()