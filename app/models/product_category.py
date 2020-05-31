from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class ProductCategory(db.Model, DBMixin):
    __tablename__ = 'product_category'

    name = db.Column(db.String(255), nullable=False)
    products = db.relationship('Product', lazy='dynamic')

    output_column = ['id', 'name', 'enabled']

    def __init__(self, name=' '):
        self.name = name

    @classmethod
    def get_items(cls, name=None, page=None, per_page=None):
        """
        get_items

        Args:
            name (string, optional): [description]. Defaults to None.
            page (int, optional): [description]. Defaults to None.
            per_page (int, optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        filter_query = None
        if name != None:
            filter_query = cls.name == name
        return cls.get(filter_query, page, per_page)
    
    @classmethod
    def get_category_from_name(cls, name):
        return ProductCategory.query.filter_by(name = name).all()
