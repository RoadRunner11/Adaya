from app.models import User, UserSubscription
from app.helpers.app_context import AppContext as AC

def test_check_subscription_active(test_client, init_database):
    isactive = UserSubscription.check_subscription_active(2)
    assert isactive == True

def test_check_all_user_subscriptions(test_client, init_database):
    UserSubscription.Check_all_user_subsriptions()
    users = User.query.all()
    assert users[0].subscribed == False
    assert users[1].subscribed == True