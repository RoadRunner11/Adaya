from app.models import Voucher
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/vouchers', methods=['GET'])
@api_v1.route('/connect/vouchers/<string:name>', methods=['GET'])
#@admin_only
def get_vouchers(name=None):
    """
    get_vouchers gets all vouchers
    
    """
    page, per_page = get_page_from_args()
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))

    items =  Voucher.get_items(name=name, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)

    return res([item.as_dict() for item in items])

@api_v1.route('/connect/vouchers/pagination', methods=['GET'])
#@admin_only
def get_vouchers_pages(name=None):
    """
    get_vouchers gets all vouchers
    
    """
    page, per_page = get_page_from_args()
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))
    
    page_details =Voucher.get_items_pages(name=name, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)

    return res({"total_items": page_details.total, "no_of_pages": page_details.pages, "per_page": page_details.per_page})


@api_v1.route('/connect/vouchers/<string:name>', methods=['PUT'])
#@admin_only
def update_vouchers(name):
    """
    update_voucher updates voucher by using name

    Args:
        name (string): 

    Returns:
        (string,int): update succesful, otherwise response no need to update
    """
    item = Voucher.get_voucher(name)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json

    if( 'discount_percent_off' in json_dict and 'discount_fixed_amount' in json_dict ):
        return Responses.OPERATION_FAILED(Messages.VOUCHER_DETAILS_WRONG)

    if len(item.update(json_dict)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()


@api_v1.route('/connect/vouchers', methods=['POST'])
#@admin_only
def add_voucher():
    json_dict = request.json
    if 'name' not in json_dict:
        return Responses.OPERATION_FAILED(Messages.VOUCHER_NAME_EMPTY)
    existing_item = Voucher.get_voucher(json_dict['name'])
    if existing_item:
        return Responses.OBJECT_EXIST(Messages.VOUCHER_EXISTS)
    if( 'discount_percent_off' in json_dict and 'discount_fixed_amount' in json_dict ):
        return Responses.OPERATION_FAILED(Messages.VOUCHER_DETAILS_WRONG)

    item = Voucher(json_dict['name'])
    error = item.insert_as_new_item(json_dict, ['name', 'redeem_by'])
    if len(error) > 0:
        return Responses.OPERATION_FAILED(error)
    return res(item.as_dict())


@api_v1.route('/connect/vouchers/<int:id>', methods=['DELETE'])
#@admin_only
def delete_vouchers(id=None):
    """
   delete voucher
    """
    page, per_page = get_page_from_args()
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))

    item =  Voucher.query.get(id)
    error = item.delete()
    if len(error) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()