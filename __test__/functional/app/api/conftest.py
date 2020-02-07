import pytest
from app.models import User
from app.models import Order
from app.models import OrderItem
from app.models import Product
from app.models import Voucher
from datetime import datetime

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
def new_order(new_product):
    order = Order()

    order_item = OrderItem()
    order_item.product_id = 2
    order_item.variation_id = 2
    order_item.quantity = 1
    order_item.start_date = datetime.strptime('1-4-2020', '%d-%m-%Y')
    order_item.end_date = datetime.strptime('8-4-2020', '%d-%m-%Y')
        
    order.order_items = []
    order.order_items.append(order_item)
    order.order_items.append(order_item)
    return order

@pytest.fixture(scope='module')
def member_order():   
    order = Order()

    first_order_item = OrderItem()
    first_order_item.quantity = 1
    first_order_item.product_id = 2
    first_order_item.variation_id = 3
    first_order_item.start_date = datetime.strptime('1-4-2020', '%d-%m-%Y').strftime('%d-%m-%Y')
    first_order_item.end_date = datetime.strptime('8-4-2020', '%d-%m-%Y').strftime('%d-%m-%Y')   

    second_order_item = OrderItem()
    second_order_item.quantity = 1
    second_order_item.product_id = 5
    second_order_item.variation_id = 2
    second_order_item.start_date = datetime.strptime('1-4-2020', '%d-%m-%Y').strftime('%d-%m-%Y')
    second_order_item.end_date = datetime.strptime('8-4-2020', '%d-%m-%Y').strftime('%d-%m-%Y') 

    third_order_item = OrderItem()
    third_order_item.quantity = 1
    third_order_item.product_id = 4
    third_order_item.variation_id = 2
    third_order_item.start_date = datetime.strptime('1-4-2020', '%d-%m-%Y').strftime('%d-%m-%Y')
    third_order_item.end_date = datetime.strptime('8-4-2020', '%d-%m-%Y').strftime('%d-%m-%Y')   
    
    fourth_order_item = OrderItem()
    fourth_order_item.variation_id = 2
    fourth_order_item.product_id = 3
    fourth_order_item.quantity = 1
    fourth_order_item.start_date = datetime.strptime('1-4-2020', '%d-%m-%Y').strftime('%d-%m-%Y')
    fourth_order_item.end_date = datetime.strptime('8-4-2020', '%d-%m-%Y').strftime('%d-%m-%Y')

    fifth_order_item = OrderItem()
    fifth_order_item.variation_id = 2
    fifth_order_item.product_id = 6
    fifth_order_item.quantity = 1
    fifth_order_item.start_date = datetime.strptime('1-4-2020', '%d-%m-%Y').strftime('%d-%m-%Y')
    fifth_order_item.end_date = datetime.strptime('8-4-2020', '%d-%m-%Y').strftime('%d-%m-%Y')
    
    voucher = Voucher('HAO20')
    voucher.product_id = 3

    
    order.order_items = []
    order.vouchers = []
    order.user_id = 2
    order.id = 43
    
    order.order_items.append(first_order_item)
    order.order_items.append(second_order_item)
    order.order_items.append(third_order_item)
    order.order_items.append(fourth_order_item)
    order.order_items.append(fifth_order_item)
    order.vouchers.append(voucher)    

    return order

