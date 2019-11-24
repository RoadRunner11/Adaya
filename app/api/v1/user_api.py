from app.models import User
from app.api.v1 import api_v1
from app.decorators.json import as_json
from flask import jsonify

@api_v1.route('/users',methods=['GET'])
def get():
    users = User.get()
    user_json1 = jsonify([user.as_dict() for user in users])
    return user_json1


