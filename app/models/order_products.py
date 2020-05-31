from app.models.order import Order
from app.models import Product

class OrderProducts(object):
    total_price = 0.00
    firstname = ""
    lastname = ""
    email = ""
    address1 = ""
    address2 = ""
    city = ""
    post_code = ""
    country = ""
    phone = ""
    late_charge = 0.00
    order_items = []

    def __init__(self, total_price=0.00):
        self.total_price = total_price

    def as_dict(self):   
        output = {}

        output_column = ['total_price', 'firstname', 'lastname', 'email', 'address1', 'address2', 'city', 'post_code', 'country', 'phone', 'late_charge', 'order_items']

        for column in output_column:
            output[column] = getattr(self, column)
            # check if the column value is a list of objects
            if isinstance(output[column], list):
                output[column] = [item.as_dict() for item in output[column]]
                continue
            # check if the column is a single object
            if hasattr(output[column], 'as_dict'):
                output[column] = output[column].as_dict()
                continue
            # convert the item to string if it is not sql object
            output[column] = str(output[column])
        
        return output
