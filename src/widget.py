import src.masks as masks


def mask_account_card(account_card: str) -> str:
    """
    :param account_card: строка, содержащая тип и номер карты или счета
    :return:возвращает строку с замаскированным номером
    Для карт и счетов используется разные типы маскировки
    """
    if 'Счет' in account_card:
        return f'Счет {masks.get_mask_account(int(account_card[5:]))}'
    else:
        card_number = ''.join([x for x in account_card if x.isdigit()])
        return f'{account_card.replace(card_number, '')}{masks.get_mask_card_number(int(card_number))}'
