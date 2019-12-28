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

# @pytest.fixture(scope='module')
# def new_product():
#     product = Product(name='name')
#     product.price = 10
#     product.id = 2
#     return product


@pytest.fixture(scope='module')
def member_order():
    first_product = Product(name='fname')
    first_product.price = 10
    first_product.id = 2

    second_product = Product(name='sname')
    second_product.price = 320
    second_product.id = 3

    third_product = Product(name='tname')
    third_product.price = 420
    third_product.id = 4

    fourth_product = Product(name='ftname')
    fourth_product.price = 520
    fourth_product.id = 5

    fifth_product = Product(name='ftname')
    fifth_product.price = 620
    fifth_product.id = 6

    order = Order()
    order.products = []

    order.products.append(first_product)
    order.products.append(second_product)
    order.products.append(third_product)
    order.products.append(fourth_product)
    order.products.append(fifth_product)
    
    return order
