import json

import pandas as pd

from src.services import simple_search


def test_simple_search_by_description():
    """Проверяет поиск по описанию."""
    transactions = pd.DataFrame({
        "Описание": ["Пятёрочка", "Магнит", "Аптека"],
        "Категория": ["Супермаркеты", "Супермаркеты", "Здоровье"],
    })

    result = json.loads(simple_search(transactions, "магнит"))

    assert len(result) == 1
    assert result[0]["Описание"] == "Магнит"


def test_simple_search_by_category():
    """Проверяет поиск по категории."""
    transactions = pd.DataFrame({
        "Описание": ["Покупка", "Лекарства"],
        "Категория": ["Супермаркеты", "Здоровье"],
    })

    result = json.loads(simple_search(transactions, "здоровье"))

    assert len(result) == 1
    assert result[0]["Категория"] == "Здоровье"


def test_simple_search_no_results():
    """Проверяет поиск без совпадений."""
    transactions = pd.DataFrame({
        "Описание": ["Покупка"],
        "Категория": ["Супермаркеты"],
    })

    result = json.loads(simple_search(transactions, "автомобиль"))

    assert result == []


def test_simple_search_empty_query():
    """Проверяет пустой поисковый запрос."""
    transactions = pd.DataFrame({
        "Описание": ["Покупка"],
        "Категория": ["Супермаркеты"],
    })

    result = json.loads(simple_search(transactions, "   "))

    assert result == []
