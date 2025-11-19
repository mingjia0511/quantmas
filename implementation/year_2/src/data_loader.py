"""Data loading utilities for Year 2."""

import csv
from pathlib import Path
from typing import Dict, List


def load_assets(data_dir: Path) -> List[Dict]:
    """Load assets from CSV file."""
    assets = []
    assets_file = data_dir / 'assets.csv'
    
    with open(assets_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            assets.append({
                'asset_id': row['id'],
                'asset_type': row['type'],
                'asset_sub_type': row['sub_type'],
                'name': row['name'],
                'available_on_day': int(row['available_on_day']),
                'region': row['region']
            })
    
    return assets


def load_valuations(data_dir: Path) -> Dict[str, Dict[int, float]]:
    """
    Load valuations from CSV file.
    
    Returns:
        Dict mapping asset_id -> {day: valuation}
    """
    valuations = {}
    valuations_file = data_dir / 'valuations.csv'
    
    with open(valuations_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            asset_id = row['asset_id']
            day = int(row['day'])
            valuation = float(row['valuation'])
            
            if asset_id not in valuations:
                valuations[asset_id] = {}
            
            valuations[asset_id][day] = valuation
    
    return valuations


def load_tax_rates(data_dir: Path) -> Dict[str, Dict[int, Dict]]:
    """
    Load tax rates from CSV file.
    
    Returns:
        Dict mapping asset_sub_type -> {day: {base_rate, modifier}}
    """
    tax_rates = {}
    tax_file = data_dir / 'tax_rates.csv'
    
    with open(tax_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sub_type = row['asset_sub_type']
            day = int(row['day'])
            
            if sub_type not in tax_rates:
                tax_rates[sub_type] = {}
            
            tax_rates[sub_type][day] = {
                'base_rate': float(row['tax_rate']),
                'modifier': float(row['base_rate_modifier'])
            }
    
    return tax_rates
