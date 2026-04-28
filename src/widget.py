from datetime import datetime

import src.masks as masks


def mask_account_card(account_card: str) -> str:
    """
    Принимает строку, содержащую тип и номер карты или счета,
    и возвращает строку с замаскированным номером.
    """
    if not account_card or not isinstance(account_card, str):
        return "Invalid input"

    if account_card.startswith("Счет"):
        account_number = "".join([x for x in account_card if x.isdigit()])
        if not account_number:
            return "Invalid account format"

        masked_number = masks.get_mask_account(account_number)
        return f"Счет {masked_number}"

    else:
        card_number = "".join([x for x in account_card if x.isdigit()])
        if not card_number:
            return "Invalid card format"

        card_type = "".join([x for x in account_card if not x.isdigit()]).strip()

        masked_number = masks.get_mask_card_number(card_number)

        return f"{card_type} {masked_number}"


def get_date(iso_date: str) -> str:
    """
    Преобразует дату из ISO формата в формат "ДД.ММ.ГГГГ"

    Args:
        iso_date: строка с датой в формате ISO

    Returns:
        строка с датой в формате "ДД.ММ.ГГГГ" или сообщение об ошибке
    """
    if not iso_date or not isinstance(iso_date, str):
        return "Invalid date format"

    iso_date = iso_date.strip()
    if not iso_date:
        return "Invalid date format"

    try:
        date_obj = datetime.fromisoformat(iso_date)
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        return "Invalid date format"
