from app.models import Product
from app.helpers.app_context import AppContext as AC

def test_get_user_products(test_client, init_database):    
    response = test_client.get('/products', json={})
    assert response.status_code == 200
    assert len(response.json['body'])== 10

