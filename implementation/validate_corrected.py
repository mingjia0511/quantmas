#!/usr/bin/env python3
"""
Re-validate Year 2 strategy with correct interpretation:
You can sell and pay taxes on the same day (receive sale_price - accumulated_taxes).
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import yaml
from pathlib import Path
from data_loader import DataLoader

def calculate_accumulated_tax(asset_id, last_payment_day, sell_day, data_loader):
    """Calculate total accumulated tax from last payment to sell day."""
    total_tax = 0.0
    
    for day in range(last_payment_day + 1, sell_day + 1):
        try:
            valuation = data_loader.get_asset_valuation(asset_id, day)
            days_since_payment = day - last_payment_day
            daily_tax = data_loader.calculate_daily_tax(asset_id, valuation, day, days_since_payment)
            total_tax += daily_tax
        except:
            continue
    
    return total_tax

def validate_strategy_corrected():
    """Check strategy with correct rule interpretation."""
    
    print("🔍 Re-validating Year 2 Strategy (Corrected Rules) 🔍")
    
    # Load the output file
    output_file = Path("../problems/year_2/output/output.yml")
    with open(output_file, 'r') as f:
        daily_actions = yaml.safe_load(f)
    
    # Load data
    data_loader = DataLoader("../problems/year_2/data", year=2)
    data_loader.load_data()
    
    # Re-simulate with correct logic
    cash = 144411
    owned_assets = {
        'asset_1': {'last_tax_payment': 0},
        'asset_2': {'last_tax_payment': 0}, 
        'asset_11': {'last_tax_payment': 0},
        'asset_13': {'last_tax_payment': 0},
        'asset_15': {'last_tax_payment': 0}
    }
    
    violations = []
    total_wealth_timeline = []
    
    print(f"Starting: {cash:,.0f} FSB cash + 5 owned assets")
    
    for day in range(1, 101):
        daily_tax_paid = 0
        daily_gross_proceeds = 0
        daily_net_proceeds = 0
        
        # Process actions for this day
        if day in daily_actions:
            for action in daily_actions[day]:
                if 'pay_tax' in action:
                    asset_id = action['pay_tax']
                    if asset_id in owned_assets:
                        # Calculate and pay accumulated tax
                        last_payment = owned_assets[asset_id]['last_tax_payment']
                        accumulated_tax = calculate_accumulated_tax(asset_id, last_payment, day, data_loader)
                        
                        cash -= accumulated_tax
                        daily_tax_paid += accumulated_tax
                        owned_assets[asset_id]['last_tax_payment'] = day
                
                elif 'sell' in action:
                    asset_id = action['sell']
                    if asset_id in owned_assets:
                        # Calculate sale price and accumulated taxes
                        sale_price = data_loader.get_asset_valuation(asset_id, day)
                        last_payment = owned_assets[asset_id]['last_tax_payment']
                        accumulated_tax = calculate_accumulated_tax(asset_id, last_payment, day, data_loader)
                        
                        # Net proceeds = sale price - accumulated taxes
                        net_proceeds = sale_price - accumulated_tax
                        cash += net_proceeds
                        
                        daily_gross_proceeds += sale_price
                        daily_net_proceeds += net_proceeds
                        daily_tax_paid += accumulated_tax
                        
                        del owned_assets[asset_id]
                        
                        print(f"Day {day}: Sold {asset_id} for {sale_price:,.0f} FSB, paid {accumulated_tax:,.0f} tax, net: {net_proceeds:,.0f} FSB")
                
                elif 'buy' in action:
                    asset_id = action['buy']
                    buy_price = data_loader.get_asset_valuation(asset_id, day)
                    
                    if cash >= buy_price:
                        cash -= buy_price
                        owned_assets[asset_id] = {'last_tax_payment': day}
                        print(f"Day {day}: Bought {asset_id} for {buy_price:,.0f} FSB")
                    else:
                        violations.append(f"Day {day}: Insufficient cash to buy {asset_id} ({buy_price:,.0f} needed, {cash:,.0f} available)")
        
        # Check for tax overdue (> 30 days)
        for asset_id in owned_assets:
            days_since_payment = day - owned_assets[asset_id]['last_tax_payment']
            if days_since_payment > 30:
                violations.append(f"Day {day}: Tax overdue for {asset_id} ({days_since_payment} days)")
        
        # Track wealth progression
        asset_value = sum(data_loader.get_asset_valuation(aid, day) for aid in owned_assets)
        total_wealth = cash + asset_value
        total_wealth_timeline.append((day, total_wealth, cash, asset_value, len(owned_assets)))
    
    # Final check - any unpaid taxes at end
    final_unpaid_tax = 0
    for asset_id in owned_assets:
        last_payment = owned_assets[asset_id]['last_tax_payment']
        if last_payment < 100:
            accumulated_tax = calculate_accumulated_tax(asset_id, last_payment, 100, data_loader)
            final_unpaid_tax += accumulated_tax
            print(f"End of year: {asset_id} has unpaid tax of {accumulated_tax:,.0f} FSB")
    
    # Calculate final wealth
    final_asset_value = sum(data_loader.get_asset_valuation(aid, 100) for aid in owned_assets)
    final_wealth_before_penalty = cash + final_asset_value
    penalty = final_unpaid_tax * 2  # 2x penalty for unpaid taxes
    final_wealth = final_wealth_before_penalty - penalty
    
    print(f"\n🏆 CORRECTED FINAL RESULTS:")
    print(f"Final Cash: {cash:,.0f} FSB")
    print(f"Final Assets Value: {final_asset_value:,.0f} FSB")
    print(f"Unpaid Tax Penalty (2x): {penalty:,.0f} FSB")
    print(f"Final Wealth: {final_wealth:,.0f} FSB")
    
    print(f"\n📊 VALIDATION RESULTS:")
    if violations:
        print(f"❌ Found {len(violations)} violations:")
        for violation in violations:
            print(f"  - {violation}")
    else:
        print("✅ No rule violations found!")
    
    return len(violations) == 0, final_wealth

if __name__ == "__main__":
    is_valid, wealth = validate_strategy_corrected()
    print(f"\n🎯 Strategy is {'VALID' if is_valid else 'INVALID'}")
    print(f"💰 Corrected final wealth: {wealth:,.0f} FSB")