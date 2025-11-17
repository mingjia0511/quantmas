"""
Test suite for the data_loader module.
"""
import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from data_loader import DataLoader


@pytest.fixture
def sample_data_dir():
    """Create a temporary directory with sample CSV files for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create sample assets.csv
        assets_data = """id,name,type,sub_type,available_on_day,region
asset_1,Test Manor,Real Estate,Residential,1,Testville
asset_2,Test Plaza,Real Estate,Commercial,5,Testtown
asset_3,Test Factory,Real Estate,Industrial,10,Testburg"""
        
        assets_path = Path(tmpdir) / "assets.csv"
        with open(assets_path, 'w') as f:
            f.write(assets_data)
        
        # Create sample valuations.csv
        valuations_data = """asset_id,day,valuation
asset_1,1,100000
asset_1,2,101000
asset_1,3,102000
asset_2,1,200000
asset_2,2,201000
asset_2,3,202000
asset_3,1,300000
asset_3,2,301000
asset_3,3,302000"""
        
        valuations_path = Path(tmpdir) / "valuations.csv"
        with open(valuations_path, 'w') as f:
            f.write(valuations_data)
        
        yield tmpdir


class TestDataLoader:
    """Test cases for DataLoader class."""
    
    def test_init(self):
        """Test DataLoader initialization."""
        loader = DataLoader("/test/path")
        assert loader.data_dir == Path("/test/path")
        assert loader.assets_df is None
        assert loader.valuations_df is None
    
    def test_load_data_success(self, sample_data_dir):
        """Test successful data loading."""
        loader = DataLoader(sample_data_dir)
        assets_df, valuations_df = loader.load_data()
        
        assert assets_df is not None
        assert valuations_df is not None
        assert len(assets_df) == 3
        assert len(valuations_df) == 9
        assert list(assets_df.columns) == ['id', 'name', 'type', 'sub_type', 'available_on_day', 'region']
        assert list(valuations_df.columns) == ['asset_id', 'day', 'valuation']
    
    def test_load_data_missing_assets(self, sample_data_dir):
        """Test loading data when assets file is missing."""
        assets_path = Path(sample_data_dir) / "assets.csv"
        os.remove(assets_path)
        
        loader = DataLoader(sample_data_dir)
        with pytest.raises(FileNotFoundError, match="Assets file not found"):
            loader.load_data()
    
    def test_load_data_missing_valuations(self, sample_data_dir):
        """Test loading data when valuations file is missing."""
        valuations_path = Path(sample_data_dir) / "valuations.csv"
        os.remove(valuations_path)
        
        loader = DataLoader(sample_data_dir)
        with pytest.raises(FileNotFoundError, match="Valuations file not found"):
            loader.load_data()
    
    def test_get_asset_info_success(self, sample_data_dir):
        """Test successful asset info retrieval."""
        loader = DataLoader(sample_data_dir)
        loader.load_data()
        
        asset_info = loader.get_asset_info("asset_1")
        assert asset_info['id'] == "asset_1"
        assert asset_info['name'] == "Test Manor"
        assert asset_info['sub_type'] == "Residential"
        assert asset_info['available_on_day'] == 1
    
    def test_get_asset_info_not_found(self, sample_data_dir):
        """Test asset info retrieval for non-existent asset."""
        loader = DataLoader(sample_data_dir)
        loader.load_data()
        
        with pytest.raises(ValueError, match="Asset nonexistent not found"):
            loader.get_asset_info("nonexistent")
    
    def test_get_asset_info_data_not_loaded(self):
        """Test asset info retrieval before loading data."""
        loader = DataLoader("/test")
        
        with pytest.raises(ValueError, match="Data not loaded"):
            loader.get_asset_info("asset_1")
    
    def test_get_asset_valuation_success(self, sample_data_dir):
        """Test successful asset valuation retrieval."""
        loader = DataLoader(sample_data_dir)
        loader.load_data()
        
        valuation = loader.get_asset_valuation("asset_1", 2)
        assert valuation == 101000.0
    
    def test_get_asset_valuation_not_found(self, sample_data_dir):
        """Test asset valuation retrieval for non-existent asset/day."""
        loader = DataLoader(sample_data_dir)
        loader.load_data()
        
        with pytest.raises(ValueError, match="No valuation found"):
            loader.get_asset_valuation("asset_1", 10)
    
    def test_get_all_assets(self, sample_data_dir):
        """Test getting all asset IDs."""
        loader = DataLoader(sample_data_dir)
        loader.load_data()
        
        assets = loader.get_all_assets()
        assert assets == ["asset_1", "asset_2", "asset_3"]
    
    def test_get_available_assets(self, sample_data_dir):
        """Test getting available assets for a specific day."""
        loader = DataLoader(sample_data_dir)
        loader.load_data()
        
        # Day 1: only asset_1 available
        available_day_1 = loader.get_available_assets(1)
        assert available_day_1 == ["asset_1"]
        
        # Day 5: asset_1 and asset_2 available
        available_day_5 = loader.get_available_assets(5)
        assert set(available_day_5) == {"asset_1", "asset_2"}
        
        # Day 10: all assets available
        available_day_10 = loader.get_available_assets(10)
        assert set(available_day_10) == {"asset_1", "asset_2", "asset_3"}
    
    def test_get_daily_valuations(self, sample_data_dir):
        """Test getting all valuations for a specific day."""
        loader = DataLoader(sample_data_dir)
        loader.load_data()
        
        day_2_valuations = loader.get_daily_valuations(2)
        expected = {"asset_1": 101000, "asset_2": 201000, "asset_3": 301000}
        assert day_2_valuations == expected
    
    def test_get_asset_price_history(self, sample_data_dir):
        """Test getting price history for an asset."""
        loader = DataLoader(sample_data_dir)
        loader.load_data()
        
        # Test full history
        history = loader.get_asset_price_history("asset_1")
        assert len(history) == 3
        assert list(history['day']) == [1, 2, 3]
        assert list(history['valuation']) == [100000, 101000, 102000]
        
        # Test history up to specific day
        history_day_2 = loader.get_asset_price_history("asset_1", up_to_day=2)
        assert len(history_day_2) == 2
        assert list(history_day_2['day']) == [1, 2]