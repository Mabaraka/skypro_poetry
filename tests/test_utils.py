import json
from pathlib import Path
from unittest.mock import patch

from src.utils import convert_json
from src.utils import get_amount


def test_convert_json_success(tmp_path, json_transactions):
    tmp_file = tmp_path / "file.json"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(json_transactions, f, ensure_ascii=False)

    result = convert_json(str(tmp_file))

    assert result == json_transactions


def test_convert_json_wrong_path():
    path = Path("wrong_path")

    result = convert_json(str(path))

    assert not path.exists()
    assert result == []


def test_convert_json_empty_file(tmp_path):
    tmp_file = tmp_path / "file.json"
    tmp_file.touch()

    result = convert_json(str(tmp_file))

    assert tmp_file.exists()
    assert result == []


def test_convert_json_wrong_structure_format(tmp_path):
    tmp_file = tmp_path / "file.json"
    tmp_file.write_text(json.dumps({"a": 1, "b": 2}))

    result = convert_json(str(tmp_file))

    assert tmp_file.exists()
    assert result == []


def test_get_amount_rub(transaction_amount_rub):
    amount = get_amount(transaction_amount_rub)

    assert "RUB" == transaction_amount_rub.get("operationAmount").get("currency").get("code")
    assert amount == float(transaction_amount_rub.get("operationAmount").get("amount"))


def test_get_amount_eur(transaction_amount_eur, exchange_rate_data_eur):
    with patch("src.utils.convert_currency") as external_mock:
        external_mock.return_value = exchange_rate_data_eur.get("result")
        amount = get_amount(transaction_amount_eur)

        assert "EUR" == exchange_rate_data_eur.get("query").get("from")
        assert amount == exchange_rate_data_eur.get("result")


def test_get_amount_usd(transaction_amount_usd, exchange_rate_data_usd):
    with patch("src.utils.convert_currency") as external_mock:
        external_mock.return_value = exchange_rate_data_usd.get("result")
        amount = get_amount(transaction_amount_usd)

        assert "USD" == exchange_rate_data_usd.get("query").get("from")
        assert amount == exchange_rate_data_usd.get("result")
