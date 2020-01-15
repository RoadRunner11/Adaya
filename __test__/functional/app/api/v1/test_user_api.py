from app.models import User
from app.helpers.app_context import AppContext as AC



def test_request_token(test_client, init_database, admin_user):
    response = test_client.post(
        '/users/token', data=dict(email=admin_user.email, password=admin_user.password))
    assert response.status_code == 400
    response = test_client.post(
        '/users/token', json={'email': admin_user.email, 'password': admin_user.password})
    assert response.status_code == 200


def test_register_user(test_client, init_database, new_member):    
    response = test_client.post(
        '/users', json={'email': new_member.email, 'password': new_member.password, 'role_id':new_member.role_id})
    assert response.status_code == 200

    # role should still be 'member' even if role_id is set to admin
    assert 'member' in response.json['body'].values()

    response = test_client.post(
        '/users', json={'email': new_member.email, 'password': new_member.password})
    assert response.status_code == 409

def test_update_user_info(test_client, init_database, new_member):    
    response = test_client.put(
        '/users/abc@gmail.com', json={'lastname': new_member.lastname })
    assert response.status_code == 200