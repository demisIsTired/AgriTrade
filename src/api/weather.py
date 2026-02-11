# src/api/weather.py
from typing import Any

import pandas as pd
import requests
from loguru import logger


class WeatherAPIClient:
    """Client to fetch daily weather metrics from Open-Meteo (Free)."""

    def __init__(self) -> None:
        self.logger = logger
        # No API key needed for Open-Meteo non-commercial use
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def fetch_daily_metrics(self, location_name: str, lat: float, lon: float) -> pd.DataFrame:
        """
        Fetch weather data and aggregate it into daily metrics.

        Args:
            location_name: Friendly name (e.g., 'Mato Grosso').
            lat: Latitude.
            lon: Longitude.
        """
        self.logger.info(f"Fetching Open-Meteo data for {location_name} ({lat}, {lon})")

        params: dict[str, Any] = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["temperature_2m_mean", "precipitation_sum"],
            "timezone": "auto",
            "forecast_days": 1,  # We only need the current/recent data
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "daily" not in data:
                self.logger.warning(f"No daily data returned for {location_name}.")
                return pd.DataFrame()

            # Open-Meteo returns data in a clean dictionary of lists
            daily_data = data["daily"]
            df_daily = pd.DataFrame(
                {
                    "date": pd.to_datetime(daily_data["time"]).date,
                    "temp_mean": daily_data["temperature_2m_mean"],
                    "precip_mm": daily_data["precipitation_sum"],
                }
            )

            # Add location and reorder to match WeatherMetrics model
            df_daily["location"] = location_name
            df_daily = df_daily[["date", "location", "temp_mean", "precip_mm"]]

            self.logger.info(f"Extracted {len(df_daily)} records for {location_name}")
            return df_daily

        except requests.RequestException as e:
            self.logger.error(f"Open-Meteo request failed: {str(e)}")
            raise


if __name__ == "__main__":
    client = WeatherAPIClient()
    # Mato Grosso coordinates
    try:
        df = client.fetch_daily_metrics("Mato Grosso", -12.5456, -55.7267)
        print(df.head())
    except Exception as e:
        logger.error(f"Manual test failed: {e}")
