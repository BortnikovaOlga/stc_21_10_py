from selenium import webdriver

from pages.main_page import MainPage
from webdriver_manager.chrome import ChromeDriverManager


class Application:
    def __init__(self, driver=webdriver.Chrome(ChromeDriverManager().install())):
        self.driver = driver
        self.main_page = MainPage(driver)

    def quit(self):
        self.driver.quit()

    def open_page(self, url):
        self.driver.get(url)