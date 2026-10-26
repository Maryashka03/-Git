import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях."""
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0))
    currency = operation_amount.get("currency", {}).get("code")

    if currency == "RUB":
        return amount

    if currency not in ("USD", "EUR"):
        return 0.0

    api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    if not api_key:
        return 0.0

    response = requests.get(
        "https://api.apilayer.com/exchangerates_data/convert",
        params={
            "to": "RUB",
            "from": currency,
            "amount": amount,
        },
        headers={"apikey": api_key},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    return float(data.get("result", 0))
