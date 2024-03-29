from app.models import Order

def test_calculate_discounted_cost(test_client, init_database, member_order):
    member_order.calculate_discounted_cost()
    assert member_order.total_price == 466
    assert member_order.products_freeze == '[{"id": "1", "name": "Haoluo", "description": "None", "variation.price": "", "image": "None"}, {"id": "1", "name": "Haoluo", "description": "None", "variation.price": "", "image": "None"}, {"id": "1", "name": "Haoluo", "description": "None", "variation.price": "", "image": "None"}]'

def test_calculate_cost(test_client, init_database, new_order):
    new_order.calculate_cost()
    assert new_order.total_price == 60.0
    assert new_order.products_freeze == '[{"id": "1", "name": "Haoluo", "description": "None", "variation.price": "", "image": "None"}, {"id": "1", "name": "Haoluo", "description": "None", "variation.price": "", "image": "None"}]'


def test_get_items(test_client, init_database, new_order):
    orders = Order.get_items(user_id=1)
    assert len(orders) == 10
    new_order.calculate_cost()
    new_order.insert()
    orders = Order.get_items(sort_by='total_price',is_desc=True)
    assert orders[0].total_price == new_order.total_price
    orders = Order.get_items(sort_by='total_price',is_desc=False)
    assert orders[0].total_price != new_order.total_price