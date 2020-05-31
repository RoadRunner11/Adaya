class Order_Item_With_Product(object):
    quantity = 0
    start_date = None
    end_date = None
    variation_id = 0 
    product = None
    days_returned_late = 0

    def __init__(self, quantity, start_date, end_date, variation_id, days_returned_late=0):
        self.quantity = quantity
        self.start_date = start_date
        self.end_date = end_date
        self.variation_id = variation_id 
        self.days_returned_late = days_returned_late
    
    def as_dict(self):   
        output = {}

        output_column = ['product', 'quantity', 'variation_id', 'start_date', 'end_date', 'days_returned_late']

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