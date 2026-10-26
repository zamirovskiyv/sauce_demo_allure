# pages/cart_page.py
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    ITEM_NAMES = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")    # только товары В КОРЗИНЕ
    ITEM_PRICES = (By.CSS_SELECTOR, ".cart_item .inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_item_names(self):
        return self.get_texts(self.ITEM_NAMES)

    def get_item_prices(self):
        return [float(price.replace('$','')) for price in self.get_texts(self.ITEM_PRICES)]

    @allure.step("Удалить из корзины: {product_name}")
    def remove(self, product_name):
        locator = (By.XPATH,
                   f"//div[text()='{product_name}']/ancestor::div[@class='cart_item']//button")
        self.click(locator)
        return self

    @allure.step("Перейти к оформлению")
    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        self.wait_url_contains("checkout-step-one")
        from pages.checkout_pages import CheckoutInfoPage
        return CheckoutInfoPage(self.driver)