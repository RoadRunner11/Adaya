from app import create_app
from app.helpers.app_context import AppContext as AC
from app.models import User, Role, Product, ProductCategory, Article, ArticleCategory, ArticleStatus,OrderStatus,Order
import random
import string

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
