from app.models.variation import Variation

class UserSubscriptionDetail(object):
    start_date = None
    end_date = None 
    subscription_type = " "
    subscription_price = 0.00

    def __init__(self, start_date=None, end_date=None, subscription_type="", subscription_price=0.0):
        self.start_date = start_date
        self.end_date = end_date
        self.subscription_type = subscription_type
        self.subscription_price = subscription_price

    def as_dict(self):   
        output = {}

        output_column = ['start_date', 'end_date', 'subscription_type', 'subscription_price']

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
