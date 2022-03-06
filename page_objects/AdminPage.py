import allure
from selenium.webdriver.common.by import By

from .BasePage import BasePage


class AdminPage(BasePage):
    USERNAME_INPUT = (By.CSS_SELECTOR, "#input-username")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#input-password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    MENU_CATALOG_BTN = (By.CSS_SELECTOR, "#menu-catalog")
    MENU_CATALOG_PRODUCTS_BTN = (By.CSS_SELECTOR, "#collapse1 > li:nth-child(2) > a")
    ADD_NEW_BTN = (By.CSS_SELECTOR, ".page-header .pull-right a.btn")
    DELETE_BTN = (By.CSS_SELECTOR, ".page-header .pull-right button.btn-danger")
    PRODUCT_NAME_INPUT = (By.CSS_SELECTOR, "#input-name1")
    META_TAG_TITLE_INPUT = (By.CSS_SELECTOR, "#input-meta-title1")
    SAVE_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    TAB_DATA = (By.CSS_SELECTOR, "a[href='#tab-data']")
    MODEL_INPUT = (By.CSS_SELECTOR, "#input-model")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    PRODUCTS_LIST = (By.CSS_SELECTOR, "#form-product table")

    def open_page(self):
        url = self.browser.url + "/admin"
        with allure.step(f"Открывается страница {url}"):
            self.browser.get(url)

    def login(self):
        self._fill_input_field(self.USERNAME_INPUT, "user")
        self._fill_input_field(self.PASSWORD_INPUT, "bitnami")
        self._find_element_and_click(self.LOGIN_BTN)

    def open_products_list(self):
        self._find_element_and_click(self.MENU_CATALOG_BTN)
        self._find_element_and_click(self.MENU_CATALOG_PRODUCTS_BTN)

    def add_new_product(self, name):
        self._find_element_and_click(self.ADD_NEW_BTN)
        self._fill_input_field(self.PRODUCT_NAME_INPUT, name)
        self._fill_input_field(self.META_TAG_TITLE_INPUT, "test test test")
        self._find_element_and_click(self.TAB_DATA)
        self._fill_input_field(self.MODEL_INPUT, "test")
        self._find_element_and_click(self.SAVE_BTN)
        self._verify_element_visibility(self.SUCCESS_ALERT)

    def get_products_list(self):
        products_list = self._verify_element_visibility(self.PRODUCTS_LIST)
        return products_list.text

    def get_last_product(self):
        products_list = (self._verify_element_visibility(self.PRODUCTS_LIST)).find_elements(By.TAG_NAME, "tr")
        return products_list[len(products_list) - 1]

    def accept_deletion_alert(self):
        confirm_alert = self.browser.switch_to.alert
        confirm_alert.accept()

    def delete_product(self):
        last_product = self.get_last_product()
        checkbox = last_product.find_element(By.TAG_NAME, "input")
        checkbox.click()
        self._find_element_and_click(self.DELETE_BTN)
        self.accept_deletion_alert()
        self._verify_element_visibility(self.SUCCESS_ALERT)
