import pytest
from app.models import User


@pytest.fixture(scope='module')
def admin_user():
    user = User()
    user.email = 'abc@gmail.com'
    user.password = '1q2w3e4r'
    return user

@pytest.fixture(scope='module')
def new_member():
    user = User()
    user.email = 'cret@gmail.com'
    user.password = '1q2w3e4r'
    user.role_id = 2
    user.lastname = 'Analytics'
    return user