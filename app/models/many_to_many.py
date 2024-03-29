from app.helpers.app_context import AppContext as AC

db = AC().db

product_order = db.Table('product_order',
                    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                    db.Column('order_id', db.Integer, db.ForeignKey('order.id'))
                    )
order_item_detail = db.Table('order_item_detail',
                    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
                    db.Column('order_item_id', db.Integer, db.ForeignKey('order_item.id'))
                    )
                    
voucher_order = db.Table('voucher_order',
                    db.Column('voucher_id', db.Integer, db.ForeignKey('voucher.id')),
                    db.Column('order_id', db.Integer, db.ForeignKey('order.id'))                                      
                    )
user_voucher = db.Table('user_voucher',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('voucher_id', db.Integer, db.ForeignKey('voucher.id'))                    
                    )