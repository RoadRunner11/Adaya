from app.models import Voucher

def test_calculate_discounted_cost(test_client, init_database, new_voucher):
    valid = Voucher.validate_voucher([new_voucher, new_voucher])
    assert valid == True