#!/usr/bin/env python3
"""
Validate Year 2 strategy output for rule compliance.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import yaml
from pathlib import Path
from data_loader import DataLoader

def validate_strategy():
    """Check if our strategy violates any rules."""
    
    print("🔍 Validating Year 2 Strategy for Rule Compliance 🔍")
    
    # Load the output file
    output_file = Path("../problems/year_2/output/output.yml")
    if not output_file.exists():
        print("❌ No output file found!")
        return False
    
    with open(output_file, 'r') as f:
        daily_actions = yaml.safe_load(f)
    
    # Load data
    data_loader = DataLoader("../problems/year_2/data", year=2)
    data_loader.load_data()
    
    # Simulate the strategy to check for violations
    cash = 144411
    owned_assets = {
        'asset_1': {'last_tax_payment': 0},
        'asset_2': {'last_tax_payment': 0},
        'asset_11': {'last_tax_payment': 0},
        'asset_13': {'last_tax_payment': 0},
        'asset_15': {'last_tax_payment': 0}
    }
    
    violations = []
    unpaid_taxes = {}  # Track unpaid taxes by asset
    
    for day in range(1, 101):
        # Check for unpaid taxes that exceed 30 days
        for asset_id in list(owned_assets.keys()):
            days_since_payment = day - owned_assets[asset_id]['last_tax_payment']
            if days_since_payment > 30:
                violations.append(f"Day {day}: Tax payment overdue for {asset_id} ({days_since_payment} days)")
        
        # Process actions for this day
        if day in daily_actions:
            for action in daily_actions[day]:
                if 'pay_tax' in action:
                    asset_id = action['pay_tax']
                    if asset_id in owned_assets:
                        owned_assets[asset_id]['last_tax_payment'] = day
                        # Remove from unpaid taxes
                        if asset_id in unpaid_taxes:
                            del unpaid_taxes[asset_id]
                
                elif 'sell' in action:
                    asset_id = action['sell']
                    if asset_id in owned_assets:
                        # Check if all taxes are paid before selling
                        days_since_payment = day - owned_assets[asset_id]['last_tax_payment']
                        if days_since_payment > 0:
                            violations.append(f"Day {day}: Selling {asset_id} with {days_since_payment} days of unpaid taxes")
                        del owned_assets[asset_id]
                        if asset_id in unpaid_taxes:
                            del unpaid_taxes[asset_id]
                
                elif 'buy' in action:
                    asset_id = action['buy']
                    owned_assets[asset_id] = {'last_tax_payment': day}
    
    # Check for unpaid taxes at end of year
    final_unpaid_taxes = 0
    for asset_id in owned_assets:
        days_since_payment = 100 - owned_assets[asset_id]['last_tax_payment']
        if days_since_payment > 0:
            violations.append(f"End of year: {asset_id} has {days_since_payment} days of unpaid taxes")
            
            # Calculate penalty (rough estimate)
            try:
                day_100_value = data_loader.get_asset_valuation(asset_id, 100)
                estimated_tax = day_100_value * 0.02 * days_since_payment  # Rough estimate
                final_unpaid_taxes += estimated_tax
            except:
                pass
    
    print(f"\n📊 VALIDATION RESULTS:")
    
    if violations:
        print(f"❌ Found {len(violations)} rule violations:")
        for violation in violations[:10]:  # Show first 10
            print(f"  - {violation}")
        if len(violations) > 10:
            print(f"  ... and {len(violations) - 10} more")
    else:
        print("✅ No rule violations found!")
    
    if final_unpaid_taxes > 0:
        print(f"⚠️ Estimated unpaid tax penalty: {final_unpaid_taxes:,.0f} FSB")
        print(f"⚠️ This would be deducted from final score (2x penalty)")
        adjusted_wealth = 2100283 - (final_unpaid_taxes * 2)
        print(f"⚠️ Adjusted final wealth: {adjusted_wealth:,.0f} FSB")
    
    return len(violations) == 0 and final_unpaid_taxes == 0

if __name__ == "__main__":
    is_valid = validate_strategy()
    print(f"\n🎯 Strategy is {'VALID' if is_valid else 'INVALID'}")