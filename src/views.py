import json
from pathlib import Path
from typing import Any, cast

import pandas as pd

SETTINGS_PATH = (
    Path(__file__).resolve().parent.parent / "user_settings.json"
)


def get_greeting(current_hour: int) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    if 6 <= current_hour < 12:
        return "Доброе утро"
    if 12 <= current_hour < 18:
        return "Добрый день"
    if 18 <= current_hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def load_user_settings() -> dict[str, Any]:
    """Загружает пользовательские настройки валют и акций."""
    if not SETTINGS_PATH.exists():
        return {
            "user_currencies": [],
            "user_stocks": [],
        }

    with open(SETTINGS_PATH, "r", encoding="utf-8") as file:
        return cast(dict[str, Any], json.load(file))


def main_page(
    transactions: pd.DataFrame,
    date_time: str,
    currency_rates: dict | None = None,
    stock_prices: dict | None = None,
) -> str:
    """Формирует данные главной страницы приложения."""
    current_date = pd.to_datetime(date_time, dayfirst=True)
    greeting = get_greeting(current_date.hour)

    settings = load_user_settings()

    currency_rates = currency_rates or {}
    stock_prices = stock_prices or {}

    data = transactions.copy()

    data["Дата операции"] = pd.to_datetime(
        data["Дата операции"],
        errors="coerce",
    )

    data["Сумма операции"] = pd.to_numeric(
        data["Сумма операции"],
        errors="coerce",
    )

    data = data[
        (data["Статус"] == "OK")
        & (data["Дата операции"] <= current_date)
    ].copy()

    # Информация по картам
    cards = []
    card_data = data.dropna(subset=["Номер карты"])

    for card_number, group in card_data.groupby("Номер карты"):
        expenses = group.loc[
            group["Сумма операции"] < 0,
            "Сумма операции",
        ].abs().sum()

        cashback = group["Кэшбэк"].fillna(0).sum()

        cards.append({
            "last_digits": str(card_number)[-4:],
            "total_spent": round(float(expenses), 2),
            "cashback": round(float(cashback), 2),
        })

    # Пять операций с наибольшей суммой
    top_transactions = data.sort_values(
        by="Сумма операции",
        ascending=False,
    ).head(5)

    result_transactions = []

    for _, row in top_transactions.iterrows():
        result_transactions.append({
            "date": row["Дата операции"].strftime("%d.%m.%Y"),
            "amount": round(float(row["Сумма операции"]), 2),
            "category": (
                str(row["Категория"])
                if pd.notna(row["Категория"])
                else "Без категории"
            ),
            "description": str(row["Описание"]),
        })

    # Курсы выбранных валют
    currencies = []

    for currency in settings.get("user_currencies", []):
        rate = currency_rates.get(currency)

        if isinstance(rate, (int, float)) and rate > 0:
            currencies.append({
                "currency": currency,
                "rate": float(rate),
            })

    # Цены выбранных акций
    stocks = []

    for stock in settings.get("user_stocks", []):
        price = stock_prices.get(stock)

        if isinstance(price, (int, float)) and price > 0:
            stocks.append({
                "stock": stock,
                "price": float(price),
            })

    result = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": result_transactions,
        "currencies": currencies,
        "stocks": stocks,
    }

    return json.dumps(result, ensure_ascii=False, indent=4)


def events_page(
    transactions: pd.DataFrame,
    date_time: str,
    period: str = "M",
    currency_rates: dict | None = None,
    stock_prices: dict | None = None,
) -> str:
    """Формирует страницу с расходами и доходами за выбранный период."""

    current_date = pd.to_datetime(date_time, dayfirst=True)
    data = transactions.copy()

    data["Дата операции"] = pd.to_datetime(
        data["Дата операции"],
        errors="coerce",
    )
    data["Сумма операции"] = pd.to_numeric(
        data["Сумма операции"],
        errors="coerce",
    )

    if period == "W":
        start_date = current_date - pd.Timedelta(days=7)
    elif period == "M":
        start_date = current_date.replace(day=1)
    elif period == "Y":
        start_date = current_date.replace(
            month=1,
            day=1,
        )
    elif period == "ALL":
        start_date = data["Дата операции"].min()
    else:
        raise ValueError("Период должен быть W, M, Y или ALL")

    data = data[
        (data["Статус"] == "OK")
        & (data["Дата операции"] >= start_date)
        & (data["Дата операции"] <= current_date)
    ].copy()

    expenses = data[data["Сумма операции"] < 0].copy()
    incomes = data[data["Сумма операции"] > 0].copy()

    expenses["Сумма операции"] = expenses["Сумма операции"].abs()

    special_categories = ["Переводы", "Наличные"]

    transfers = expenses[
        expenses["Категория"].fillna("").str.casefold()
        == "переводы"
    ]["Сумма операции"].sum()

    cash = expenses[
        expenses["Категория"].fillna("").str.casefold()
        == "наличные"
    ]["Сумма операции"].sum()

    categories = (
        expenses[
            ~expenses["Категория"].fillna("").isin(
                special_categories
            )
        ]
        .groupby("Категория")["Сумма операции"]
        .sum()
        .sort_values(ascending=False)
    )

    top_categories = categories.head(7)

    category_result = [
        {
            "category": str(category),
            "amount": round(float(amount)),
        }
        for category, amount in top_categories.items()
    ]

    other_amount = categories.iloc[7:].sum()

    if other_amount > 0:
        category_result.append({
            "category": "Остальное",
            "amount": round(float(other_amount)),
        })

    currency_rates = currency_rates or {}
    stock_prices = stock_prices or {}
    settings = load_user_settings()

    currencies = [
        {
            "currency": currency,
            "rate": currency_rates[currency],
        }
        for currency in settings.get("user_currencies", [])
        if currency in currency_rates
    ]

    stocks = [
        {
            "stock": stock,
            "price": stock_prices[stock],
        }
        for stock in settings.get("user_stocks", [])
        if stock in stock_prices
    ]

    result = {
        "expenses": {
            "total_amount": round(float(expenses["Сумма операции"].sum())),
            "categories": category_result,
            "transfers": round(float(transfers)),
            "cash": round(float(cash)),
        },
        "incomes": {
            "total_amount": round(
                float(incomes["Сумма операции"].sum())
            ),
        },
        "currency_rates": currencies,
        "stock_prices": stocks,
    }

    return json.dumps(result, ensure_ascii=False, indent=4)
