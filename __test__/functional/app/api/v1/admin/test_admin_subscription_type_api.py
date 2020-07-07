from app.models import UserSubscription, User
from app.helpers.app_context import AppContext as AC
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity


def test_admin_get_subscriptiontype(test_client, init_database): 
    server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
    # get admin user
    user = User.get_user_by_email(email='abc@gmail.com')
    token = create_access_token(identity=user.token_identity())
    test_client.set_cookie(server_name, key='access_token_cookie', value=token)

    response = test_client.get(
    '/connect/subscribetype', json={})

    assert response.status_code == 200    
    assert response.json['body'][0]['plan'] == 'Adaya Lite'
    assert len(response.json['body'])== 2

def test_admin_add_subscriptiontype(test_client, init_database): 
    server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
    # get admin user
    user = User.get_user_by_email(email='abc@gmail.com')
    token = create_access_token(identity=user.token_identity())
    test_client.set_cookie(server_name, key='access_token_cookie', value=token)

    response = test_client.post(
    '/connect/subscribetype', json={'plan': '5','price': '70'})

    assert response.status_code == 200    
    assert response.json['body']['plan'] == '5'
    assert response.json['body']['price'] == '70.00'

def test_admin_update_subscriptiontype(test_client, init_database, new_product):
    server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
    # get admin user
    user = User.get_user_by_email(email='abc@gmail.com')
    token = create_access_token(identity=user.token_identity())
    test_client.set_cookie(server_name, key='access_token_cookie', value=token)
    
    response = test_client.put(
        '/connect/subscribetype/Adaya Lite', json={'plan': 'Adaya Lite','price': '78'})

    assert response.status_code == 200
    assert response.json['body'] == 'Operation Success'
