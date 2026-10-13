from sense_hat import SenseHat
import time
import datetime
import sys
from validators.password_validator import validate_password
from validators.email_validator import validate_email
from validators.phone_validator import validate_phone
from validators.csv_validator import validate_csv_file
from validators.rule_loader import load_rules
from led_display import validation_result_display

sense = SenseHat()

# Session log
session_log = []

def log_attempt(field_type, value_raw, passed, code):
    session_log.append({
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "field_type": field_type,
        "value_raw": value_raw,
        "pass": passed,
        "code": code
    })

def show_log():
    if not session_log:
        print("No attempts logged yet.")
        return
    print("-" * 88, "Session Log", "-" * 88)
    print(f"{'Timestamp':<28} {'Type':<10} {'Value':<75} {'Pass':<10} {'Code'}")
    print("-" * 189)
    for entry in session_log:
        print(f"{entry['timestamp']:<28} {entry['field_type']:<10} {entry['value_raw']:<75} {str(entry['pass']):<10} {entry['code']}")
    print("-" * 189)
    print(f"Total attempts: {len(session_log)}\n")

# Menu options
menu_options = ["Email", "Phone", "Pass", "CSV", "Log", "Quit"]

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

def display_selection(index):
    """Show current menu selection on LED matrix and terminal."""
    sense.clear()
    option = menu_options[index]
    print(f"\r> {option}    ", end="", flush=True)
    sense.show_message(option, scroll_speed=0.15, text_colour=GREEN, back_colour=BLACK)
    # After scrolling, show the option number on LED
    sense.show_letter(str(index + 1), text_colour=GREEN)

def validate_email_input():
    while True:
        email = input("Enter the email address (e to exit): ").strip()
        if email.lower() == "e":
            break
        result = validate_email(email)
        print(result)
        validation_result_display(result)
        passed = result == "OK0"
        log_attempt("email", email, passed, result)

def validate_phone_input():
    while True:
        phone = input("Enter the phone number (e to exit): ").strip()
        if phone.lower() == "e":
            break
        result = validate_phone(phone)
        print(result)
        validation_result_display(result)
        passed = result == "OK0"
        log_attempt("phone", phone, passed, result)

def validate_password_input():
    while True:
        password = input("Enter the password (e to exit): ")
        if password.lower() == "e":
            break
        result = validate_password(password)
        print(result)
        validation_result_display(result)
        passed = result == "OK0"
        log_attempt("password", password, passed, result)

def validate_csv_input():
    while True:
        file_path = input("Enter CSV file path (e to exit): ").strip()
        if file_path.lower() == "e":
            break
        try:
            num_of_columns = int(input("Enter number of columns: "))
            max_num_rows = int(input("Enter max number of rows: "))
        except ValueError:
            print("Error: enter numbers only")
            continue
        result = validate_csv_file(file_path, num_of_columns, max_num_rows)
        print(result)
        validation_result_display(result)
        passed = result == "OK0"
        log_attempt("csv", file_path, passed, result)

def run_option(index):
    """Run the selected menu option."""
    sense.clear()

    if index == 0:
        sense.show_message("Email", scroll_speed=0.15, text_colour=BLUE)
        print("\n--- Email Validation ---")
        validate_email_input()

    elif index == 1:
        sense.show_message("Phone", scroll_speed=0.15, text_colour=BLUE)
        print("\n--- Phone Validation ---")
        validate_phone_input()

    elif index == 2:
        sense.show_message("Pass", scroll_speed=0.15, text_colour=BLUE)
        print("\n--- Password Validation ---")
        validate_password_input()

    elif index == 3:
        sense.show_message("CSV", scroll_speed=0.15, text_colour=BLUE)
        print("\n--- CSV Validation ---")
        validate_csv_input()

    elif index == 4:
        sense.show_message("Log", scroll_speed=0.15, text_colour=BLUE)
        print("\n--- Session Log ---")
        show_log()

    elif index == 5:
        sense.show_message("Bye!", scroll_speed=0.15, text_colour=RED)
        sense.clear()
        print("\nProgram exits")
        sys.exit(0)

def main():
    try:
        load_rules()
        print("rules.csv loaded and validated successfully")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    current_index = 0

    print("\n=== Sense HAT Validation Menu ===")
    print("Use joystick UP/DOWN to navigate, press MIDDLE to select\n")

    # Show menu options in terminal
    for i, option in enumerate(menu_options):
        print(f"  {i + 1}. {option}")
    print()

    # Display first option on LED
    display_selection(current_index)

    while True:
        for event in sense.stick.get_events():
            if event.action == "pressed":

                if event.direction == "up":
                    current_index = (current_index - 1) % len(menu_options)
                    display_selection(current_index)

                elif event.direction == "down":
                    current_index = (current_index + 1) % len(menu_options)
                    display_selection(current_index)

                elif event.direction == "middle":
                    run_option(current_index)
                    # After returning, show menu again
                    print("\n=== Sense HAT Validation Menu ===")
                    print("Use joystick UP/DOWN to navigate, press MIDDLE to select\n")
                    for i, option in enumerate(menu_options):
                        print(f"  {i + 1}. {option}")
                    print()
                    display_selection(current_index)

        time.sleep(0.1)

if __name__ == "__main__":
    main()
