from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class ArticleCategory(db.Model, DBMixin):
    __tablename__ = 'article_category'
   
    name = db.Column(db.String(255), nullable=False)
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    def __init__(self, name):
        self.name = name
