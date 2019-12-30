from app.models import Order, Product
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
    product_ids = json_dict['product_ids']
    if product_ids:
        # Allow max of 4 products per order
        if len(product_ids) <= 4:
            if type(product_ids) == list:
                products = [Product.query.get(id)
                            for id in json_dict['product_ids']]
                item.products = products
                item.calculate_cost()
    if len(item.update(json_dict,force_insert=True)) > 0:
        return Responses.OPERATION_FAILED()
    return res(item.as_dict())

@api_v1.route('/orders/<int:id>', methods=['PUT'])
@user_only
def update_user_order(id):
    item = Order.query.get(id)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
    product_ids = json_dict['product_ids']
    if product_ids:
        # manually go through Ids
        if type(product_ids) == list:
            products = [Product.query.get(id)
                        for id in json_dict['product_ids']]
            item.products = products
            item.calculate_cost()
    if len(item.update(json_dict,force_insert=True)) > 0:
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
