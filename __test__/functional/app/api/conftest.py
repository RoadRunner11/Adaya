import pytest
from app.models import User
from app.models import Order
from app.models import OrderItem
from app.models import Product
from app.models import Voucher
import datetime

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
def member_order():    
    first_product = Product(name='fname')
    first_product.price = 10
    first_product.id = 2
    first_product.variation_id = 2

    first_order_item = OrderItem()
    first_order_item.product_id = first_product.id
    first_order_item.quantity = 1
    first_order_item.start_date = datetime.date(2020, 4, 1)
    first_order_item.end_date = datetime.date(2020, 4, 8)   
    
    second_product = Product(name='sname')
    second_product.price = 320
    second_product.id = 3
    second_product.variation_id = 2

    second_order_item = OrderItem()
    second_order_item.product_id = second_product.id
    second_order_item.quantity = 1
    second_order_item.start_date = datetime.date(2020, 4, 1)
    second_order_item.end_date = datetime.date(2020, 4, 8)   
    
    third_product = Product(name='tname')
    third_product.price = 420
    third_product.id = 4
    third_product.variation_id = 2

    third_order_item = OrderItem()
    third_order_item.product_id = third_product.id
    third_order_item.quantity = 1
    third_order_item.start_date = datetime.date(2020, 4, 1)
    third_order_item.end_date = datetime.date(2020, 4, 8)   
    
    fourth_product = Product(name='ftname')
    fourth_product.price = 520
    fourth_product.id = 5
    fourth_product.variation_id = 2

    fourth_order_item = OrderItem()
    fourth_order_item.product_id =  fourth_product.id
    fourth_order_item.quantity = 1
    fourth_order_item.start_date = datetime.date(2020, 4, 1)
    fourth_order_item.end_date = datetime.date(2020, 4, 8)   
    

    fifth_product = Product(name='fthname')
    fifth_product.price = 620
    fifth_product.id = 6
    fifth_product.variation_id = 2

    fifth_order_item = OrderItem()
    fifth_order_item.product_id = fifth_product.id
    fifth_order_item.quantity = 1
    fifth_order_item.start_date = datetime.date(2020, 4, 1)
    fifth_order_item.end_date = datetime.date(2020, 4, 8)   
    

    voucher = Voucher('HAO20')
    voucher.product_id = 3

    order = Order()
    order.order_items = []
    order.vouchers = []
    order.user_id = 43
    order.id = 43
    
    order.order_items.append(first_order_item)
    order.order_items.append(second_order_item)
    order.order_items.append(third_order_item)
    order.order_items.append(fourth_order_item)
    order.order_items.append(fifth_order_item)
    order.vouchers.append(voucher)    

    return order
