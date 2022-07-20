import os.path

from selenium import webdriver
from selenium.common import NoSuchElementException, InvalidCookieDomainException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
from time import sleep
from json import dumps, load

from utils import fetch_config


class Operations:
    def __init__(self, config: dict[str: str]):
        self.chrome_version = config['chrome_version']
        self.sleep_time = int(config['sleep_time'])

        options = Options()
        options.add_argument("start-maximized")
        if self.chrome_version:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(version=self.chrome_version).install()), options=options)
        else:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def __del__(self):
        print("Shutting down")
        self.driver.close()

    def __str__(self):
        return f"Sleep_time: {self.sleep_time}, Chrome_version: {self.chrome_version}"

    def dump_cookies(self):
        # getting sessionid cookie
        self.driver.get('https://internal-api.prolific.co/')
        session_id = self.driver.get_cookie('sessionid')
        sleep(self.sleep_time)

        self.driver.get('https://app.prolific.co/studies')
        sleep(self.sleep_time)
        # close popup and get klaro cookie
        try:
            self.driver.find_element(By.XPATH, value='//*[@id="klaro"]/div/div/div[2]/div/div/div/button[2]').click()
        except NoSuchElementException:
            print('nie ma co zamknac')
        klaro = self.driver.get_cookie('klaro')

        cookies: dict[str: dict[str: str]] = {"sessionid": session_id, "klaro": klaro}
        json = dumps(cookies, indent=4)
        with open('cookies.json', 'w') as f:
            f.write(json)

    def log_in_with_cookies(self):
        with open('./cookies.json', 'r') as f:
            cookies = load(f)

        session_id = cookies['sessionid']
        klaro = cookies['klaro']
        self.driver.get('https://internal-api.prolific.co/auth/accounts/login/')
        self.driver.add_cookie(session_id)
        self.driver.add_cookie(klaro)
        self.driver.get('https://app.prolific.co/studies')

    def log_in(self, email: str, password: str) -> None:
        # CHECK IF COOKIES ARE PRESENT
        if os.path.exists('./cookies.json'):
            # self.log_in_with_cookies()
            # exit(1)
            try:
                self.log_in_with_cookies()
                return
            except InvalidCookieDomainException:
                os.remove('./cookies.json')
        self.driver.get('https://internal-api.prolific.co/auth/accounts/login/')
        sleep(self.sleep_time)
        self.driver.find_element(By.XPATH, value='//*[@id="id_username"]').send_keys(email)
        sleep(self.sleep_time)
        self.driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div[3]/div/div/input').send_keys(password)
        sleep(self.sleep_time)
        self.driver.find_element(By.XPATH, value='//*[@id="login"]').submit()
        sleep(self.sleep_time * 1.5)
        # dump cookies
        self.dump_cookies()

    def main_loop(self) -> bool:
        self.driver.execute_script("document.body.style.zoom = '50%'")
        while True:
            try:
                html = self.driver.page_source
                soup = Soup(html, "html.parser")
                if soup.find_all('h3'):
                    self.driver.find_element(
                        By.XPATH,
                        value='/html/body/div[1]/div[2]/div/div/div/div/div[1]/ul/li/div/div[1]/div[2]/div').click()
                    self.driver.find_element(
                        By.XPATH,
                        value='/html/body/div[1]/div[2]/div/div/div/div/div[2]/div[1]/div[3]/button').click()
                    return True
                sleep(self.sleep_time)
            except Exception as e:
                print(e)
                return False


if __name__ == '__main__':
    operations = Operations(fetch_config())
    input()
