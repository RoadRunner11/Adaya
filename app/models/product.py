from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class Product(db.Model, DBMixin):
    __tablename__ = 'product'

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))    
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), default=1)
        
    category = db.relationship('ProductCategory')

    output_column = ['id', 'name', 'description','image', 'category_id', 'category.name', 'enabled']

    def __init__(self, name=' '):
        self.name = name

    @classmethod
    def get_items(cls, category_id=None, page=None, per_page=None, sort_by=None, is_desc=None):
        """
        get_products returns products after applying certain filter queries

        Args:
            category_id ([type], optional): [description]. Defaults to None.
            page ([type], optional): which page. Defaults to None.
            per_page ([type], optional): items per page. Defaults to None.
            sort_by ([type], optional): what column to sort. Defaults to None.
            is_desc ([type], optional): sort desc? (1 or 0). Defaults to None.

        Returns:
            [type]: [description]
        """
        # default sort by time
        sort_query = db.desc(cls.created_time)
        if sort_by != None:
            if sort_by == 'price':
                # only support sorting by price
                sort_query = db.desc(cls.price)
                if not is_desc:
                    sort_query = db.asc(cls.created_time)
        filter_query = None
        if category_id != None:
            filter_query = cls.category_id == category_id
        return cls.get(filter_query, page, per_page, sort_query)
    
    @classmethod
    def get_product_from_id(cls, product_id):
        product = Product.query.get(product_id)
        return product

    @classmethod
    def get_products_from_id(cls, product_ids):        
        if type(product_ids) == list:  
            products = []
            for id in product_ids:
                products.append(Product.get_product_from_id(id))
            return products
        else:
            product = Product.get_product_from_id(product_ids)   
            return product    
