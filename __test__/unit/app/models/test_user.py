from app.models import User
from app.helpers.app_context import AppContext as AC

def test_get_user_by_email(test_client, init_database):
    user = User.get_user_by_email(email='abc@gmail.com')
    assert user.email == 'abc@gmail.com'


def test_get_users_by_role(test_client, init_database):
    user = User.get_users_by_role('member')[0]
    assert user.email == 'abcd@gmail.com'


def test_authenticate(test_client, init_database):
    user = User.authenticate('abcd@gmail.com', '1q2w3e4r')
    assert user.email == 'abcd@gmail.com'
    user = User.authenticate('abcd@gmail.com', '1q2w3e4')
    assert user == None
    user = User.authenticate('abcde@gmail.com', '1q2w3e4')
    assert user == None


def test_authorisation(test_client, init_database):
    assert User.authorisation(
        'abc@gmail.com', ['member', 'random_role']) != True
    assert User.authorisation('abc@gmail.com', ['member', 'admin']) == True
    assert User.authorisation(
        'abc@gmail.com', ['random_role', 'admin']) == True


def test_update_from_dict(test_client, init_database, new_user):
    user_dict = {'password': 'abcdefg','firstname':'haha'}
    new_user.update_from_dict(user_dict)
    assert new_user.password != 'abcdefg'
    assert AC().bcrypt.check_password_hash(new_user.password, 'abcdefg') ==  True
    assert new_user.firstname == 'haha'
    assert new_user.password != '1q2w3e4r'