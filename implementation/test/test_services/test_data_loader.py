"""Tests for DataLoader service."""
import pytest
import pandas as pd
from pathlib import Path
from src.services.data_loader import DataLoader


class TestDataLoader:
    """Test suite for DataLoader service."""

    def test_load_assets_returns_dataframe(self) -> None:
        """Should return pandas DataFrame with correct structure."""
        loader = DataLoader("../problems/year_1/data")
        df = loader.load_assets()

        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 15

    def test_load_assets_has_required_columns(self) -> None:
        """Should have all required columns."""
        loader = DataLoader("../problems/year_1/data")
        df = loader.load_assets()

        required_columns = {"id", "name", "type", "sub_type", "available_on_day", "region"}
        assert required_columns.issubset(set(df.columns))

    def test_load_valuations_returns_dataframe(self) -> None:
        """Should return pandas DataFrame with valuations."""
        loader = DataLoader("../problems/year_1/data")
        df = loader.load_valuations()

        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1500  # 15 assets * 100 days

    def test_load_valuations_has_required_columns(self) -> None:
        """Should have all required columns."""
        loader = DataLoader("../problems/year_1/data")
        df = loader.load_valuations()

        required_columns = {"asset_id", "day", "valuation"}
        assert required_columns.issubset(set(df.columns))

    def test_load_assets_invalid_path_raises_error(self) -> None:
        """Should raise FileNotFoundError for invalid path."""
        loader = DataLoader("invalid/path")

        with pytest.raises(FileNotFoundError):
            loader.load_assets()

    def test_get_asset_valuations_returns_series(self) -> None:
        """Should return valuation series for specific asset."""
        loader = DataLoader("../problems/year_1/data")
        valuations = loader.get_asset_valuations("asset_1")

        assert valuations is not None
        assert len(valuations) == 100
        assert all(1 <= day <= 100 for day in valuations.index)

    def test_all_assets_have_day_1_valuations(self) -> None:
        """All assets should have day 1 valuations for comparison."""
        loader = DataLoader("../problems/year_1/data")
        assets_df = loader.load_assets()
        valuations_df = loader.load_valuations()

        for _, asset in assets_df.iterrows():
            asset_id = asset["id"]
            day1_vals = valuations_df[
                (valuations_df["asset_id"] == asset_id) & (valuations_df["day"] == 1)
            ]
            assert not day1_vals.empty, f"{asset_id} missing day 1 valuation"

    def test_all_assets_have_day_100_valuations(self) -> None:
        """All assets should have day 100 valuations for comparison."""
        loader = DataLoader("../problems/year_1/data")
        assets_df = loader.load_assets()
        valuations_df = loader.load_valuations()

        for _, asset in assets_df.iterrows():
            asset_id = asset["id"]
            day100_vals = valuations_df[
                (valuations_df["asset_id"] == asset_id) & (valuations_df["day"] == 100)
            ]
            assert not day100_vals.empty, f"{asset_id} missing day 100 valuation"

    def test_all_assets_have_complete_valuations(self) -> None:
        """All assets should have valuations for all 100 days."""
        loader = DataLoader("../problems/year_1/data")
        assets_df = loader.load_assets()
        valuations_df = loader.load_valuations()

        for _, asset in assets_df.iterrows():
            asset_id = asset["id"]
            asset_vals = valuations_df[valuations_df["asset_id"] == asset_id]
            assert len(asset_vals) == 100, f"{asset_id} has {len(asset_vals)} days, expected 100"
