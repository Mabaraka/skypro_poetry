from unittest.mock import patch

import pytest

from src.widget import get_date
from src.widget import mask_account_card


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        # Счета
        ("Счет 40817810099910004312", "Счет **4312"),
        ("Счет 1234567890", "Счет **7890"),
        ("Счет 1234", "Счет **1234"),
        ("Счет 00001234", "Счет **1234"),
        # Карты
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
        ("Visa 0012345678901234", "Visa 0012 34** **** 1234"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
        ("American Express 1234567890123456", "American Express 1234 56** **** 3456"),
        ("MasterCard Gold 1234567890123456", "MasterCard Gold 1234 56** **** 3456"),
        # Ошибки
        ("", "Invalid input"),
        (None, "Invalid input"),
        (12345, "Invalid input"),
        ("Счет", "Invalid account format"),
        ("Visa", "Invalid card format: no card number found"),
    ],
)
def test_mask_account_card_parametrized(input_data, expected_output):
    """Параметризованный тест для всех случаев"""
    with patch("src.widget.masks.get_mask_account") as mock_acc:
        with patch("src.widget.masks.get_mask_card_number") as mock_card:
            if isinstance(input_data, str) and input_data.startswith("Счет"):
                mock_acc.return_value = expected_output.split()[-1]
            elif isinstance(input_data, str) and not input_data.startswith("Счет"):
                mock_card.return_value = " ".join(expected_output.split()[-4:])

            result = mask_account_card(input_data)
            assert result == expected_output


def test_get_date():
    assert get_date("0") == 0
