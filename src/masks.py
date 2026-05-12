import logging
from typing import Union

logger = logging.getLogger(__name__)


def get_mask_card_number(card_number: str) -> str:
    """
    Принимает номер карты (строка) и возвращает маску в формате
    XXXX XX** **** XXXX, где X - это цифра номера.
    """
    if card_number is None:
        logger.error("Invalid card number")
        return "Invalid card number"

    n = str(card_number).strip()

    if not n or not n.isdigit():
        logger.error("Invalid card number")
        return "Invalid card number"

    if len(n) < 16:
        logger.error("Account number too short")
        return "Card number too short"

    logger.debug(f"Account number: {n}")
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
        logger.error("Invalid account number")
        return "Invalid account number"

    n = str(account).strip()

    if not n or not n.isdigit():
        logger.error("Invalid account number")
        return "Invalid account number"

    if len(n) < 4:
        logger.error("Account number too short")
        return "Account number too short"

    logger.debug(f"Account number: {n}")
    return f"**{n[-4:]}"
