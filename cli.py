import time
import datetime
import sys
import csv
import sqlite3

from validators.password_validator import validate_password
from validators.email_validator import validate_email
from validators.phone_validator import validate_phone
from validators.timestamp_validator import validate_timestamp
from validators.csv_validator import validate_csv_file, batch_validate_csv
from validators.rule_loader import load_rules
from led_display import validation_result_display


session_log = []

def create_table():
    conn = sqlite3.connect("logs_validation.db")
    c = conn.cursor()

    c.execute(""" CREATE TABLE IF NOT EXISTS validation_attempts( id INTEGER PRIMARY KEY AUTOINCREMENT,
              timestamp TEXT,
              field_type TEXT,
              value_raw TEXT,
              passed INTEGER,
              code TEXT
              )""")
    conn.commit()
    conn.close()

def log_attempt(field_type, value_raw, passed, code):
    """Append a validation attempt to the session log."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    session_log.append({
        "timestamp": timestamp,
        "field_type": field_type,
        "value_raw": value_raw,
        "pass": passed,
        "code": code
    })

    conn = sqlite3.connect("logs_validation.db")
    c = conn.cursor()

    c.execute(""" INSERT INTO validation_attempts (timestamp, field_type, value_raw, passed, code)
              VALUES (?, ?, ?, ?, ?)
              """, (timestamp, field_type, value_raw, int(passed), code))
    conn.commit()
    conn.close()

def show_log():
    """Display the internal session log."""

    if not session_log:
        print("No attempts logged yet.")
        return

    print("-" * 88, "Session Log", "-" * 88)

    print(
        f"{'Timestamp':<28} "
        f"{'Type':<10} "
        f"{'Value':<75} "
        f"{'Pass':<10} "
        f"{'Code'}"
    )

    print("-" * 189)

    for entry in session_log:
        print(
            f"{entry['timestamp']:<28} "
            f"{entry['field_type']:<10} "
            f"{entry['value_raw']:<75} "
            f"{str(entry['pass']):<10} "
            f"{entry['code']}"
        )

    print("-" * 189)

    print(f"Total attempts: {len(session_log)}\n")


def export_log():
    """Export session log to CSV file."""

    if not session_log:
        print("No attempts to export.")
        return

    file_name = "validation_log.csv"

    with open(file_name, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "field_type",
                "value_raw",
                "pass",
                "code"
            ]
        )

        writer.writeheader()
        writer.writerows(session_log)

    print(f"{file_name} exported successfully.")


# =========================
# MENUS
# =========================

def main_menu():

    print("----------------")
    print("   Main Menu")
    print("----------------")
    print("1. Validation")
    print("2. History")
    print("3. Quit")


def validation_menu():

    print("----------------")
    print(" Validation Menu")
    print("----------------")
    print("1. Validate email")
    print("2. Validate phone")
    print("3. Validate password")
    print("4. Validate CSV")
    print("5. Batch validate CSV")
    print("6. Validate timestamp")
    print("7. Back")
    print("8. Main Menu")


def history_menu():

    print("----------------")
    print("  History Menu")
    print("----------------")
    print("1. Show session log")
    print("2. Export session log")
    print("3. Back")


# =========================
# VALIDATION INPUTS
# =========================

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

def validate_timestamp_input():

    while True:
        timestamp = input("Enter timestamp (e to exit): ").strip()

        if timestamp.lower() == "e":
            break

        result = validate_timestamp(timestamp)

        print(result)
        validation_result_display(result)

        passed = result == "OK0"

        log_attempt("timestamp", timestamp, passed, result)


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

        result = validate_csv_file(
            file_path,
            num_of_columns,
            max_num_rows
        )

        print(result)
        validation_result_display(result)
        passed = result == "OK0"

        log_attempt("csv", file_path, passed, result)


def batch_validate_csv_input():

    while True:

        file_path = input(
            "Enter batch CSV file path (e to exit): "
        ).strip()

        if file_path.lower() == "e":
            break

        results = batch_validate_csv(file_path, log_attempt)

        for result in results:
            print(result)
            validation_result_display(result)


# =========================
# MENU RUNNERS
# =========================

def run_validation_menu():

    valid_options = {"1", "2", "3", "4", "5", "6", "7", "8"}

    while True:

        validation_menu()

        choice = input("Choose an option: ").strip()

        if choice not in valid_options:
            print("Error: invalid option")
            time.sleep(1)
            continue

        if choice == "1":
            validate_email_input()
            time.sleep(1)

        elif choice == "2":
            validate_phone_input()
            time.sleep(1)

        elif choice == "3":
            validate_password_input()
            time.sleep(1)

        elif choice == "4":
            validate_csv_input()
            time.sleep(1)

        elif choice == "5":
            batch_validate_csv_input()
            time.sleep(1)
        
        elif choice == "6":
            validate_timestamp_input()
            time.sleep(1)

        elif choice == "7":
            break

        elif choice == "8":
            return

def run_history_menu():

    valid_options = {"1", "2", "3"}

    while True:

        history_menu()

        choice = input("Choose an option: ").strip()

        if choice not in valid_options:
            print("Error: invalid option")
            time.sleep(1)
            continue

        if choice == "1":
            show_log()
            time.sleep(1)

        elif choice == "2":
            export_log()

        elif choice == "3":
            break

        time.sleep(1)


# =========================
# PROGRAM EXIT
# =========================

def quit_program():

    answer = input(
        "Do you want to quit? (y/n): "
    ).strip().lower()

    return answer == "y"


# =========================
# MAIN PROGRAM
# =========================

def main():

    try:
        load_rules()
        create_table()
        print("rules.csv loaded and validated successfully")
        time.sleep(1)

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)

    valid_options = {"1", "2", "3"}

    while True:

        main_menu()

        choice = input("Choose an option: ").strip()

        if choice not in valid_options:
            print("Error: invalid option")
            time.sleep(1)
            continue

        if choice == "1":
            run_validation_menu()

        elif choice == "2":
            run_history_menu()

        elif choice == "3":

            if quit_program():
                print("Program exits")
                break


if __name__ == "__main__":
    main()