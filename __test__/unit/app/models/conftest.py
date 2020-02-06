import pytest
from app.models import Product, Order, User, OrderItem, Variation
from datetime import datetime
from app.models import Voucher


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
def member_order(new_product):   
    order = Order()

    first_order_item = OrderItem()
    first_order_item.quantity = 1
    first_order_item.product_id = 2
    first_order_item.variation_id = 3
    first_order_item.start_date = datetime.strptime('1-4-2020', '%d-%m-%Y')
    first_order_item.end_date = datetime.strptime('8-4-2020', '%d-%m-%Y')   

    second_order_item = OrderItem()
    second_order_item.quantity = 1
    second_order_item.product_id = 3
    second_order_item.variation_id = 2
    second_order_item.start_date = datetime.strptime('1-4-2020', '%d-%m-%Y')
    second_order_item.end_date = datetime.strptime('8-4-2020', '%d-%m-%Y') 

    third_order_item = OrderItem()
    third_order_item.quantity = 1
    third_order_item.product_id = 4
    third_order_item.variation_id = 2
    third_order_item.start_date = datetime.strptime('1-4-2020', '%d-%m-%Y')
    third_order_item.end_date = datetime.strptime('8-4-2020', '%d-%m-%Y') 
        
    voucher = Voucher('LUO20')
    voucher.product_id = 1
    voucher.discount_fixed_amount = 8.00

    
    order.order_items = []
    order.vouchers = []
    order.user_id = 2
    order.id = 43
    
    order.order_items.append(first_order_item)
    order.order_items.append(second_order_item)
    order.order_items.append(third_order_item)
    order.vouchers.append(voucher)    

    return order

@pytest.fixture(scope='module')
def new_user():
    user = User('abcdefg@gmail.com','1q2w3e4r')
    return user

@pytest.fixture(scope='module')
def new_voucher():   
    voucher = Voucher('LUO20')
    voucher.product_id = 1
    voucher.discount_fixed_amount = 8.00
    voucher.max_redemptions = 2
    voucher.no_of_redemptions = 1
    voucher.redeem_by = datetime.strptime('8-4-2020', '%d-%m-%Y') 

    return voucher