from app.models.variation import Variation
from app.models import Product

class ProductVariations(object):
    product = None
    variations = []

    def __init__(self, product=None):
        self.product = product

    def as_dict(self):   
        output = {}

        output_column = ['product', 'variations']

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
