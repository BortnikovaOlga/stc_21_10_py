from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class MainPageLocators:
    SEARCH_INPUT = (By.NAME, "q")


class MainPage(BasePage):

    def search(self, text: str):
        element = self.input(MainPageLocators.SEARCH_INPUT, text)
        self.click_enter(element)

