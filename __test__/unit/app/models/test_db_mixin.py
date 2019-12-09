import json
from app.models import Product


def test_as_dict(new_order, new_product):
    product_dict = {'name': new_product.name, 'price': str(new_product.price)}
    assert new_product.as_dict(
        ['name', 'price']) == product_dict
    order_dict = {'products': [
        item.as_dict() for item in new_order.products]}
    assert new_order.as_dict(
        ['products']) == order_dict


def test_update_from_dict(new_product):
    product_dict = {'name': 'test_name', 'price': 20}
    new_product.update_from_dict(product_dict, ['name'])
    assert new_product.name == 'name'
    assert new_product.price == 20


def test_insert(test_client, init_database, new_product):
    new_product.insert()
    product = Product.query.get(new_product.id)
    assert product.id == new_product.id


def test_update(test_client, init_database):
    products = Product.get_items()
    product = products[0]
    product.update(obj_dict={'name': 'test_name', 'price': 20})
    assert product.price == Product.query.get(product.id).price


def test_get(test_client, init_database):
    filter_query = Product.category_id == 2
    products = Product.get(filter_queries=filter_query)
    assert len(products) == 5
    filter_queries = [filter_query]
    products = Product.get(filter_queries=filter_queries)
    assert len(products) == 5