from app.models import User
from app.helpers.app_context import AppContext as AC



def test_request_token(test_client, init_database, admin_user):
    response = test_client.post(
        '/users/token', data=dict(email=admin_user.email, password=admin_user.password))
    assert response.status_code == 400
    response = test_client.post(
        '/users/token', json={'email': admin_user.email, 'password': admin_user.password})
    assert response.status_code == 200
