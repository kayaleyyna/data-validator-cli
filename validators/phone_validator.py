from validators.rule_loader import load_rules


def validate_phone(phone):

    if phone.startswith("+"):
        digits = phone[1:]
    else:
        digits = phone

    if not digits.isdigit():
        return "NDG"

    if len(phone) < 10 or len(phone) > 15:
        return "LEN"

    rules = load_rules()
    
    phone_rules = rules.get("phone", {})
    
    starts_with = phone_rules.get("starts_with")
    
    if starts_with:
        if not phone.startswith(starts_with):
            return "RUL"
        
    return "OK0"