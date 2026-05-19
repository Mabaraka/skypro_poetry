import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Фильтрует список банковских операций по наличию строки поиска в описании.
    Использует re.search для гибкого поиска (по умолчанию регистронезависимый).
    """
    if not search:
        return data

    filtered_op = []
    pattern = re.escape(search)
    for op in data:
        description = op.get("description", "")
        if type(description) is str and re.search(pattern, description, re.IGNORECASE):
            filtered_op.append(op)

    return filtered_op
