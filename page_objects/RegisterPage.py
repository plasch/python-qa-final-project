import allure
from selenium.webdriver.common.by import By

from .BasePage import BasePage


class RegisterPage(BasePage):
    MY_ACCOUNT_BTN = (By.CSS_SELECTOR, "a[title='My Account']")
    REGISTER_BTN = (By.CSS_SELECTOR, "#top-links > ul > li.dropdown.open > ul > li:nth-child(1) > a")
    CONTINUE_BTN = (By.CSS_SELECTOR, "input[type='submit']")
    PRIVACY_CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#content > h1")

    TEST_USER = {
        "firstname": "Bread",
        "lastname": "Peet",
        "email": "test@test.copm",
        "telephone": "1234567890",
        "password": "12345",
        "confirm": "12345",
    }

    def open_page(self):
        with allure.step(f"Открывается страница {self.browser.url}"):
            self.browser.get(self.browser.url)
        self._find_element_and_click(self.MY_ACCOUNT_BTN)
        self._find_element_and_click(self.REGISTER_BTN)

    def create_new_user(self):
        for i in self.TEST_USER.keys():
            self._fill_input_field((By.CSS_SELECTOR, f"input[name='{i}']"), self.TEST_USER[i])
        self._find_element_and_click(self.PRIVACY_CHECKBOX)
        self._find_element_and_click(self.CONTINUE_BTN)

    @property
    def success_register_message(self):
        msg = self._verify_element_visibility(self.SUCCESS_MESSAGE)
        return msg.text
