import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def auth():
    session = requests.Session()
    url = 'http://taman.trans.efko.ru/login.php'
    data = {'xLogin':'test', 'xPassword':'test'}

    session.post(url, data=data)

def find():
    url = "http://y91805lt.beget.tech/"
    html = requests.get(url, verify=False, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
    soup = BeautifulSoup(html.content, 'html.parser')

    trs = soup.find_all('tr')
    urls_bett = []

    for tr in trs:
        if "Анапа" in tr.text:
            btns = tr.find_all('button')
            for btn in btns:
                if "10" in btn.text:
                    urls_bett.append(btn.attrs['href'])


    url_b = "http://taman.trans.efko.ru/trade/2" + urls_bett[1]
    #requests.get()


    print(url_b)

def main():
    find()

if __name__ == '__main__':
    main()