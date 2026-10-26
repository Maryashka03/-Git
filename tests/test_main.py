from src import main as main_module
from src.main import filter_by_currency, filter_by_status, sort_by_date

TRANSACTIONS = [
    {
        "state": "EXECUTED",
        "date": "2024-03-01",
        "operationAmount": {"currency": {"code": "RUB"}},
    },
    {
        "state": "CANCELED",
        "date": "2024-01-01",
        "operationAmount": {"currency": {"code": "USD"}},
    },
    {
        "state": "EXECUTED",
        "date": "2024-02-01",
        "operationAmount": {"currency": {"code": "RUB"}},
    },
]


def test_filter_by_status():
    result = filter_by_status(TRANSACTIONS, "executed")
    assert len(result) == 2


def test_filter_by_status_without_filter():
    assert filter_by_status(TRANSACTIONS, "") == TRANSACTIONS


def test_filter_by_currency():
    result = filter_by_currency(TRANSACTIONS)
    assert len(result) == 2


def test_sort_by_date_ascending():
    result = sort_by_date(TRANSACTIONS)
    assert [item["date"] for item in result] == [
        "2024-01-01",
        "2024-02-01",
        "2024-03-01",
    ]


def test_sort_by_date_descending():
    result = sort_by_date(TRANSACTIONS, ascending=False)
    assert [item["date"] for item in result] == [
        "2024-03-01",
        "2024-02-01",
        "2024-01-01",
    ]


def test_get_transactions_json(monkeypatch):
    expected = [{"description": "Перевод"}]
    monkeypatch.setattr(
        main_module, "load_transactions", lambda path: expected
    )

    assert main_module.get_transactions("data.json", "1") == expected


def test_get_transactions_csv(monkeypatch):
    expected = [{"description": "Покупка"}]
    monkeypatch.setattr(
        main_module, "read_csv_transactions", lambda path: expected
    )

    assert main_module.get_transactions("data.csv", "2") == expected


def test_get_transactions_excel(monkeypatch):
    expected = [{"description": "Оплата"}]
    monkeypatch.setattr(
        main_module, "read_excel_transactions", lambda path: expected
    )

    assert main_module.get_transactions("data.xlsx", "3") == expected


def test_get_transactions_unknown_format():
    assert main_module.get_transactions("data.txt", "4") == []


def test_main_invalid_format(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "4")

    main_module.main()

    assert "Неизвестный формат файла." in capsys.readouterr().out


def test_main_empty_file(monkeypatch, capsys):
    answers = iter(["1", "empty.json"])
    monkeypatch.setattr(
        "builtins.input", lambda prompt="": next(answers)
    )
    monkeypatch.setattr(main_module, "load_transactions", lambda path: [])

    main_module.main()

    assert "Операции не найдены" in capsys.readouterr().out


def test_main_success(monkeypatch, capsys):
    answers = iter(["1", "data.json", "", "нет", "нет", ""])
    monkeypatch.setattr(
        "builtins.input", lambda prompt="": next(answers)
    )
    monkeypatch.setattr(
        main_module,
        "load_transactions",
        lambda path: [{"description": "Перевод", "state": "EXECUTED"}],
    )

    main_module.main()

    output = capsys.readouterr().out
    assert "Найдено операций: 1" in output
    assert "Перевод" in output
