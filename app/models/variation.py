from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class Variation(db.Model, DBMixin):
    __tablename__ = 'variation'
    name = db.Column(db.String(50), unique=False, nullable=False)   
    price = db.Column(db.Numeric(10, 2),default=0)
    stock = db.Column(db.Integer, default=0)
    retail_price = db.Column(db.Numeric(10, 2),default=0)
    next_available_date = db.Column(db.DateTime, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), default=1)

    product = db.relationship('Product')
    output_column = ['id','name', 'price', 'stock', 'retail_price','next_available_date','product_id']

    def __init__(self, name=''):
        self.name = name
    
    @classmethod
    def get_variation_from_id(cls, variation_id):
        variation = Variation.query.get(variation_id)
        return variation

    @classmethod
    def get_variation_from_size(cls, size):
        return Variation.query.filter_by(name = size).all()

    @classmethod
    def get_unique_variations(cls):
        return Variation.query.with_entities(Variation.name).distinct()


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
        
        #TODO return all variations
        return cls.get(filter_query, page, 100000, sort_query)
