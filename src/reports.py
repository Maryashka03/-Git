from pathlib import Path
from collections.abc import Callable
from typing import ParamSpec, TypeVar

import pandas as pd

P = ParamSpec("P")
R = TypeVar("R")


def save_report(
    filename: str = "report.csv",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Декоратор сохраняет отчет в CSV-файл."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = func(*args, **kwargs)

            if isinstance(result, pd.DataFrame):
                path = Path(filename)
                path.parent.mkdir(parents=True, exist_ok=True)
                result.to_csv(
                    path,
                    index=False,
                    encoding="utf-8-sig",
                )

            return result

        return wrapper

    return decorator


@save_report()
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: str | None = None,
) -> pd.DataFrame:
    """Возвращает расходы по категории за последние три месяца."""

    if date is None:
        end_date = pd.Timestamp.today().normalize()
    else:
        end_date = pd.to_datetime(date, dayfirst=True).normalize()

    start_date = end_date - pd.DateOffset(months=3)

    operation_dates = pd.to_datetime(
        transactions["Дата операции"],
        errors="coerce",
    )

    mask = (
        (transactions["Категория"].fillna("").str.casefold()
         == category.casefold())
        & (transactions["Статус"] == "OK")
        & (transactions["Сумма операции"] < 0)
        & (operation_dates >= start_date)
        & (operation_dates <= end_date)
    )

    return transactions.loc[mask].copy()
