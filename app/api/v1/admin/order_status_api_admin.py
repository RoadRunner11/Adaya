from app.models import OrderStatus
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/order_status', methods=['GET'])
@api_v1.route('/connect/order_status/<int:id>', methods=['GET'])
#@admin_only
def get_order_status(id=None):
    page, per_page = get_page_from_args()
    name = request.args.get('name')
    per_page_for_stat = 50 # not many statuses so return all
    items = [OrderStatus.query.get(id)] if id else OrderStatus.get_items(
        name=name, page=page, per_page=per_page_for_stat)
    return res([item.as_dict() for item in items])


@api_v1.route('/connect/order_status/<int:id>', methods=['PUT'])
#@admin_only
def update_order_status(id):
    item = OrderStatus.query.get(id)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
    if len(item.update(json_dict)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()


@api_v1.route('/connect/order_status', methods=['POST'])
#@admin_only
def add_order_status():
    json_dict = request.json
    item = OrderStatus()
    error = item.update(json_dict)
    if len(error) > 0:
        return Responses.OPERATION_FAILED()
    return res(item.as_dict())

@api_v1.route('/connect/order_status/<int:id>', methods=['DELETE'])
#@admin_only
def delete_order_status(id=None):
    item = OrderStatus.query.get(id)
    error = item.delete()
    if len(error) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()