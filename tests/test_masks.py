import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        # Валидные — стандартная длина (16 цифр)
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("9999999999999999", "9999 99** **** 9999"),
        # Валидные — длина > 16 (берутся первые 6 и последние 4)
        ("123456789012345678", "1234 56** **** 5678"),  # 18 цифр
        ("1234567890123456789", "1234 56** **** 6789"),  # 19 цифр
        # Пробелы вокруг — допустимы
        ("  1234567890123456  ", "1234 56** **** 3456"),
        # Слишком короткие номера (< 16 цифр)
        ("123456789012", "Card number too short"),  # 12 цифр
        ("123456789012345", "Card number too short"),  # 15 цифр
        ("1", "Card number too short"),
        # Невалидные значения
        ("", "Invalid card number"),
        ("1234 5678 9012 3456", "Invalid card number"),  # пробелы внутри
        ("1234-5678-9012-3456", "Invalid card number"),
        ("1234abcd90123456", "Invalid card number"),
        ("!@#$%^&*()", "Invalid card number"),
        (None, "Invalid card number"),
    ],
)
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account, expected",
    [
        # Валидные строки
        ("1234567890", "**7890"),
        ("40817810099910004312", "**4312"),
        ("1234", "**1234"),
        ("0000", "**0000"),
        ("00001234", "**1234"),  # ведущие нули
        ("  1234567890  ", "**7890"),  # пробелы вокруг
        # Валидные int
        (1234567890, "**7890"),
        (1234, "**1234"),
        (1000, "**1000"),
        # Слишком короткие (< 4 цифры)
        ("123", "Account number too short"),
        ("1", "Account number too short"),
        ("00", "Account number too short"),
        (0, "Account number too short"),  # "0" после strip — длина 1
        # Невалидные значения
        ("", "Invalid account number"),
        ("1234 5678 90", "Invalid account number"),  # пробелы внутри
        ("1234-5678", "Invalid account number"),
        ("1234abcd", "Invalid account number"),
        ("!@#$%^&*()", "Invalid account number"),
        ("-1234567890", "Invalid account number"),
        ("12345.67", "Invalid account number"),
        (None, "Invalid account number"),
    ],
)
def test_get_mask_account(account, expected):
    assert get_mask_account(account) == expected
