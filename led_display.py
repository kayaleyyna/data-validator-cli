try:
    from sense_hat import SenseHat
except ImportError:
    SenseHat = None

Display = "sensehat"

def get_display():
    if SenseHat is None:
        return None

    if Display == "sensehat":
        try:
            return SenseHat()
        except Exception:
            return None

    return None

def show_code_result(code: str):
    code = code[:3].upper()
    device = get_display()

    if Display == "sensehat" and device:
        if code == "OK0":
            colour = (0, 200, 0)
            device.show_message(code, text_colour = colour, scroll_speed = 0.15)
            device.clear()
        else:
            colour = (200, 0 ,0)
            device.show_message(code, text_colour = colour, scroll_speed = 0.15)
            device.clear()

def validation_result_display(result: str):
    show_code_result(result)