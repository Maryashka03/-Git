import pandas as pd
import pytest

from src.utils import load_transactions, get_successful_transactions


def test_load_transactions(tmp_path):
    """Проверяет загрузку Excel-файла."""
    data = {
        "Дата операции": ["01.01.2021"],
        "Статус": ["OK"],
        "Сумма операции": [-100],
        "Валюта операции": ["RUB"],
        "Номер карты": ["*1234"],
        "Кэшбэк": [5],
        "Категория": ["Супермаркеты"],
        "Описание": ["Покупка"],
    }

    file_path = tmp_path / "operations.xlsx"
    pd.DataFrame(data).to_excel(file_path, index=False)

    result = load_transactions(file_path)

    assert len(result) == 1
    assert result.iloc[0]["Сумма операции"] == -100


def test_load_transactions_file_not_found():
    """Проверяет ошибку при отсутствии файла."""
    with pytest.raises(FileNotFoundError):
        load_transactions("missing_file.xlsx")


def test_load_transactions_missing_columns(tmp_path):
    """Проверяет отсутствие обязательных столбцов."""
    file_path = tmp_path / "wrong.xlsx"
    pd.DataFrame({"Название": ["Тест"]}).to_excel(
        file_path,
        index=False,
    )

    with pytest.raises(ValueError):
        load_transactions(file_path)


def test_get_successful_transactions():
    """Проверяет отбор успешных операций."""
    data = pd.DataFrame({
        "Статус": ["OK", "FAILED", "OK"],
        "Сумма операции": [-100, -200, -300],
    })

    result = get_successful_transactions(data)

    assert len(result) == 2
    assert all(result["Статус"] == "OK")
