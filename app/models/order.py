from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class Order(db.Model, DBMixin):
    __tablename__ = 'order'
   
    name = db.Column(db.String(255), nullable=False)
    products = db.relationship('Product', secondary='product_order',
                               backref=db.backref('orders', lazy='dynamic'))
    amount = db.Column(db.Numeric(10,2),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('order_status.id'))

    def __init__(self, name):
        self.name = name
