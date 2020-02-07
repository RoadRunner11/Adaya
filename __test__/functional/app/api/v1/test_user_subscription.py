from app.models import UserSubscription, User
from app.helpers.app_context import AppContext as AC
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def test_user_subscription(test_client, init_database): 
    response = test_client.post(
    '/subscribe', json={'email': 'abcd@gmail.com', 'subscription_type':1})
    
    end_date = (date.today() + relativedelta(months=1)).strftime('%Y-%m-%d')   

    assert response.status_code == 200    
    assert response.json['body']['end_date'] == end_date
    assert len(response.json['body'])== 4
