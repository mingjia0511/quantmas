"""
Data loading module for Quantmas challenges.
Handles loading and parsing of assets, valuations, and tax rates data.
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class DataLoader:
    """Handles loading and processing of asset, valuation, and tax data."""
    
    def __init__(self, data_dir: str, year: int = 1):
        """Initialize with data directory path and year."""
        self.data_dir = Path(data_dir)
        self.year = year
        self.assets_df = None
        self.valuations_df = None
        self.tax_rates_df = None
    
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, Optional[pd.DataFrame]]:
        """Load assets, valuations, and optionally tax rates data from CSV files."""
        assets_path = self.data_dir / "assets.csv"
        valuations_path = self.data_dir / "valuations.csv"
        
        if not assets_path.exists():
            raise FileNotFoundError(f"Assets file not found: {assets_path}")
        if not valuations_path.exists():
            raise FileNotFoundError(f"Valuations file not found: {valuations_path}")
        
        self.assets_df = pd.read_csv(assets_path)
        self.valuations_df = pd.read_csv(valuations_path)
        
        # Load tax rates for Year 2 and beyond
        tax_rates_path = self.data_dir / "tax_rates.csv"
        if tax_rates_path.exists() and self.year >= 2:
            self.tax_rates_df = pd.read_csv(tax_rates_path)
        
        return self.assets_df, self.valuations_df, self.tax_rates_df
    
    def get_asset_info(self, asset_id: str) -> Dict:
        """Get asset information by ID."""
        if self.assets_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        asset_info = self.assets_df[self.assets_df['id'] == asset_id]
        if asset_info.empty:
            raise ValueError(f"Asset {asset_id} not found")
        
        return asset_info.iloc[0].to_dict()
    
    def get_asset_valuation(self, asset_id: str, day: int) -> float:
        """Get asset valuation for a specific day."""
        if self.valuations_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        valuation = self.valuations_df[
            (self.valuations_df['asset_id'] == asset_id) & 
            (self.valuations_df['day'] == day)
        ]
        
        if valuation.empty:
            raise ValueError(f"No valuation found for {asset_id} on day {day}")
        
        return float(valuation['valuation'].iloc[0])
    
    def get_all_assets(self) -> List[str]:
        """Get list of all asset IDs."""
        if self.assets_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        return self.assets_df['id'].tolist()
    
    def get_available_assets(self, day: int) -> List[str]:
        """Get list of assets available for purchase on a given day."""
        if self.assets_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        available_assets = self.assets_df[self.assets_df['available_on_day'] <= day]
        return available_assets['id'].tolist()
    
    def get_daily_valuations(self, day: int) -> Dict[str, float]:
        """Get valuations for all assets on a specific day."""
        if self.valuations_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        day_valuations = self.valuations_df[self.valuations_df['day'] == day]
        return dict(zip(day_valuations['asset_id'], day_valuations['valuation']))
    
    def get_asset_price_history(self, asset_id: str, up_to_day: int = None) -> pd.DataFrame:
        """Get price history for an asset up to a specific day."""
        if self.valuations_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        asset_history = self.valuations_df[self.valuations_df['asset_id'] == asset_id]
        
        if up_to_day is not None:
            asset_history = asset_history[asset_history['day'] <= up_to_day]
        
        return asset_history.sort_values('day')
    
    def get_tax_rate(self, asset_id: str, day: int) -> Tuple[float, float]:
        """Get tax rate and rate modifier for an asset on a specific day."""
        if self.tax_rates_df is None:
            return 0.0, 0.0  # No taxes in Year 1
        
        # Get asset type info
        asset_info = self.get_asset_info(asset_id)
        asset_type = asset_info['type']
        asset_sub_type = asset_info['sub_type']
        
        # Find the most recent tax rate entry for this asset type/subtype
        relevant_rates = self.tax_rates_df[
            (self.tax_rates_df['asset_type'] == asset_type) &
            (self.tax_rates_df['asset_sub_type'] == asset_sub_type) &
            (self.tax_rates_df['day'] <= day)
        ].sort_values('day', ascending=False)
        
        if relevant_rates.empty:
            raise ValueError(f"No tax rate found for {asset_type}/{asset_sub_type} up to day {day}")
        
        latest_rate = relevant_rates.iloc[0]
        return float(latest_rate['tax_rate']), float(latest_rate['base_rate_modifier'])
    
    def calculate_daily_tax(self, asset_id: str, current_valuation: float, day: int, days_since_last_payment: int) -> float:
        """Calculate daily tax owed for an asset."""
        tax_rate, rate_modifier = self.get_tax_rate(asset_id, day)
        effective_rate = tax_rate + (rate_modifier * days_since_last_payment)
        return current_valuation * effective_rate