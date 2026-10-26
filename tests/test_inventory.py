# tests/test_inventory.py
import pytest
from pages.login_page import LoginPage


def test_catalog_has_6_products(logged_in):
    assert len(logged_in.get_product_names()) == 6


def test_sort_price_low_to_high(logged_in):
    prices = logged_in.sort_by("lohi").get_product_prices()
    assert prices == sorted(prices)


def test_sort_name_z_to_a(logged_in):
    names = logged_in.sort_by("za").get_product_names()
    assert names == sorted(names, reverse=True)


# Доп. 1: автотест находит настоящий баг в продукте
#
# ШАГ 2 (включаем ПОТОМ, когда баг уже заведён в трекере как BUG-1, но ещё не исправлен).
# Чтобы известный баг не красил весь прогон, помечаем этот набор как xfail:
# раскомментируйте блок ниже и закомментируйте parametrize из ШАГА 1.
# В pytest тест станет XFAIL, в Allure — серым Skipped с номером бага.
# Когда баг починят, pytest покажет XPASS — значит, xfail пора убирать.
#
@pytest.mark.parametrize("username", [
    "standard_user",
    pytest.param("problem_user", marks=pytest.mark.xfail(reason="BUG-1: у problem_user не работает сортировка")),
])

# ШАГ 1 (сейчас). Мы ещё НЕ знаем о баге: тест для problem_user падает КРАСНЫМ (Failed).
# Смотрим скриншот в Allure и оформляем баг-репорт.
# @pytest.mark.parametrize("username", ["standard_user", "problem_user"])
def test_sort_works_for_user(driver, username):
    inventory = LoginPage(driver).open_page().login_as_valid_user(username, "secret_sauce")
    names = inventory.sort_by("za").get_product_names()
    assert names == sorted(names, reverse=True)
