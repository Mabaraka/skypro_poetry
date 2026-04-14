import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        # Валидные случаи
        ("1234567890123456", "1234 56** **** 3456"),
        ("1111222233334444", "1111 22** **** 4444"),
        ("0012345678901234", "0012 34** **** 1234"),
        ("0000111122223333", "0000 11** **** 3333"),
        ("9999999999999999", "9999 99** **** 9999"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("123456789012345678", "1234 56** **** 5678"),  # 18 цифр
        ("1234567890123456789", "1234 56** **** 6789"),  # 19 цифр
        ("  1234567890123456  ", "1234 56** **** 3456"),  # с пробелами
        # Невалидные случаи (короткие номера)
        ("123456789012", "Card number too short"),
        ("123456789012345", "Card number too short"),
        ("1", "Card number too short"),
        ("000000000000000", "Card number too short"),
        # Невалидные случаи (нецифровые символы)
        ("", "Invalid card number"),
        ("1234 5678 9012 3456", "Invalid card number"),
        ("1234-5678-9012-3456", "Invalid card number"),
        ("1234abcd90123456", "Invalid card number"),
        ("!@#$%^&*()", "Invalid card number"),
        ("     ", "Invalid card number"),
        ("12AB34CD56EF78GH", "Invalid card number"),
    ],
)
def test_get_mask_card_number(card_number, expected):
    """Параметризованный тест для всех случаев"""
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_with_none():
    """Отдельный тест для None"""
    assert get_mask_card_number(None) == "Invalid card number"


@pytest.mark.parametrize(
    "account, expected",
    [
        # Валидные случаи
        ("1234567890", "**7890"),
        ("40817810099910004312", "**4312"),
        ("12345", "**2345"),
        ("1234", "**1234"),
        ("0000", "**0000"),
        ("9999", "**9999"),
        ("001234", "**1234"),
        ("00001234", "**1234"),
        ("12340000", "**0000"),
        ("1000", "**1000"),
        ("  1234567890  ", "**7890"),
        ("\t1234567890\n", "**7890"),
        ("1" * 50, "**" + "1" * 4),
        # Короткие номера (меньше 4 цифр)
        ("123", "Account number too short"),
        ("1", "Account number too short"),
        ("0", "Account number too short"),
        ("00", "Account number too short"),
        # Невалидные случаи (нецифровые символы)
        ("", "Invalid account number"),
        ("1234 5678 90", "Invalid account number"),
        ("1234-5678-90", "Invalid account number"),
        ("1234abcd90", "Invalid account number"),
        ("account1234", "Invalid account number"),
        ("!@#$%^&*()", "Invalid account number"),
        ("123!@#", "Invalid account number"),
        ("     ", "Invalid account number"),
        ("\t\n\r", "Invalid account number"),
        ("-1234567890", "Invalid account number"),
        ("12345.67", "Invalid account number"),
        ("12 34", "Invalid account number"),
    ],
)
def test_get_mask_account(account, expected):
    """Параметризованный тест для всех случаев"""
    assert get_mask_account(account) == expected


@pytest.mark.parametrize(
    "account, expected",
    [
        (1234567890, "**7890"),  # int -> будет преобразован в строку
        (1234, "**1234"),
        (0, "Account number too short"),  # "0" - слишком короткий
        (1000, "**1000"),
        (9999, "**9999"),
    ],
)
def test_get_mask_account_with_int_input(account, expected):
    """Тест с передачей int вместо str"""
    assert get_mask_account(account) == expected


def test_get_mask_account_with_none():
    """Отдельный тест для None"""
    assert get_mask_account(None) == "Invalid account number"
