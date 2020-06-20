from app.models import ProductCategory
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/product_categories', methods=['GET'])
@api_v1.route('/connect/product_categories/<int:id>', methods=['GET'])
@admin_only
def get_product_categories(id=None):
    page, per_page = get_page_from_args()
    per_page_for_cat = 50 # not many catgeories
    name = request.args.get('name')
    items = [ProductCategory.query.get(id)] if id else ProductCategory.get_items(
        name=name, page=page, per_page=per_page_for_cat)
    return res([item.as_dict() for item in items])


@api_v1.route('/connect/product_categories/<int:id>', methods=['PUT'])
@admin_only
def update_product_category(id):
    item = ProductCategory.query.get(id)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
    if len(item.update(json_dict)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()


@api_v1.route('/connect/product_categories', methods=['POST'])
@admin_only
def add_product_category():
    json_dict = request.json
    item = ProductCategory()
    error = item.update(json_dict)
    if len(error) > 0:
        return Responses.OPERATION_FAILED()
    return res(item.as_dict())
