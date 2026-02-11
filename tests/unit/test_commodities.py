# tests/unit/test_commodities.py
from datetime import date

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from src.api.commodities import CommodityAPIClient


@pytest.fixture
def client() -> CommodityAPIClient:
    """Fixture to provide a reusable instance of the client."""
    return CommodityAPIClient()


def test_fetch_daily_prices_success(client: CommodityAPIClient, mocker: MockerFixture) -> None:
    """Test successful data extraction and formatting."""
    # 1. Arrange: Create a fake yfinance DataFrame
    mock_dates = pd.to_datetime(["2024-01-01", "2024-01-02"])
    mock_data = pd.DataFrame(
        {"Close": [1240.5, 1250.0], "Volume": [10000, 15000]}, index=mock_dates
    )
    mock_data.index.name = "Date"  # yfinance sets the index name to 'Date'

    # Mock the yfinance Ticker to return our fake data
    mock_ticker = mocker.patch("src.api.commodities.yf.Ticker")
    mock_ticker.return_value.history.return_value = mock_data

    # 2. Act: Call the method
    start_dt = date(2024, 1, 1)
    end_dt = date(2024, 1, 2)
    result = client.fetch_daily_prices(symbol="ZS=F", start_date=start_dt, end_date=end_dt)

    # 3. Assert: Check the transformations
    assert not result.empty
    assert list(result.columns) == ["date", "close_price", "volume", "symbol"]
    assert result.iloc[0]["symbol"] == "ZS=F"
    assert result.iloc[0]["close_price"] == 1240.5
    assert result.iloc[0]["volume"] == 10000
    assert result.iloc[0]["date"] == start_dt  # Ensures date conversion worked


def test_fetch_daily_prices_empty(client: CommodityAPIClient, mocker: MockerFixture) -> None:
    """Test behavior when yfinance returns no data."""
    # Mock yfinance to return an empty DataFrame
    mock_ticker = mocker.patch("src.api.commodities.yf.Ticker")
    mock_ticker.return_value.history.return_value = pd.DataFrame()

    result = client.fetch_daily_prices("ZS=F", date(2024, 1, 1))

    # Assert it gracefully returns an empty DataFrame
    assert result.empty


def test_fetch_daily_prices_exception(client: CommodityAPIClient, mocker: MockerFixture) -> None:
    """Test that exceptions are logged and re-raised."""
    # Mock yfinance to crash
    mock_ticker = mocker.patch("src.api.commodities.yf.Ticker")
    mock_ticker.return_value.history.side_effect = Exception("API Connection Timeout")

    # Assert that the exception bubbles up correctly
    with pytest.raises(Exception, match="API Connection Timeout"):
        client.fetch_daily_prices("ZS=F", date(2024, 1, 1))
