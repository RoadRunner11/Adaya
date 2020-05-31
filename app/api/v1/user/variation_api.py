from app.models import Product, Variation, ProductVariations, ProductCategory
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import user_only
from datetime import datetime
from dateutil.relativedelta import relativedelta

@api_v1.route('/variations', methods=['GET'])
#@user_only
def user_variations(name=None):
    """
    gets all unique variation types
    Args:
        id ([type]): product id

    Returns:
        [type]: [description]
    """

    variations = Variation.get_unique_variations().all()

    variation_names = []
    for variation in variations:
        variation_names.append(variation.name)

    variation_dict = { i : variation_names[i] for i in range(0, len(variation_names) ) }
 

    return res(variation_dict)
