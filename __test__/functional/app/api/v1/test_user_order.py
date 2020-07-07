from app.models import Order, User
from app.helpers.app_context import AppContext as AC
from datetime import datetime
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

def test_unsubscribed_member_order(test_client, init_database, member_order): 
  order_items = order_items_as_dict(member_order)
  server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
  # get member user
  user = User.get_user_by_email(email='abcd@gmail.com')
  token = create_access_token(identity=user.token_identity())
  test_client.set_cookie(server_name, key='access_token_cookie', value=token)
  
  response = test_client.post(
    '/orders', json={'order_items':[order_items[0], order_items[1]], 'user_id': 1})
     
  # number of produts
  assert response.json['body']['total_price'] == '70.00'

def test_subscribed_member_order(test_client, init_database, member_order): 
  order_items = order_items_as_dict(member_order)
  server_name = flask.current_app.config["ALLOW_ORIGIN"] or "localhost"
  # get member user
  user = User.get_user_by_email(email='abcd@gmail.com')
  token = create_access_token(identity=user.token_identity())
  test_client.set_cookie(server_name, key='access_token_cookie', value=token)

  response = test_client.post(
    '/orders', json={'order_items':[order_items[0], order_items[1]], 'user_id': member_order.user_id})
     
  # number of produts
  assert response.json['body']['total_price'] == '0.00'

def order_items_as_dict(member_order):
  output_columns = ['variation_id', 'quantity', 'start_date', 'end_date']

  firstoid = member_order.order_items[0].as_dict(output_columns)
  secondoid = member_order.order_items[1].as_dict(output_columns)
  thirdoid = member_order.order_items[2].as_dict(output_columns)
  fourthoid = member_order.order_items[3].as_dict(output_columns)
  fifthoid = member_order.order_items[4].as_dict(output_columns)
     
  firstoid['quantity'] = 1  
  secondoid['quantity'] = 1
  thirdoid['quantity'] = 1
  fourthoid['quantity'] = 1
  fifthoid['quantity'] = 1

  return [firstoid, secondoid, thirdoid, fourthoid, fifthoid]

#add 21 order items for this test to pass, limit per month is 20
# def test_member_order_with_more_than_allowed_limit(test_client, init_database, member_order): 
#   order_items = order_items_as_dict(member_order)

#   response = test_client.post(
#     '/orders', json={'order_items':[order_items[0], order_items[1], order_items[2], order_items[3], order_items[4]], 'user_id': member_order.user_id})
   
#   # should fail if more than 4 products in order
#   assert response.status_code == 400
  
# Order with vouchers needs to be finished
# def test_member_order_with_voucher(test_client, init_database, member_order): 
#   order_items = order_items_as_dict(member_order)

#   response = test_client.post(
#     '/orders', json={'order_items':[order_items[0], order_items[1]], 'user_id': member_order.user_id})
    
#   second_response = test_client.post(
#     '/orders', json={'order_items':[order_items[0], order_items[1]], 'user_id': member_order.user_id, 
#                         'voucher_codes':[member_order.vouchers[0].name]})
#   assert response.status_code == 200
     
#   # number of produts
#   assert len(response.json['body']['order_items'] ) == 2

#   assert second_response.json['body']['total_price'] == '350.00'
  