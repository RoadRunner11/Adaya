import stripe
import json
import os
from flask import Flask, render_template, jsonify, request, send_from_directory, url_for
from app.models import Product, Variation, ProductVariations, User
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from app.decorators.authorisation import user_only
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import time
from app import mail
from app.models.config_values import ConfigValues
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from mailin import Mailin

class Payment(object):

    name=""

    
    def __init__(self, product=None):
        self.name = product
       
    @classmethod
    def send_payment_request_authorisation_email(cls, user_email): 
        my_account_link = 'http://localhost:8010/my-account'

        payment_authentication_html = render_template('offline_payment_authentication.html', my_accountr_url=my_account_link)

        msg = Message('Payment Authentication Needed', sender='adaya@adayahouse.com', recipients=[user_email], html=payment_authentication_html)

        mail.send(msg)
