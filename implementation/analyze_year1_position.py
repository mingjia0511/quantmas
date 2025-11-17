#!/usr/bin/env python3
"""
Analyze Year 1 ending position to determine starting position for Year 2.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import yaml
from pathlib import Path

def load_year1_output():
    """Load Year 1 output and determine final portfolio state."""
    output_path = Path("../problems/year_1/output/output.yml")
    
    with open(output_path, 'r') as f:
        trades = yaml.safe_load(f)
    
    return trades

def load_year1_data():
    """Load Year 1 assets and valuations data."""
    data_dir = Path("../problems/year_1/data")
    
    assets_df = pd.read_csv(data_dir / "assets.csv")
    valuations_df = pd.read_csv(data_dir / "valuations.csv")
    
    return assets_df, valuations_df

def analyze_final_position():
    """Analyze what we own at the end of Year 1."""
    print("🎄 Analyzing Year 1 Final Position 🎄")
    
    # Load data
    trades = load_year1_output()
    assets_df, valuations_df = load_year1_data()
    
    # Track portfolio over time
    portfolio = {}
    cash = 1_000_000  # Starting cash
    
    print("📊 Processing trades...")
    
    for day, actions in trades.items():
        day = int(day)
        
        for action in actions:
            if 'buy' in action:
                asset_id = action['buy']
                # Get the price on this day
                price = valuations_df[
                    (valuations_df['asset_id'] == asset_id) & 
                    (valuations_df['day'] == day)
                ]['valuation'].iloc[0]
                
                portfolio[asset_id] = day  # Track when we bought it
                cash -= price
                print(f"Day {day}: Bought {asset_id} for {price:,.0f} FSB")
                
            elif 'sell' in action:
                asset_id = action['sell']
                # Get the price on this day
                price = valuations_df[
                    (valuations_df['asset_id'] == asset_id) & 
                    (valuations_df['day'] == day)
                ]['valuation'].iloc[0]
                
                if asset_id in portfolio:
                    del portfolio[asset_id]
                    cash += price
                    print(f"Day {day}: Sold {asset_id} for {price:,.0f} FSB")
    
    # Calculate final position on day 100
    print("\n🏆 Final Position on Day 100:")
    print(f"💰 Cash: {cash:,.0f} FSB")
    
    total_asset_value = 0
    print("🏠 Assets owned:")
    
    for asset_id in portfolio:
        # Get day 100 valuation
        day_100_value = valuations_df[
            (valuations_df['asset_id'] == asset_id) & 
            (valuations_df['day'] == 100)
        ]['valuation'].iloc[0]
        
        asset_name = assets_df[assets_df['id'] == asset_id]['name'].iloc[0]
        asset_type = assets_df[assets_df['id'] == asset_id]['sub_type'].iloc[0]
        
        total_asset_value += day_100_value
        print(f"  - {asset_id} ({asset_name}, {asset_type}): {day_100_value:,.0f} FSB")
    
    total_wealth = cash + total_asset_value
    print(f"\n💎 Total Wealth: {total_wealth:,.0f} FSB")
    print(f"   Cash: {cash:,.0f} FSB")
    print(f"   Assets: {total_asset_value:,.0f} FSB")
    
    return cash, portfolio, assets_df

if __name__ == "__main__":
    analyze_final_position()