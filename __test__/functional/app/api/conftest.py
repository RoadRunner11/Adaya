import pytest
from app.models import User
from app.models import Order
from app.models import Product

@pytest.fixture(scope='module')
def admin_user():
    user = User()
    user.email = 'abc@gmail.com'
    user.password = '1q2w3e4r'
    return user

@pytest.fixture(scope='module')
def new_member():
    user = User()
    user.email = 'cret@gmail.com'
    user.password = '1q2w3e4r'
    user.role_id = 2
    user.lastname = 'Analytics'
    return user

@pytest.fixture(scope='module')
def new_product():
    product = Product(name='name')
    product.price = 10
    return product


@pytest.fixture(scope='module')
def member_order(new_product):
    order = Order()
    order.products = []
    order.products.append(new_product)
    order.products.append(new_product)
    return order
