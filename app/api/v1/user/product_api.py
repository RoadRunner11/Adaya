from app.models import Product, Variation, ProductVariations, ProductCategory
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import user_only
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_cors import CORS, cross_origin

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
    sort_by_price = request.args.get('sort_by_price')
    is_desc = parse_int(request.args.get('is_desc'))
    category_id = parse_int(request.args.get('category'))
    items = [Product.query.get(id)] if id else Product.get_items(
        category_id=category_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
    
    variations = Variation.get_items(category_id=None, page=1, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
    
    all_product_variations = []
    
    for item in items:
        available_product_variations = []
        for variation in variations:
            if (item.id == variation.product_id):
                available_product_variations.append(variation)

        product_variations = ProductVariations(product=item)
        product_variations.variations = available_product_variations
        
        all_product_variations.append(product_variations)

    if sort_by_price == 'price':
        sorted_productVariations_by_price = sorted(all_product_variations, key=lambda x: x.variations[0].price, reverse=False)
        return res([product_variation.as_dict() for product_variation in sorted_productVariations_by_price])
    
    return res([product_variation.as_dict() for product_variation in all_product_variations])

@api_v1.route('/products/<string:name>', methods=['GET'])
#@user_only
def user_get_productsearch(name=None):
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

    itemSearchResult = []
    
    products = Product.query.filter(Product.name.like("%"+name+"%")).all()
    if len(products) > 0:
      for item in products:
        variations = Variation.get_items_for_id(item.id)
        product_variations = ProductVariations(product=item)
        product_variations.variations = variations
        itemSearchResult.append(product_variations)

    categories = ProductCategory.query.filter(ProductCategory.name.like("%"+name+"%")).all()
    if len(categories) > 0:
        for category in categories:
            productsInCategory =  Product.get_items(category_id=category.id, page=page, per_page=50, sort_by=sort_by, is_desc=is_desc)
            for product in productsInCategory:
                variations = Variation.get_items_for_id(product.id)
                product_variations = ProductVariations(product=product)
                product_variations.variations = variations
                itemSearchResult.append(product_variations)

    return res([product_variation.as_dict() for product_variation in itemSearchResult])

@api_v1.route('/products/quicksearch', methods=['GET'])
#@user_only
def user_get_quicksearch(name=None):
    """
    get_products meeting criteria
    Args:
        id ([type]): product id

    Returns:
        [type]: [description]
    """
    page, per_page = get_page_from_args()    
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))
    category_id = parse_int(request.args.get('category'))
    date = request.args.get('date')
    size = request.args.get('size')
    requested_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    
    variations = Variation.get_items_for_size(size=size, page=page, per_page=100, sort_by=sort_by) # show only 100 results 
    
    all_product_variations = []

    for variation in variations:
        if  int(variation.stock) < 0:
            if variation.next_available_date != None:
                nad = datetime.strptime(variation.next_available_date, '%Y-%m-%d %H:%M:%S') 
                if requested_date > nad + relativedelta(days=14):
                    product = Product.get_product_from_id(variation.product_id)
                    product_variations = ProductVariations(product=product)
                    product_variations.variations = variation
                    all_product_variations.append(product_variations)
        else:
            product = Product.get_product_from_id(variation.product_id)
            product_variations = ProductVariations(product=product)
            product_variations.variations = variation
            all_product_variations.append(product_variations)

    return res([product_variation.as_dict() for product_variation in all_product_variations])

@api_v1.route('/products/category/<string:category>', methods=['GET'])
@api_v1.route('/products/category', methods=['GET'])
#@user_only
@cross_origin(origins="http://localhost:5000")
def user_get_productcategories(category=None):
    """
    get_products meeting criteria
    Args:
        id ([type]): product id

    Returns:
        [type]: [description]
    """
    page, per_page = get_page_from_args()    
    sort_by = request.args.get('sort_by')
    sort_by_price = request.args.get('sort_by_price')
    is_desc = parse_int(request.args.get('is_desc'))
    
    category_details = []
    if request.args.get('category') is None:
        category_details = ProductCategory.get_category_from_name(category)
    else:
        category_details = ProductCategory.get_category_from_name(request.args.get('category'))
    print(category)
    cat_id = category_details[0].id

    # category_details = ProductCategory.get_category_from_name(category)
    # cat_id = category_details[0].id

    items =  Product.get_items(
        category_id=cat_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)


    variations = Variation.get_items(category_id=None, page=1, per_page=per_page, sort_by=sort_by, is_desc=is_desc) # TODO UPDATE from one page, done as only currently small number of prods
    
    all_product_variations = []
    
    for item in items:
        available_product_variations = []
        for variation in variations:
            if (item.id == variation.product_id):
                available_product_variations.append(variation)

        product_variations = ProductVariations(product=item)
        product_variations.variations = available_product_variations
        
        all_product_variations.append(product_variations)
    
    if sort_by_price == 'price':
        sorted_productVariations_by_price = sorted(all_product_variations, key=lambda x: x.variations[0].price, reverse=False)
        return res([product_variation.as_dict() for product_variation in sorted_productVariations_by_price])

    return res([product_variation.as_dict() for product_variation in all_product_variations])

@api_v1.route('/products/sizes/<string:size>', methods=['GET'])
#@user_only
def user_get_sizes(size=None):
    """
    get_products meeting criteria
    Args:
        id ([type]): product id

    Returns:
        [type]: [description]
    """
    page, per_page = get_page_from_args()    
    sort_by = request.args.get('sort_by')
    sort_by_price = request.args.get('sort_by_price')
    # category_id = parse_int(request.args.get('category'))

    variations = Variation.get_items_for_size(size=size, page=page, per_page=per_page, sort_by=sort_by)
    
    all_product_variations = []

    for variation in variations:
        product = Product.get_product_from_id(variation.product_id)
        product_variations = ProductVariations(product=product)
        product_variations.variations = variation
        all_product_variations.append(product_variations)
    
    if sort_by_price == 'price':
        sorted_productVariations_by_price = sorted(all_product_variations, key=lambda x: x.variations.price, reverse=False)
        return res([product_variation.as_dict() for product_variation in sorted_productVariations_by_price])

    return res([product_variation.as_dict() for product_variation in all_product_variations])

@api_v1.route('/products/pagination', methods=['GET'])
def user_get_product_pages(name=None): # pagination details for all products

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

@api_v1.route('/products/pagination/<string:category>', methods=['GET'])
def user_get_product_pages_category(category=None): # pagination details for products filtered by category

    """
    get_products meeting criteria
    Args:
        id ([type]): product id

    Returns:
        [type]: [description]
    """
    page, per_page = get_page_from_args()    
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))
    category_details = []
    if request.args.get('category') is None:
        category_details = ProductCategory.get_category_from_name(category)
    else:
        category_details = ProductCategory.get_category_from_name(request.args.get('category'))
    cat_id = category_details[0].id

    page_details =  Product.get_items_pages(
        category_id=cat_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)    

    return res({"total_items": page_details.total, "no_of_pages": page_details.pages, "per_page": page_details.per_page})

@api_v1.route('/products/pagination/size/<string:size>', methods=['GET'])
def user_get_product_pages_size(size=None): # pagination details for products filtered by size
    """
    get_products meeting criteria
    Args:
        id ([type]): product id

    Returns:
        [type]: [description]
    """
    page, per_page = get_page_from_args()    
    sort_by = request.args.get('sort_by')

    page_details = Variation.get_items_for_size_paging(size=size, page=page, per_page=per_page, sort_by=sort_by)
    
    return res({"total_items": page_details.total, "no_of_pages": page_details.pages, "per_page": page_details.per_page})