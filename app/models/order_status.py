from app.helper.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class OrderStatus(db.Model, DBMixin):
    __tablename__ = 'order_status'
   
    name = db.Column(db.String(255), nullable=False)
    orders = db.relationship('Order', backref='status', lazy='dynamic')

    def __init__(self, name):
        self.name = name
