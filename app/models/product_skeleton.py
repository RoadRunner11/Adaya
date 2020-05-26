from app.models.order import Order
from app.models import Product

class ProductSkeleton(object):
    name = ""
    image = ""

    def __init__(self, name=None):
        self.name = name

    def as_dict(self):   
        output = {}

        output_column = ['name', 'image']

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
