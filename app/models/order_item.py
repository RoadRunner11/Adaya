from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class OrderItem(db.Model, DBMixin):
    __tablename__ = 'order_item'

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, default=1)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, default=1)
    variation_id = db.Column(db.Integer, db.ForeignKey('variation.id'), default=1)
    quantity = db.Column(db.Integer, default=0)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    product = db.relationship('Product')
    #order = db.relationship('Order')
    variation = db.relationship('Variation')

    output_column = ['order_id', 'quantity', 'product.name', 'variation.name', 'start_date', 'end_date']
