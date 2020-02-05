from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
from app.models.voucher import Voucher 
from app.models import Product, User, UserSubscription
from app.models.config_values import ConfigValues
from app.models.variation import Variation
from app.models.order_item import OrderItem
from datetime import datetime
import json

db = AC().db


class Order(db.Model, DBMixin):
    __tablename__ = 'order'

    order_items = db.relationship('OrderItem', backref=db.backref('order')) 
    vouchers = db.relationship('Voucher', secondary='voucher_order',
                               backref=db.backref('order', lazy='dynamic'))  
    products_freeze = db.Column(db.Text)
    payment_ref = db.Column(db.String(255))
    total_price = db.Column(db.Numeric(10, 2))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, default=1)
    status_id = db.Column(db.Integer, db.ForeignKey(
        'order_status.id'), default=1)

    user = db.relationship('User')
    status = db.relationship('OrderStatus')
    

    output_column = ['id', 'order_items', 'products_freeze','payment_ref',
                     'total_price', 'user.email', 'status.name', 'enabled']

    def update_from_dict(self, obj_dict, not_updatable_columns=[]):
        """
        update_from_dict updates self by using dict

        Args:
            obj_dict (dict):
            not_updatable_columns (list, optional): columns that won't be updated

        Returns:
            [type]: [description]
        """
        not_updatable_columns = not_updatable_columns if len(
            not_updatable_columns) > 0 else self.not_updatable_columns
        flag = False
        if obj_dict:
            for key in obj_dict:
                if key in not_updatable_columns:
                    continue
                if key == 'order_items':
                    count = 0
                    for order_item_dict in obj_dict['order_items']:
                        self.order_items[count].update_from_dict(order_item_dict)
                        count += 1 
                    continue               
                       
                if hasattr(self, key):         
                    setattr(self, key, obj_dict[key])
                    flag = True          
        return flag

    @classmethod
    def get_items(cls, user_id=None, status_id=None, page=None, per_page=None, sort_by=None, is_desc=None):
        # default sort by time
        sort_query = db.desc(cls.created_time)
        if sort_by != None:
            if sort_by == 'created_time':
                sort_query = db.desc(cls.created_time)
                if not is_desc:
                    sort_query = db.asc(cls.created_time)
            if sort_by == 'total_price':
                sort_query = db.desc(cls.total_price)
                if not is_desc:
                    sort_query = db.asc(cls.total_price)
        filter_queries = []
        if user_id != None:
            filter_queries.append(cls.user_id == user_id)
        if status_id != None:
            filter_queries.append(cls.status_id == status_id)
        return cls.get(filter_queries, page, per_page, sort_query)
    

    def calculate_cost(self):
        total_price = 0
        products_freeze = []
        
        for order_item in self.order_items:
            variation = Variation.get_variation_from_id(order_item.variation_id)
            #TODO decrease stock count
            #variation.stock -= 1
            product = Product.get_product_from_id(variation.product_id)
            duration = self.date_difference(order_item.start_date, order_item.end_date)
            total_price += (variation.price * duration.days)
            products_freeze.append(product.as_dict(['id', 'name', 'description', 'variation.price', 'image']))
        self.total_price = total_price
        user = User.query.get(self.user_id)
        if user.subscribed:
            if UserSubscription.check_subscription_active(self.user_id):
                self.total_price = 0.00
        self.products_freeze = json.dumps(products_freeze)
    
    def calculate_discounted_cost(self):
        total_price = 0
        product_price = 0        
        products_freeze = []    
        min_duration = int(ConfigValues.get_config_value('min_duration_of_rental')) 
        max_duration = int(ConfigValues.get_config_value('max_duration_of_rental')) 
        valid_durations = [min_duration, max_duration]    
        voucher_products_id = Voucher.get_voucher_product_ids(self.vouchers)

        for order_item in self.order_items:
            duration = self.date_difference(order_item.start_date, order_item.end_date)            
            variation = Variation.get_variation_from_id(order_item.variation_id)
            product = Product.get_product_from_id(variation.product_id)
            product_price = 0.00
            
            if not duration.days in (valid_durations):
                return False            
            #TODO decrease stock count
            #variation.stock -= 1

            if(product.id in voucher_products_id):
                voucher = Voucher.get_voucher_by_product_id(product.id)
                if(voucher.discount_fixed_amount > 0):
                    product_price = (variation.price * duration.days) - voucher.discount_fixed_amount                    
                else:
                    product_price = (variation.price * duration.days) * (1 - (voucher.discount_percent_off/100))
            else:
                product_price = variation.price * duration.days
            total_price += product_price
            products_freeze.append(product.as_dict(['id','name','description','variation.price','image']))

        self.total_price = total_price
        self.products_freeze = json.dumps(products_freeze)
        
    def check_quantity_products(self, max_number):
        """
            Checks the number of products in the order 
            to ensure it is not beyond permitted number per order.
        """
        quantity = 0
        for order_item in self.order_items:
            quantity += order_item.quantity
        if quantity > max_number:
            return True
    
    def check_stock(self):
        for order_item in self.order_items:
            variation = Variation.get_variation_from_id(order_item.variation_id)
            if order_item.quantity <= variation.stock:
                continue
            else:
                return False
        return True
    
    def check_order_status(self):
        if self.status_id == 1:
            return False
    
    def populate_order_items(self, order_items_dict):
         for order_item_dict in order_items_dict:
            order_item = OrderItem()
            if order_item.update_from_dict(order_item_dict):
                self.order_items.append(order_item)

    def set_order_items(self, order_items):
        self.order_items.clear()
        self.populate_order_items(order_items)          
    
    def date_difference(self, start_date, end_date):
        return end_date - start_date