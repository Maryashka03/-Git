import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_currency_rates(currencies: list[str]) -> list[dict]:
    """Получает актуальные курсы валют."""
    api_key = os.getenv("EXCHANGE_RATES_API_KEY")

    if not api_key:
        return []

    url = "https://api.apilayer.com/exchangerates_data/latest"
    params = {"base": "RUB", "symbols": ",".join(currencies)}
    headers = {"apikey": api_key}

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        return [
            {"currency": currency, "rate": rate}
            for currency, rate in data.get("rates", {}).items()
            if isinstance(rate, (int, float)) and rate > 0
        ]
    except requests.RequestException:
        return []


def get_stock_prices(stocks: list[str]) -> list[dict]:
    """Получает цены акций через Alpha Vantage."""
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    if not api_key:
        return []

    results = []

    for stock in stocks:
        try:
            response = requests.get(
                "https://www.alphavantage.co/query",
                params={
                    "function": "GLOBAL_QUOTE",
                    "symbol": stock,
                    "apikey": api_key,
                },
                timeout=10,
            )
            response.raise_for_status()
            quote = response.json().get("Global Quote", {})
            price = float(quote.get("05. price", 0))

            if price > 0:
                results.append({
                    "stock": stock,
                    "price": price,
                })
        except (requests.RequestException, ValueError):
            continue

    return results
