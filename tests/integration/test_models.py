# tests/integration/test_models.py
from datetime import date

from src.models.db import CommodityPrices, WeatherMetrics


def test_weather_metrics_instantiation() -> None:
    """Test that the Weather model can be initialized."""
    weather = WeatherMetrics(
        date=date(2024, 1, 1), location="Mato Grosso", temp_mean=28.5, precip_mm=12.4
    )
    assert weather.location == "Mato Grosso"
    assert weather.temp_mean == 28.5


def test_commodity_prices_instantiation() -> None:
    """Test that the Commodity model can be initialized."""
    commodity = CommodityPrices(
        date=date(2024, 1, 1), symbol="ZS=F", close_price=1240.50, volume=15000
    )
    assert commodity.symbol == "ZS=F"
    assert commodity.close_price == 1240.50
