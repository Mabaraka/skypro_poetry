import json

from src.external_api import convert_currency


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


def get_amount(transactions):
    """
    метод предстовляет из себя способ получить количество рублей
    из транзакции

    :param transactions: словарь представляющий транзакцию
    :return: float количество в рублях
    """
    currency_code = transactions.get("operationAmount").get("currency").get("code")
    amount = transactions.get("operationAmount").get("amount")

    if currency_code == "RUB":
        return float(amount)
    else:
        return convert_currency(currency_code, amount).get("result")
