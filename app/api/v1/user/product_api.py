from app.models import Product, Variation, ProductVariations
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import user_only

@api_v1.route('/products', methods=['GET'])
@api_v1.route('/products/<int:id>', methods=['GET'])
#@user_only
def user_get_products(id=None):
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
    
    variations = Variation.get_items(category_id=None, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
    
    all_product_variations = []
    
    for item in items:
        available_product_variations = []
        for variation in variations:
            if (item.id == variation.product_id):
                available_product_variations.append(variation)

        product_variations = ProductVariations(product=item)
        product_variations.variations = available_product_variations
        
        all_product_variations.append(product_variations)

    return res([product_variation.as_dict() for product_variation in all_product_variations])