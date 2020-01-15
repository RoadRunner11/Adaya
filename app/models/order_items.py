from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class OrderItems(db.Model, DBMixin):
    __tablename__ = 'order_items'

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, default=1)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, default=1)
    quantity = db.Column(db.Integer, default=0)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    product = db.relationship('Product')
    order = db.relationship('Order')

    def __init__(self, name):
        self.name = name