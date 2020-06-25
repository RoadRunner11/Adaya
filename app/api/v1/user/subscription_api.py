from app.models import Product, Variation, ProductVariations, User, SubscriptionType, UserSubscription, UserSubscriptionDetail, ConfigValues
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from app.decorators.authorisation import user_only
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

@api_v1.route('/subscribe', methods=['POST'])
#@user_only
# this not a needed api as subscription is now done through the payment api
def user_subscribe():
    json_dict = request.json
    email = json_dict['email']
    user = User.get_user_by_email(email)
    if not user:
        return Responses.NOT_EXIST()
    if not user.email_confirmed:
        return Responses.UNCONFIRMED_USER()
    
    subscription_type = json_dict['subscription_type']
    subscription = SubscriptionType.get_items(plan=subscription_type)[0]
    subscription_price = subscription.price

    start_date=date.today()
    end_date = start_date + relativedelta(months=1)
    user_subscription_detail = UserSubscriptionDetail(start_date, end_date, subscription.plan, subscription_price)
    
    return res(user_subscription_detail.as_dict())


@api_v1.route('/subscribe/<int:id>', methods=['GET'])
#@user_only
def get_user_subscription(id=None):
    """
    get_subscriptions gets all user subscriptions
    
    """  
    item =  UserSubscription.get_subscription(user_id=id)
    response={}
    if(len(item)>0):
        response = item[0]

    return res(response.as_dict())


@api_v1.route('/subscribe/confirm/<token>')
#@user_only
def confirm_user_subscription(token):
    secret_key = ConfigValues.get_config_value('EMAIL_PASSWORD_RESET_SECRET_KEY')

    confirm_serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = confirm_serializer.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return Responses.TOKEN_EXPIRED()
    json_dict = request.json
    email = json_dict['email']
    user = User.get_user_by_email(email)
    if not user:
        return Responses.NOT_EXIST()
    
    subscription_type = json_dict['subscription_type']
    subscription = SubscriptionType.get_items(subscription_type)

    start_date=date.today()
    end_date = start_date + relativedelta(months=int(1))
    #end_date = start_date + relativedelta(months=int(subscription.plan))

    user_subscription = UserSubscription(user.id,end_date,subscription.id)
    error = user_subscription.update()
    if len(error) > 0:
        Responses.OPERATION_FAILED()

    user.subscribed = True
    user_error = user.update()
    if len(user_error) > 0:
        Responses.OPERATION_FAILED()
    return Responses.SUCCESS()