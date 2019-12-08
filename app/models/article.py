from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
from flask_sqlalchemy import SQLAlchemy

db = AC().db


class Article(db.Model, DBMixin):
    __tablename__ = 'article'

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'article_category.id'), default=1)
    status_id = db.Column(db.Integer, db.ForeignKey(
        'article_status.id'), default=1)
    category = db.relationship('ArticleCategory')
    status = db.relationship('ArticleStatus')
    user = db.relationship('User')

    output_column = ['id', 'title', 'content',
                     'user.email', 'status.name', 'category.name', 'enabled']

    def __init__(self, title=' '):
        self.title = title

    @classmethod
    def get_items(cls, category_id=None, user_id=None, status_id=None, page=None, per_page=None, sort_by=None, is_desc=None):
        # default sort by time
        sort_query = db.desc(cls.created_time)
        if sort_by != None:
            if sort_by == 'created_time':
                # only support sorting by price
                sort_query = db.desc(cls.created_time)
                if not is_desc:
                    sort_query = db.asc(cls.created_time)
        filter_queries = []
        if category_id != None:
            filter_queries.append(cls.category_id == category_id)
        if user_id != None:
            filter_queries.append(cls.user_id == user_id)
        if status_id != None:
            filter_queries.append(cls.status_id == status_id)
        return cls.get(filter_queries, page, per_page, sort_query)
