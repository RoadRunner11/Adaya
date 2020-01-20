import json
from app.models import Product
from app.models import Variation


def test_as_dict(new_product):
    product_dict = {'name': new_product.name, 'variation_id': str(new_product.variation_id)}
    assert new_product.as_dict(
        ['name', 'variation_id']) == product_dict
    # How to serialise the test class as json
    # order_dict = {'products': [
    #     item.as_dict() for item in new_order.order_items]}
    # assert new_order.as_dict(
    #     ['products']) == order_dict


def test_update_from_dict(new_product):
    product_dict = {'name': 'test_name', 'variation_id': 4}
    new_product.update_from_dict(product_dict, ['name'])
    assert new_product.name == 'name'
    assert new_product.variation_id == 4


def test_insert(test_client, init_database, new_product):
    new_product.insert()
    product = Product.query.get(new_product.id)
    assert product.id == new_product.id


def test_update(test_client, init_database):
    products = Product.get_items()
    product = products[0]
    product.update(obj_dict={'name': 'test_name', 'variation_id': 3})
    assert product.variation_id == 3


def test_get(test_client, init_database):
    filter_query = Product.category_id == 2
    products = Product.get(filter_queries=filter_query)
    assert len(products) == 5
    filter_queries = [filter_query]
    products = Product.get(filter_queries=filter_queries)
    assert len(products) == 5