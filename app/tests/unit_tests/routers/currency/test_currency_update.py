from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import CoinbaseCurrenciesPublicApiModel
from app.schemas.currency import CurrencyInput

NEW_RATE = 50.41
NEW_AMOUNT = 120.45
NEW_BACKED_CURRENCY_AMOUNT = 33.80


def test_should_update_existing_currency_in_database(
    client: TestClient,
    session: Session,
    create_hurb_currency,
    fictitious_currency_data_hurb: dict,
):
    original_currency = CurrencyInput(**create_hurb_currency)
    currency_id_db = (
        session.query(CoinbaseCurrenciesPublicApiModel.id)
        .filter(
            CoinbaseCurrenciesPublicApiModel.currency_code
            == original_currency.currency_code
        )
        .scalar()
    )

    payload = fictitious_currency_data_hurb.copy()
    payload["rate"] = NEW_RATE

    res = client.put(f"/currency/{original_currency.currency_code}", json=payload)
    res_data = res.json()["data"]

    updated_currency = CurrencyInput(**payload)
    assert res.status_code == 200
    assert res_data["currency_code"] == updated_currency.currency_code
    assert res_data["rate"] == updated_currency.rate
    assert res_data["backed_by"] == updated_currency.backed_by


def test_should_not_update_currency_not_found_in_db(
    client: TestClient, fictitious_currency_data_hurb: dict
):
    payload = fictitious_currency_data_hurb.copy()
    payload["rate"] = NEW_RATE
    updated_currency = CurrencyInput(**payload)

    res = client.put(f"/currency/{updated_currency.currency_code}", json=payload)
    assert res.status_code == 404


def test_should_update_currency_not_found_in_db_using_alternative_input(
    client: TestClient, fictitious_currency_data_hurb_alternative_input: dict
):
    payload = fictitious_currency_data_hurb_alternative_input.copy()
    payload["amount"] = NEW_AMOUNT
    payload["backed_currency_amount"] = NEW_BACKED_CURRENCY_AMOUNT
    updated_currency = CurrencyInput(**payload)

    res = client.put(f"/currency/{updated_currency.currency_code}", json=payload)
    assert res.status_code == 404


def test_should_update_currency_found_in_db_using_alternative_input(
    client: TestClient,
    session: Session,
    create_hurb_currency,
    fictitious_currency_data_hurb_alternative_input: dict,
):
    original_currency = CurrencyInput(**create_hurb_currency)
    currency_id_db = (
        session.query(CoinbaseCurrenciesPublicApiModel.id)
        .filter(
            CoinbaseCurrenciesPublicApiModel.currency_code
            == original_currency.currency_code
        )
        .scalar()
    )

    payload = fictitious_currency_data_hurb_alternative_input.copy()
    payload["amount"] = NEW_AMOUNT
    payload["backed_currency_amount"] = NEW_BACKED_CURRENCY_AMOUNT

    res = client.put(f"/currency/{original_currency.currency_code}", json=payload)
    res_data = res.json()["data"]

    updated_currency = CurrencyInput(**payload)
    assert res.status_code == 200
    assert res_data["currency_code"] == updated_currency.currency_code
    assert res_data["rate"] == updated_currency.rate
    assert res_data["backed_by"] == updated_currency.backed_by


def test_should_not_update_currency_found_in_db_with_missing_field(
    client: TestClient,
    session: Session,
    create_hurb_currency,
    fictitious_currency_data_hurb_missing_field_input: dict,
):
    original_currency = CurrencyInput(**create_hurb_currency)
    currency_id_db = (
        session.query(CoinbaseCurrenciesPublicApiModel.id)
        .filter(
            CoinbaseCurrenciesPublicApiModel.currency_code
            == original_currency.currency_code
        )
        .scalar()
    )

    payload = fictitious_currency_data_hurb_missing_field_input.copy()
    payload["amount"] = NEW_AMOUNT

    res = client.put(f"/currency/{original_currency.currency_code}", json=payload)

    assert res.status_code == 422
    assert (
        res.json()["detail"][0]["msg"]
        == "You should provide whether a rate field or an amount and backed_currency_amount fields"
    )


def test_should_update_currency_found_in_db_providing_invalid_fields_in_body(
    client: TestClient,
    create_hurb_currency: dict,
    fictitious_currency_data_hurb_all_fields_input: dict,
):
    res = client.put(
        f"/currency/{create_hurb_currency['currency_code']}",
        json=fictitious_currency_data_hurb_all_fields_input,
    )
    assert res.status_code == 422
    assert (
        res.json()["detail"][0]["msg"]
        == "You should provide only a rate field or an amount and backed_currency_amount fields"
    )


def test_should_not_update_coinbase_api_currency_found_in_db(
    client: TestClient, real_currency_data_brl, fictitious_currency_data_test: dict
):
    res = client.put(
        f"/currency/{real_currency_data_brl['currency_code']}",
        json=fictitious_currency_data_test,
    )
    assert res.status_code == 409
    assert (
        res.json()["detail"]
        == f"Currency code {real_currency_data_brl['currency_code']} is an coinbase_api currency and cannot be changed"
    )
