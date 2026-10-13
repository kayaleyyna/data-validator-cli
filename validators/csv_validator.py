import csv
import os

from validators.email_validator import validate_email
from validators.phone_validator import validate_phone
from validators.password_validator import validate_password


def validate_csv_file(file_path, num_of_columns, max_num_rows):
    if not os.path.isfile(file_path):
        return "PTH"
    
    row_count = 0

    with open(file_path, "r", newline = "", encoding = "utf-8-sig") as file:
        read = csv.reader(file, delimiter = ";")

        for row in read:
            row_count += 1
            if len(row) > num_of_columns:
                return "COL"
            
    if max_num_rows > 0 and row_count > max_num_rows:
        return "MRO"
    
    return "OK0"

#US15

def validate_csv_row(row):
    if len(row) != 2:
        return "CSV"
    
    field_type = row[0].strip().lower()
    value = row[1].strip()

    if field_type == "email":
        return validate_email(value)
    
    if field_type == "phone":
        return validate_phone(value)
    
    if field_type == "password":
        return validate_password(value)
    
    return "CSV"



def batch_validate_csv(file_path, log_attempt):
    if not os.path.isfile(file_path):
        return["PTH"]
    
    results = []

    with open(file_path, "r", newline = "", encoding = "utf-8-sig") as file:
        read = csv.reader(file, delimiter = ";")

        for row in read:
            result_code = validate_csv_row(row)

            if len(row) == 2:
                field_type = row[0].strip().lower()
                value = row[1].strip()
            else:
                field_type = "csv"
                value = ";".join(row)
            
            is_valid = result_code == "OK0"
            log_attempt(field_type, value, is_valid, result_code)
            results.append(result_code)

    return results
            