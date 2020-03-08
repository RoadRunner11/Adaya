from app.models import UserSubscription, User
from app.helpers.app_context import AppContext as AC
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def test_admin_get_subscriptiontype(test_client, init_database): 
    response = test_client.get(
    '/connect/subscribetype', json={})

    assert response.status_code == 200    
    assert response.json['body'][0]['duration'] == '1'
    assert len(response.json['body'])== 2

def test_admin_add_subscriptiontype(test_client, init_database): 
    response = test_client.post(
    '/connect/subscribetype', json={'duration': '5','price': '70'})

    assert response.status_code == 200    
    assert response.json['body']['duration'] == '5'
    assert response.json['body']['price'] == '70.00'

def test_admin_update_subscriptiontype(test_client, init_database, new_product):
    response = test_client.put(
        '/connect/subscribetype/1', json={'duration': '5','price': '78'})

    assert response.status_code == 200
    assert response.json['body'] == 'Operation Success'
