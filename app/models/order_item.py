from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin 
from datetime import datetime

db = AC().db


class OrderItem(db.Model, DBMixin):
    __tablename__ = 'order_item'

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, default=1)
    variation_id = db.Column(db.Integer, db.ForeignKey('variation.id'), default=1)
    quantity = db.Column(db.Integer, default=0)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    days_returned_late = db.Column(db.Integer, default=0)

    variation = db.relationship('Variation')  

    output_column = ['id','order_id', 'quantity', 'variation_id', 'variation.product_id', 'variation.name', 'variation.price', 'start_date', 'end_date', 'days_returned_late']

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
                if hasattr(self, key): 
                    if key == 'start_date':
                        self.start_date = datetime.strptime(obj_dict[key], '%Y-%m-%d %H:%M:%S') 
                        continue  
                    if key == 'end_date':
                        self.end_date = datetime.strptime(obj_dict[key], '%Y-%m-%d %H:%M:%S')    
                        continue   
                    setattr(self, key, obj_dict[key])
                    flag = True
        return flag