"""
Debug tax calculations to understand why they're so high.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import DataLoader

def test_tax_calculation():
    """Test tax calculation for a simple case."""
    
    data_loader = DataLoader("../problems/year_2/data", year=2)
    assets_df, valuations_df, tax_rates_df = data_loader.load_data()
    
    print("=== TAX CALCULATION DEBUG ===")
    
    # Test with asset_1 (Residential)
    asset_id = "asset_1"
    asset_info = data_loader.get_asset_info(asset_id)
    print(f"\nAsset: {asset_id} - {asset_info['name']} ({asset_info['sub_type']})")
    
    # Get day 1 and day 10 valuations
    day1_val = data_loader.get_asset_valuation(asset_id, 1)
    day10_val = data_loader.get_asset_valuation(asset_id, 10)
    
    print(f"Day 1 valuation: {day1_val:,.0f} FSB")
    print(f"Day 10 valuation: {day10_val:,.0f} FSB")
    
    # Check tax rates
    tax_rate, rate_modifier = data_loader.get_tax_rate(asset_id, 1)
    print(f"Base tax rate: {tax_rate:.3%}")
    print(f"Rate modifier: {rate_modifier:.3%} per day")
    
    # Calculate daily tax for different days since last payment
    print(f"\nDaily tax calculations:")
    for days_since_payment in range(1, 11):
        daily_tax = data_loader.calculate_daily_tax(asset_id, day1_val, 1, days_since_payment)
        effective_rate = tax_rate + (rate_modifier * days_since_payment)
        print(f"Day {days_since_payment}: {daily_tax:>8.0f} FSB (rate: {effective_rate:.3%})")
    
    # Calculate 10-day tax burden if we pay every 10 days
    total_tax = 0
    for day in range(1, 11):
        valuation = data_loader.get_asset_valuation(asset_id, day)
        daily_tax = data_loader.calculate_daily_tax(asset_id, valuation, day, day)  # Pay each day
        total_tax += daily_tax
        print(f"Day {day}: val={valuation:>8.0f}, tax={daily_tax:>6.0f} (cumulative: {total_tax:>8.0f})")
    
    print(f"\nTotal tax for 10 days (paying daily): {total_tax:,.0f} FSB")
    print(f"As percentage of average valuation: {total_tax / ((day1_val + day10_val) / 2) * 100:.2f}%")

if __name__ == "__main__":
    test_tax_calculation()