from app.models import UserSubscription, User, Voucher
from app.helpers.app_context import AppContext as AC
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

def test_admin_get_voucher(test_client, init_database): 
    server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
    # get admin user
    user = User.get_user_by_email(email='abc@gmail.com')
    token = create_access_token(identity=user.token_identity())
    test_client.set_cookie(server_name, key='access_token_cookie', value=token)

    response = test_client.get(
    '/connect/vouchers', json={})

    assert response.status_code == 200    
    assert response.json['body'][0]['name'] == 'HAO20'
    assert len(response.json['body'])== 2

def test_admin_update_voucher(test_client, init_database, new_product):
    server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
    # get admin user
    user = User.get_user_by_email(email='abc@gmail.com')
    token = create_access_token(identity=user.token_identity())
    test_client.set_cookie(server_name, key='access_token_cookie', value=token)

    response = test_client.put(
        '/connect/vouchers/HAO20', json={'name': 'HAC20'})

    assert response.status_code == 200
    assert response.json['body'] == 'Operation Success'
    
# def test_admin_add_voucher(test_client, init_database): 
#     req_date = datetime.strptime('Wednesday, June 6, 2018', '%A, %B %d, %Y')
#     req2 = req_date
#     response = test_client.post(
#     '/connect/vouchers', json={'name': 'HAT13','redeem_by': req_date})

#     assert response.status_code == 200    
#     assert response.json['body']['duration'] == '5'
#     assert response.json['body']['price'] == '70.00'
