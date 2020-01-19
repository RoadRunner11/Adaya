from flask import Blueprint

# Create new Blueprint
api_v1 = Blueprint('api_v1',__name__)

from app.api.v1 import user_api
from app.api.v1.admin import *



# @api_v1.before_request
# def before_request(response):
#     """
#     before_request contains actions before request
    
#     Args:
#         response ([type]): [description]
    
#     Returns:
#         [type]: [description]
#     """
#     return response

@api_v1.after_request
def after_request(response):
    """
    after_request contains actions after request
    
    Args:
        response ([type]): [description]
    
    Returns:
        [type]: [description]
    """
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response