"""Data loading utilities for Year 1 challenge."""

import csv
from pathlib import Path
from typing import Dict, List, Tuple


class DataLoader:
    """Loads and parses challenge data files."""
    
    def __init__(self, data_dir: Path):
        """Initialize data loader with data directory path."""
        self.data_dir = data_dir
        self.assets_file = data_dir / "assets.csv"
        self.valuations_file = data_dir / "valuations.csv"
    
    def load_assets(self) -> Dict[str, Dict]:
        """Load asset metadata from assets.csv.
        
        Returns:
            Dict mapping asset_id to asset metadata
        """
        assets = {}
        with open(self.assets_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                asset_id = row['id']
                assets[asset_id] = {
                    'name': row['name'],
                    'type': row['type'],
                    'sub_type': row['sub_type'],
                    'available_on_day': int(row['available_on_day']),
                    'region': row['region']
                }
        return assets
    
    def load_valuations(self) -> Dict[str, Dict[int, int]]:
        """Load asset valuations from valuations.csv.
        
        Returns:
            Dict mapping asset_id to dict of {day: valuation}
        """
        valuations = {}
        with open(self.valuations_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                asset_id = row['asset_id']
                day = int(row['day'])
                valuation = int(row['valuation'])
                
                if asset_id not in valuations:
                    valuations[asset_id] = {}
                valuations[asset_id][day] = valuation
        
        return valuations
    
    def load_all(self) -> Tuple[Dict[str, Dict], Dict[str, Dict[int, int]]]:
        """Load both assets and valuations.
        
        Returns:
            Tuple of (assets, valuations)
        """
        return self.load_assets(), self.load_valuations()
