from validators.password_validator import validate_password


def test_valid_password():
    assert validate_password("Test@123") == "OK0"


def test_password_with_space():
    assert validate_password("Test 123@") == "WSP"


def test_password_without_digit():
    assert validate_password("Password@") == "NDT"


def test_password_without_letter():
    assert validate_password("1234567@") == "NLT"


def test_password_without_special_char():
    assert validate_password("Password123") == "NSC"


def test_password_too_short():
    assert validate_password("T@1a") == "LEN"


def test_password_too_long():
    long_password = "T@12345678901234567890123456789012345678901234567890123456789012345"
    assert validate_password(long_password) == "LEN"