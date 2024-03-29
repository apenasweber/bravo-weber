from time import sleep

import requests
from config import settings
from models import CoinbaseCurrenciesPublicApiModel
from schemas import Currency
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def update_coinbase_currencies_prices():
    engine = create_engine(
        f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()

    coinbase_currencies_response = requests.get(
        "https://api.coinbase.com/v2/exchange-rates", params={"currency": "USD"}
    )
    if coinbase_currencies_response.status_code == 200:
        db.query(CoinbaseCurrenciesPublicApiModel).delete()

        db.execute(
            "ALTER SEQUENCE coinbase_currencies_public_api_id_seq RESTART WITH 1"
        )

    currencies = coinbase_currencies_response.json()["data"]["rates"]

    for currency_code, rate in currencies.items():
        currency = Currency(currency_code=currency_code, rate=rate)
        currency_db = CoinbaseCurrenciesPublicApiModel(
            currency_code=currency.currency_code, rate=currency.rate
        )
        db.add(currency_db)

    db.commit()
    db.close()


if __name__ == "__main__":
    update_coinbase_currencies_prices()
    sleep(60)
