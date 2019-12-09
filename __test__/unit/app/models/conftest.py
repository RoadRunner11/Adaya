import pytest
from app.models import Product, Order


@pytest.fixture(scope='module')
def new_product():
    product = Product(name='name')
    product.price = 10
    return product


@pytest.fixture(scope='module')
def new_order(new_product):
    order = Order()
    order.products = []
    order.products.append(new_product)
    order.products.append(new_product)
    return order
