import tempfile
import os

from cli import validate_csv_file


def test_valid_csv():

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as file:
        file.write("name;age\nJohn;25")
        temp_path = file.name

    result = validate_csv_file(temp_path, 2, 5)

    os.remove(temp_path)

    assert result == "OK0"


def test_invalid_path():

    result = validate_csv_file("wrong_path.csv", 2, 5)

    assert result == "PTH"


def test_too_many_columns():

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as file:
        file.write("name;age;city")
        temp_path = file.name

    result = validate_csv_file(temp_path, 2, 5)

    os.remove(temp_path)

    assert result == "COL"


def test_too_many_rows():

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as file:
        file.write("a;b\n1;2\n3;4\n5;6")
        temp_path = file.name

    result = validate_csv_file(temp_path, 2, 2)

    os.remove(temp_path)

    assert result == "MRO"