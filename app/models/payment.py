import stripe
import json
import os
from flask import Flask, render_template, jsonify, request, send_from_directory, url_for
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
    
    @classmethod
    def send_payment_failed_email(cls, user_email): 
        my_account_link = 'http://localhost:8010/my-account'

        payment_failed_html = render_template('payment_failed.html', my_accountr_url=my_account_link)

        msg = Message('Payment Authentication Needed', sender='adaya@adayahouse.com', recipients=[user_email], html=payment_failed_html)

        mail.send(msg)

    @classmethod
    def send_subscription_renewal_failure_email(cls, user_email):         
        subscription_renewal_failure_html = render_template('subscription_renewal_failure.html')

        msg = Message('Subscription Renewal Failure', sender='adaya@adayahouse.com', recipients=[user_email], html=subscription_renewal_failure_html)

        mail.send(msg)

    @classmethod
    def send_subscription_renewal_success_email(cls, user_email): 
        subscription_renewal_success_html = render_template('subscription_renewal_success.html')

        msg = Message('Subscription Renewed', sender='adaya@adayahouse.com', recipients=[user_email], html=subscription_renewal_success_html)

        mail.send(msg)
    
    @classmethod
    def send_subscription_cancelled_email(cls, user_email): 
        subscription_cancelled_html = render_template('subscription_ended.html')

        msg = Message('Subscription Cancelled', sender='adaya@adayahouse.com', recipients=[user_email], html=subscription_cancelled_html)

        mail.send(msg)
    

    @classmethod
    def send_subscription_confirmation_email_adayalite(cls, user_email, user_name, subscription_start): 
        adayalite_subscription_confirmation_html = render_template('adayalite_subscription_confirmation.html', user_name=user_name, subscription_start=subscription_start)

        msg = Message('Subscription Confirmed', sender='adaya@adayahouse.com', recipients=[user_email], html=adayalite_subscription_confirmation_html)

        mail.send(msg)
    
    @classmethod
    def send_subscription_confirmation_email_adayalifestyle(cls, user_email, user_name, subscription_start): 
        adayalifestyle_subscription_confirmation_html = render_template('adayalifestyle_subscription_confirmation.html', user_name=user_name, subscription_start=subscription_start)

        msg = Message('Subscription Confirmed', sender='adaya@adayahouse.com', recipients=[user_email], html=adayalifestyle_subscription_confirmation_html)

        mail.send(msg)