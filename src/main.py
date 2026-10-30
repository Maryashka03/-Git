from datetime import datetime
from pathlib import Path

from src.external_api import get_currency_rates, get_stock_prices
from src.utils import load_transactions
from src.views import load_user_settings, main_page

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "operations.xls"


def main() -> None:
    """Запускает приложение для анализа банковских операций."""
    transactions = load_transactions(DATA_PATH)

    settings = load_user_settings()

    currencies = settings.get("user_currencies", [])
    stocks = settings.get("user_stocks", [])

    currency_data = get_currency_rates(currencies)
    stock_data = get_stock_prices(stocks)

    currency_rates = {
        item["currency"]: item["rate"]
        for item in currency_data
    }

    stock_prices = {
        item["stock"]: item["price"]
        for item in stock_data
    }

    current_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    result = main_page(
        transactions,
        current_date,
        currency_rates,
        stock_prices,
    )

    print(result)


if __name__ == "__main__":
    main()
