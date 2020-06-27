import stripe
import json
import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory, url_for
from app.models import Product, Variation, ProductVariations, User, Payment, SubscriptionType, UserSubscription, Order, OrderItem, ConfigValues
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
    item = Order()
    item.user_id = json_dict['user_id']
    
    order_items_dict = json_dict['order_items']
    for order_item_dict in order_items_dict:
        order_item = OrderItem()
        if order_item.update_from_dict(order_item_dict):
            item.order_items.append(order_item)
    
    item.update_from_dict(json_dict)
    calculated_details = Order.calculate_cost_for_users(item)
    total_price = float(calculated_details['total_cost'])
    user_id = json_dict['user_id']
    
    publishable_key = ConfigValues.get_config_value('STRIPE_PK')
    stripe.api_key =  ConfigValues.get_config_value('STRIPE_SK') 
    
    user = User.query.get(user_id)
    if not user.stripe_customer_id or len(user.stripe_customer_id) < 1:
        s_customer = stripe.Customer.create(email=user.email, name=user.firstname)
        sid = s_customer['id']
        user.update({"stripe_customer_id": sid})

    user_stripe_id = user.stripe_customer_id
    stripe_total_price = int (total_price * 100) #amount to stripe has to be integer so convert to smallest currency unit

    intent = stripe.PaymentIntent.create(
        amount=stripe_total_price,
        currency='gbp',
        customer=user_stripe_id, 
        setup_future_usage='off_session',
        receipt_email=user.email
    )
    try:
    # Send publishable key and PaymentIntent details to client
        response = jsonify({'publicKey': publishable_key, 'clientSecret': intent.client_secret, 'id': intent.id})
        return response.json
    except Exception as e:
        return jsonify(error=str(e)), 403
    
    #return generate_response(intent)

@api_v1.route('/create-payment-intent-late-fee', methods=['POST'])
#@user_only
def create_customer_intent_late_payment():
    json_dict = request.json
    user_id = json_dict['user_id']
    total_price = float(json_dict['late_fee_total_price'])

    publishable_key = ConfigValues.get_config_value('STRIPE_PK')
    stripe.api_key =  ConfigValues.get_config_value('STRIPE_SK') 
    
    user = User.query.get(user_id)
    if not user.stripe_customer_id or len(user.stripe_customer_id) < 1:
        s_customer = stripe.Customer.create(email=user.email, name=user.firstname)
        sid = s_customer['id']
        user.update({"stripe_customer_id": sid})

    user_stripe_id = user.stripe_customer_id
    stripe_total_price = int (total_price * 100) #amount to stripe has to be integer so convert to smallest currency unit

    intent = stripe.PaymentIntent.create(
        amount=stripe_total_price,
        currency='gbp',
        customer=user_stripe_id, 
        setup_future_usage='off_session',
        receipt_email=user.email
    )
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
    stripe.api_key =  ConfigValues.get_config_value('STRIPE_SK')
    
    user = User.query.get(user_id)
    if not user.stripe_customer_id:
        s_customer = stripe.Customer.create(email=user.email, name=user.firstname)
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
    subscription_type = json_dict['subscription_type']
    subType = SubscriptionType.get_items(plan=subscription_type)
    subscriptionType = {}
    if(len(subType) > 0):
        subscriptionType = subType[0]
    subscription_type_id = subscriptionType.id
    subscription_price = subscriptionType.stripe_price

    user_id = json_dict['user_id']
    user = User.query.get(user_id)

    try:
        stripe.PaymentMethod.attach(
            json_dict['paymentMethodId'],
            customer=json_dict['customer_id'],
        )
        # Set the default payment method on the customer
        stripe.Customer.modify(json_dict['customer_id'], invoice_settings={
                'default_payment_method': json_dict['paymentMethodId'],
            }, email=user.email, name=user.firstname
        )
       
        # Create the subscription
        subscription = stripe.Subscription.create(
            customer=json_dict['customer_id'],
            items=[
                {
                    'price': subscription_price
                }
            ],
            expand=['latest_invoice.payment_intent'],
        )
        print("Subscription object")
        print(subscription)
        print("Subscription object invoice")
        print(subscription.latest_invoice.payment_intent.status)
        
        user_subscription_dict = {}
        if(subscription.latest_invoice.payment_intent.status == 'succeeded'):
            subscription_dict = jsonify(subscription).json
            user_subscription_dict['user_id'] = json_dict['user_id']
            user_subscription_dict['subscription_id'] = subscription_dict['id']
            user_subscription_dict['subscription_type_id'] = subscription_type_id
            s_date = datetime.fromtimestamp(subscription_dict['current_period_start'])
            user_subscription_dict['current_start_date'] = s_date
            e_date = datetime.fromtimestamp(subscription_dict['current_period_end'])
            user_subscription_dict['current_end_date'] = e_date
            user_subscription_dict['type_object'] = subscription_dict['object']
            user_subscription_dict['application_fee_percent'] = subscription_dict['application_fee_percent']
            user_subscription_dict['billing_cycle_anchor'] = subscription_dict['billing_cycle_anchor']
            user_subscription_dict['billing_thresholds'] = subscription_dict['billing_thresholds']
            user_subscription_dict['cancel_at'] = subscription_dict['cancel_at']
            user_subscription_dict['cancel_at_period_end'] = subscription_dict['cancel_at_period_end']
            user_subscription_dict['canceled_at'] = subscription_dict['canceled_at']
            user_subscription_dict['collection_method'] = subscription_dict['collection_method']
            
            userSubscription = UserSubscription.get_subscription(user_id=user_id)
            if len(userSubscription) > 0:
                userSubscription[0].update(user_subscription_dict)
            else:
                newUserSubscription = UserSubscription()
                newUserSubscription.update(user_subscription_dict)
            user.update({'subscribed':1})

        start_date = userSubscription.current_start_date.strftime('%Y-%m-%d %H:%M:%S')
        if subscriptionType.plan == 'Adaya Lite': #adayalite
            Payment.send_subscription_confirmation_email_adayalite(user_email=user.email, user_name=user.firstname, subscription_start=start_date)
        if subscriptionType.plan == 'Adaya Lifestyle': #adayalifestyle
            Payment.send_subscription_confirmation_email_adayalifestyle(user_email=user.email, user_name=user.firstname, subscription_start=start_date)
        
        return jsonify(subscription).json

    except Exception as e:
        return jsonify(error={'message': str(e)}), 200


@api_v1.route('/cancel-subscription', methods=['POST'])
def cancel_subscription():
    json_dict = request.json
    user_id = json_dict['user_id']
    userSub = UserSubscription.get_subscription(user_id=user_id)
    userSubscription = {}
    if len(userSub) > 0:
        userSubscription = userSub[0]
    subscriptionId = userSubscription.subscription_id
    user = User.query.get(user_id)

    stripe.api_key =  ConfigValues.get_config_value('STRIPE_SK')

    try:
         # Cancel the subscription by deleting it
        deletedSubscription = stripe.Subscription.delete(subscriptionId)
        print(deletedSubscription)
        
        user_subscription_dict = {}
        
        user_subscription_dict['user_id'] = user.id
        user_subscription_dict['subscription_id'] = deletedSubscription['id']
        user_subscription_dict['subscription_type_id'] = userSubscription.subscription_type_id
        s_date = datetime.fromtimestamp(deletedSubscription['current_period_start'])
        user_subscription_dict['current_start_date'] = s_date
        e_date = datetime.fromtimestamp(deletedSubscription['current_period_end'])
        user_subscription_dict['current_end_date'] = e_date
        user_subscription_dict['application_fee_percent'] = deletedSubscription['application_fee_percent']
        user_subscription_dict['billing_cycle_anchor'] = deletedSubscription['billing_cycle_anchor']
        user_subscription_dict['billing_thresholds'] = deletedSubscription['billing_thresholds']
        user_subscription_dict['cancel_at'] = deletedSubscription['cancel_at']
        user_subscription_dict['cancel_at_period_end'] = deletedSubscription['cancel_at_period_end']
        ca_date = datetime.fromtimestamp(deletedSubscription['canceled_at'])
        user_subscription_dict['canceled_at'] = ca_date
        user_subscription_dict['collection_method'] = deletedSubscription['collection_method']
       
        userSubscription.update(user_subscription_dict)
        Payment.send_subscription_cancelled_email(user_email=user.email)

        if datetime.now() > userSubscription.current_end_date:  # else, there is another check when user makes an order and sets to 0 if it fails this validation
            user.update({'subscribed':0})
           

        return jsonify(deletedSubscription).json
    except Exception as e:
        return jsonify(error=str(e)), 403

@api_v1.route('/late-payment', methods=['POST'])
@api_v1.route('/late-payment/<int:id>', methods=['POST'])
#@user_only
def charge_customer_offline():
    json_dict = request.json
    user_id = json_dict['user_id']
    order_id = json_dict['order_id']
    
    item = Order.query.get(order_id)
    order_items = item.order_items
    total_cost = 0.00
    for order_item in order_items:
        variation = Variation.get_variation_from_id(order_item.variation_id)
        if order_item.days_returned_late > 14:
            total_cost += float(variation.retail_price)
        else:
            total_cost += (0.5 * float(variation.price)) * int(order_item.days_returned_late)
    
    stripe_total_price = int (float(total_cost) * 100)
    
    publishable_key = ConfigValues.get_config_value('STRIPE_PK')
    

    user = User.query.get(user_id)
    if not user.stripe_customer_id:
        return Responses.OPERATION_FAILED()

    user_stripe_id = user.stripe_customer_id
    stripe.api_key =  ConfigValues.get_config_value('STRIPE_SK')

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
            amount=stripe_total_price,
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

        order = Order.query.get(order_id)
        order.update({'late_charge': str(total_cost),'late_charge_paid': 1})

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
            order = Order.query.get(order_id)
            order.update({'late_charge': str(total_cost),'late_charge_paid': 0})
            return jsonify({
                'error': 'authentication_required', 
                'paymentMethod': err.payment_method.id, 
                'amount': total_cost,
                'card': err.payment_method.card, 
                'publicKey': publishable_key, 
                'clientSecret': err.payment_intent.client_secret
            }).json
        elif err.code:
            # The card was declined for other reasons (e.g. insufficient funds)
            # Bring the customer back on-session to ask them for a new payment method

            Payment.send_payment_failed_email(user.email)
            order = Order.query.get(order_id)
            order.update({'late_charge': str(total_cost),'late_charge_paid': 0})
            return jsonify({
                'error': err.code, 
                'publicKey': publishable_key, 
                'clientSecret': err.payment_intent.client_secret
            }).json

@api_v1.route('/stripe-webhook', methods=['POST'])
def webhook_received():

    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = ConfigValues.get_config_value('STRIPE_WHS') #"whsec_Z5rqV5EyWqGAcsGVsf1id7kfCk8hQXkI" #os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']

    data_object = data['object']

    if event_type == 'invoice.payment_succeeded':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        print(data)
        sid = request_data['data']['object']['customer']
        user = User.get_user_by_stripe_id(stripe_id=sid)
        email = user.email
        Payment.send_subscription_renewal_success_email(user_email=email)
        userSub = UserSubscription.get_subscription(user_id=user.id)
        userSubscription = {}
        if len(userSub > 0):
            userSubscription = userSub[0]

        user_subscription_dict = {}
        user_subscription_dict['user_id'] = user.id
        user_subscription_dict['subscription_type_id'] = userSubscription.subscription_type_id
        s_date = datetime.fromtimestamp(data['object']['period_start'])
        user_subscription_dict['current_start_date'] = s_date
        e_date = datetime.fromtimestamp(data['object']['period_end'])
        user_subscription_dict['current_end_date'] = e_date

        userSubscription.update(user_subscription_dict)
        user.update({'subscribed': 1, 'number_of_items_ordered_this_month' : 0})

    if event_type == 'invoice.payment_failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        print(data)
        
        sid = request_data['data']['object']['customer']
        user = User.get_user_by_stripe_id(stripe_id=sid)
        email = user.email
        Payment.send_subscription_renewal_failure_email(user_email=email)
                
        userSub = UserSubscription.get_subscription(user_id=user.id)
        userSubscription = {}
        if len(userSub > 0):
            userSubscription = userSub[0]

        user_subscription_dict = {}
        user_subscription_dict['user_id'] = user.id
        user_subscription_dict['subscription_type_id'] = userSubscription.subscription_type_id
        s_date = datetime.fromtimestamp(data['object']['period_start'])
        user_subscription_dict['current_start_date'] = s_date
        e_date = datetime.fromtimestamp(data['object']['period_end'])
        user_subscription_dict['current_end_date'] = e_date

        userSubscription.update(user_subscription_dict)
        user.update({'subscribed': 0, 'number_of_items_ordered_this_month' : 0})

    if event_type == 'invoice.finalized':
        # If you want to manually send out invoices to your customers
        # or store them locally to reference to avoid hitting Stripe rate limits.
        print(data)

    if event_type == 'customer.subscription.deleted':
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        print(data)
        sid = request_data['data']['object']['customer']
        user = User.get_user_by_stripe_id(stripe_id=sid)
        email = user.email
        
        userSub = UserSubscription.get_subscription(user_id=user.id)
        userSubscription = {}
        if len(userSub > 0):
            userSubscription = userSub[0]

        user_subscription_dict = {}
        user_subscription_dict['user_id'] = user.id
        user_subscription_dict['subscription_type_id'] = userSubscription.subscription_type_id
        s_date = datetime.fromtimestamp(data['object']['period_start'])
        user_subscription_dict['current_start_date'] = s_date
        e_date = datetime.fromtimestamp(data['object']['period_end'])
        user_subscription_dict['current_end_date'] = e_date

        userSubscription.update(user_subscription_dict)
        Payment.send_subscription_cancelled_email(user_email=email)
        if datetime.now() > userSubscription.current_end_date:  # else, there is another check when user makes an order and sets to 0 if it fails this validation
            user.update({'subscribed': 0, 'number_of_items_ordered_this_month' : 0})
          

    if event_type == 'customer.subscription.trial_will_end':
        # Send notification to your user that the trial will end
        print(data)

    return jsonify({'status': 'success'})

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
