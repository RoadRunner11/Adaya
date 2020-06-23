from app.models import SubscriptionType
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/subscribetype', methods=['GET'])
@api_v1.route('/connect/subscribetype/<string:plan>', methods=['GET'])
#@admin_only
def get_subscription_types(plan=None):
    """
    get_subscription_types gets all subscription types
    
    """
    page, per_page = get_page_from_args()

    items =  SubscriptionType.get_items(plan=plan, page=page, per_page=per_page)

    return res([item.as_dict() for item in items])


@api_v1.route('/connect/subscribetype/<string:plan>', methods=['PUT'])
#@admin_only
def update_subscription_type(plan):
    """
    update_subscription_type updates subscription type by using duration in months

    Args:
        plan (string): 

    Returns:
        (string,int): update succesful, otherwise response no need to update
    """
    item = SubscriptionType.get_items(plan=plan)[0]
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
    if len(item.update(json_dict)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()


@api_v1.route('/connect/subscribetype', methods=['POST'])
#@admin_only
def add_subscription_type():
    json_dict = request.json
    if 'plan' not in json_dict:
        return Responses.OPERATION_FAILED(Messages.NEEDED_FIELD_EMPTY)
    if 'price' not in json_dict:
        return Responses.OPERATION_FAILED(Messages.NEEDED_FIELD_EMPTY)
    existing_item = SubscriptionType.get_items(plan=json_dict['plan'])
    if len(existing_item) > 0:
        return Responses.OBJECT_EXIST()
    item = SubscriptionType(json_dict['plan'], json_dict['price'])
    error = item.insert_as_new_item(json_dict, ['plan', 'price'])
    if len(error) > 0:
        return Responses.OPERATION_FAILED(error)
    return res(item.as_dict())

@api_v1.route('/connect/subscribetype/<string:plan>', methods=['DELETE'])
#@admin_only
def delete_subscription_types(plan=None):
    """
    get_subscription_types gets all subscription types
    
    """
    page, per_page = get_page_from_args()

    item =  SubscriptionType.get_items(plan=plan, page=page, per_page=per_page)
    error = item.delete()
    if len(error) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()