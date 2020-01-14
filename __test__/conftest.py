import pytest
from app.helpers.app_context import AppContext as AC
from app.helpers.utility import randomString
from app.models import User, Role, Product, ProductCategory, Article, ArticleCategory, ArticleStatus, OrderStatus, Order, ConfigValues, Voucher
import random
import string
import datetime
from app import create_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('config.test')
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    db = AC().db
    # Create the database and the database table
    db.create_all()
    member = Role("member")
    admin = Role("admin")
    user = User("abc@gmail.com", "1q2w3e4r")
    user2 = User("abcd@gmail.com", "1q2w3e4r")
    user.role = admin
    configvalues = ConfigValues('max_no_products_per_order', 4)
    voucher = Voucher('HAO20')
    voucher.discount_fixed_amount = 100
    voucher.product_id = 3    
    voucher.redeem_by = datetime.date(2020, 4, 13)
    db.session.add(configvalues)
    db.session.add(voucher)
    db.session.add(member)
    db.session.add(user)
    db.session.add(user2)
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
        product.price = 100
        article = Article(randomString(10))
        order = Order()
        order.products = []
        order.products.append(product)
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
        db.session.add(article)
    db.session.commit()
    yield db
    db.drop_all()
