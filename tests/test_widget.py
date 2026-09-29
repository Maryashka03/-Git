import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "account_card, expected",
    [
        ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
        ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
        ("Счет 40817810099910004312", "Счет **4312"),
    ],
)
def test_mask_account_card(account_card, expected):
    assert mask_account_card(account_card) == expected


@pytest.fixture
def dates():
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59", "31.12.2023"),
        ("2020-01-01T00:00:00", "01.01.2020"),
    ]


def test_get_date(dates):
    for date_string, expected in dates:
        assert get_date(date_string) == expected


@pytest.mark.parametrize(
    "invalid_data",
    [
        "",
        "не дата",
        "2024",
    ],
)
def test_get_date_invalid(invalid_data):
    assert get_date(invalid_data) == "Некорректная дата"
