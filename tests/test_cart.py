
# tests/test_cart.py
def test_remove_from_cart(logged_in):
    cart = (logged_in
            .add_to_cart("Sauce Labs Backpack")
            .add_to_cart("Sauce Labs Bike Light")
            .open_cart()
            .remove("Sauce Labs Backpack"))

    assert cart.get_item_names() == ["Sauce Labs Bike Light"]
