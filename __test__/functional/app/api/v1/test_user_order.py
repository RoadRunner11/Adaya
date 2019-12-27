from app.models import Order
from app.helpers.app_context import AppContext as AC

def test_member_order(test_client, init_database, member_order):
     response = test_client.post(
        '/orders', json={'product_ids': [member_order.products[0].id, member_order.products[1].id], 'user_id': member_order.user_id})

     assert response.status_code == 200
 
#  orders = Order.get_items(user_id=1)
#     assert len(orders) == 10
#     new_order.calculate_cost()
#     new_order.insert()
#     orders = Order.get_items(sort_by='total_price',is_desc=True)
#     assert orders[0].total_price == new_order.total_price
#     orders = Order.get_items(sort_by='total_price',is_desc=False)
#     assert orders[0].total_price != new_order.total_price