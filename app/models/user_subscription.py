from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class UserSubscription(db.Model, DBMixin):
    __tablename__ = 'user_subscription'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    subscription_type_id = db.Column(db.Integer, db.ForeignKey('subscription_type.id'))
    payment_ref = db.Column(db.String(255))

    user = db.relationship('User')
    subscription_type = db.relationship('SubscriptionType')
    output_column = ['user_id', 'start_date', 'end_date', 'subscription_type_id']

    def __init__(self, user_id=0, start_date=None, end_date=None, subscription_type_id=0):
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.subscription_type_id = subscription_type_id
