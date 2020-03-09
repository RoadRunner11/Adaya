from app.models import Order, Product, OrderItem
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/orders', methods=['GET'])
@api_v1.route('/connect/orders/<int:id>', methods=['GET'])
#@admin_only
def get_orders(id=None):
    page, per_page = get_page_from_args()
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))
    user_id = parse_int(request.args.get('user'))
    status_id = parse_int(request.args.get('status'))
    items = [Order.query.get(id)] if id else Order.get_items(
        user_id=user_id, status_id=status_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
    return res([item.as_dict() for item in items])


@api_v1.route('/connect/orders/<int:id>', methods=['PUT'])
@admin_only
def update_order(id):
    item = Order.query.get(id)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
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


@api_v1.route('/connect/orders', methods=['POST'])
@admin_only
def add_order():
    json_dict = request.json
    item = Order()
    item.user_id = json_dict['user_id']
    item.status_id = json_dict['status_id']
    order_items_dict = json_dict['order_items']

    for order_item_dict in order_items_dict:
        order_item = OrderItem()       
        order_item.update_from_dict(order_item_dict)
        item.order_items.append(order_item)
    
    item.calculate_cost()
    
    if len(item.update(force_insert=True)) > 0:
        return Responses.OPERATION_FAILED()
    return res(item.as_dict())
