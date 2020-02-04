from app import create_app
from app.helpers.app_context import AppContext as AC
from app.models import (User, Role, Product, ProductCategory,Article, ArticleCategory, 
ArticleStatus,OrderStatus,Order, OrderItem ,ConfigValues, Voucher, Variation, SubscriptionType, UserSubscription)
import random
from random import randint
import string
from datetime import datetime

db = AC().db


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


if __name__ == "__main__":
    app = create_app("config.dev")  # start app with config
    with app.app_context():
        db.drop_all()
        db.create_all()
        member = Role("member")
        admin = Role("admin")
        user = User("abc@gmail.com", "1q2w3e4r")
        user2 = User("abcd@gmail.com", "1q2w3e4r")
        user.role = admin
        configvalues = ConfigValues('max_no_products_per_order', 4)
        configvalues2 = ConfigValues('min_duration_of_rental', 4)
        configvalues3 = ConfigValues('max_duration_of_rental', 7)
        configvalues4 = ConfigValues('max_no_of_vouchers', 2)
        configvalues5 = ConfigValues('MAIL_USERNAME', 'adayahouseshop@gmail.com')
        configvalues6 = ConfigValues('MAIL_PASSWORD', 'adaya1234')
        configvalues7 = ConfigValues('MAIL_SERVER', 'smtp.gmail.com')
        configvalues8 = ConfigValues('MAIL_PORT', 465)
        configvalues9 = ConfigValues('MAIL_DEFAULT_SENDER', 'adayahouseshop@gmail.com')
        configvalues10 = ConfigValues('EMAIL_PASSWORD_RESET_SECRET_KEY', 'Thisisasecret!')
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
        voucher = Voucher('HAO20')
        voucher.discount_fixed_amount = 5
        voucher.product_id = 3
        voucher.redeem_by = datetime.strptime('13-4-2020', '%d-%m-%Y')
        voucher2 = Voucher('LUO20')
        voucher2.discount_fixed_amount = 20
        voucher2.product_id = 5
        voucher2.redeem_by = datetime.strptime('18-4-2020', '%d-%m-%Y')
        subscription_type = SubscriptionType(1, 10.00)
        subscription_type2 = SubscriptionType(6, 59.99)
        subscription_type3 = SubscriptionType(12, 99.00)
        db.session.add(subscription_type)
        db.session.add(subscription_type2)
        db.session.add(subscription_type3)
        db.session.add(configvalues)
        db.session.add(configvalues2)
        db.session.add(configvalues3)
        db.session.add(configvalues4)
        db.session.add(configvalues5)
        db.session.add(configvalues6)
        db.session.add(configvalues7)
        db.session.add(configvalues8)
        db.session.add(configvalues9)
        db.session.add(configvalues10)
        db.session.add(member)
        db.session.add(user)
        db.session.add(user2)
        db.session.add(voucher)
        db.session.add(voucher2)
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
            product = Product(randomString(10))            
            article = Article(randomString(10))
            order = Order()
            order_item = OrderItem()
            order_item.quantity = 1
            order_item.start_date = datetime.strptime('1-4-2020', '%d-%m-%Y')
            order_item.end_date = datetime.strptime('8-4-2020', '%d-%m-%Y')
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
