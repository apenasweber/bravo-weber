from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, text

from app.database import Base


class CoinbaseCurrenciesPublicApiModel(Base):
    __tablename__ = "coinbase_currencies_public_api"

    id = Column(Integer, primary_key=True)
    currency_code = Column(String, nullable=False, index=True, unique=True)
    rate = Column(Float, nullable=False)
    backed_by = Column(String, nullable=False, server_default="USD")
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.utcnow,
    )
    currency_type = Column(
        String, nullable=False, index=True, server_default="coinbase"
    )


class FictitiousCoinModel(Base):
    __tablename__ = "fictitious_currencies"

    id = Column(Integer, primary_key=True)
    currency_code = Column(String, nullable=False, index=True, unique=True)
    rate = Column(Float, nullable=False)
    backed_by = Column(String, nullable=False, server_default="USD")
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        onupdate=datetime.utcnow,
    )
    currency_type = Column(
        String, nullable=False, index=True, server_default="fictitious"
    )
