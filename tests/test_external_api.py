import requests

from src.external_api import get_currency_rates, get_stock_prices


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


def test_currency_rates_without_api_key(monkeypatch):
    monkeypatch.delenv("EXCHANGE_RATES_API_KEY", raising=False)

    assert get_currency_rates(["USD"]) == []


def test_currency_rates_success(monkeypatch):
    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "test_key")

    monkeypatch.setattr(
        "src.external_api.requests.get",
        lambda *args, **kwargs: FakeResponse({
            "rates": {
                "USD": 0.01,
                "EUR": 0.02,
                "BAD": -1,
                "ZERO": 0,
            }
        }),
    )

    result = get_currency_rates(["USD", "EUR"])

    assert result == [
        {"currency": "USD", "rate": 0.01},
        {"currency": "EUR", "rate": 0.02},
    ]


def test_currency_rates_request_error(monkeypatch):
    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "test_key")

    def raise_error(*args, **kwargs):
        raise requests.RequestException("Ошибка соединения")

    monkeypatch.setattr(
        "src.external_api.requests.get",
        raise_error,
    )

    assert get_currency_rates(["USD"]) == []


def test_stock_prices_without_api_key(monkeypatch):
    monkeypatch.delenv("ALPHA_VANTAGE_API_KEY", raising=False)

    assert get_stock_prices(["AAPL"]) == []


def test_stock_prices_success(monkeypatch):
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test_key")

    monkeypatch.setattr(
        "src.external_api.requests.get",
        lambda *args, **kwargs: FakeResponse({
            "Global Quote": {"05. price": "250.50"}
        }),
    )

    result = get_stock_prices(["AAPL"])

    assert result == [
        {"stock": "AAPL", "price": 250.50}
    ]


def test_stock_prices_invalid_price(monkeypatch):
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test_key")

    monkeypatch.setattr(
        "src.external_api.requests.get",
        lambda *args, **kwargs: FakeResponse({
            "Global Quote": {"05. price": "invalid"}
        }),
    )

    assert get_stock_prices(["AAPL"]) == []


def test_stock_prices_request_error(monkeypatch):
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test_key")

    def raise_error(*args, **kwargs):
        raise requests.RequestException("Ошибка соединения")

    monkeypatch.setattr(
        "src.external_api.requests.get",
        raise_error,
    )

    assert get_stock_prices(["AAPL"]) == []
