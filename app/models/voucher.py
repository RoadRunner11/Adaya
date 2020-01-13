from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
import datetime

db = AC().db

class Voucher(db.Model, DBMixin):
    __tablename__ = 'voucher'    

    # orders = db.relationship('Order', secondary='voucher_order',
    #                            backref=db.backref('vouchers', lazy='dynamic'))
    users = db.relationship('User', secondary='user_voucher',
                               backref=db.backref('vouchers', lazy='dynamic'))
    name = db.Column(db.String(50), unique=True, nullable=False)
    discount_percent_off = db.Column(db.Numeric(10, 2),default=0)
    discount_fixed_amount = db.Column(db.Numeric(10, 2),default=0)
    max_redemptions = db.Column(db.Integer, default=0)
    no_of_redemptions = db.Column(db.Integer, default=0)    
    redeem_by = db.Column(db.DateTime, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=1)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, default=1)    
    #user = db.relationship('User')
    product = db.relationship('Product')

    @classmethod
    def get_items(cls, name=None, page=None, per_page=None):
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
        if name != None:
            filter_query = cls.name == name
        return cls.get(filter_query, page, per_page)   
    
    def __init__(self, name):
        self.name = name
    
    @classmethod
    def get_voucher(cls, voucher_code):
        return Voucher.query.filter_by(name = voucher_code).first()

    @classmethod
    def get_voucher_by_product_id(cls, voucher_product_id):
        return Voucher.query.filter_by(product_id = voucher_product_id).first()

    @classmethod
    def get_vouchers(cls, voucher_codes):
        if type(voucher_codes) == list:  
            vouchers = []
            for code in voucher_codes:
                voucher = Voucher.get_voucher(code)
                vouchers.append(voucher)
            return vouchers
    
    @classmethod
    def get_voucher_product_ids(cls, vouchers):
        product_ids = []
        for voucher in vouchers:
            product_ids.append(voucher.product_id)
        return product_ids

    @classmethod
    def validate_voucher(cls, vouchers):
        for voucher in vouchers:
            voucher_date_status = voucher.check_voucher_date()  
            if not voucher_date_status:
                return False      
            
            
            if (voucher.max_redemptions > 0):
                voucher_redeem_status = voucher.check_voucher_redemption()
                if not voucher_redeem_status:
                    return False          
        return True

    def check_voucher_date(self):
        if self.redeem_by > datetime.datetime.now():
            return True

    def check_voucher_redemption(self):        
        if self.no_of_redemptions <= self.max_redemptions:
            return True
        