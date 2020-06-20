from app.models import Order, Product, ConfigValues, Voucher, OrderItem, User, OrderItem, UserSubscription, OrderProducts, Order_Item_With_Product, Variation, ProductSkeleton
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import user_only

@api_v1.route('/orders', methods=['POST'])
#@user_only
def create_order():
    json_dict = request.json
    item = Order()
    item.user_id = json_dict['user_id']

    order_items_dict = json_dict['order_items']
    for order_item_dict in order_items_dict:
        order_item = OrderItem()
        if order_item.update_from_dict(order_item_dict):
            item.order_items.append(order_item)
    
    item.update_from_dict(json_dict)
    

    user = User.query.get(item.user_id)
       
    # check if user is not blacklisted
    # if user.blacklist:
    #     return Responses.SUBSCRIPTION_INACTIVE()

    # if user.subscribed:
    #     if UserSubscription.check_subscription_active(user.id):
    #         return Responses.SUBSCRIPTION_INACTIVE()

    # if 'voucher_codes' in json_dict.keys():
    #     voucher_codes = json_dict['voucher_codes']
    #     number_vouchers_allowed = int(ConfigValues.get_config_value('max_no_of_vouchers'))
    #     if len(voucher_codes) >  number_vouchers_allowed:
    #         return Responses.NO_VOUCHERS_EXCEEDED()
    #     vouchers = Voucher.get_vouchers(voucher_codes)
    #     if not vouchers[0]:
    #         return Responses.INVALID_VOUCHER()        
    #     valid = Voucher.validate_voucher(vouchers)
    #     if valid:
    #         item.vouchers = vouchers
    #         item.calculate_discounted_cost()
    # else:    
    details = item.calculate_cost()

    if details != -1:        
        user.update({'number_of_items_ordered_this_month': int(details['no_items_this_month']), 'month_first_order' : details['month_first_order']})

    if len(item.update(json_dict,force_insert=True)) > 0:
        return Responses.OPERATION_FAILED()
    
    #send email confirmation to user
    Order.send_order_confirmation_email(order_number=item.id, user_email=user.email)
    return res(item.as_dict())

@api_v1.route('/orders/valid', methods=['POST'])
#@user_only
def validate_order():
    json_dict = request.json
    item = Order()
    item.user_id = json_dict['user_id']

    order_items_dict = json_dict['order_items']
    for order_item_dict in order_items_dict:
        order_item = OrderItem()
        if order_item.update_from_dict(order_item_dict):
            item.order_items.append(order_item)
    
    item.update_from_dict(json_dict)
    
    if not item.check_stock():
        return Responses.NO_STOCK()
    
    user = User.query.get(item.user_id)
    # check if user is blacklisted
    # if user.blacklist:
    #     return Responses.SUBSCRIPTION_INACTIVE()

    if user.subscribed:
        if not UserSubscription.check_subscription_active(user.id):
            user.update({'subscribed': 0})
            #return Responses.SUBSCRIPTION_INACTIVE()

    # if 'voucher_codes' in json_dict.keys():
    #     voucher_codes = json_dict['voucher_codes']
    #     number_vouchers_allowed = int(ConfigValues.get_config_value('max_no_of_vouchers'))
    #     if len(voucher_codes) >  number_vouchers_allowed:
    #         return Responses.NO_VOUCHERS_EXCEEDED()
    #     vouchers = Voucher.get_vouchers(voucher_codes)
    #     if not vouchers[0]:
    #         return Responses.INVALID_VOUCHER()        
    #     valid = Voucher.validate_voucher(vouchers)
    #     if valid:
    #         item.vouchers = vouchers
    #         item.calculate_discounted_cost()
    # else:    
    details = Order.calculate_cost_for_users(item)

    if details == -1:        
        return Responses.OPERATION_FAILED()
        
    return res(details)

@api_v1.route('/calculate-order-cost', methods=['POST'])
#@user_only
def calculate_order_cost():
    json_dict = request.json
    item = Order()
    item.user_id = json_dict['user_id']
    # item.firstname = json_dict['firstname']
    # item.lastname = json_dict['lastname']
    # item.email = json_dict['email']
    # item.address1 = json_dict['address1']
    # item.address2 = json_dict['address2']
    # item.city = json_dict['city']
    # item.post_code = json_dict['post_code']
    # item.country = json_dict['country']
    # item.phone = json_dict['phone']
    order_items_dict = json_dict['order_items']
   
    for order_item_dict in order_items_dict:
        order_item = OrderItem()
        if order_item.update_from_dict(order_item_dict):
            item.order_items.append(order_item)
    
    item.update_from_dict(json_dict)

    response = Order.calculate_cost_for_users(item)

    if response == -1:
        return Responses.NO_ORDERS_EXCEEDED()
    return res(response)

@api_v1.route('/orders/<int:id>', methods=['PUT'])
@user_only
def update_user_order():
    item = Order.query.get(id)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
    if json_dict['order_items']:
        order_items_dict = json_dict['order_items']

        for order_item_dict in order_items_dict:
            order_item = OrderItem()
            if "id" in order_item_dict.keys():
                order_item = OrderItem.query.get(order_item_dict['id'])        
            order_item.update_from_dict(order_item_dict)
            
            if not "id" in order_item_dict.keys():
                item.order_items.append(order_item)
            else:
                for oid in item.order_items:
                    if(oid.id == order_item_dict['id']):
                        oid = order_item

    item.calculate_cost()
        
    if len(item.update(force_insert=True)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()



@api_v1.route('/orders/confirmed/<int:id>', methods=['PUT'])
@user_only
def update_confirmed_user_order(id):
    item = Order.query.get(id)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
    item.update_from_dict(json_dict)
    
    # if not json_dict['payment_ref']:
    #     return Responses.OPERATION_FAILED()
        
    if len(item.update(force_insert=True)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()

@api_v1.route('/orders/unconfirmed/<int:id>', methods=['DELETE'])
#@user_only
def remove_unconfirmed_user_order(id):
    item = Order.query.get(id)
    if not item:
        return Responses.NOT_EXIST()
    item.delete()
        
    if len(item.delete()) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()


@api_v1.route('/orders/voucher', methods=['POST'])
@user_only
def calculate_order_discount():
    json_dict = request.json
    item = Order()
    order_items_dict = json_dict['order_items']

    for order_item_dict in order_items_dict:
        order_item = OrderItem()
        if order_item.update_from_dict(order_item_dict):
            item.order_items.append(order_item)

    voucher_codes = json_dict['voucher_codes']
    number_vouchers_allowed = int(ConfigValues.get_config_value('max_no_of_vouchers'))
    if len(voucher_codes) >  number_vouchers_allowed:
        return Responses.NO_VOUCHERS_EXCEEDED()
    vouchers = Voucher.get_vouchers(voucher_codes)
    if not vouchers[0]:
        return Responses.INVALID_VOUCHER()        
    valid = Voucher.validate_voucher(vouchers)
    if valid:
        item.vouchers = vouchers
        item.calculate_discounted_cost()
    return res(item.as_dict())

@api_v1.route('/orders/return/<int:id>', methods=['PUT'])
@user_only
def return_user_order(id): 
    item = Order.query.get(id)
    item.status_id = 1
    # ToDo
    #  send confirmation email on receiving items ?

@api_v1.route('/orders', methods=['GET'])
@api_v1.route('/orders/<int:id>', methods=['GET'])
#@user_only
def get_user_orders(id=None):
    page, per_page = get_page_from_args()
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))
    user_id = parse_int(request.args.get('user_id'))
    # order_id = parse_int(request.args.get('order_id'))
    status_id = parse_int(request.args.get('status'))
    
    if user_id:
        items = Order.get_items(
        user_id=user_id, status_id=status_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
        return res([item.as_dict() for item in items])

    elif id:
        items = [Order.query.get(id)] if id else Order.get_items(
            user_id=user_id, status_id=status_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
        return res([item.as_dict() for item in items][0])
    else:
        return Responses.OPERATION_FAILED()
    

@api_v1.route('/order/id/<int:id>', methods=['GET'])
#@user_only
def get_order_with_id(id=None):
    page, per_page = get_page_from_args()
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))
    user_id = parse_int(request.args.get('user_id'))
    # order_id = parse_int(request.args.get('order_id'))
    status_id = parse_int(request.args.get('status'))
    
    items = [Order.query.get(id)] if id else Order.get_items(
        user_id=user_id, status_id=status_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
    return res([item.as_dict() for item in items][0])
  

@api_v1.route('/order/my_account/<int:id>', methods=['GET'])
#@user_only
def get_order_with_product(id=None):
    item = Order.query.get(id)
    
    order_with_product = OrderProducts(total_price=item.total_price)
    order_with_product.firstname = item.firstname
    order_with_product.lastname = item.lastname
    order_with_product.email = item.email
    order_with_product.address1 = item.address1
    order_with_product.address2 = item.address2
    order_with_product.city = item.city
    order_with_product.post_code = item.post_code
    order_with_product.country = item.country
    order_with_product.phone = item.phone
    order_with_product.late_charge = item.late_charge
    if len(order_with_product.order_items) > 0:
        order_with_product.order_items = [] #empty the array again. and then get new data

    for order_item in item.order_items:
        order_item_with_product = Order_Item_With_Product(order_item.quantity, order_item.start_date, order_item.end_date, order_item.variation_id, order_item.days_returned_late)
        variation = Variation.get_variation_from_id(order_item.variation_id)
        product = Product.get_product_from_id(variation.product_id)
        new_product = ProductSkeleton(name=product.name)
        new_product.image = product.image.split(",")[0]
        order_item_with_product.product = new_product
        order_with_product.order_items.append(order_item_with_product)
    
    return res(order_with_product.as_dict())
   
