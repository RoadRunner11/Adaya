from app.models import User
from app.api.v1 import api_v1
from app.helper import ErrorMessages
from app.helper.utility import res
from flask import jsonify, request
from flask_jwt_extended import create_access_token


@api_v1.route('/connect/users', methods=['GET'])
def get_all_users():
    users = User.get()
    return res([user.as_dict() for user in users])



