from src.processing import filter_by_state, sort_by_date


OPERATIONS = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


def test_filter_by_state_default() -> None:
    result = filter_by_state(OPERATIONS)
    assert [item["state"] for item in result] == ["EXECUTED", "EXECUTED"]


def test_filter_by_state_canceled() -> None:
    result = filter_by_state(OPERATIONS, "CANCELED")
    assert [item["state"] for item in result] == ["CANCELED", "CANCELED"]


def test_filter_returns_new_list() -> None:
    assert filter_by_state(OPERATIONS) is not OPERATIONS


def test_sort_by_date_descending() -> None:
    result = sort_by_date(OPERATIONS)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending() -> None:
    result = sort_by_date(OPERATIONS, descending=False)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates)


def test_sort_returns_new_list() -> None:
    assert sort_by_date(OPERATIONS) is not OPERATIONS
