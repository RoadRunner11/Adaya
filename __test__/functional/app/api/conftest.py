import pytest
from app.models import User
from app.models import UserSubscription
from app.models import Order
from app.models import OrderItem
from app.models import Product
from app.models import Voucher
from app.models import Variation
#from datetime import datetime
import datetime

@pytest.fixture(scope='module')
def admin_user():
    user = User()
    user.email = 'abc@gmail.com'
    user.password = '1q2w3e4r'
    user.email_confirmed = 'True'
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
    product = Product()
    product.name = 'Hao Trouser'
    product.description = '1sythq2w3stre4r'
    product.category_id = 2
    return product

@pytest.fixture(scope='module')
def new_subscription():
    subscription = UserSubscription()
    subscription.subscription_type_id = '1'
    subscription.start_date = datetime.datetime.strptime('2020-7-1 00:00:00', '%Y-%m-%d %H:%M:%S')
    subscription.end_date = datetime.datetime.strptime('2020-8-1 00:00:00', '%Y-%m-%d %H:%M:%S')
    return subscription

@pytest.fixture(scope='module')
def new_variation():
    variation = Variation()
    variation.name = 'XS'
    variation.price = '17.99'
    variation.stock = 2
    variation.total_stock = 3
    variation.next_available_date = datetime.datetime(2020, 8, 17)
    variation.retail_price = 33.99
    return variation

@pytest.fixture(scope='module')
def new_variation2():
    variation = Variation()
    variation.name = 'XXS'
    variation.price = '11.99'
    variation.stock = 1
    variation.total_stock = 3
    variation.next_available_date = datetime.datetime(2020, 9, 17)
    variation.retail_price = 35.99
    return variation

@pytest.fixture(scope='module')
def new_order(new_product):
    order = Order()

    order_item = OrderItem()
    order_item.product_id = 2
    order_item.variation_id = 2
    order_item.quantity = 1
    order_item.start_date = datetime.datetime.strptime('2020-8-1 00:00:00', '%Y-%m-%d %H:%M:%S')
    order_item.end_date = datetime.datetime.strptime('2020-8-8 00:00:00', '%Y-%m-%d %H:%M:%S')
        
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
    first_order_item.start_date = datetime.datetime.strptime('2020-8-1 00:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    first_order_item.end_date = datetime.datetime.strptime('2020-8-8 00:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')   

    second_order_item = OrderItem()
    second_order_item.quantity = 1
    second_order_item.product_id = 5
    second_order_item.variation_id = 2
    second_order_item.start_date = datetime.datetime.strptime('2020-8-1 00:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    second_order_item.end_date = datetime.datetime.strptime('2020-8-8 00:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') 

    third_order_item = OrderItem()
    third_order_item.quantity = 1
    third_order_item.product_id = 4
    third_order_item.variation_id = 2
    third_order_item.start_date = datetime.datetime.strptime('2020-8-1 00:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    third_order_item.end_date = datetime.datetime.strptime('2020-8-8 00:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')  
    
    fourth_order_item = OrderItem()
    fourth_order_item.variation_id = 2
    fourth_order_item.product_id = 3
    fourth_order_item.quantity = 1
    fourth_order_item.start_date = datetime.datetime.strptime('2020-8-1 00:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    fourth_order_item.end_date = datetime.datetime.strptime('2020-8-8 00:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') 

    fifth_order_item = OrderItem()
    fifth_order_item.variation_id = 2
    fifth_order_item.product_id = 6
    fifth_order_item.quantity = 1
    fifth_order_item.start_date = datetime.datetime.strptime('2020-8-1 00:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    fifth_order_item.end_date = datetime.datetime.strptime('2020-8-8 00:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S') 
    
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

