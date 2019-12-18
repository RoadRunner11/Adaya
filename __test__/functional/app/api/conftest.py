import pytest
from app.models import User


@pytest.fixture(scope='module')
def admin_user():
    user = User()
    user.email = 'abc@gmail.com'
    user.password = '1q2w3e4r'
    return user

@pytest.fixture(scope='module')
def new_user():
    user = User()
    user.email = 'hao@gmail.com'
    user.password = '1q2w3e4r'
    return user