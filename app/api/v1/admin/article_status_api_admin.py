from app.models import ArticleStatus
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/article_status', methods=['GET'])
@api_v1.route('/connect/article_status/<int:id>', methods=['GET'])
@admin_only
def get_article_status(id=None):
    page, per_page = get_page_from_args()
    name = request.args.get('name')
    items = [ArticleStatus.query.get(id)] if id else ArticleStatus.get_items(
        name=name, page=page, per_page=per_page)
    return res([item.as_dict() for item in items])


@api_v1.route('/connect/article_status/<int:id>', methods=['PUT'])
@admin_only
def update_article_status(id):
    item = ArticleStatus.query.get(id)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
    if len(item.update(json_dict)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()


@api_v1.route('/connect/article_status', methods=['POST'])
@admin_only
def add_article_status():
    json_dict = request.json
    item = ArticleStatus()
    error = item.update(json_dict)
    if len(error) > 0:
        return Responses.OPERATION_FAILED()
    return res(item.as_dict())
