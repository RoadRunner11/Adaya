from app.models import Product, Variation, ProductVariations
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import admin_only
import datetime
from dateutil.parser import parse


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
    page, per_page = get_page_from_args()
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))
    category_id = parse_int(request.args.get('category'))
    items = [Product.query.get(id)] if id else Product.get_items(
        category_id=category_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
    
    variations = Variation.get_items(page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
    
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

@api_v1.route('/connect/products/pagination', methods=['GET'])
def get_product_pages(name=None): # pagination details for all products

    """
    get default get query

    Args:
        filter_queries (single query or query list, optional): example - [Article.category_id == 1] or Article.category_id == 1
        page (int, optional): which page. Defaults to 1.
        per_page (int, optional): how many items for each return. Defaults to 10.
        order ([type], optional): example db.desc(Post.post_date) or db.asc
        error_out (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    page, per_page = get_page_from_args()    
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))
    category_id = parse_int(request.args.get('category'))

    page_details =  Product.get_items_pages(category_id=category_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
    

    return res({"total_items": page_details.total, "no_of_pages": page_details.pages, "per_page": page_details.per_page})

@api_v1.route('/connect/products/<int:id>', methods=['PUT'])
@admin_only
def update_product(id):
    item = Product.query.get(id)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
    if len(item.update(json_dict['product'])) > 0:
        return Responses.OPERATION_FAILED()
    
    current_variations = Variation.query.filter_by(product_id=item.id).all()
    current_variations_names = []
    for variation in current_variations:
        current_variations_names.append(variation.name)

    variations_dict = json_dict['variations']
    for variation_dict in variations_dict:
        variation = Variation()
        variation.update_from_dict(variation_dict)
        if variation.next_available_date != None: # ensure this is a date string
            if is_date(variation.next_available_date):
                variation.next_available_date = datetime.datetime.strptime(variation.next_available_date, '%Y-%m-%d %H:%M:%S')     
        
        if variation.name in current_variations_names:            
            for current_variation in current_variations:
                if variation.name == current_variation.name:
                    if len(current_variation.update(variation_dict)) > 0:
                        return Responses.OPERATION_FAILED()
        else: #a new variation is being added to this product
            if len(variation.update()) > 0:
                return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()

@api_v1.route('/connect/products', methods=['POST'])
@admin_only
def add_product():
    json_dict = request.json
    item = Product()
    error = item.update(json_dict['product'])    
    if len(error) > 0:
        return Responses.OPERATION_FAILED()
    product = Product.query.filter_by(name = json_dict['product']['name']).first()
    
    variations = []
    variations_dict = json_dict['variations']
    
    for variation_dict in variations_dict:
        variation = Variation()
        if variation.update_from_dict(variation_dict):
            variation.product_id = product.id    
            if variation.next_available_date != None: # ensure this is a date string
                if is_date(variation.next_available_date):
                    variation.next_available_date = datetime.datetime.strptime(variation.next_available_date, '%Y-%m-%d %H:%M:%S')        
            variations.append(variation)    

    for variation in variations:
        if len(variation.update()) > 0:
            return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()


@api_v1.route('/connect/products/<int:id>', methods=['DELETE'])
@admin_only
def delete_product(id=None):
    """
    get_products returns all product or the product with specific id
    Args:
        id ([type]): product id

    Returns:
        [type]: [description]
    """
    item = Product.query.get(id)

    variations = Variation.get_items_for_id(product_id = item.id)
    
    # delete variations before product
    for variation in variations:
       if len(variation.delete()) > 0:
           return Responses.OPERATION_FAILED()

    # deletes product
    error = item.delete()
    
    if len(error) > 0:
        return Responses.OPERATION_FAILED()

    return Responses.SUCCESS()

@api_v1.route('/connect/products/variation/<int:id>', methods=['DELETE'])
@admin_only
def delete_variation(id=None):
    """
    get_products returns all product or the product with specific id
    Args:
        id ([type]): product id

    Returns:
        [type]: [description]
    """
    variation = Variation.get_variation_from_id(id)
    
    # delete variation before product
    if len(variation.delete()) > 0:
        return Responses.OPERATION_FAILED()

    return Responses.SUCCESS()

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False