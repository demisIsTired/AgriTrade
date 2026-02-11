# tests/unit/test_weather.py
import pytest
import requests
from pytest_mock import MockerFixture

from src.api.weather import WeatherAPIClient


@pytest.fixture
def client() -> WeatherAPIClient:
    """Fixture to provide a reusable instance of the WeatherAPIClient."""
    return WeatherAPIClient()


def test_fetch_weather_success(client: WeatherAPIClient, mocker: MockerFixture) -> None:
    """Test successful data extraction and formatting."""
    # Mock the Open-Meteo JSON response structure.
    mock_response = {
        "daily": {
            "time": ["2026-02-11"],
            "temperature_2m_mean": [28.5],
            "precipitation_sum": [12.4],
        }
    }

    mock_get = mocker.patch("src.api.weather.requests.get")
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    df = client.fetch_daily_metrics("Mato Grosso", -12.5, -55.5)

    assert not df.empty
    assert df.iloc[0]["temp_mean"] == 28.5
    assert df.iloc[0]["location"] == "Mato Grosso"
    assert "precip_mm" in df.columns


def test_fetch_weather_empty(client: WeatherAPIClient, mocker: MockerFixture) -> None:
    """Test behavior when Open-Meteo returns no daily data."""
    # Mock response without "daily" key
    mock_response: dict[str, object] = {}

    mock_get = mocker.patch("src.api.weather.requests.get")
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    result = client.fetch_daily_metrics("Mato Grosso", -12.5, -55.5)

    # Assert it gracefully returns an empty DataFrame
    assert result.empty


def test_fetch_weather_request_exception(client: WeatherAPIClient, mocker: MockerFixture) -> None:
    """Test that network exceptions are logged and re-raised."""
    # Mock requests.get to raise a RequestException
    mock_get = mocker.patch("src.api.weather.requests.get")
    mock_get.side_effect = requests.RequestException("Connection timeout")

    # Assert that the exception bubbles up correctly
    with pytest.raises(requests.RequestException, match="Connection timeout"):
        client.fetch_daily_metrics("Mato Grosso", -12.5, -55.5)


def test_fetch_weather_json_parsing_error(client: WeatherAPIClient, mocker: MockerFixture) -> None:
    """Test that JSON parsing errors are logged and re-raised."""
    # Mock response that will cause JSON parsing to fail
    mock_get = mocker.patch("src.api.weather.requests.get")
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.side_effect = ValueError("Invalid JSON")

    # Assert that the exception bubbles up correctly
    with pytest.raises(ValueError, match="Invalid JSON"):
        client.fetch_daily_metrics("Mato Grosso", -12.5, -55.5)


def test_fetch_weather_missing_key_error(client: WeatherAPIClient, mocker: MockerFixture) -> None:
    """Test that missing keys in response are handled gracefully."""
    # Mock response with "daily" key but missing expected sub-keys
    mock_response = {
        "daily": {
            "time": ["2026-02-11"],
            # Missing "temperature_2m_mean" and "precipitation_sum"
        }
    }

    mock_get = mocker.patch("src.api.weather.requests.get")
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    # Assert that the KeyError bubbles up correctly
    with pytest.raises(KeyError):
        client.fetch_daily_metrics("Mato Grosso", -12.5, -55.5)
