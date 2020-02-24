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

    def __init__(self, name=''):
        self.name = name
    
    @classmethod
    def get_variation_from_id(cls, variation_id):
        variation = Variation.query.get(variation_id)
        return variation

    @classmethod
    def get_items(cls, category_id=None, page=None, per_page=None, sort_by=None, is_desc=None):   
        sort_query = db.desc(cls.created_time)
        if sort_by != None:
            if sort_by == 'price':
                # only support sorting by price
                sort_query = db.desc(cls.price)
                if not is_desc:
                    sort_query = db.asc(cls.created_time)
        filter_query = None
        
        return cls.get(filter_query, page, 100, sort_query)
