from app.models.variation import Variation

class ProductVariations(object):
    id = 0
    name = "" 
    description = "" 
    image = "" 
    category_id = 0
    variations = []

    def __init__(self, id=0,name=None, description=None, image=None, category_id=0):
        self.id = id
        self.name = name
        self.description = description
        self.image = image
        self.category_id = category_id

    def as_dict(self):   
        output = {}

        output_column = ['id','name', 'description', 'image', 'category_id', 'variations']

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
