from flask import Blueprint

# Create new Blueprint
api_v1 = Blueprint('api_v1',__name__)

from app.api.v1 import user_api
from app.api.v1.admin import user_api_admin
from app.api.v1.member import user_api_member

