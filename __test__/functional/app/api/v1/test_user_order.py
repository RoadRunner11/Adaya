from app.models import Order
from app.helpers.app_context import AppContext as AC

def test_member_order(test_client, init_database, member_order):     
     response = test_client.post(
       '/orders', json={'product_ids':[member_order.products[0].id, member_order.products[1].id, member_order.products[2].id,
                        member_order.products[3].id, member_order.products[4].id], 'user_id': member_order.user_id})
     
     second_response = test_client.post(
       '/orders', json={'product_ids':[member_order.products[0].id, member_order.products[1].id], 'user_id': member_order.user_id})
    

     assert response.status_code == 200

     assert second_response.status_code == 200

     # ensure no products are sent back if more than 4 in order
     assert len(response.json['body']['products'] ) == 0
     
     # number of produts
     assert len(second_response.json['body']['products'] ) == 2

def test_update_member_order(test_client, init_database, member_order):  
    response = test_client.post(
       '/orders', json={'product_ids':[member_order.products[0].id, member_order.products[1].id, member_order.products[2].id,
                        member_order.products[3].id], 'user_id': member_order.user_id})
    
    # check order created succesfully
    assert response.status_code == 200

    # update the order    
    update_response = test_client.put(
       '/orders/11', json={'product_ids':[member_order.products[3].id, member_order.products[4].id], 'user_id': member_order.user_id})
       
    # check the order updated
    assert update_response.status_code == 200
    
    
    
   
  