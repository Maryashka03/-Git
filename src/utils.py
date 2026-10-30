from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "Дата операции",
    "Статус",
    "Сумма операции",
    "Валюта операции",
    "Номер карты",
    "Кэшбэк",
    "Категория",
    "Описание",
]


def load_transactions(file_path: str | Path) -> pd.DataFrame:
    """Загружает банковские операции из Excel-файла."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    transactions = pd.read_excel(path)

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in transactions.columns
    ]

    if missing_columns:
        raise ValueError(
            f"В файле отсутствуют столбцы: {missing_columns}"
        )

    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        dayfirst=True,
        errors="coerce",
    )

    transactions["Сумма операции"] = pd.to_numeric(
        transactions["Сумма операции"],
        errors="coerce",
    )

    transactions["Кэшбэк"] = pd.to_numeric(
        transactions["Кэшбэк"],
        errors="coerce",
    ).fillna(0)

    return transactions


def get_successful_transactions(
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    """Возвращает только успешно выполненные операции."""
    return transactions[
        transactions["Статус"] == "OK"
    ].copy()
