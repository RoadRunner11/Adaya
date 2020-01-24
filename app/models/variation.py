from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class Variation(db.Model, DBMixin):
    __tablename__ = 'variation'
    name = db.Column(db.String(50), unique=False, nullable=False)   
    price = db.Column(db.Numeric(10, 2),default=0)
    stock = db.Column(db.Integer, default=0)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), default=1)

    product = db.relationship('Product')
    output_column = ['name', 'price', 'stock', 'product_id']

    def __init__(self, name):
        self.name = name
    
    @classmethod
    def get_variation_from_id(cls, variation_id):
        variation = Variation.query.get(variation_id)
        return variation

    @classmethod
    def get_all_product_variations(cls, product_id=None,):
        #filter_query = cls.product_id == product_id
        return cls.get(per_page=30)