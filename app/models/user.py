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
    token = db.Column(db.String(255))
    salt = db.Column(db.String(255), nullable=False)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=1)
    role = db.relationship('Role')
    articles = db.relationship('Article', lazy='dynamic')
    orders = db.relationship('Order', lazy='dynamic')

    new_item_must_have_column=['email','password']
    output_column = ['id', 'email', 'firstname', 'lastname', 'address1',
                     'address2', 'city', 'post_code', 'country', 'phone', 'enabled', 'role.name', 'role.id']
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
        access_key = ConfigValues.get_config_value('SIB_KEY')
        m = Mailin("https://api.sendinblue.com/v2.0", access_key)
        
        inner_to = {}
        inner_to[user_email] = user_email
        data = {"from" : ["adayahouse@gmail.com", "from email!"],
            "subject" : "Adaya Email Confirmation",
        }
        data['to'] = inner_to
        data['html'] = """Your account on Adaya was successfully created.
                <br>Please click <a href={{confirm_url}} target=\"_blank\">here</a> to confirm your email address and activate your account """
        
        m.send_email(data)

    def send_password_reset_email(self, user_email): 
        access_key = ConfigValues.get_config_value('SIB_KEY')
        m = Mailin("https://api.sendinblue.com/v2.0", access_key)
        
        inner_to = {}
        inner_to[user_email] = user_email
        data = {"from" : ["adayahouse@gmail.com", "from email!"],
            "subject" : "Adaya -Account Password Reset",
        }
        data['to'] = inner_to
        data['html'] = """We have received your password rest request on Adaya.
            <br><br>Please click <a href={{password_reset_url}} target=\"_blank\">here</a> to reset your password
                <br><br>If this was not you, call 0800111111"""
        
        m.send_email(data)