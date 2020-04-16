from app.models import ProductCategory
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import user_only


@api_v1.route('/product_categories', methods=['GET'])
@api_v1.route('/product_categories/<int:id>', methods=['GET'])
#@user_only
def user_get_product_categories(id=None):
    page, per_page = get_page_from_args()
    name = request.args.get('name')
    items = [ProductCategory.query.get(id)] if id else ProductCategory.get_items(
        name=name, page=page, per_page=per_page)
    return res([item.as_dict() for item in items])

