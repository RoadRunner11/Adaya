import pytest
from app.models import Product, Order, User


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

@pytest.fixture(scope='module')
def new_user():
    user = User('abcdefg@gmail.com','1q2w3e4r')
    return user
