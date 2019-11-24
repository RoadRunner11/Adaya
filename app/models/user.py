from app.helper.app_context import AppContext as AC
from app.models.db_mixin import DBMixin

db = AC().db


class User(db.Model, DBMixin):
    __tablename__ = 'user'
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'),default = 1)
    articles = db.relationship('Article', backref='user', lazy='dynamic')
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    output_column=['email','role.name']

    def __init__(self, email, password):
        '''
        __init__ initiates the user as well as hashing the password by using bcrypt
        
        Args:
            email (string): [description]
            password (string): [description]
        '''
        self.email = email
        self.password = AC().bcrypt.generate_password_hash(password)