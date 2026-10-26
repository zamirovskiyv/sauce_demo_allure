
# tests/test_e2e_purchase.py
import allure
import pytest

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


@allure.feature("Покупка")
@allure.title("E2E: покупка двух товаров, сверка корзины и суммы")
def test_purchase_two_products(logged_in):
    inventory = logged_in

    # 1. Запоминаем цены ИЗ КАТАЛОГА (это наш "ценник")
    expected_total = sum(inventory.get_price_of(name) for name in PRODUCTS)

    # 2. Кладём товары
    for name in PRODUCTS:
        inventory.add_to_cart(name)
    assert inventory.get_cart_count() == len(PRODUCTS)

    # 3. Сверяем список 1 (что положили) со списком 2 (что в корзине)
    cart = inventory.open_cart()
    assert sorted(cart.get_item_names()) == sorted(PRODUCTS)

    # 4. Checkout
    overview = cart.checkout().fill_info("Ivan", "Tester", "11000")
    assert sorted(overview.get_item_names()) == sorted(PRODUCTS)

    # 5. Сверяем сумму в "чеке" с ценниками
    assert overview.get_item_total() == pytest.approx(expected_total)

    # 6. Финал
    complete = overview.finish()
    assert complete.get_header() == "Thank you for your order!"
