from unittest.mock import patch

from src.readers import read_csv_transactions, read_excel_transactions


def test_read_csv_transactions() -> None:
    """Проверяет чтение CSV."""
    expected = [{"id": 1, "amount": 100}]

    with patch("src.readers.pd.read_csv") as mock:
        mock.return_value.to_dict.return_value = expected
        result = read_csv_transactions("transactions.csv")

    assert result == expected
    mock.assert_called_once_with(
        "transactions.csv", sep=None, engine="python"
    )


def test_read_excel_transactions() -> None:
    """Проверяет чтение Excel."""
    expected = [{"id": 1, "amount": 100}]

    with patch("src.readers.pd.read_excel") as mock:
        mock.return_value.to_dict.return_value = expected
        result = read_excel_transactions("transactions.xlsx")

    assert result == expected
    mock.assert_called_once_with("transactions.xlsx")


def test_read_csv_file_not_found() -> None:
    """Проверяет обработку отсутствующего CSV-файла."""
    with patch(
        "src.readers.pd.read_csv",
        side_effect=FileNotFoundError,
    ):
        assert read_csv_transactions("missing.csv") == []


def test_read_excel_file_not_found() -> None:
    """Проверяет обработку отсутствующего Excel-файла."""
    with patch(
        "src.readers.pd.read_excel",
        side_effect=FileNotFoundError,
    ):
        assert read_excel_transactions("missing.xlsx") == []
