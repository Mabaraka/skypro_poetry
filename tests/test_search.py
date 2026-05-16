import pytest

from src.search import process_bank_search


@pytest.mark.parametrize(
    "pattern, expected_ids",
    [
        ("первая", [1]),
        ("ВТОРАЯ", [2]),
        ("транзакция", [1, 2, 3]),
        ("", [1, 2, 3, 4, 5]),
        ("четвертая", []),
    ],
)
def test_process_bank_search(transaction_with_descriptions, pattern, expected_ids):
    filtered_op = process_bank_search(transaction_with_descriptions, pattern)
    ids = [op["id"] for op in filtered_op]
    assert ids == expected_ids


@pytest.mark.parametrize(
    "corrupted_data, search, expected",
    [
        ([], "транзакция", []),
        (
            [{"id": 10, "description": "Перевод другу (Иван) +7999..."}],
            "другу (иван)",
            [{"id": 10, "description": "Перевод другу (Иван) +7999..."}],
        ),
    ],
)
def test_process_bank_search_edge_cases(corrupted_data, search, expected):
    assert process_bank_search(corrupted_data, search) == expected


def test_process_bank_search_missing_description_field():
    invalid_data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "amount": 100}]
    assert process_bank_search(invalid_data, "текст") == []
