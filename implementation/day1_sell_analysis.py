#!/usr/bin/env python3
"""
Quick analysis: What if we sell all assets on Day 1?
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import DataLoader

def main():
    print("🎄 Day 1 Sell Analysis 🎄")
    
    data_loader = DataLoader("../problems/year_2/data", year=2)
    data_loader.load_data()
    
    owned_assets = ['asset_1', 'asset_13', 'asset_2', 'asset_11', 'asset_15']
    starting_cash = 144411
    
    total_day1_value = 0
    
    print("Selling all assets on Day 1:")
    for asset_id in owned_assets:
        day1_price = data_loader.get_asset_valuation(asset_id, 1)
        asset_info = data_loader.get_asset_info(asset_id)
        total_day1_value += day1_price
        print(f"  {asset_id} ({asset_info['name']}): {day1_price:,.0f} FSB")
    
    final_cash = starting_cash + total_day1_value
    print(f"\nStarting cash: {starting_cash:,.0f} FSB")
    print(f"Asset sale proceeds: {total_day1_value:,.0f} FSB")
    print(f"Final cash (no taxes): {final_cash:,.0f} FSB")
    
    # Compare to Year 1 ending wealth
    year1_wealth = 1386404  # From our analysis
    print(f"\nYear 1 ending wealth: {year1_wealth:,.0f} FSB")
    print(f"Year 2 'sell everything' wealth: {final_cash:,.0f} FSB")
    print(f"Difference: {final_cash - year1_wealth:,.0f} FSB")

if __name__ == "__main__":
    main()