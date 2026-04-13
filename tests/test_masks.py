from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number():
    assert get_mask_card_number("0") == 0


def test_get_mask_account():
    assert get_mask_account("0") == 0
