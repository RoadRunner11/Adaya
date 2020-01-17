from app import create_app
from app.helpers.app_context import AppContext as AC
from app.models import (User, Role, Product, ProductCategory,Article, ArticleCategory, 
ArticleStatus,OrderStatus,Order, OrderItems ,ConfigValues, Voucher, Variation)
import random
from random import randint
import string
import datetime

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
        variation = Variation('S')
        variation.price = 10
        variation.stock = 1
        variation1 = Variation('M')
        variation1.price = 20
        variation1.stock = 1
        variation2 = Variation('L')
        variation2.price = 30
        variation2.stock = 1
        variation3 = Variation('XL')
        variation3.price = 40
        variation3.stock = 1
        voucher = Voucher('HAO20')
        voucher.discount_fixed_amount = 5
        voucher.product_id = 3
        voucher.redeem_by = datetime.date(2020, 4, 13)
        db.session.add(configvalues)
        db.session.add(configvalues2)
        db.session.add(configvalues3)
        db.session.add(configvalues4)
        db.session.add(variation)
        db.session.add(variation1)
        db.session.add(variation2)
        db.session.add(variation3)
        db.session.add(member)
        db.session.add(user)
        db.session.add(user2)
        db.session.add(voucher)
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
            product.variation_id = randint(1, 4)
            article = Article(randomString(10))
            order = Order()
            order_item = OrderItems()
            order_item.product_id = product.id
            order_item.quantity = 1
            order_item.start_date = datetime.date(2020, 4, 1)
            order_item.end_date = datetime.date(2020, 4, 8)
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
