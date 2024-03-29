import pytest
from app.helpers.app_context import AppContext as AC
from app.helpers.utility import randomString
from app.models import (User, Role, Product, ProductCategory, Article, ArticleCategory, 
ArticleStatus, OrderStatus, Order, OrderItem, ConfigValues, Voucher, Variation, SubscriptionType, UserSubscription)
import random
from random import randint
import string
from app.helpers.utility import res
from datetime import datetime
from app import create_app
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from flask_jwt_extended import jwt_required, get_jwt_identity
import flask


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('config.test')
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()

@pytest.fixture(scope='module')
def admins_user():
    user = User()
    user.email = 'abc@gmail.com'
    user.password = '1q2w3e4r'
    user.role_id = 2
    admin = Role("admin")
    user.role = admin
    user.email_confirmed = 'True'
    return user

@pytest.fixture(scope='module')
def init_database():
    db = AC().db
    # Create the database and the database table
    db.create_all()
    member = Role("member")
    admin = Role("admin")
    user = User("abc@gmail.com", "1q2w3e4r")
    user.email_confirmed = True
    user2 = User("abcd@gmail.com", "1q2w3e4r")
    user3 = User("abcd3@gmail.com", "1q2w3e4r")
    user4 = User("abcd4@gmail.com", "1q2w3e4r")
    user.role = admin
    user2.email_confirmed = True
    user2.subscribed=True
    user3.email_confirmed = True
    user3.subscribed = True
    user4.email_confirmed = False
    max_no_products_per_month = ConfigValues('max_no_products_per_month', 20)
    max_no_free_products_adayalite_user = ConfigValues('max_no_free_products_adayalite_user', 4)
    max_no_of_items_per_order_adayalifestyle = ConfigValues('max_no_of_items_per_order_adayalifestyle', 4)
    max_no_products_per_order = ConfigValues('max_no_products_per_order', 4)
    min_duration_of_rental = ConfigValues('min_duration_of_rental', 4)
    max_duration_of_rental = ConfigValues('max_duration_of_rental', 7)
    max_no_of_vouchers = ConfigValues('max_no_of_vouchers', 2)
    MAIL_USERNAME = ConfigValues('MAIL_USERNAME', 'adayahouseshop@gmail.com')
    MAIL_PASSWORD = ConfigValues('MAIL_PASSWORD', 'adaya1234')
    MAIL_SERVER = ConfigValues('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = ConfigValues('MAIL_PORT', 465)
    MAIL_DEFAULT_SENDER = ConfigValues('MAIL_DEFAULT_SENDER', 'adayahouseshop@gmail.com')
    EMAIL_PASSWORD_RESET_SECRET_KEY = ConfigValues('EMAIL_PASSWORD_RESET_SECRET_KEY', 'Thisisasecret!')
    SIB_KEY = ConfigValues('SIB_KEY', 'gzryVUPZHa1GW7n6')
    subtype = SubscriptionType(plan='Adaya Lite', price=10)
    subtype2 = SubscriptionType(plan='Adaya Premium', price=40)
    usersubscription = UserSubscription()
    usersubscription.user_id=2
    usersubscription.current_start_date=datetime.now()
    usersubscription.current_end_date=datetime.strptime('2020-09-06 05:58:00', '%Y-%m-%d %H:%M:%S')
    usersubscription.subscription_type=subtype
    usersubscription2 = UserSubscription()
    usersubscription2.user_id=3
    usersubscription2.current_start_date=datetime.now()
    usersubscription2.current_end_date=datetime.strptime('2020-08-06 05:58:00', '%Y-%m-%d %H:%M:%S')
    usersubscription2.subscription_type=subtype2
    voucher = Voucher('HAO20')
    voucher.discount_fixed_amount = 100
    voucher.product_id = 3    
    voucher.redeem_by = datetime.strptime('2020-8-13 00:00:00', '%Y-%m-%d %H:%M:%S')
    voucher2 = Voucher('LUO20')
    voucher2.discount_fixed_amount = 8.00
    voucher2.product_id = 1    
    voucher2.redeem_by = datetime.strptime('2020-8-13 00:00:00', '%Y-%m-%d %H:%M:%S')
    for x in range(1, 11):
            variation = Variation('S')
            variation.product_id = x
            variation.price = 10
            variation.stock = 1
            variation1 = Variation('M')
            variation1.product_id = x
            variation1.price = 20
            variation1.stock = 1
            variation2 = Variation('L')
            variation2.product_id = x
            variation2.price = 30
            variation2.stock = 1
            variation3 = Variation('XL')
            variation3.product_id = x
            variation3.price = 40
            variation3.stock = 1
            db.session.add(variation)
            db.session.add(variation1)
            db.session.add(variation2)
            db.session.add(variation3)    
    db.session.add(max_no_products_per_order)
    db.session.add(max_no_products_per_month)
    db.session.add(max_no_free_products_adayalite_user)
    db.session.add(max_no_of_items_per_order_adayalifestyle)
    db.session.add(min_duration_of_rental)
    db.session.add(max_duration_of_rental)
    db.session.add(max_no_of_vouchers)
    db.session.add(MAIL_USERNAME)
    db.session.add(MAIL_PASSWORD)
    db.session.add(MAIL_SERVER)
    db.session.add(MAIL_PORT)
    db.session.add(MAIL_DEFAULT_SENDER)
    db.session.add(EMAIL_PASSWORD_RESET_SECRET_KEY)
    db.session.add(SIB_KEY)
    db.session.add(voucher)
    db.session.add(voucher2)
    db.session.add(member)
    db.session.add(user)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(subtype)
    db.session.add(subtype2)
    db.session.add(usersubscription)
    db.session.add(usersubscription2)
    food_category = ProductCategory('food')
    clothes_category = ProductCategory('cloth')
    food_article = ArticleCategory('food-article')
    clothes_article = ArticleCategory('cloth-article')
    status = ArticleStatus('draft')
    order_status = OrderStatus('completed')
    db.session.add(order_status)
    db.session.add(food_article)
    db.session.add(clothes_article)
    db.session.add(food_category)
    db.session.add(clothes_category)    
    for x in range(10):
        product = Product('Haoluo')       
        article = Article(randomString(10))
        order = Order()
        order_item = OrderItem()
        order_item.quantity = 1
        order_item.variation_id = 2
        order_item.start_date = datetime.strptime('2020-4-1 00:00:00', '%Y-%m-%d %H:%M:%S')
        order_item.end_date = datetime.strptime('2020-4-8 00:00:00', '%Y-%m-%d %H:%M:%S')
        order.order_items = []
        order.order_items.append(order_item)
        article_category = food_article
        category = food_category
        if x % 2 == 0:
            category = clothes_category
            article_category = clothes_article
        product.category = category
        article.category = article_category
        article.status = status
        db.session.add(order)
        db.session.add(product)
        db.session.add(order_item)
        db.session.add(article)
    db.session.commit()
    yield db
    db.drop_all()
