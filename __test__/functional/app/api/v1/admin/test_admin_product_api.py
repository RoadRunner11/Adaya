from app.models import Product
from app.helpers import Messages, Responses
from app.helpers.app_context import AppContext as AC

def test_add_products(test_client, init_database, new_product, new_variation):
    response = test_client.post(
        '/connect/products', json={'product': new_product.as_dict(), 'variations':[new_variation.as_dict()]})

    assert response.status_code == 200
    assert response.json['body'] == 'Operation Success'

def test_update_products(test_client, init_database, new_product, new_variation2):
    response = test_client.put(
        '/connect/products/5', json={'product': new_product.as_dict(), 'variations':[new_variation2.as_dict()]})

    assert response.status_code == 200
    assert response.json['body'] == 'Operation Success'

def test_get_products(test_client, init_database):
    response = test_client.get('/connect/products', json={})

    assert response.status_code == 200
    assert len(response.json['body'][0]['variations']) == 4
    assert response.json['body'][0]['product']['name'] == 'Haoluo'