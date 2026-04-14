from unittest.mock import patch

import pytest

from src.widget import get_date
from src.widget import mask_account_card


@pytest.mark.parametrize(
    "input_data, expected",
    [
        # Счета
        ("Счет 40817810099910004312", "Счет **4312"),
        ("Счет 1234", "Счет **1234"),
        # Карты
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
        # Ошибки
        ("", "Invalid input"),
        (None, "Invalid input"),
        (12345, "Invalid input"),
        ("Счет", "Invalid account format"),
        ("Visa", "Invalid card format"),
    ],
)
def test_mask_account_card(input_data, expected):
    with patch("src.widget.masks.get_mask_account") as mock_acc, patch(
        "src.widget.masks.get_mask_card_number"
    ) as mock_card:

        if isinstance(input_data, str) and input_data.startswith("Счет"):
            mock_acc.return_value = expected.split()[-1]
        elif isinstance(input_data, str):
            mock_card.return_value = " ".join(expected.split()[-4:])

        assert mask_account_card(input_data) == expected


@pytest.mark.parametrize(
    "iso_date, expected",
    [
        ("2024-03-15", "15.03.2024"),
        ("2024-03-15T14:30:00", "15.03.2024"),  # со временем
        ("2024-03-15T14:30:45.123456", "15.03.2024"),  # с миллисекундами
        ("2024-03-15T14:30:00+03:00", "15.03.2024"),  # с timezone
        ("2024-02-29", "29.02.2024"),  # високосный год
        ("2024-01-01", "01.01.2024"),  # начало года
        ("2024-12-31", "31.12.2024"),  # конец года
    ],
)
def test_get_date_valid(iso_date, expected):
    assert get_date(iso_date) == expected


@pytest.mark.parametrize(
    "iso_date",
    [
        "",
        "   ",
        "invalid-date",
        "2024-13-45",
        "15.03.2024",  # формат DD.MM.YYYY — не ISO
        "03/15/2024",
    ],
)
def test_get_date_invalid(iso_date):
    """Невалидный ввод возвращает строку с ошибкой (не выбрасывает исключение)."""
    result = get_date(iso_date)
    assert "Invalid" in result


def test_get_date_none():
    assert "Invalid" in get_date(None)


def test_get_date_output_format():
    """Структура вывода: ДД.ММ.ГГГГ."""
    result = get_date("2024-03-15")
    day, month, year = result.split(".")
    assert day == "15" and month == "03" and year == "2024"
    assert len(result) == 10
