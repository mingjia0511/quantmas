"""Tests for DataLoader class."""

import pytest
from pathlib import Path
from src.data_loader import DataLoader


class TestDataLoader:
    """Test cases for DataLoader class."""
    
    @pytest.fixture
    def data_dir(self):
        """Get path to test data directory."""
        project_root = Path(__file__).parent.parent.parent.parent
        return project_root / "problems" / "year_1" / "data"
    
    @pytest.fixture
    def loader(self, data_dir):
        """Create DataLoader instance."""
        return DataLoader(data_dir)
    
    def test_load_assets(self, loader):
        """Test loading assets from CSV."""
        assets = loader.load_assets()
        
        assert len(assets) == 15
        assert "asset_1" in assets
        assert assets["asset_1"]["name"] == "Snowflake Manor"
        assert assets["asset_1"]["type"] == "Real Estate"
        assert assets["asset_1"]["sub_type"] == "Residential"
        assert isinstance(assets["asset_1"]["available_on_day"], int)
        assert assets["asset_1"]["region"] in [
            "Frostpeak", "Tinseltown", "Evergreen Valley", "Mistletoe Meadows"
        ]
    
    def test_load_valuations(self, loader):
        """Test loading valuations from CSV."""
        valuations = loader.load_valuations()
        
        assert len(valuations) == 15
        assert "asset_1" in valuations
        assert len(valuations["asset_1"]) == 100
        assert 1 in valuations["asset_1"]
        assert 100 in valuations["asset_1"]
        assert isinstance(valuations["asset_1"][1], int)
    
    def test_load_all(self, loader):
        """Test loading both assets and valuations."""
        assets, valuations = loader.load_all()
        
        assert len(assets) == 15
        assert len(valuations) == 15
        
        # Verify all assets have valuations
        for asset_id in assets:
            assert asset_id in valuations
            assert len(valuations[asset_id]) == 100
