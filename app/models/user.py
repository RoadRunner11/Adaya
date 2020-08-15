from app.helpers.app_context import AppContext as AC
from app.models.db_mixin import DBMixin
from app.models.role import Role
from app.models.config_values import ConfigValues
from app import mail
import config
import os
from flask import url_for, render_template
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from mailin import Mailin

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
    stripe_customer_id = db.Column(db.String(255))
    token = db.Column(db.String(255))
    salt = db.Column(db.String(255), nullable=False)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    subscribed = db.Column(db.Boolean, nullable=True, default=0)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=1)
    role = db.relationship('Role')
    number_of_items_ordered_this_month = db.Column(db.Integer, default=0)
    month_first_order = db.Column(db.DateTime, nullable=True)
    blacklist = db.Column(db.Boolean, nullable=True, default=0)
    birthday = db.Column(db.String(255))
    occupation = db.Column(db.String(255))
    size = db.Column(db.String(255))
    fav_brands = db.Column(db.String(255))
    instagram_handle = db.Column(db.String(255))
    interest = db.Column(db.String(255))
    style = db.Column(db.String(255))

    articles = db.relationship('Article', lazy='dynamic')
    orders = db.relationship('Order', lazy='dynamic')
    

    new_item_must_have_column=['email','password']
    output_column = ['id', 'email', 'firstname', 'lastname', 'address1',
                     'address2', 'city', 'post_code', 'country', 'phone', 
                     'enabled', 'role.name', 'role.id', 'email_confirmed', 'email_confirmed_on', 
                     'number_of_items_ordered_this_month', 'subscribed','month_first_order', 'blacklist']
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
        self.update_salt()

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
                        self.update_salt()
                    else:
                        setattr(self, key, obj_dict[key])
                    flag = True
        return flag

    def token_identity(self):
        """
        token_identity generates the identify for jwt_extend to generate jwt token

        Returns:
            [string]: [email+salt identity]
        """
        return User.generate_token_identity(self.email, self.salt)

    def update_salt(self):
        """
        update_salt refresh salt
        """
        self.salt = str(os.urandom(30)).replace('\\', '')

    @staticmethod
    def get_email_from_identity(token_identity):
        """
        get_email_from_identity verifies the salt and return the user email

        Args:
            token_identity ([string]): identity from jwt_extend

        Returns:
            [string]: will return None if salt does not match
        """
        email, salt = token_identity.split("||token||")
        user = User.get_user_by_email(email)
        if user.salt != salt:
            return None
        return email

    @classmethod
    def get_user_by_email(cls, email, page=None, per_page=None):
        filter_query = cls.email == email
        users = cls.get(filter_query, page, per_page)
        return users[0] if len(users) > 0 else None

    @classmethod
    def get_user_by_stripe_id(cls, stripe_id, page=None, per_page=None):
        filter_query = cls.stripe_customer_id == stripe_id
        users = cls.get(filter_query, page, per_page)
        return users[0] if len(users) > 0 else None

    @classmethod
    def get_users_by_role(cls, role, page=None, per_page=None):
        # How to filter by roles
        filter_query = cls.role.has(Role.name == role)
        return cls.get(filter_query, page, per_page)

    @staticmethod
    def generate_token_identity(email, salt=None):
        if not salt:
            user = User.get_user_by_email(email)
            salt = user.salt
            if not user:
                return None
        return email+"||token||"+salt

    @staticmethod
    def authenticate(email, password):
        """
        authenticate verifies user's password returns user object

        Args:
            email (string): [description]
            password (string): [description]

        Returns:
            User: user object
        """
        user = User.get_user_by_email(email)
        if user and AC().bcrypt.check_password_hash(user.password, password):
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
        if len(permitted_roles) <= 0:
            # allow all access as permitted roles are empty
            return True
        user = User.get_user_by_email(email)
        if user and user.role.name in permitted_roles:
            return True
        return False
    
    def send_confirmation_email(self, user_email): 
        secret_key = ConfigValues.get_config_value('EMAIL_PASSWORD_RESET_SECRET_KEY')

        confirm_serializer = URLSafeTimedSerializer(secret_key)

        token = confirm_serializer.dumps(user_email, salt='email-confirm')

        confirm_link = url_for('api_v1.confirm_email', token=token, _external=True)

        email_confirmation_html = render_template('email_confirmation.html', confirm_url=confirm_link)

        msg = Message('Confirm Email', sender='adaya@adayahouse.com', recipients=[user_email], html=email_confirmation_html)

        mail.send(msg)

    def send_password_reset_email(self, user_email): 
        secret_key = ConfigValues.get_config_value('EMAIL_PASSWORD_RESET_SECRET_KEY')

        password_reset_serializer = URLSafeTimedSerializer(secret_key)

        token = password_reset_serializer.dumps(user_email, salt='password-reset')

        password_reset_link = url_for('api_v1.password_reset_with_token', token=token, _external=True)

        password_reset_html = render_template('email_password_reset.html', password_reset_url=password_reset_link)

        msg = Message('Password Reset', sender='adaya@adayahouse.com', recipients=[user_email], html=password_reset_html)

        mail.send(msg)
    
    @classmethod
    def contact_us_email(cls, user_email, subject, name, message): 

        contact_us_html = render_template('contact_us.html', name=name, message=message)

        msg = Message(subject, sender=user_email, recipients=["adayahouseshop@gmail.com"], html=contact_us_html)

        mail.send(msg)
    