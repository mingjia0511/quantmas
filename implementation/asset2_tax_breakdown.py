#!/usr/bin/env python3
"""
Detailed breakdown of asset_2 tax calculation.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import DataLoader

def analyze_asset_2_taxes():
    print("🔍 Asset 2 Tax Breakdown Analysis 🔍")
    
    data_loader = DataLoader("../problems/year_2/data", year=2)
    data_loader.load_data()
    
    asset_id = 'asset_2'
    asset_info = data_loader.get_asset_info(asset_id)
    
    print(f"Asset: {asset_id} ({asset_info['name']})")
    print(f"Type: {asset_info['type']} - {asset_info['sub_type']}")
    
    # Get tax rates for commercial assets
    print("\nTax Rates for Commercial Assets:")
    tax_rates = data_loader.tax_rates_df[
        (data_loader.tax_rates_df['asset_type'] == 'Real Estate') &
        (data_loader.tax_rates_df['asset_sub_type'] == 'Commercial')
    ]
    for _, row in tax_rates.iterrows():
        print(f"  Day {row['day']}: Base {row['tax_rate']*100:.1f}% + {row['base_rate_modifier']*100:.1f}% per delay day")
    
    # Scenario: Hold from Day 1 to Day 25 (when we should sell based on analysis)
    print(f"\nScenario: Own asset_2 from Day 1 to Day 25")
    print(f"Strategy: Pay taxes daily (1-day intervals)")
    
    total_tax = 0.0
    print(f"\n{'Day':<4} {'Valuation':<10} {'Days Since':<11} {'Tax Rate':<9} {'Daily Tax':<10} {'Running Total':<12}")
    print("-" * 70)
    
    for day in range(1, 26):  # Day 1 to 25
        try:
            valuation = data_loader.get_asset_valuation(asset_id, day)
            days_since_payment = 1  # Paying daily
            
            # Get tax rate for this day
            base_rate, rate_modifier = data_loader.get_tax_rate(asset_id, day)
            effective_rate = base_rate + (rate_modifier * days_since_payment)
            
            daily_tax = valuation * effective_rate
            total_tax += daily_tax
            
            print(f"{day:<4} {valuation:<10,.0f} {days_since_payment:<11} {effective_rate*100:<8.2f}% {daily_tax:<10,.0f} {total_tax:<12,.0f}")
            
        except Exception as e:
            print(f"Day {day}: Error - {e}")
    
    print(f"\nTotal tax for 25 days (daily payments): {total_tax:,.0f} FSB")
    
    # Now let's see what happens with different payment intervals
    print(f"\n" + "="*80)
    print("COMPARISON: Different Payment Intervals")
    print("="*80)
    
    intervals = [1, 3, 5, 10, 15]
    
    for interval in intervals:
        total_tax_interval = 0.0
        last_payment_day = 0
        current_day = 1
        
        while current_day <= 25:
            # Pay every 'interval' days
            payment_day = min(last_payment_day + interval, 25)
            
            # Calculate accumulated tax for this period
            period_tax = 0.0
            for day in range(last_payment_day + 1, payment_day + 1):
                valuation = data_loader.get_asset_valuation(asset_id, day)
                days_since_payment = day - last_payment_day
                base_rate, rate_modifier = data_loader.get_tax_rate(asset_id, day)
                effective_rate = base_rate + (rate_modifier * days_since_payment)
                daily_tax = valuation * effective_rate
                period_tax += daily_tax
            
            total_tax_interval += period_tax
            print(f"  {interval}-day interval: Pay on day {payment_day}, period cost: {period_tax:,.0f} FSB")
            
            last_payment_day = payment_day
            current_day = payment_day + 1
        
        print(f"  Total tax ({interval}-day intervals): {total_tax_interval:,.0f} FSB")
        print()
    
    # Let's also check: what's the asset value progression?
    print("Asset Value Progression:")
    day1_value = data_loader.get_asset_valuation(asset_id, 1)
    day25_value = data_loader.get_asset_valuation(asset_id, 25)
    print(f"  Day 1 value: {day1_value:,.0f} FSB")
    print(f"  Day 25 value: {day25_value:,.0f} FSB")
    print(f"  Value increase: {day25_value - day1_value:,.0f} FSB ({((day25_value/day1_value-1)*100):+.1f}%)")
    print(f"  Daily tax (1-day): {total_tax:,.0f} FSB")
    print(f"  Net gain: {(day25_value - day1_value) - total_tax:,.0f} FSB")

if __name__ == "__main__":
    analyze_asset_2_taxes()