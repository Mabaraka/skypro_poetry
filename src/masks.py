from typing import Union


def get_mask_card_number(card_number: str) -> str:
    """
    Принимает номер карты (строка) и возвращает маску в формате
    XXXX XX** **** XXXX, где X - это цифра номера.
    """
    if not card_number or not card_number.isdigit():
        return "Invalid card number"

    n = card_number.strip()
    if len(n) < 16:
        return "Card number too short"

    return f"{n[:4]} {n[4:6]}** **** {n[-4:]}"


def get_mask_account(account: Union[str, int]) -> str:
    """
    Принимает номер счета (строка) и возвращает маску в формате
    **XXXX, где X - это цифра номера.
    Видны только последние 4 цифры счета.

    Args:
        account: номер счета в виде строки (может содержать только цифры)

    Returns:
        замаскированный номер счета в формате **XXXX или сообщение об ошибке
    """
    if account is None:
        return "Invalid account number"

    n = str(account).strip()

    if not n or not n.isdigit():
        return "Invalid account number"

    if len(n) < 4:
        return "Account number too short"

    return f"**{n[-4:]}"
