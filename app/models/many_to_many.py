from app.helpers.app_context import AppContext as AC

db = AC().db

product_order = db.Table('product_order',
                    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                    db.Column('order_id', db.Integer, db.ForeignKey('order.id'))
                    )
