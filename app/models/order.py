from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
from app.models.voucher import Voucher 
from app.models import Product
from app.models.config_values import ConfigValues
from app.models.variation import Variation
from app.models.order_items import OrderItems
from datetime import datetime
import json

db = AC().db


class Order(db.Model, DBMixin):
    __tablename__ = 'order'

    order_items = db.relationship('OrderItems', backref=db.backref('orders')) 
    vouchers = db.relationship('Voucher', secondary='voucher_order',
                               backref=db.backref('orders', lazy='dynamic'))  
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
            # decrease stock count
            #variation.stock -= 1
            product = Product.get_product_from_id(order_item.product_id)
            duration = self.date_difference(order_item.start_date, order_item.end_date)
            total_price += (variation.price * duration.days)
            products_freeze.append(product.as_dict(['id','name','description','variation.price','image']))
        self.total_price = total_price
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
            product = Product.get_product_from_id(order_item.product_id)
            variation = Variation.get_variation_from_id(order_item.variation_id)
            product_price = 0.00
            
            if not duration.days in (valid_durations):
                return False            
            # decrease stock count
            #variation.stock -= 1

            if(product.id in voucher_products_id):
                voucher = Voucher.get_voucher_by_product_id(product.id)
                if(voucher.discount_fixed_amount > 0):
                    product_price = (variation.price * duration.days) - voucher.discount_fixed_amount                    
                else:
                    product_price = (variation.price * duration.days) * (1 - (voucher.discount_percent_off/100))
            else:
                product_price = variation.price
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
    
    def populate_order_items(self, order_items):
        for order_item in order_items:
            _order_item = OrderItems()
            _order_item.product_id = order_item['product_id']
            _order_item.variation_id = order_item['variation_id']
            _order_item.quantity = order_item['quantity']
            _order_item.start_date = datetime.strptime(order_item['start_date'], '%d-%m-%Y')
            _order_item.end_date = datetime.strptime(order_item['end_date'], '%d-%m-%Y')
            self.order_items.append(_order_item)
    
    def set_order_items(self, order_items):
        self.order_items.clear()
        self.populate_order_items(order_items)


     
    # def get_product_from_id(self, product_id):
    #     product = Product.query.get(product_id)
    #     return product

    # def get_products_from_id(self, product_ids):        
    #     if type(product_ids) == list:  
    #         products = []
    #         for id in product_ids:
    #             products.append(self.get_product_from_id(id))
    #         return products
    #     else:
    #         product = self.get_product_from_id(product_ids)   
    #         return product                       
    
    def date_difference(self, start_date, end_date):
        return end_date - start_date