from datetime import datetime

import src.masks as masks


def mask_account_card(account_card: str) -> str:
    """
    :param account_card: строка, содержащая тип и номер карты или счета
    :return:возвращает строку с замаскированным номером
    Для карт и счетов используется разные типы маскировки
    """
    if "Счет" in account_card:
        return f"Счет {masks.get_mask_account(int(account_card[5:]))}"
    else:
        card_number = "".join([x for x in account_card if x.isdigit()])
        return f"{account_card.replace(card_number, '')}{masks.get_mask_card_number(int(card_number))}"


def get_date(iso_date: str) -> str:
    """
    :param iso_date: строка с датой в формате ISO
    :return: строка с датой в формате "ДД.ММ.ГГГГ"
    """
    date_obj = datetime.fromisoformat(iso_date)
    return date_obj.strftime("%d.%m.%Y")
