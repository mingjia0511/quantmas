"""Data loading service for market data."""
from pathlib import Path
from typing import Dict, Set
import pandas as pd


class DataLoader:
    """Handles loading and validation of market data."""

    def __init__(self, data_path: str):
        """Initialize data loader.

        Args:
            data_path: Path to directory containing data files
        """
        self._path = Path(data_path)
        self._assets_cache: pd.DataFrame | None = None
        self._valuations_cache: pd.DataFrame | None = None

    def load_assets(self) -> pd.DataFrame:
        """Load assets from CSV with validation.

        Returns:
            DataFrame with asset information

        Raises:
            FileNotFoundError: If assets.csv doesn't exist
            ValueError: If required columns are missing
        """
        if self._assets_cache is not None:
            return self._assets_cache

        file_path = self._path / "assets.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Assets file not found: {file_path}")

        df = pd.read_csv(file_path)
        self._validate_assets(df)
        self._assets_cache = df
        return df

    def load_valuations(self) -> pd.DataFrame:
        """Load valuations from CSV with validation.

        Returns:
            DataFrame with daily valuations for all assets

        Raises:
            FileNotFoundError: If valuations.csv doesn't exist
            ValueError: If required columns are missing
        """
        if self._valuations_cache is not None:
            return self._valuations_cache

        file_path = self._path / "valuations.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Valuations file not found: {file_path}")

        df = pd.read_csv(file_path)
        self._validate_valuations(df)
        self._valuations_cache = df
        return df

    def get_asset_valuations(self, asset_id: str) -> pd.Series:
        """Get valuation series for specific asset.

        Args:
            asset_id: Asset identifier

        Returns:
            Series with day as index and valuation as values
        """
        df = self.load_valuations()
        asset_data = df[df["asset_id"] == asset_id]
        return asset_data.set_index("day")["valuation"]

    def get_valuation_on_day(self, asset_id: str, day: int) -> float:
        """Get valuation for specific asset on specific day.

        Args:
            asset_id: Asset identifier
            day: Trading day (1-100)

        Returns:
            Valuation in FSB
        """
        df = self.load_valuations()
        result = df[(df["asset_id"] == asset_id) & (df["day"] == day)]
        if result.empty:
            raise ValueError(f"No valuation found for {asset_id} on day {day}")
        return float(result["valuation"].iloc[0])

    def _validate_assets(self, df: pd.DataFrame) -> None:
        """Validate assets DataFrame has required columns.

        Args:
            df: Assets DataFrame to validate

        Raises:
            ValueError: If required columns are missing
        """
        required: Set[str] = {"id", "name", "type", "sub_type", "available_on_day", "region"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns in assets: {missing}")

    def _validate_valuations(self, df: pd.DataFrame) -> None:
        """Validate valuations DataFrame has required columns.

        Args:
            df: Valuations DataFrame to validate

        Raises:
            ValueError: If required columns are missing
        """
        required: Set[str] = {"asset_id", "day", "valuation"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns in valuations: {missing}")
