import json

import pandas as pd

from src.views import main_page, get_greeting


def test_get_greeting():
    assert get_greeting(8) == "Доброе утро"
    assert get_greeting(14) == "Добрый день"
    assert get_greeting(20) == "Добрый вечер"
    assert get_greeting(2) == "Доброй ночи"


def test_main_page():
    transactions = pd.DataFrame({
        "Дата операции": pd.to_datetime([
            "2021-12-01",
            "2021-12-02",
        ]),
        "Статус": ["OK", "OK"],
        "Сумма операции": [-100, -200],
        "Номер карты": ["*1234", "*1234"],
        "Кэшбэк": [1, 2],
        "Категория": ["Магазины", "Кафе"],
        "Описание": ["Покупка", "Обед"],
    })

    result = json.loads(main_page(
        transactions,
        "02.12.2021 14:00:00",
        {"USD": 90.0},
        {"AAPL": 250.0},
    ))

    assert result["greeting"] == "Добрый день"
    assert len(result["cards"]) == 1
    assert len(result["top_transactions"]) == 2
    assert len(result["currencies"]) == 1
    assert len(result["stocks"]) == 1
