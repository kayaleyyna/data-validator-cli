from datetime import datetime


def validate_timestamp(timestamp):
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return "OK0"
    except ValueError:
        return "TSF"