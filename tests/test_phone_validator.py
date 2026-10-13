from validators.phone_validator import validate_phone


def test_valid_phone():
    assert validate_phone("+491234567890") == "OK0"


def test_valid_phone_with_plus():
    assert validate_phone("+491112223334") == "OK0"


def test_non_digit_phone():
    assert validate_phone("12345abcd") == "NDG"


def test_short_phone():
    assert validate_phone("12345") == "LEN"


def test_long_phone():
    assert validate_phone("1234567890123456") == "LEN"

def test_phone_rule_fail():
    assert validate_phone("+33123456789") == "RUL"