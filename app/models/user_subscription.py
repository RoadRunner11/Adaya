from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
from datetime import datetime
from app.models import User

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
    
    
    @classmethod
    def check_subscription_active(cls, user_id):
        user_subscription = UserSubscription.query.filter_by(user_id = user_id).first()
        #TODO sort list by end_date and select most recent end date for check
        if user_subscription.end_date < datetime.datetime.now():
            return True
    
    # timeloop = Timeloop()

    # @timeloop.job(interval=timedelta(seconds=60))
    # @classmethod
    # def Check_all_user_subsriptions(cls):
    #     user_subscriptions = UserSubscription.query.all()
        
    #     for user_subscription in user_subscriptions:
    #         if user_subscription.end_date > datetime.datetime.now():
    #             user = User.query.filter_by(user_id = user_subscription.user_id)
    #             user.subscribed = False
