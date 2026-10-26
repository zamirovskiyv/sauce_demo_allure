# pages/checkout_pages.py
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")

    @allure.step("Заполнить данные покупателя")
    def fill_info(self, first_name, last_name, postal_code):
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)
        self.wait_url_contains("checkout-step-two")
        return CheckoutOverviewPage(self.driver)


class CheckoutOverviewPage(BasePage):
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    FINISH_BUTTON = (By.ID, "finish")

    def get_item_names(self):
        return self.get_texts(self.ITEM_NAMES)

    def get_item_total(self):
        return float(self.get_text(self.SUBTOTAL).split("$")[1])

    @allure.step("Завершить заказ")
    def finish(self):
        self.click(self.FINISH_BUTTON)
        self.wait_url_contains("checkout-complete")
        return CheckoutCompletePage(self.driver)


class CheckoutCompletePage(BasePage):
    HEADER = (By.CLASS_NAME, "complete-header")

    def get_header(self):
        return self.get_text(self.HEADER)