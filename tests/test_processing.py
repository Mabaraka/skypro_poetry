from src.processing import filter_by_state, sort_by_date


def test_filter_by_state():
    assert filter_by_state("0") == 0


def test_sort_by_date():
    assert sort_by_date("0") == 0
