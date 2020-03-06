from app.models import UserSubscription
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/subscribe', methods=['GET'])
@api_v1.route('/connect/subscribe/<string:name>', methods=['GET'])
#@admin_only
def get_subscriptions(id=None):
    """
    get_subscriptions gets all user subscriptions
    
    """
    page, per_page = get_page_from_args()
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))

    items =  UserSubscription.get_items(id=id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)

    return res([item.as_dict() for item in items])


@api_v1.route('/connect/subscribe/<int:id>', methods=['PUT'])
#@admin_only
def update_subscription(id):
    """
    update_subscription updates user subscription by using id

    Args:
        id (int): 

    Returns:
        (string,int): update succesful, otherwise response no need to update
    """
    item = UserSubscription.query.get(id)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
    if len(item.update(json_dict)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()


@api_v1.route('/connect/subscribe', methods=['POST'])
#@admin_only
def add_subscription():
    json_dict = request.json

    item = UserSubscription(user_id=json_dict['user_id'], end_date=json_dict['end_date'], subscription_type_id=json_dict['subscription_type_id'])
    error = item.insert_as_new_item(json_dict)
    if len(error) > 0:
        return Responses.OPERATION_FAILED(error)
    return res(item.as_dict())
