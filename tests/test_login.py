
import allure
import pytest
from pages.login_page import LoginPage

PASSWORD = "secret_sauce"


@allure.feature("Логин")
@allure.title("Успешный вход: standard_user попадает в каталог")
def test_login_valid_user(driver):
    inventory = LoginPage(driver).open_page().login_as_valid_user("standard_user", PASSWORD)
    assert inventory.get_title() == "Products"


@allure.feature("Логин")
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("locked_out_user", PASSWORD, "Sorry, this user has been locked out."),
        ("standard_user", "wrong_password", "Username and password do not match any user in this service"),
        ("", PASSWORD, "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
    ids=["locked_user", "wrong_password", "empty_username", "empty_password"],
)
def test_login_negative(driver, username, password, expected_error):
    login_page = LoginPage(driver).open_page().login_expecting_error(username, password)
    # Текст ошибки начинается с "Epic sadface: ", поэтому проверяем вхождение
    assert expected_error in login_page.get_error_text()
