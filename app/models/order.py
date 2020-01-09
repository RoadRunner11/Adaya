from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
import json

db = AC().db


class Order(db.Model, DBMixin):
    __tablename__ = 'order'

    products = db.relationship('Product', secondary='product_order',
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

    output_column = ['id', 'products', 'products_freeze','payment_ref',
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
        for product in self.products:
            total_price += product.price
            products_freeze.append(product.as_dict(['id','name','description','price','image']))
        self.total_price = total_price
        self.products_freeze = json.dumps(products_freeze)
        
    def check_quantity_products(self, max_number):
        """
            Checks the number of products in the order 
            to ensure it is not beyond permitted number per order.
        """
        if len(self.products) > max_number:
            return False
    
    def check_stock(self):
        for product in self.products:
            if product.stock > 0:
                continue
            else:
                return False
    
    def check_order_status(self):
        if self.status_id == 1:
            return False

    #def check_apply_promotion_code():
        # info on percentage of discount based on promotion code

        # reduce total cost using the percentage