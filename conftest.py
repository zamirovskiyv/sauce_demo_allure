# conftest.py
import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage

def build_chrome_options():
    options = Options()
    # ❗ Chrome знает, что "secret_sauce" есть в базах утёкших паролей,
    # и показывает окно "Смените пароль", которое блокирует клики. Отключаем.
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })

    # На сервере GitHub переменная CI = "true". Локально её нет.
    if os.getenv("CI") == "true":
        options.add_argument("--headless=new")  # без окна
        options.add_argument("--window-size=1920,1080")  # виртуальный монитор (иначе 800x600 и сайт "скукожится")
        options.add_argument("--no-sandbox")  # стабильность в Linux-контейнере
        options.add_argument("--disable-dev-shm-usage")  # мало служебной памяти на сервере
    return options


@pytest.fixture
def driver():
    browser = webdriver.Chrome(options=build_chrome_options())
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture
def logged_in(driver):
    """Предусловие: пользователь залогинен и находится в каталоге."""
    return LoginPage(driver).open_page().login_as_valid_user("standard_user", "secret_sauce")


# Хук из урока 41: при падении теста прикладываем скриншот в Allure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
