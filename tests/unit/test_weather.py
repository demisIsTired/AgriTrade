# tests/unit/test_weather.py
import pytest
from pytest_mock import MockerFixture

from src.api.weather import WeatherAPIClient


@pytest.fixture
def client() -> WeatherAPIClient:
    return WeatherAPIClient()


def test_fetch_weather_success(client: WeatherAPIClient, mocker: MockerFixture) -> None:
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
