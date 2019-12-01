from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class Article(db.Model, DBMixin):
    __tablename__ = 'article'

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    category_id = db.Column(db.Integer, db.ForeignKey('article_category.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('article_status.id'))

    def __init__(self, title=' '):
        self.title = title
