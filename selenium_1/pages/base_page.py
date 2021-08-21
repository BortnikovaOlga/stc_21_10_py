from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

BASE_URL = "http://www.python.org"


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, wait_time=10):
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}")

    def page_source(self):
        return self.driver.page_source

    def input(self, locator, text: str, wait_time: int = 10) -> WebElement:
        element = self.find_element(locator, wait_time)
        element.send_keys(text)
        return element

    def click_enter(self, element):
        element.send_keys(Keys.RETURN)

    def click(self, locator, wait_time: int = 10):
        element = WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable(locator),
            message=f"Can't find element by locator {locator}")
        element.click()

    def open_main_page(self):
        self.driver.get(BASE_URL)

    def get_title(self) -> str:
        return self.driver.title
