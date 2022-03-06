import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from .BasePage import BasePage


class CatalogPage(BasePage):
    NOTEBOOKS_BTN = (By.CSS_SELECTOR, "#menu > div.collapse.navbar-collapse.navbar-ex1-collapse > ul > li:nth-child(2)")
    SHOW_ALL_BTN = (By.CSS_SELECTOR, "li.dropdown.open .see-all")
    CONTENT = (By.CSS_SELECTOR, "#content .product-grid")
    SORT_FILTER = (By.CSS_SELECTOR, "select#input-sort")

    def open_laptop_page(self):
        with allure.step(f"Открывается страница {self.browser.url}"):
            self.browser.get(self.browser.url)
        self._find_element_and_click(self.NOTEBOOKS_BTN)
        self._find_element_and_click(self.SHOW_ALL_BTN)

    def sort_products_by(self, text="Price (High > Low)"):
        sort_filter = Select(self._verify_element_visibility(self.SORT_FILTER))
        sort_filter.select_by_visible_text(text)

    @property
    def count_product_cards(self):
        content = self._verify_elements_visibility(self.CONTENT)
        return len(content)

    @property
    def get_current_sort_filter(self):
        sort_filter = Select(self._verify_element_visibility(self.SORT_FILTER))
        return sort_filter.first_selected_option.text
