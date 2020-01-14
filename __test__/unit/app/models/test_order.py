from app.models import Order


def test_calculate_cost(new_order):
    new_order.calculate_cost()
    assert new_order.total_price == 20
    assert new_order.products_freeze == '[{"id": "None", "name": "name", "description": "None", "price": "10", "image": "None"}, {"id": "None", "name": "name", "description": "None", "price": "10", "image": "None"}]'


def test_get_items(test_client, init_database, new_order):
    orders = Order.get_items(user_id=1)
    assert len(orders) == 10
    new_order.calculate_cost()
    new_order.insert()
    orders = Order.get_items(sort_by='total_price',is_desc=True)
    assert orders[0].total_price == new_order.total_price
    orders = Order.get_items(sort_by='total_price',is_desc=False)
    assert orders[0].total_price != new_order.total_price