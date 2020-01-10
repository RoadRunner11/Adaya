from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
import datetime

db = AC().db

class Coupon(db.Model, DBMixin):
    __tablename__ = 'coupon'
    name = db.Column(db.String(50), unique=True, nullable=False)
    percent_off = db.Column(db.Numeric(10, 2),default=0)
    max_redemptions = db.Column(db.Integer, default=0)
    no_of_redemptions = db.Column(db.Integer, default=0)
    fixed_amount = db.Column(db.Numeric(10, 2),default=0)
    redeem_by = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=1)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, default=1)
    product = db.relationship('Product')
    user = db.relationship('User')

    def __init__(self, name):
        self.name = name
    
    def validate_coupon(self, coupon_name):
        coupon_date = self.check_coupon_date()
        
        if (self.max_redemptions > 0):
            coupon_redeem = self.check_coupon_redemption()
            if coupon_date and coupon_redeem:
                return True
        else:
            return coupon_date

    def check_coupon_date(self):
        if self.redeem_by > datetime.datetime.now():
            return True

    def check_coupon_redemption(self):        
        if self.no_of_redemptions <= self.max_redemptions:
            return True
        