from app.helpers.app_context import AppContext as AC


db = AC().db


class DBMixin():
    """
    This is a base class for basic DB operations
    """
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.DateTime, server_default=db.func.now())
    modified_time = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    output_column = []
    not_updatable_columns = []

    def insert(self):
        """
        insert adds itself to the database
        """
        error = ''
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            error = str(e)
        return error

    def delete(self):
        """
        delete deletes itself from database
        """
        error = ''
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            error = str(e)
        return error

    def update(self, obj_dict=None, not_updatable_columns=[]):
        """
        update updates the properties from dictionary and push to the database

        Args:
            obj_dict (dict): object dictionary

        Returns:
            bool: updated or not
        """
        error = ''
        flag = True
        if obj_dict:
            flag = self.update_from_dict(obj_dict)
        if flag:
            # update the object in database
            error = self.insert()
        return error

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
                    setattr(self, key, obj_dict[key])
                    flag = True
        return flag

    def as_dict(self, output_column=[]):
        """
        as_dict turns this SQLAlchemy object into dictionary 

        Args:
            output_column ([string], optional): columns for export. Defaults to self.output_column.

        Returns:
            dict: [description]
        """
        output = {}
        # Use self.output_column if no output_column is passed in
        output_column = output_column if len(
            output_column) > 0 else self.output_column
        # Use all columns if self.output_column is empty
        output_column = output_column if len(output_column) > 0 else [
            c.name for c in self.__table__.columns]
        for column in output_column:
            column_list = column.split('.')
            if len(column_list) > 1:
                value = self
                for x in range(0, len(column_list)):
                    if hasattr(value, column_list[x]):
                        value = getattr(value, column_list[x])
                    else:
                        value = ''
                        break
                output[column] = str(value)
                continue
            output[column] = str(getattr(self, column))
        return output

    @classmethod
    def get(cls, query=True, page=1, per_page=10, error_out=False):
        return cls.query.filter(query).paginate(page, per_page, error_out).items
