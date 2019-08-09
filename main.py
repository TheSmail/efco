import requests
import auth_data
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

session = requests.Session()

def auth():
    url = 'http://taman.trans.efko.ru/login.php'
    session.post(url, data=auth_data.get_pass())

def find():
    #url = "http://y91805lt.beget.tech"
    url = "http://taman.trans.efko.ru/trade/2"
    urls_bett = []
    url_logout = "http://taman.trans.efko.ru/logout.php"
    city = "Анапа"

    html = session.get(url, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
    soup = BeautifulSoup(html.content, 'html.parser')

    if soup.find('table') != None:
        trs = soup.find_all('tr')
        for tr in trs:
            if city in tr.text:
                btns = tr.find_all('button')
                for btn in btns:
                    if "10" in btn.text:
                        urls_bett.append(btn.attrs['href'])

        url_b = url + urls_bett[0]
        session.get(url_b, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
        session.get(url_logout)
        print("Ставка сделана")
    else:
        print("Нет торгов")
        session.get(url_logout)

def main():
    auth()
    find()

if __name__ == '__main__':
    main()