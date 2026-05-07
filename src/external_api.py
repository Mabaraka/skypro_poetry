import os

import requests
from dotenv import load_dotenv


def convert_currency(from_, amount_, to_="RUB"):
    """
    Метод использует Exchange Rates Data API
    для конвертации разного типа валют

    :param from_: из какой валюты
    :param amount_: количество
    :param to_: в какую валюту
    :return: float, итоговый amount
    """
    load_dotenv()
    api_key = os.getenv("APILayer_API_KEY")

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_}&from={from_}&amount={amount_}"
    headers = {"apikey": api_key}

    response = requests.get(url, headers=headers)

    return response.json().get("result")
