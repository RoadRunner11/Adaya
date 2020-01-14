import pytest
from app.helpers import utility


def test_parse_int():
    assert utility.parse_int(None) == None 
    assert utility.parse_int('1') == 1 
    assert utility.parse_int('test string') == None
