from validators.rule_loader import load_rules


def validate_email(email):

    mistakes = []

    if email.count("@") == 0:
        mistakes.append("EAT")

    if email.count("@") > 1:
        mistakes.append("MAT")

    if " " in email:
        mistakes.append("SPC")

    if email.count("@") == 1:
        name, domain = email.split("@")

        if "." not in domain:
            mistakes.append("DOT")

    if mistakes:
        return ",".join(mistakes)
    
    rules = load_rules()
    
    email_rules = rules.get("email", {})
    
    allowed_domain = email_rules.get("allowed_domain")
    
    if allowed_domain:
        if not email.endswith("@" + allowed_domain):
            return "RUL"
        
    return "OK0"