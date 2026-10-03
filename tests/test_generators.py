import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)


@pytest.fixture
def transactions():
    """Создает тестовые данные с транзакциями."""
    return [
        {
            "id": 1,
            "operationAmount": {
                "currency": {
                    "code": "USD",
                },
            },
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "operationAmount": {
                "currency": {
                    "code": "EUR",
                },
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 3,
            "operationAmount": {
                "currency": {
                    "code": "USD",
                },
            },
            "description": "Перевод с карты на карту",
        },
    ]


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [1, 3]),
        ("EUR", [2]),
        ("GBP", []),
    ],
)
def test_filter_by_currency(transactions, currency, expected_ids):
    """Проверяет фильтрацию транзакций по валюте."""
    result = list(filter_by_currency(transactions, currency))

    assert [transaction["id"] for transaction in result] == expected_ids


def test_filter_by_currency_empty_list():
    """Проверяет работу с пустым списком транзакций."""
    assert list(filter_by_currency([], "USD")) == []


def test_transaction_descriptions(transactions):
    """Проверяет получение описаний транзакций."""
    result = list(transaction_descriptions(transactions))

    assert result == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
    ]


def test_transaction_descriptions_empty_list():
    """Проверяет работу с пустым списком."""
    assert list(transaction_descriptions([])) == []


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (
            1,
            3,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
            ],
        ),
        (
            9999999999999998,
            9999999999999999,
            [
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
            ],
        ),
    ],
)
def test_card_number_generator(start, stop, expected):
    """Проверяет генерацию номеров карт."""
    assert list(card_number_generator(start, stop)) == expected


def test_card_number_generator_single_number():
    """Проверяет генерацию одного номера карты."""
    assert list(card_number_generator(1, 1)) == [
        "0000 0000 0000 0001"
    ]


def test_card_number_generator_empty_range():
    """Проверяет пустой диапазон."""
    assert list(card_number_generator(5, 1)) == []
