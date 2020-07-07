from app.models import Product, User
from app.helpers import Messages, Responses
from app.helpers.app_context import AppContext as AC
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

def test_add_products(test_client, init_database, new_product, new_variation):
    server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
    # get admin user
    user = User.get_user_by_email(email='abc@gmail.com')
    token = create_access_token(identity=user.token_identity())
    test_client.set_cookie(server_name, key='access_token_cookie', value=token)

    response = test_client.post(
        '/connect/products', json={'product': new_product.as_dict(), 'variations':[new_variation.as_dict()]})

    assert response.status_code == 200
    assert response.json['body'] == 'Operation Success'

def test_update_products(test_client, init_database, new_product, new_variation2):
    server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
    # get admin user
    user = User.get_user_by_email(email='abc@gmail.com')
    token = create_access_token(identity=user.token_identity())
    test_client.set_cookie(server_name, key='access_token_cookie', value=token)

    response = test_client.put(
        '/connect/products/5', json={'product': new_product.as_dict(), 'variations':[new_variation2.as_dict()]})

    assert response.status_code == 200
    assert response.json['body'] == 'Operation Success'

def test_get_products(test_client, init_database):
    server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
    # get admin user
    user = User.get_user_by_email(email='abc@gmail.com')
    token = create_access_token(identity=user.token_identity())
    test_client.set_cookie(server_name, key='access_token_cookie', value=token)
    
    response = test_client.get('/connect/products', json={})

    assert response.status_code == 200
    assert len(response.json['body'][0]['variations']) == 4
    assert response.json['body'][0]['product']['name'] == 'Haoluo'