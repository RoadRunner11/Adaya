from app.helper.app_context import AppContext as AC


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

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def as_dict(self, output_column=[]):
        output = {}
        # Use default self.output_column if output_column is empty
        output_column = output_column if len(
            output_column) > 0 else self.output_column
        # Use all columns if self.output_column is empty
        output_column = output_column if len(output_column) > 0 else [
            c.name for c in self.__table__.columns]
        for column in output_column:
            column_list = column.split('.')
            if len(column_list) > 1:
                value  = self
                for x in range(0,len(column_list)):
                    if hasattr(value,column_list[x]):
                        value = getattr(value,column_list[x])
                    else:
                        value = ''
                        break
                output[column] = str(value)
                continue
            output[column] = str(getattr(self, column))
        return output

    @classmethod
    def get(cls, page=1, per_page=10, error_out=False):
        return cls.query.paginate(page, per_page, error_out).items
