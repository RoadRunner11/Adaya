from app.models import Product
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int
from flask import jsonify, request
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/products', methods=['GET'])
@api_v1.route('/connect/products/<int:id>', methods=['GET'])
@admin_only
def get_products(id=None):
    """
    get_products returns all product or the product with specific id
    Args:
        id ([type]): product id

    Returns:
        [type]: [description]
    """
    page = parse_int(request.args.get('page')) or 1
    per_page = parse_int(request.args.get('per_page')) or 10
    category_id = parse_int(request.args.get('category'))
    products = [Product.query.get(id)] if id else Product.get_products_by_category(
        category_id=category_id, page=page, per_page=per_page)
    return res([product.as_dict() for product in products])
