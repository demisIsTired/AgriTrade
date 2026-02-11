from datetime import date

import pandas as pd
import yfinance as yf
from loguru import logger


class CommodityAPIClient:
    """Client to fetch daily commodity futures prices."""

    def __init__(self) -> None:
        self.logger = logger

    def fetch_daily_prices(
        self, symbol: str, start_date: date, end_date: date | None = None
    ) -> pd.DataFrame:
        """
        Fetch historical prices for a given ticker symbol.

        Args:
            symbol: The Yahoo Finance ticker (e.g., 'ZS=F' for Soybeans).
            start_date: The start date for data extraction.
            end_date: The end date (defaults to today if None).

        Returns:
            A cleaned Pandas DataFrame ready for database insertion.
        """
        _end_date = end_date or date.today()
        self.logger.info(f"Fetching {symbol} data from {start_date} to {_end_date}")

        try:
            ticker = yf.Ticker(symbol)

            df: pd.DataFrame = ticker.history(
                start=start_date.strftime("%Y-%m-%d"),
                end=_end_date.strftime("%Y-%m-%d"),
            )

            if df.empty:
                self.logger.warning(
                    f"No data returned for {symbol}\
                                    in given date range."
                )
                return pd.DataFrame()

            # Reset index to turn the Date index into a standard column
            df = df.reset_index()

            # Keep only the columns we mapped in our database schema
            df = df[["Date", "Close", "Volume"]].copy()

            # Rename columns to match the SQLAlchemy `CommodityPrices` model exactly
            df = df.rename(
                columns={
                    "Date": "date",
                    "Close": "close_price",
                    "Volume": "volume",
                }
            )

            # Insert the symbol column so we know what this data represents
            df["symbol"] = symbol

            # Standardize the date column to Python date objects
            df["date"] = pd.to_datetime(df["date"]).dt.date

            self.logger.info(f"Successfully extracted {len(df)} rows for {symbol}")
            return df

        except Exception as e:
            self.logger.error(f"Failed to fetch data for {symbol}: {str(e)}")
            raise
