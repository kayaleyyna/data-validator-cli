# Data Validation framework for IOT

## Overview
The Data Validation Framework for IOT is a Python-based CLI project to validate structured data such as email addresses, passwords, timestamps, phone numbers, and data from CSV files. It uses a configurable validator design with rule-based checking to keep the process of validation flexible and easy to manage.

# Features
- **CLI User Interface**: Menu-driven CLI navigation for selecting validation options and entering input data such as email, phone number, timestamp, and passwords.

- **Validation**:  Validation of email, phone number, password, timestamp and CSV-based data is performed using rule-based checking through `rules.csv`. The framework returns 3-character codes such as `OK0`, `RUL`, `LEN`, `MAT` and similar codes to represent results of the validation. It also supports CSV batch validation, where a csv file is read and the multiple data types are validated from the file.

-  **Session Logs and Export**: Validated data is logged with timestamps and can be viewed in the option of session log. It can also be exported to csv file as `validation_log.csv` and this session data can be stored in the SQLite database.

-  **CLI Tests**:  Validator functions can be tested by running these test files `test_csv_validator.py`, `test_email_validator.py`, `test_password_validator.py`, `test_phone_validator.py`

- **Raspberry Pi & Sense HAT**:  Along with displaying the 3-char codes in the CLI, the same codes are also shown on the Sense HAT LED display. By running `hat_ui.py`, user can select validation options using the Raspberry Pi Sense HAT joystick, and the corresponding result code appears in both the terminal and on the LED display.


# Tech Stack
- **Core Language**:  Python for the validation logic and CLI interface
- **Data Storage**: `CSV` & `SQLite`
- **Hardware**: Raspberry Pi & Sense HAT

# Installation & Setup

### 1. Clone the Repository


```bash
git clone https://gitlab-fi.ostfalia.de/id319720/dt-ss26-validator-cli.git
cd dt-ss26-validator-cli
```

### 2. Create a virtual Environment and Install Dependencies

```bash
python3 -m venv venv
```


#### On macOS/Linux:
```bash
 source venv/bin/activate
 ```


#### On Windows:
```bash
 .\venv\Scripts\activate
```

#### Install requirements
```bash
pip install -r requirements.txt

```

### 3. Run the Project

```bash
python cli.py
```


# Usage Instructions for the Validation framework:
- Enter option `1` to open the validation menu.
- In the validation sub-menu, choose an option by entering its number.
- Enter the required data such as email address, phone number, password, timestamp or CSV file path.
- Enter e to exit the validation type.
- Use the other menu options in the same way.
- Sense HAT LED display output and `hat_ui.py` only work when the project is run on a Raspberry Pi.
- Run `pytest -v` to test the validator functions.

  ## Team

- Emre Aykut Sevindik
- Aleyna Kaya
- Chakri Ajit Kusampudi
- Kajal Thakur

