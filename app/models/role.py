from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class Role(db.Model, DBMixin):
    __tablename__ = 'role'
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', lazy='dynamic')
    
    output_column=['id','name']

    def __init__(self, name):
        self.name = name
