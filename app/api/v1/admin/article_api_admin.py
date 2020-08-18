from app.models import Article
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import admin_only

# this api not currently being used
@api_v1.route('/connect/articles', methods=['GET'])
@api_v1.route('/connect/articles/<int:id>', methods=['GET'])
@admin_only
def get_articles(id=None):
    page, per_page = get_page_from_args()
    sort_by = request.args.get('sort_by')
    is_desc = parse_int(request.args.get('is_desc'))
    category_id = parse_int(request.args.get('category'))
    user_id = parse_int(request.args.get('user'))
    status_id = parse_int(request.args.get('status'))
    items = [Article.query.get(id)] if id else Article.get_items(
        category_id=category_id, user_id=user_id, status_id=status_id, page=page, per_page=per_page, sort_by=sort_by, is_desc=is_desc)
    return res([item.as_dict() for item in items])


@api_v1.route('/connect/articles/<int:id>', methods=['PUT'])
@admin_only
def update_article(id):
    item = Article.query.get(id)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
    if len(item.update(json_dict)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()


@api_v1.route('/connect/articles', methods=['POST'])
@admin_only
def add_item():
    json_dict = request.json
    item = Article()
    if len(item.update(json_dict)) > 0:
        return Responses.OPERATION_FAILED()
    return res(item.as_dict())
