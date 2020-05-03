from flask import Blueprint
from flask import request

# Create new Blueprint
api_v1 = Blueprint('api_v1',__name__)

from app.api.v1.user import user_api
from app.api.v1.user import order_api
from app.api.v1.user import product_api
from app.api.v1.user import subscription_api
from app.api.v1.user import product_category_api
from app.api.v1.admin import *
from app.api.v1 import heartbeat
import flask


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
    referrer = request.headers.get("Referer")
    if referrer in flask.current_app.config['ALLOW_ORIGIN']:
        response.headers.add('Access-Control-Allow-Origin', referrer)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'content-type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, HEAD')
        
        # header = response.headers
        # header['Access-Control-Allow-Origin'] = referrer
        # header['Access-Control-Allow-Credentials'] = 'true'
        # header['Access-Control-Allow-Headers'] = 'content-type'
        # header['Access-Control-Allow-Methods']='GET, PUT, POST, DELETE, HEAD'
    return response