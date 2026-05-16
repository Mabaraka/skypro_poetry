import csv

import pandas as pd


def load_csv(path):
    """
    функция для считывания финансовых операций из CSV
    :param path: Путь до файла
    :return: Список словарей с транзакциями
    """
    with open(path, "r", encoding="utf-8") as csvfile:
        dict_reader = csv.DictReader(csvfile, delimiter=";")
        return list(dict_reader)


def load_xlsx(path):
    """
    Функция для считывания финансовых операций из Excel
    :param path: Путь до файла
    :return: Список словарей с транзакциями
    """
    df = pd.read_excel(path)
    return df.to_dict(orient="records")
