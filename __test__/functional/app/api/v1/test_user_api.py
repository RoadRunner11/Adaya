from app.models import User
from app.helpers.app_context import AppContext as AC



def test_request_token(test_client, init_database, admin_user):
    response = test_client.post(
        '/users/token', data=dict(email=admin_user.email, password=admin_user.password))
    assert response.status_code == 400
    response = test_client.post(
        '/users/token', json={'email': admin_user.email, 'password': admin_user.password})
    assert response.status_code == 200


def register_user(test_client, init_database, new_user):    
    response = test_client.post(
        '/users', json={'email': new_user.email, 'password': new_user.password})
    assert response.status_code == 200

    response = test_client.post(
        '/users', data=dict(email=new_user.email, password=new_user.password))
    assert response.status_code == 400

