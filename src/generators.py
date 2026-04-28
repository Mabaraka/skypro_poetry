from typing import Any
from typing import Dict
from typing import Generator
from typing import List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any], None, None]:
    """Функция возвращать итератор,
    который поочередно выдает транзакции,
     где валюта операции соответствует заданной"""
    for transaction in transactions:
        amount = transaction.get("operationAmount") or {}
        currency_data = amount.get("currency") or {}
        if currency_data.get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """принимает список словарей с транзакциями и возвращает описание каждой операции по очереди"""
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """выдает номера банковских карт в формате XXXX XXXX XXXX XXXX , где X — цифра номера карты.
    Генератор может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999.
     Генератор должен принимать начальное и конечное значения для генерации диапазона номеров."""
    for number in range(start, end + 1):
        s = f"{number:016}"
        yield f"{s[:4]} {s[4:8]} {s[8:12]} {s[12:16]}"
