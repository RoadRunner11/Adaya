from app.models import UserSubscription, User, Voucher
from app.helpers.app_context import AppContext as AC
from datetime import datetime
from dateutil.relativedelta import relativedelta

def test_admin_get_voucher(test_client, init_database): 
    response = test_client.get(
    '/connect/vouchers', json={})

    assert response.status_code == 200    
    assert response.json['body'][0]['name'] == 'HAO20'
    assert len(response.json['body'])== 2

def test_admin_update_voucher(test_client, init_database, new_product):
    response = test_client.put(
        '/connect/vouchers/HAO20', json={'name': 'HAC20'})

    assert response.status_code == 200
    assert response.json['body'] == 'Operation Success'
    
# def test_admin_add_voucher(test_client, init_database): 
#     req_date = datetime.strptime('Wednesday, June 6, 2018', '%A, %B %d, %Y')
#     req2 = req_date
#     response = test_client.post(
#     '/connect/vouchers', json={'name': 'HAT13','redeem_by': req_date})

#     assert response.status_code == 200    
#     assert response.json['body']['duration'] == '5'
#     assert response.json['body']['price'] == '70.00'
