import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def operations():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-02"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-03"},
    ]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(operations, state, expected_ids):
    result = filter_by_state(operations, state)
    assert [operation["id"] for operation in result] == expected_ids


def test_filter_by_state_default(operations):
    result = filter_by_state(operations)
    assert [operation["id"] for operation in result] == [1, 3]


def test_filter_by_state_returns_new_list(operations):
    result = filter_by_state(operations)
    assert result is not operations


@pytest.mark.parametrize(
    "descending, expected_ids",
    [
        (True, [3, 2, 1]),
        (False, [1, 2, 3]),
    ],
)
def test_sort_by_date(operations, descending, expected_ids):
    result = sort_by_date(operations, descending=descending)
    assert [operation["id"] for operation in result] == expected_ids


def test_sort_by_date_empty_list():
    assert sort_by_date([]) == []


def test_sort_by_date_returns_new_list(operations):
    result = sort_by_date(operations)
    assert result is not operations


def test_sort_by_date_without_date():
    operations = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-02"},
    ]
    result = sort_by_date(operations)
    assert [operation["id"] for operation in result] == [2, 1]
