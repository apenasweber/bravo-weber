import pytest
from fastapi.testclient import TestClient

from app.schemas.currency import Currency


@pytest.mark.parametrize(
    "index, expected_currency_code, expected_rate, expected_backed_by, expected_currency_type",
    [
        (0, "BRL", 5.12, "USD", "coinbase"),
        (1, "BTC", 0.00005, "USD", "coinbase"),
        (2, "ETH", 0.0006, "USD", "coinbase"),
        (3, "EUR", 1.01, "USD", "coinbase"),
        (4, "USD", 1.0, "USD", "coinbase"),
    ],
)
def test_should_get_all_currencies_in_db(
    client: TestClient,
    index,
    expected_currency_code,
    expected_rate,
    expected_backed_by,
    expected_currency_type,
):
    res = client.get("/currency")
    res_data = res.json()["data"][index]

    assert res.status_code == 200
    assert res_data["currency_code"] == expected_currency_code
    assert res_data["rate"] == expected_rate
    assert res_data["backed_by"] == expected_backed_by
    assert res_data["currency_type"] == expected_currency_type


@pytest.mark.parametrize(
    "currency_code, expected_rate, expected_backed_by, expected_currency_type",
    [
        ("BRL", 5.12, "USD", "coinbase"),
        ("BTC", 0.00005, "USD", "coinbase"),
        ("ETH", 0.0006, "USD", "coinbase"),
        ("EUR", 1.01, "USD", "coinbase"),
        ("USD", 1.0, "USD", "coinbase"),
    ],
)
def test_should_get_specific_existing_currency_in_db(
    client: TestClient,
    currency_code,
    expected_rate,
    expected_backed_by,
    expected_currency_type,
):
    res = client.get(f"/currency/{currency_code}/")
    res_data = res.json()["data"]

    assert res.status_code == 200
    assert res_data["currency_code"] == currency_code
    assert res_data["backed_by"] == expected_backed_by
    assert res_data["rate"] == expected_rate
    assert res_data["currency_type"] == expected_currency_type


def test_should_not_get_non_existing_currency_in_db(client: TestClient):
    currency_code = "HURB"
    res = client.get(f"/currency/{currency_code}/")
    assert res.status_code == 404
    assert res.json()["detail"] == f"Currency code {currency_code} not found"


def test_should_get_existing_currency_in_db(
    client: TestClient, create_hurb_currency: dict
):
    currency = Currency(**create_hurb_currency)
    res = client.get(f"/currency/{currency.currency_code}/")
    res_data = res.json()["data"]
    assert res.status_code == 200
    assert res_data["currency_code"] == currency.currency_code
