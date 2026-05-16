import pandas as pd

from src.transactions_reader import load_csv
from src.transactions_reader import load_xlsx


def test_load_csv_success(tmp_path, csv_content):
    test_file = tmp_path / "test_operations.csv"
    test_file.write_text(csv_content, encoding="utf-8")

    result = load_csv(test_file)

    assert len(result) == 2

    first_row = result[0]
    assert first_row["id"] == "650703"
    assert first_row["state"] == "EXECUTED"
    assert first_row["amount"] == "16210"
    assert first_row["currency_code"] == "PEN"


def test_load_xlsx_success(tmp_path, mock_excel_data):
    test_file = tmp_path / "operations.xlsx"
    df_write = pd.DataFrame(mock_excel_data)
    df_write.to_excel(test_file, index=False, engine="openpyxl")

    result = load_xlsx(test_file)

    assert isinstance(result, list)
    assert len(result) == 2

    first_row = result[0]
    assert first_row["id"] == 650703
    assert first_row["state"] == "EXECUTED"
    assert first_row["currency_code"] == "PEN"
