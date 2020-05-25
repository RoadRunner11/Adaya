from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
from app.models.voucher import Voucher 
from app.models import Product, User
from app.models.order_item_with_price import Order_Item_With_Price
from app.models.config_values import ConfigValues
from app.models.variation import Variation
from app.models.order_item import OrderItem
from app.models.user_subscription import UserSubscription
from datetime import datetime
from dateutil.relativedelta import relativedelta
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=1)
    status_id = db.Column(db.Integer, db.ForeignKey('order_status.id'), default=1)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(120))
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(255))
    post_code = db.Column(db.String(255))
    country = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    late_charge = db.Column(db.Numeric(10, 2))
    late_charge_paid = db.Column(db.Boolean, nullable=True, default=True)
   
    user = db.relationship('User')
    status = db.relationship('OrderStatus')
    

    output_column = ['id', 'order_items', 'products_freeze','payment_ref', 'status_id', 'user_id',
                     'total_price', 'vouchers', 'user.email', 'user.firstname', 'user.lastname', 'status.name', 'enabled', 'firstname', 'lastname',
                      'email', 'address1', 'address2', 'city', 'post_code', 'country', 'phone', 'created_time', 'late_charge', 'late_charge_paid']

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
        # else, there is another check when user makes an order and sets subscribed flag to 0 if it fails this validation
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
                #TODO update number of redemptions of voucher
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
        #user.update({'number_of_items_ordered_this_month': no_items_this_month, 'month_first_order' : date_first_month_order})
        #user.update({'subscribed': 0})
    @classmethod
    def calculate_cost_for_users(cls, json_dict):
        item = Order()
        item.user_id = json_dict['user_id']
        order_items_dict = json_dict['order_items']
        user = User.query.get(json_dict['user_id'])
        order_items=[]
        max_number_adayalite = int(ConfigValues.get_config_value('max_no_free_products_adayalite_user'))
        max_number_products_monthly = int(ConfigValues.get_config_value('max_no_products_per_month'))

        for order_item_dict in order_items_dict:
            order_item = OrderItem()
            if order_item.update_from_dict(order_item_dict):
                order_items.append(order_item)
        
        
        order_items_with_price = Order.add_price_on_order_item(order_items)
        
        no_items_this_order = Order.get_number_of_items_in_order(order_items)
        no_items_this_month = user.number_of_items_ordered_this_month
        
        date_first_month_order = user.month_first_order
        if date_first_month_order is None:  # add current date as first order this month if blank
            date_first_month_order = datetime.now()
        print('current date plus a month')
        print(date_first_month_order + relativedelta(months=1))
        
        # set first order date to current time if the old first date is more than a month ago
        if (date_first_month_order + relativedelta(months=1)) < datetime.now():  
            date_first_month_order = datetime.now()
        
        orders = Order.get_items(user_id=json_dict['user_id'], per_page=30)

        orders_this_month = []
        for order in orders:
            if (order.created_time >= date_first_month_order) and (order.created_time < date_first_month_order + relativedelta(months=1)):
                orders_this_month.append(order)
        
        # for order in orders_this_month:
        #     order_items_in_order = OrderItem.get_items(order_id=order.id)
        #     for order_item in order_items_in_order:
        #         no_items_this_month += 1
        
        userSub = UserSubscription.get_subscription(user_id=json_dict['user_id'])
        userSubscription = {}
        if len(userSub) > 0:
            userSubscription = userSub[0]

        total_cost = 0.00
        if(user.subscribed):
            if UserSubscription.check_subscription_active(user.id):
                if(userSubscription.subscription_type_id == 1): #AdayaLite plan 
                    if no_items_this_month > 4 and no_items_this_month <= max_number_products_monthly:
                        total_cost = Order.get_cost(order_items)
                    elif no_items_this_month < max_number_adayalite:
                        no_uncharged_items_left = max_number_adayalite - no_items_this_month
                        if no_items_this_order <= no_uncharged_items_left: #check if number of items in order is covered by number of uncharged items left
                            total_cost = 0.00
                        else:
                            total_cost = Order.get_cost(order_items)
                            order_items_sorted = Order.sort_order_items_on_price(order_items_with_price)
                            index = 0
                            while(index < no_uncharged_items_left):
                                variation = Variation.get_variation_from_id(order_items_sorted[index].variation_id)
                                duration = order_items_sorted[index].end_date - order_items_sorted[index].start_date
                                if(duration.days == 7):
                                    total_cost -= float(variation.price + 10)
                                else:
                                    total_cost -= float(variation.price)   
                                index += 1
                    else:
                        return -1
                            
                if(userSubscription.subscription_type_id == 2): #AdayaLifestyle plan
                    total_cost = 0.00
            else:
                user.update({'subscribed': 0})
        else: #unsubscribed user
            if no_items_this_month > max_number_products_monthly:
                return -1
            total_cost = Order.get_cost(order_items)

        no_items_this_month += no_items_this_order

        #user.update({'number_of_items_ordered_this_month': no_items_this_month, 'month_first_order' : date_first_month_order})

        return ({'total_cost':total_cost, 'no_items_this_month': no_items_this_month})
    
    @classmethod
    def get_cost(cls, order_items):
        total = 0.00
        for order_item in order_items:
            variation = Variation.get_variation_from_id(order_item.variation_id)
            duration = order_item.end_date - order_item.start_date
            if(duration.days == 7):
                total += float((variation.price + 10))
            else:
                total += float(variation.price)
        return total
    
    @classmethod
    def get_number_of_items_in_order(cls, order_items):
        total = 0
        for order_item in order_items:
            total += order_item.quantity
        return total
    
    @classmethod
    def sort_order_items_on_price(cls, order_items):
        sortedOrderItems = sorted(order_items, key=lambda x: x.price, reverse=True)
        return sortedOrderItems
    
    @classmethod
    def add_price_on_order_item(cls, order_items):
         # add price to order items
        items_with_price = []
        for order_item in order_items:
            variation = Variation.get_variation_from_id(order_item.variation_id)
            order_item_with_price =  Order_Item_With_Price()
            
            duration = order_item.end_date - order_item.start_date
            if duration.days == 7:
                order_item_with_price.price = float(variation.price + 10)
            else:
                order_item_with_price.price = float(variation.price)


            order_item_with_price.quantity = order_item.quantity
            order_item_with_price.start_date = order_item.start_date
            order_item_with_price.end_date = order_item.end_date
            order_item_with_price.variation_id = order_item.variation_id

            items_with_price.append(order_item_with_price)
        return items_with_price

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