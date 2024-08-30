import pytest
from marketmaster.common import get_number_suffix
from marketmaster.common import round_


def test_get_number_suffix_empty():
    with pytest.raises(ValueError):
        get_number_suffix("")


def test_get_number_suffix_with_period():
    with pytest.raises(ValueError):
        get_number_suffix("5.30")


def test_get_number_suffix_with_comma():
    with pytest.raises(ValueError):
        get_number_suffix("1,234")


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("1", ""),
        ("10", ""),
        ("100", ""),
        ("1000", "k"),
        ("10000", "k"),
        ("100000", "k"),
        ("1000000", "M"),
        ("10000000", "M"),
        ("100000000", "M"),
        ("1000000000", "B"),
        ("10000000000", "B"),
        ("100000000000", "B"),
        ("1000000000000", "T"),
        ("10000000000000", "T"),
        ("100000000000000", "T"),
    ],
)
def test_get_number_suffix(test_input: str, expected: str):
    assert get_number_suffix(test_input) == expected


def test_round__invalid():
    with pytest.raises(ValueError):
        round_("1.1.1")


def test_round__empty():
    with pytest.raises(ValueError):
        round_("")


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("379", "379"),
        ("182.5", "182.50"),
        ("1.445", "1.45"),
        ("2.675", "2.68"),
        ("1.995", "2"),
        ("1072", "1.07k"),
        ("10072", "10.07k"),
        ("7485275", "7.49M"),
        ("74852750", "74.85M"),
        ("748527500", "748.53M"),
    ],
)
def test_round_(test_input: str, expected: str):
    assert round_(test_input) == expected
