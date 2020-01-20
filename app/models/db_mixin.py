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
    enabled = db.Column(db.Integer, default=1)
    new_item_must_have_column = []
    output_column = []
    not_updatable_columns = ['id']

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

    def insert_as_new_item(self, obj_dict=None, new_item_must_have_column=[]):
        new_item_must_have_column = new_item_must_have_column if len(
            new_item_must_have_column) > 0 else self.new_item_must_have_column
        for column in new_item_must_have_column:
            if column not in obj_dict:
                return "Missing Attribute: "+str(column)
        return self.update(obj_dict)

    def update(self, obj_dict=None, not_updatable_columns=[], force_insert=False):
        """
        update updates the properties from dictionary and push to the database

        Args:
            obj_dict ([type], optional): [description]. Defaults to None.
            not_updatable_columns (list, optional): [description]. Defaults to [].
            force_insert (bool): force execute insert function even there is no change in the object, defaults to false

        Returns:
            error: will be empty if there is no error
        """
        error = ''
        flag = True
        if obj_dict:
            flag = self.update_from_dict(obj_dict, not_updatable_columns)
        if flag or force_insert:
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
                # resolve the multi level output column such as cateogry.name
                value = self
                for x in range(0, len(column_list)):
                    if hasattr(value, column_list[x]):
                        value = getattr(value, column_list[x])
                    else:
                        value = ''
                        break
                output[column] = value
            else:
                output[column] = getattr(self, column)
            # check if the column value is a list of objects
            if str(type(output[column])) == "<class 'sqlalchemy.orm.collections.InstrumentedList'>":
                output[column] = [item.as_dict() for item in output[column]]
                continue
            # check if the column is a single object
            if hasattr(output[column], 'as_dict'):
                output[column] = output[column].as_dict()
                continue
            # convert the item to string if it is not sql object
            output[column] = str(output[column])
        return output

    @classmethod
    def get(cls, filter_queries=None, page=1, per_page=10, sort_query=None, display_enabled_only=True, error_out=False):
        """
        get default get query

        Args:
            filter_queries (single query or query list, optional): example - [Article.category_id == 1] or Article.category_id == 1
            page (int, optional): which page. Defaults to 1.
            per_page (int, optional): how many items for each return. Defaults to 10.
            order ([type], optional): example db.desc(Post.post_date) or db.asc
            error_out (bool, optional): [description]. Defaults to False.

        Returns:
            [type]: [description]
        """
        query = cls.query.filter(cls.enabled == 1)
        if filter_queries is not None:
            if type(filter_queries) == list:
                for filter_query in filter_queries:
                    query = query.filter(filter_query)
            else:
                query = query.filter(filter_queries)
        if sort_query is not None:
            query = query.order_by(sort_query)
        return query.paginate(page, per_page, error_out).items
