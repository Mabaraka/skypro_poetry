from collections import Counter
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по ключу 'date'.
    По умолчанию сортировка идет от новых к старым (убывание).
    """
    if not isinstance(data, list):
        raise ValueError("Data must be a list")

    if not data:
        return []

    def parse_date(date_value: Any) -> datetime:
        if not date_value:
            return datetime.min
        try:
            if isinstance(date_value, str):
                return datetime.fromisoformat(date_value)
            elif isinstance(date_value, datetime):
                return date_value
        except (ValueError, TypeError):
            return datetime.min
        return datetime.min

    return sorted(data, key=lambda x: parse_date(x.get("date")), reverse=reverse)


def process_bank_search(data, categories):
    """
    Подсчитывает количество банковских операций для каждой заданной категории
    с использованием collections.Counter.
    """
    descriptions = (operations.get("description") for operations in data if operations.get("description"))
    counts = Counter(descriptions)
    return {category: counts[category] for category in categories}
