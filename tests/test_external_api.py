from unittest.mock import Mock, patch

from src.external_api import convert_to_rub


def test_rub_amount_does_not_call_api():
    transaction = {
        "operationAmount": {
            "amount": "1500",
            "currency": {"code": "RUB"},
        }
    }

    with patch("src.external_api.requests.get") as mock_get:
        result = convert_to_rub(transaction)

    assert result == 1500.0
    mock_get.assert_not_called()


def test_unsupported_currency_returns_zero():
    transaction = {
        "operationAmount": {
            "amount": "200",
            "currency": {"code": "GBP"},
        }
    }

    with patch("src.external_api.requests.get") as mock_get:
        result = convert_to_rub(transaction)

    assert result == 0.0
    mock_get.assert_not_called()


def test_usd_is_converted_to_rub():
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "USD"},
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = {"result": 9000}

    with patch("src.external_api.requests.get", return_value=mock_response) as mock_get:
        with patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "test_key"}):
            result = convert_to_rub(transaction)

    assert result == 9000.0
    mock_get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()


def test_missing_api_key_returns_zero():
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "EUR"},
        }
    }

    with patch.dict("os.environ", {}, clear=True):
        result = convert_to_rub(transaction)

    assert result == 0.0
