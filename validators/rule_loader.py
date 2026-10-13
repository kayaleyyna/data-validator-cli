import csv
import os


def load_rules():

    rules = {}

    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "config",
        "rules.csv"
    )

    if not os.path.exists(config_path):
        raise FileNotFoundError("rules.csv file is missing")
    

    try:
        with open(config_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")

            if reader.fieldnames != ["field", "rule", "value"]:
                raise ValueError("rules.csv has invalid columns")

            for row in reader:
                field = row["field"]
                rule = row["rule"]
                value = row["value"]

                if field not in rules:
                    rules[field] = {}

                rules[field][rule] = value
    
    except OSError:
        raise OSError("rules.csv cannot be read")

    return rules