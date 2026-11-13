"""Day 5 · Bug hunt

We planted 3 bugs in 3 copies of the cart. Write tests here, using the `Cart` fixture,
that pass on the real cart (cart.py) but fail on each buggy copy.

Read the rules at the top of cart.py, then test them, including the edges.
Run `python quest.py 5` to see which bugs you've caught.
"""
import pytest


def test_add_one_item(Cart):
    cart = Cart()
    cart.add("notebook", 120)
    assert cart.subtotal() == 120


def test_subtotal_counts_quantity(Cart):
    cart = Cart()
    cart.add("notebook", 120, qty=3)
    assert cart.subtotal() == 360


def test_shipping_is_free_at_exactly_500(Cart):
    cart = Cart()
    cart.add("backpack", 500)
    assert cart.shipping() == 0


def test_coupon_cannot_be_applied_twice(Cart):
    cart = Cart()
    cart.add("notebook", 100)
    cart.apply_coupon("SAVE10")

    with pytest.raises(ValueError):
        cart.apply_coupon("SAVE10")
