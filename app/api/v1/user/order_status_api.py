from app.models import OrderStatus
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import user_only


@api_v1.route('/connect/order_status/<int:id>', methods=['GET'])
@user_only
def get_order_status(id=None):
    page, per_page = get_page_from_args()
    name = request.args.get('name')
    items = [OrderStatus.query.get(id)] if id else OrderStatus.get_items(
        name=name, page=page, per_page=per_page)
    return res([item.as_dict() for item in items])