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


@pytest.fixture
def json_transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
    ]


@pytest.fixture
def transaction_amount_rub() -> Dict[str, Any]:
    return {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    }


@pytest.fixture
def transaction_amount_usd() -> Dict[str, Any]:
    return {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2010-02-22T02:08:58.425572",
        "operationAmount": {"amount": "50", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }


@pytest.fixture
def transaction_amount_eur() -> Dict[str, Any]:
    return {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2010-02-22T02:08:58.425572",
        "operationAmount": {"amount": "50", "currency": {"name": "EUR", "code": "EUR"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }


@pytest.fixture
def exchange_rate_data_usd() -> Dict[str, Any]:
    return {
        "date": "2010-02-22",
        "historical": "",
        "info": {"rate": 30, "timestamp": 1519328414},
        "query": {"amount": 50, "from": "USD", "to": "RUB"},
        "result": 1500,
        "success": "true",
    }


@pytest.fixture
def exchange_rate_data_eur() -> Dict[str, Any]:
    return {
        "date": "2010-02-22",
        "historical": "",
        "info": {"rate": 40, "timestamp": 1519328414},
        "query": {"amount": 50, "from": "EUR", "to": "RUB"},
        "result": 2000,
        "success": "true",
    }


@pytest.fixture
def csv_content():
    return (
        "id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "650703;EXECUTED;2023-09-05;16210;Sol;PEN;Счет 58803664561291;Счет 3974;Перевод организации\n"
        "5380041;CANCELED;2021-02-01T11:54:58Z;23789;Peso;UYU;;Счет 23294994494356835683;Открытие вклада"
    )


@pytest.fixture
def mock_excel_data():
    return {
        "id": [650703, 5380041],
        "state": ["EXECUTED", "CANCELED"],
        "date": ["2023-09-05T11:30:32Z", "2021-02-01T11:54:58Z"],
        "amount": [16210, 23789],
        "currency_name": ["Sol", "Peso"],
        "currency_code": ["PEN", "UYU"],
        "from": ["Счет 58803664561298323391", None],  # Пустое значение
        "to": ["Счет 39745660563456619397", "Счет 23294994494356835683"],
        "description": ["Перевод организации", "Открытие вклада"],
    }
