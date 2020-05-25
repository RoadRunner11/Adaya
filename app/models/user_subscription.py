from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
from datetime import datetime
from app.models import User
import time
from timeloop import Timeloop
from datetime import timedelta

db = AC().db
#timeloop = Timeloop()

class UserSubscription(db.Model, DBMixin):
    __tablename__ = 'user_subscription'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    subscription_id = db.Column(db.String(255))
    subscription_product = db.Column(db.String(255), nullable=True)
    subscription_type_id = db.Column(db.Integer, db.ForeignKey('subscription_type.id'))
    current_start_date = db.Column(db.DateTime, nullable=True)
    current_end_date = db.Column(db.DateTime, nullable=True)
    type_object = db.Column(db.String(255))
    application_fee_percent = db.Column(db.String(255))
    billing_cycle_anchor = db.Column(db.String(255))
    billing_thresholds = db.Column(db.String(255), nullable=True)
    cancel_at = db.Column(db.String(255), nullable=True)
    cancel_at_period_end = db.Column(db.Boolean, nullable=True)
    canceled_at = db.Column(db.DateTime, nullable=True)
    collection_method = db.Column(db.String(255), nullable=True)
    
    user = db.relationship('User')
    subscription_type = db.relationship('SubscriptionType')
    output_column = ['id', 'user_id', 'user.firstname', 'user.lastname', 'current_start_date', 'current_end_date', 'subscription_type_id', 'subscription_type.plan']

    def __init__(self, user_id=0, end_date=None, subscription_type_id=0):
        self.user_id = user_id
        self.current_start_date = datetime.now()
        self.current_end_date = end_date
        self.subscription_type_id = subscription_type_id       
    
    @classmethod
    def get_items(cls, id=None, page=None, per_page=None, sort_by=None, is_desc=None):
        """
        get_items

        Args:
            name (string, optional): [description]. Defaults to None.
            page (int, optional): [description]. Defaults to None.
            per_page (int, optional): [description]. Defaults to None.
            sort_by ([type], optional): what column to sort. Defaults to None.
            is_desc ([type], optional): sort desc? (1 or 0). Defaults to None.

        Returns:
            [type]: [description]
        """
        sort_query = db.desc(cls.created_time)
        if sort_by != None:
            if sort_by == 'user_id':
                # only support sorting by user_id
                sort_query = db.desc(cls.name)
                if not is_desc:
                    sort_query = db.asc(cls.created_time)

        filter_query = None
        if id != None:
            filter_query = cls.user_id == id
        return cls.get(filter_query, page, per_page, sort_query)
    @classmethod
    def get_subscription(cls, user_id=None, page=None, per_page=None):
        """
        get_items

        Args:
            name (string, optional): [description]. Defaults to None.
            page (int, optional): [description]. Defaults to None.
            per_page (int, optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        filter_query = None
        if user_id != None:
            filter_query = cls.user_id == user_id
        return cls.get(filter_query, page, per_page)

    @classmethod
    def check_subscription_active(cls, user_id):
        user_subscription = UserSubscription.query.filter_by(user_id = user_id).first()
        if user_subscription.current_end_date > datetime.now():
            return True
    
    #@timeloop.job(interval=timedelta(seconds=30))
    @classmethod
    def Check_all_user_subsriptions(cls):
        user_subscriptions = UserSubscription.query.all()
        
        for user_subscription in user_subscriptions:
            if datetime.now() > user_subscription.end_date:
                user = User.query.filter_by(id = user_subscription.user_id).first()
                user.subscribed = False
                user.update()
