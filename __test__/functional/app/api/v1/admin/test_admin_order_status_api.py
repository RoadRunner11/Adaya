from app.models import UserSubscription, User
from app.helpers.app_context import AppContext as AC
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def test_admin_get_orderstatus(test_client, init_database): 
    response = test_client.get(
    '/connect/order_status', json={})

    assert response.status_code == 200    
    assert response.json['body'][0]['name'] == 'completed'
    assert len(response.json['body'])== 1

def test_admin_add_orderstatus(test_client, init_database): 
    response = test_client.post(
    '/connect/order_status', json={'name': 'returned'})

    assert response.status_code == 200    
    assert response.json['body']['name'] == 'returned'

def test_admin_update_orderstatus(test_client, init_database, new_product):
    response = test_client.put(
        '/connect/order_status/1', json={'name': 'processing'})

    assert response.status_code == 200
    assert response.json['body'] == 'Operation Success'
