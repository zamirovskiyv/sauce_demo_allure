# pages/login_page.py
import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.XPATH, "//h3[@data-test='error']")

    @allure.step("Открыть страницу логина")
    def open_page(self):
        self.open(self.URL)
        return self

    def _fill_and_submit(self, username, password):
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Войти как {username}")
    def login_as_valid_user(self, username, password):
        self._fill_and_submit(username, password)
        return InventoryPage(self.driver)

    @allure.step("Попытка входа как {username} (ожидаем ошибку)")
    def login_expecting_error(self, username, password):
        self._fill_and_submit(username, password)
        return self

    def get_error_text(self):
        return self.get_text(self.ERROR)
