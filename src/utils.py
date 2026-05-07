import json


def convert_json(json_path):
    """
    Принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о финансовых транзакциях

    :param json_path: Путь к JSON-файлу
    :type json_path: str
    """
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    if type(data) is not list:
        return []
    return data
