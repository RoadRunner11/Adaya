from app.models import Product
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import user_only

@api_v1.route('/products', methods=['GET'])
@user_only
def get_products(id=None):
    """
    get_products returns all product or the product with specific id
    Args:
        id ([type]): product id

    Returns:
        [type]: [description]
    """
    page, per_page = get_page_from_args()
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))
    category_id = parse_int(request.args.get('category'))
    items = [Product.query.get(id)] if id else Product.get_items(
        category_id=category_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
    return res([item.as_dict() for item in items])