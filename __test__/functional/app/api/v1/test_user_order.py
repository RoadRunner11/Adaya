from app.models import Order
from app.helpers.app_context import AppContext as AC

def test_member_order(test_client, init_database, member_order): 
     response = test_client.post(
       '/orders', json={'order_items':[member_order.order_items[0], member_order.order_items[1], member_order.order_items[2],
                        member_order.order_items[3], member_order.order_items[4]], 'user_id': member_order.user_id})
     
     second_response = test_client.post(
       '/orders', json={'order_items':[member_order.order_items[0], member_order.order_items[1]], 'user_id': member_order.user_id})
    
     third_response = test_client.post(
       '/orders', json={'order_items':[member_order.order_items[0], member_order.order_items[1]], 'user_id': member_order.user_id, 
                        'voucher_codes':[member_order.vouchers[0].name]})

     # should fail if more than 4 products in order
     assert response.status_code == 400

     assert second_response.status_code == 200
     
     # number of produts
     assert len(second_response.json['body']['products'] ) == 2

     assert third_response.json['body']['total_price'] == '100.00'

def test_update_member_order(test_client, init_database, member_order):  
    response = test_client.post(
       '/orders', json={'order_items':[member_order.order_items[0], member_order.order_items[1], member_order.order_items[2],
                          member_order.order_items[3]], 'user_id': member_order.user_id})
    
    # check order created succesfully
    assert response.status_code == 200

    # update the order    
    update_response = test_client.put(
       '/orders/11', json={'order_items':[member_order.order_items[3], member_order.order_items[4]], 'user_id': member_order.user_id})

    # check the order updated
    assert update_response.status_code == 200
    
    
    
   
  