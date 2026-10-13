from validators.email_validator import validate_email


def test_valid_email():
    assert validate_email("test@gmail.com") == "OK0"


def test_missing_at():
    assert validate_email("testgmail.com") == "EAT"


def test_multiple_at():
    assert validate_email("test@@gmail.com") == "MAT"


def test_space_in_email():
    assert validate_email("test @gmail.com") == "SPC"


def test_missing_dot():
    assert validate_email("test@gmailcom") == "DOT"


def test_multiple_errors():
    assert validate_email("test gmailcom") == "EAT,SPC"

def test_email_rule_fail():
    assert validate_email("test@yahoo.com") == "RUL"