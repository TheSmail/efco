import keyring
def get_pass():
    login = "evgen28rus@mail.ru"
    passwd = keyring.get_password("system", login)
    data = {'xLogin':login, 'xPassword':passwd}

    return data

def main():
    keyring.set_password("system", "evgen28rus@mail.ru", "had2911")

if __name__ == '__main__':
    main()