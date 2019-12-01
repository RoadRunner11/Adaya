from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class Product(db.Model, DBMixin):
    __tablename__ = 'product'

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    category = db.relationship('ProductCategory')

    def __init__(self, title):
        self.title = title

    @classmethod
    def get_products_by_category(cls, category_id, page=None, per_page=None):
        # filter by category
        query = Product.category_id == category_id
        return cls.get(query, page, per_page)
