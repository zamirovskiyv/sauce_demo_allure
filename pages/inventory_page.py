# pages/inventory_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure                                             # УРОК 42
from pages.cart_page import CartPage                      # УРОК 42
from selenium.webdriver.support.ui import Select          # УРОК 42

class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")

    def _add_button_for(self, product_name):
        return (By.XPATH,
                f"//div[text()='{product_name}']"
                f"/ancestor::div[contains(@class,'inventory_item_description')]//button")

    def get_title(self):
        return self.get_text(self.TITLE)

    def get_product_names(self):
        return self.get_texts(self.PRODUCT_NAMES)

    def get_product_prices(self):
        # "$29.99" → 29.99 (float), чтобы можно было считать и сравнивать
        return [float(price.replace('$', '')) for price in self.get_texts(self.PRODUCT_PRICES)]

    def get_price_of(self, product_name):
        locator = (By.XPATH,
                   f"//div[text()='{product_name}']"
                   f"/ancestor::div[contains(@class,'inventory_item_description')]"
                   f"//div[@class='inventory_item_price']")
        return float(self.get_text(locator).replace('$', ''))

    @allure.step("Добавить в корзину: {product_name}")
    def add_to_cart(self, product_name):
        self.click(self._add_button_for(product_name))
        return self

    def get_cart_count(self):
        if not self.is_present(self.CART_BADGE):
            return 0
        return int(self.get_text(self.CART_BADGE))

    @allure.step("Сортировка: {value}")
    def sort_by(self, value):
        Select(self.find(self.SORT_SELECT)).select_by_value(value)
        return self

    @allure.step("Открыть корзину")
    def open_cart(self):
        self.click(self.CART_LINK)
        self.wait_url_contains("cart.html")             # ждём, пока откроется корзина
        return CartPage(self.driver)
