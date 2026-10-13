def validate_password(password):
    if any(char.isspace() for char in password):
        return "WSP"

    if not any(char.isdigit() for char in password):
        return "NDT"

    if not any(char.isalpha() for char in password):
        return "NLT"

    special_chars = "!§$%&/=?@"
    if not any(char in special_chars for char in password):
        return "NSC"

    if len(password) < 8 or len(password) > 64:
        return "LEN"

    return "OK0"