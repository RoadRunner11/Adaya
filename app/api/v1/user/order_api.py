from app.models import Order, Product, ConfigValues, Voucher
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
    order_items = json_dict['order_items']

    if order_items:
        item.order_items = order_items
        if not item.check_stock():
            return Responses.NO_STOCK()
    
    max_number = int(ConfigValues.get_config_value('max_no_products_per_order'))
    if item.check_quantity_products(max_number):
       return Responses.OPERATION_FAILED()
    
    if 'voucher_codes' in json_dict.keys():
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
    else:    
        item.calculate_cost()

    # TODO update stock
    if len(item.update(json_dict,force_insert=True)) > 0:
        return Responses.OPERATION_FAILED()
    return res(item.as_dict())

@api_v1.route('/orders/voucher', methods=['POST'])
#@user_only
def calculate_order_discount():
    json_dict = request.json
    item = Order()
    order_items = json_dict['order_items']
    if order_items:
        item.order_items = order_items
    if 'voucher_codes' in json_dict.keys():
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

@api_v1.route('/orders/<int:id>', methods=['PUT'])
#@user_only
def update_user_order(id):
    item = Order.query.get(id)
    if not item:
        return Responses.NOT_EXIST()

    if  item.check_order_status():
        return Responses.OPERATION_FAILED()
    
    if not item.check_stock():
        return Responses.NO_STOCK()

    json_dict = request.json
    order_items = json_dict['order_items']

    if order_items:        
        item.order_items = order_items
        # ToDO: check what products been updated a
        # if voucher been used before in initial order
        # check if new product been added and if voucher
        item.calculate_cost()

    if len(item.update(json_dict,force_insert=False)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()

@api_v1.route('/orders/<int:id>', methods=['GET'])
@user_only
def get_user_orders(id=None):
    page, per_page = get_page_from_args()
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))
    user_id = parse_int(request.args.get('user'))
    status_id = parse_int(request.args.get('status'))
    items = [Order.query.get(id)] if id else Order.get_items(
        user_id=user_id, status_id=status_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
    return res([item.as_dict() for item in items])
