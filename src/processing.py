from typing import Any
from typing import Dict
from typing import List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    return [item for item in data if item.get("state") == state]
