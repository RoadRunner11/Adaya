from app.models import Role
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/roles', methods=['GET'])
@admin_only
def get_roles():
    items = Role.get(per_page=100)
    return res([item.as_dict() for item in items])