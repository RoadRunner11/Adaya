import pytest
from app.models import Product, Order, User, OrderItem, Variation
from datetime import datetime


@pytest.fixture(scope='module')
def new_product():
    product = Product(name='name')
    product.variation_id = 3
    return product


@pytest.fixture(scope='module')
def new_order(new_product):
    order = Order()

    order_item = OrderItem()
    order_item.variation_id = 2
    order_item.quantity = 1
    order_item.start_date = datetime.strptime('1-4-2020', '%d-%m-%Y')
    order_item.end_date = datetime.strptime('8-4-2020', '%d-%m-%Y')
        
    order.order_items = []
    order.order_items.append(order_item)
    order.order_items.append(order_item)
    return order

@pytest.fixture(scope='module')
def new_user():
    user = User('abcdefg@gmail.com','1q2w3e4r')
    return user