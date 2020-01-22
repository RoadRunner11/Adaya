from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class Variation(db.Model, DBMixin):
    __tablename__ = 'variation'
    name = db.Column(db.String(50), unique=True, nullable=False)   
    price = db.Column(db.Numeric(10, 2),default=0)
    stock = db.Column(db.Integer, default=0)

    output_column = ['name', 'price', 'stock', 'category.name']

    def __init__(self, name):
        self.name = name
    
    @classmethod
    def get_variation_from_id(cls, variation_id):
        variation = Variation.query.get(variation_id)
        return variation
