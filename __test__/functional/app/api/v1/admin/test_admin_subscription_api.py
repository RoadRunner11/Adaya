from app.models import UserSubscription, User
from app.helpers.app_context import AppContext as AC
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def test_admin_get_subscription(test_client, init_database): 
    response = test_client.get(
    '/connect/subscribe', json={})

    assert response.status_code == 200    
    assert response.json['body'][0]['subscription_type_id'] == '1'
    assert len(response.json['body'])== 2

def test_admin_update_subscription(test_client, init_database):
    response = test_client.put(
        '/connect/subscribe/1', json={'subscription_type_id': '2'})

    assert response.status_code == 200
    assert response.json['body'] == 'Operation Success'
