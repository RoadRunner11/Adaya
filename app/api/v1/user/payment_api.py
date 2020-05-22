import stripe
import json
import os
from flask import Flask, render_template, jsonify, request, send_from_directory, url_for
from app.models import Product, Variation, ProductVariations, User, Payment
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

@api_v1.route('/create-payment-intent', methods=['POST'])
#@user_only
def create_customer_intent():
    json_dict = request.json
    user_id = json_dict['user_id']
    #total_price = json_dict['total_price']
    total_price = '85.9'
    publishable_key = 'pk_test_wfEV385fd15MX1lKUFsPpG1F00EVVb5Dl7'
    #secret_key = 'sk_test_Fp5a2iT7YRDCEckASE3ExS5q004e2IXvcs'
    stripe.api_key = "sk_test_Fp5a2iT7YRDCEckASE3ExS5q004e2IXvcs"
    
    user = User.query.get(user_id)
    if not user.stripe_customer_id:
        s_customer = stripe.Customer.create()
        sid = s_customer['id']
        user.update({"stripe_customer_id": sid})

    user_stripe_id = user.stripe_customer_id
    stripe_total_price = int (float(total_price) * 100) #amount to stripe has to be integer so convert to smallest currency unit

    intent = stripe.PaymentIntent.create(
        amount=stripe_total_price,
        currency='gbp',
        customer=user_stripe_id, 
        setup_future_usage='off_session',
    )
    #print(intent)
    try:
    # Send publishable key and PaymentIntent details to client
        response = jsonify({'publicKey': publishable_key, 'clientSecret': intent.client_secret, 'id': intent.id})
        return response.json
    except Exception as e:
        return jsonify(error=str(e)), 403
    
    #return generate_response(intent)

@api_v1.route('/create-customer', methods=['POST'])
#@user_only
def create_customer_for_subscription():
    json_dict = request.json
    user_id = json_dict['user_id']
    #subscription_price =  SubscriptionType.get_items(plan=plan)[0]
    publishable_key = 'pk_test_wfEV385fd15MX1lKUFsPpG1F00EVVb5Dl7'
    #secret_key = 'sk_test_Fp5a2iT7YRDCEckASE3ExS5q004e2IXvcs'
    stripe.api_key = "sk_test_Fp5a2iT7YRDCEckASE3ExS5q004e2IXvcs"
    
    user = User.query.get(user_id)
    if not user.stripe_customer_id:
        s_customer = stripe.Customer.create()
        sid = s_customer['id']
        user.update({"stripe_customer_id": sid})

    user_stripe_id = user.stripe_customer_id
    
    try:
    # Send publishable key and PaymentIntent details to client
        response = jsonify({'customerId': user_stripe_id})
        return response.json
    except Exception as e:
        return jsonify(error=str(e)), 403

@api_v1.route('/create-subscription', methods=['POST'])
#@user_only
def create_subscription():
    json_dict = request.json
    try:
        stripe.PaymentMethod.attach(
            json_dict['paymentMethodId'],
            customer=json_dict['customer_id'],
        )
        # Set the default payment method on the customer
        stripe.Customer.modify(
            json_dict['customerId'],
            invoice_settings={
                'default_payment_method': json_dict['paymentMethodId'],
            },
        )
         #subscription_price =  SubscriptionType.get_items(plan=plan)[0]

        # Create the subscription
        subscription = stripe.Subscription.create(
            customer=json_dict['customerId'],
            items=[
                {
                    'price': 9900 #subscription_price
                }
            ],
            expand=['latest_invoice.payment_intent'],
        )
        return jsonify(subscription).json
    except Exception as e:
        return jsonify(error={'message': str(e)}), 200


@api_v1.route('/late-payment', methods=['POST'])
@api_v1.route('/late-payment/<int:id>', methods=['POST'])
#@user_only
def charge_customer_offline():
    json_dict = request.json
    user_id = json_dict['user_id']
    number_days_late = json_dict['number_days_late']
    charge_per_day = 1000 #10GBP
    publishable_key = 'pk_test_wfEV385fd15MX1lKUFsPpG1F00EVVb5Dl7'
    
    user = User.query.get(user_id)
    if not user.stripe_customer_id:
        return Responses.OPERATION_FAILED()

    user_stripe_id = user.stripe_customer_id

    try:
        # List the customer's payment methods to find one to charge
        payment_methods = stripe.PaymentMethod.list(
            customer = user_stripe_id,
            type='card'
        )
        # Create and confirm a PaymentIntent with the
        # order amount, currency, Customer and PaymentMethod IDs
        # If authentication is required or the card is declined, Stripe
        # will throw an error
        intent = stripe.PaymentIntent.create(
            amount=charge_per_day * number_days_late,
            currency='gbp',
            payment_method=payment_methods['data'][0]['id'],
            customer=user_stripe_id,
            confirm=True,
            off_session=True
        )

        responseObject =  jsonify({
            'succeeded': True, 
            'publicKey': publishable_key, 
            'clientSecret': intent.client_secret
        })

        return responseObject.json

    except stripe.error.CardError as e:
        err = e.error
        if err.code == 'authentication_required':
            # Bring the customer back on-session to authenticate the purchase
            # You can do this by sending an email or app notification to let them know
            # the off-session purchase failed
            # Use the PM ID and client_secret to authenticate the purchase
            # without asking your customers to re-enter their details

            Payment.send_payment_request_authorisation_email(user.email)

            return jsonify({
                'error': 'authentication_required', 
                'paymentMethod': err.payment_method.id, 
                'amount': charge_per_day * number_days_late,
                'card': err.payment_method.card, 
                'publicKey': publishable_key, 
                'clientSecret': err.payment_intent.client_secret
            }).json
        elif err.code:
            # The card was declined for other reasons (e.g. insufficient funds)
            # Bring the customer back on-session to ask them for a new payment method
            return jsonify({
                'error': err.code, 
                'publicKey': charge_per_day * number_days_late, 
                'clientSecret': err.payment_intent.client_secret
            }).json

def generate_response(intent):
    status = intent['status']
    if status == 'requires_action' or status == 'requires_source_action':
        # Card requires authentication
        return jsonify({'requiresAction': True, 'paymentIntentId': intent['id'], 'clientSecret': intent['client_secret']})
    elif status == 'requires_payment_method' or status == 'requires_source':
        # Card was not properly authenticated, suggest a new payment method
        return jsonify({'error': 'Your card was denied, please provide a new payment method'})
    elif status == 'succeeded':
        # Payment is complete, authentication not required
        # To cancel the payment after capture you will need to issue a Refund (https://stripe.com/docs/api/refunds)
        print("💰 Payment received!")
        return jsonify({'clientSecret': intent['client_secret']})
