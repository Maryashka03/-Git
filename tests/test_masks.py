import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567812345678", "1234 56** **** 5678"),
        ("1234 5678 1234 5678", "1234 56** **** 5678"),
        ("0000111122223333", "0000 11** **** 3333"),
    ],
)
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("40817810099910004312", "**4312"),
        ("1234567890", "**7890"),
        ("0000", "**0000"),
    ],
)
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected


@pytest.fixture
def invalid_numbers():
    return ["123", "", "abc"]


def test_get_mask_card_number_invalid(invalid_numbers):
    for number in invalid_numbers:
        assert get_mask_card_number(number) == "Некорректный номер карты"


def test_get_mask_account_invalid(invalid_numbers):
    for number in invalid_numbers:
        assert get_mask_account(number) == "Некорректный номер счета"
