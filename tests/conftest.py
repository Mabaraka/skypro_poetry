from datetime import datetime
from typing import Any
from typing import Dict
from typing import List

import pytest


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    return []


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-15", "amount": 1000},
        {"id": 2, "state": "PENDING", "date": "2024-03-14", "amount": 500},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-13", "amount": 750},
        {"id": 4, "state": "CANCELED", "date": "2024-03-12", "amount": 200},
        {"id": 5, "state": "EXECUTED", "date": "2024-03-11", "amount": 1500},
        {"id": 6, "state": "PENDING", "date": "2024-03-10", "amount": 300},
    ]


@pytest.fixture
def transactions_without_state() -> List[Dict[str, Any]]:
    """Часть элементов не имеет ключа 'state'."""
    return [
        {"id": 1, "date": "2024-03-15"},
        {"id": 2, "state": "EXECUTED", "date": "2024-03-14"},
        {"id": 3, "date": "2024-03-13"},
    ]


@pytest.fixture
def transactions_for_sort() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "date": "2024-03-15", "state": "EXECUTED"},
        {"id": 2, "date": "2024-01-10", "state": "PENDING"},
        {"id": 3, "date": "2024-06-20", "state": "EXECUTED"},
        {"id": 4, "date": "2024-03-01", "state": "CANCELED"},
        {"id": 5, "date": "2024-12-31", "state": "EXECUTED"},
        {"id": 6, "date": "2024-09-15", "state": "PENDING"},
    ]


@pytest.fixture
def transactions_with_bad_dates() -> List[Dict[str, Any]]:
    """Смесь валидных, невалидных дат и отсутствующих ключей."""
    return [
        {"id": 1, "date": "2024-03-15"},  # валидная
        {"id": 2, "date": "invalid-date"},  # невалидная строка
        {"id": 3, "date": None},  # None
        {"id": 4},  # нет ключа
        {"id": 5, "date": "2024-03-14"},  # валидная
    ]


@pytest.fixture
def transactions_datetime_objects() -> List[Dict[str, Any]]:
    """date хранится как объект datetime."""
    return [
        {"id": 1, "date": datetime(2024, 3, 15, 10, 30)},
        {"id": 2, "date": datetime(2024, 3, 14, 15, 45)},
        {"id": 3, "date": datetime(2024, 3, 15, 8, 0)},
        {"id": 4, "date": datetime(2024, 3, 16, 12, 0)},
    ]


@pytest.fixture
def transactions_with_currency() -> List[Dict[str, Any]]:
    """транзакции с включенным словарем operationAmount, в котором хранятся валюта"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-03-15",
            "operationAmount": {"amount": 1000, "currency": {"name": "USD", "code": "USD"}},
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2024-03-16",
            "operationAmount": {"amount": 1200, "currency": {"name": "RUB", "code": "RUB"}},
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-03-17",
            "operationAmount": {"amount": 1220, "currency": {"name": "JIN", "code": "JIN"}},
        },
        {
            "id": 4,
            "state": "EXECUTED",
            "date": "2025-03-17",
            "operationAmount": {"amount": 13320, "currency": {"name": "USD", "code": "USD"}},
        },
        {"id": 5, "state": "EXECUTED", "date": "2026-03-17", "operationAmount": {"amount": 0, "currency": None}},
        {"id": 6, "state": "EXECUTED", "date": "2026-03-18", "operationAmount": None},
        {"id": 6, "state": "EXECUTED", "date": "2026-03-18"},
    ]


@pytest.fixture
def transaction_with_descriptions() -> List[Dict[str, Any]]:
    """транзакции с описаниями"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-15", "description": "первая транзакция"},
        {"id": 2, "state": "EXECUTED", "date": "2024-03-16", "description": "вторая транзакция"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-17", "description": "третья транзакция"},
        {"id": 4, "state": "EXECUTED", "date": "2025-03-17", "description": None},
        {"id": 5, "state": "EXECUTED", "date": "2026-03-18"},
    ]
