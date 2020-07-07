from app.models import UserSubscription, User
from app.helpers.app_context import AppContext as AC
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity


def test_admin_get_subscription(test_client, init_database): 
    server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
    # get admin user
    user = User.get_user_by_email(email='abc@gmail.com')
    token = create_access_token(identity=user.token_identity())
    test_client.set_cookie(server_name, key='access_token_cookie', value=token)
    
    response = test_client.get(
    '/connect/subscribe', json={})

    assert response.status_code == 200    
    assert response.json['body'][0]['subscription_type_id'] == '1'
    assert len(response.json['body'])== 2

def test_admin_update_subscription(test_client, init_database):
    server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
    # get admin user
    user = User.get_user_by_email(email='abc@gmail.com')
    token = create_access_token(identity=user.token_identity())
    test_client.set_cookie(server_name, key='access_token_cookie', value=token)
    
    response = test_client.put(
        '/connect/subscribe/1', json={'subscription_type_id': '2'})

    assert response.status_code == 200
    assert response.json['body'] == 'Operation Success'
