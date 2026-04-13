from src.widget import mask_account_card, get_date


def test_mask_account_card():
    assert mask_account_card(get_date("0")) == "0"


def test_get_date():
    assert get_date("0") == 0
