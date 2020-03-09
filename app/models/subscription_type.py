from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class SubscriptionType(db.Model, DBMixin):
    __tablename__ = 'subscription_type'

    duration = db.Column(db.String(50), unique=False, nullable=False)   
    price = db.Column(db.Numeric(10, 2),default=0, nullable=False)
    
    output_column=['id','duration','price']

    def __init__(self, duration='', price=0.0):
        self.duration = duration
        self.price = price
    
    @classmethod
    def get_items(cls, duration=None, page=None, per_page=None):
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
        if duration != None:
            filter_query = cls.duration == duration
        return cls.get(filter_query, page, per_page)
