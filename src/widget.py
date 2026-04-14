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
    :param iso_date: строка с датой в формате ISO
    :return: строка с датой в формате "ДД.ММ.ГГГГ"
    """
    date_obj = datetime.fromisoformat(iso_date)
    return date_obj.strftime("%d.%m.%Y")
