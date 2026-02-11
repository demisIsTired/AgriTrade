# src/models/db.py
from sqlalchemy import Column, Date, Float, Integer, MetaData, String
from sqlalchemy.orm import DeclarativeBase  # Changed from declarative_base

# Define naming conventions for constraints to avoid Alembic migration errors
metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


# Create the Base class explicitly for Mypy compatibility
class Base(DeclarativeBase):
    metadata = metadata


class WeatherMetrics(Base):
    __tablename__ = "weather_metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    location = Column(String, nullable=False)
    temp_mean = Column(Float, nullable=False)
    precip_mm = Column(Float, nullable=False)


class CommodityPrices(Base):
    __tablename__ = "commodity_prices"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    symbol = Column(String, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=True)
