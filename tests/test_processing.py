import pytest

from src.processing import filter_by_state
from src.processing import process_bank_search
from src.processing import sort_by_date


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3, 5]),
        ("PENDING", [2, 6]),
        ("CANCELED", [4]),
        ("FAILED", []),
        ("", []),
    ],
)
def test_filter_parametrized(sample_transactions, state, expected_ids):
    """Основные случаи фильтрации одним параметризованным тестом."""
    result = filter_by_state(sample_transactions, state=state)
    assert [item["id"] for item in result] == expected_ids
    assert all(item["state"] == state for item in result)  # все элементы нужного статуса


def test_filter_default_state(sample_transactions):
    """Проверяем, что state по умолчанию — EXECUTED."""
    result = filter_by_state(sample_transactions)
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_empty_list(empty_transactions):
    result = filter_by_state(empty_transactions)
    assert result == []


def test_filter_missing_state_key(transactions_without_state):
    """Элементы без ключа 'state' не должны попадать в результат."""
    result = filter_by_state(transactions_without_state, state="EXECUTED")
    assert [item["id"] for item in result] == [2]


def test_filter_does_not_mutate(sample_transactions):
    original = sample_transactions.copy()
    filter_by_state(sample_transactions, state="EXECUTED")
    assert sample_transactions == original


@pytest.mark.parametrize(
    "reverse, expected_ids",
    [
        (True, [5, 6, 3, 1, 4, 2]),  # по убыванию
        (False, [2, 4, 1, 3, 6, 5]),  # по возрастанию
    ],
)
def test_sort_parametrized(transactions_for_sort, reverse, expected_ids):
    """Сортировка по убыванию и возрастанию одним параметризованным тестом."""
    result = sort_by_date(transactions_for_sort, reverse=reverse)
    assert [item["id"] for item in result] == expected_ids


def test_sort_default_is_descending(transactions_for_sort):
    """Параметр reverse=True по умолчанию."""
    result = sort_by_date(transactions_for_sort)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_empty_list(empty_transactions):
    assert sort_by_date(empty_transactions) == []


def test_sort_bad_dates_go_last(transactions_with_bad_dates):
    """Невалидные / отсутствующие даты уходят в конец при убывающей сортировке."""
    result = sort_by_date(transactions_with_bad_dates)
    ids = [item["id"] for item in result]
    # Валидные даты — первые два места
    assert ids[0] == 1  # 2024-03-15
    assert ids[1] == 5  # 2024-03-14
    assert set(ids[2:]) == {2, 3, 4}


def test_sort_datetime_objects(transactions_datetime_objects):
    """sort_by_date должен работать, когда date — объект datetime."""
    result = sort_by_date(transactions_datetime_objects)
    assert [item["id"] for item in result] == [4, 1, 3, 2]


def test_sort_does_not_mutate(transactions_for_sort):
    original = transactions_for_sort.copy()
    sort_by_date(transactions_for_sort)
    assert transactions_for_sort == original


def test_process_bank_search_standard(sample_operations):
    """Тест стандартного подсчета для существующих и отсутствующих категорий."""
    categories = ["Перевод организации", "Открытие вклада", "Перевод частному лицу"]

    result = process_bank_search(sample_operations, categories)

    assert result == {"Перевод организации": 2, "Открытие вклада": 1, "Перевод частному лицу": 0}


def test_process_bank_search_empty_data():
    """Тест работы функции с пустым списком операций."""
    categories = ["Перевод организации"]

    result = process_bank_search([], categories)

    assert result == {"Перевод организации": 0}


def test_process_bank_search_empty_categories(sample_operations):
    """Тест работы функции с пустым списком искомых категорий."""
    result = process_bank_search(sample_operations, [])

    assert result == {}


def test_process_bank_search_missing_description(sample_operations):
    """Тест, что функции не падают, если в данных есть None или отсутствует ключ."""
    categories = ["Покупка авиабилетов"]

    result = process_bank_search(sample_operations, categories)

    assert result == {"Покупка авиабилетов": 1}
