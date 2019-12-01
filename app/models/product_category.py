from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class ProductCategory(db.Model, DBMixin):
    __tablename__ = 'product_category'
   
    name = db.Column(db.String(255), nullable=False)
    products = db.relationship('Product',lazy='dynamic')

    def __init__(self, name):
        self.name = name
