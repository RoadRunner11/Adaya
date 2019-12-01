from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
from app.models.role import Role

db = AC().db


class User(db.Model, DBMixin):
    __tablename__ = 'user'
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(255))
    post_code = db.Column(db.String(255))
    country = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    enabled = db.Column(db.Integer, default=1)
    token = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=1)
    role = db.relationship('Role')
    articles = db.relationship('Article', backref='user', lazy='dynamic')
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    output_column = ['id', 'email', 'firstname', 'lastname', 'address1',
                     'address2', 'city', 'post_code', 'country', 'phone', 'enabled', 'role.name']
    not_updatable_columns = ['id']

    def __init__(self, email=' ', password=' '):
        '''
        __init__ initiates the user as well as hashing the password by using bcrypt

        Args:
            email (string): [description]
            password (string): [description]
        '''
        self.email = email
        self.password = AC().bcrypt.generate_password_hash(password)

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
                if hasattr(self, key):
                    if key in not_updatable_columns:
                        continue
                    if key == 'password':
                        setattr(self, key, AC().bcrypt.generate_password_hash(
                            obj_dict[key]))
                    else:
                        setattr(self, key, obj_dict[key])
                    flag = True
        return flag

    @classmethod
    def get_user_by_email(cls, email, valid_only=True, page=None, per_page=None):
        query = User.email == email
        users = cls.get(query, page, per_page)
        if len(users) > 0:
            user = users[0]
            if valid_only:
                if user.enabled:
                    return user
            return user
        return None

    @classmethod
    def get_users_by_role(cls, role, page=None, per_page=None):
        # How to filter by roles
        query = User.role.has(Role.name == role)
        return cls.get(query, page, per_page)

    @staticmethod
    def authenticate(email, password):
        """
        authenticate verifies user's password

        Args:
            email (string): [description]
            password (string): [description]

        Returns:
            User: user object
        """
        user = User.get_user_by_email(email)
        if user and user and AC().bcrypt.check_password_hash(user.password, password):
            return user
        return None

    @staticmethod
    def authorisation(email, permitted_roles):
        """
        authorisation verifies user's role without checking user's password

        Args:
            email (string): [description]
            permitted_roles ([string]): [description]

        Returns:
            boolean: does user have permission
        """
        user = User.get_user_by_email(email)
        if user and user.role.name in permitted_roles:
            return True
        return False
