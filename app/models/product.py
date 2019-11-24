from app.helper.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class Product(db.Model, DBMixin):
    __tablename__ = 'product'
   
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    price = db.Column(db.Numeric(10,2))
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))

    def __init__(self, title):
        self.title = title
