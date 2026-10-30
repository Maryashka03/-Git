import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category():
    """Проверяет поиск расходов за три месяца."""
    transactions = pd.DataFrame({
        "Дата операции": pd.to_datetime([
            "2021-12-01",
            "2021-10-01",
            "2021-05-01",
        ]),
        "Статус": ["OK", "OK", "OK"],
        "Сумма операции": [-100, -200, -300],
        "Категория": [
            "Супермаркеты",
            "Супермаркеты",
            "Супермаркеты",
        ],
    })

    result = spending_by_category(
        transactions,
        "Супермаркеты",
        "31.12.2021",
    )

    assert len(result) == 2
    assert result["Сумма операции"].sum() == -300


def test_spending_by_category_excludes_income():
    """Проверяет, что пополнения не входят в расходы."""
    transactions = pd.DataFrame({
        "Дата операции": pd.to_datetime([
            "2021-12-01",
            "2021-12-02",
        ]),
        "Статус": ["OK", "OK"],
        "Сумма операции": [-100, 500],
        "Категория": ["Супермаркеты", "Супермаркеты"],
    })

    result = spending_by_category(
        transactions,
        "Супермаркеты",
        "31.12.2021",
    )

    assert len(result) == 1
    assert result.iloc[0]["Сумма операции"] == -100
