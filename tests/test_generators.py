import pytest

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [1, 4]),
        ("EUR", []),
        ("RUB", [2]),
    ],
)
def test_filter_by_currency(transactions_with_currency, currency, expected_ids):
    result = list(filter_by_currency(transactions_with_currency, currency))
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_currency_empty_list(empty_transactions):
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert result == []


def test_transaction_descriptions(transaction_with_descriptions):
    result = transaction_descriptions(transaction_with_descriptions)

    assert next(result) == "первая транзакция"
    assert next(result) == "вторая транзакция"
    assert next(result) == "третья транзакция"


def test_transaction_descriptions_empty_list(empty_transactions):
    result = transaction_descriptions(empty_transactions)
    with pytest.raises(StopIteration):
        next(result)


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (1234567812345008, 1234567812345009, ["1234 5678 1234 5008", "1234 5678 1234 5009"]),
        (1, 1, ["0000 0000 0000 0001"]),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
        (100, 10, []),
    ],
)
def test_card_number_generator(start, end, expected):
    result = list(card_number_generator(start, end))
    assert result == expected
