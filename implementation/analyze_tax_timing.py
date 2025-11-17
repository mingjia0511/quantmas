#!/usr/bin/env python3
"""
Analyze our Year 2 strategy to see if we're using strategic tax timing.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import yaml
from pathlib import Path
from data_loader import DataLoader

def analyze_tax_timing_strategy():
    """Analyze our actual tax payment timing decisions."""
    
    print("🔍 Analyzing Tax Timing Strategy 🔍")
    
    # Load the output file
    output_file = Path("../problems/year_2/output/output.yml")
    with open(output_file, 'r') as f:
        daily_actions = yaml.safe_load(f)
    
    # Load data
    data_loader = DataLoader("../problems/year_2/data", year=2)
    data_loader.load_data()
    
    # Track tax payment patterns
    owned_assets = {
        'asset_1': {'buy_day': 0, 'last_tax_payment': 0},
        'asset_2': {'buy_day': 0, 'last_tax_payment': 0},
        'asset_11': {'buy_day': 0, 'last_tax_payment': 0},
        'asset_13': {'buy_day': 0, 'last_tax_payment': 0},
        'asset_15': {'buy_day': 0, 'last_tax_payment': 0}
    }
    
    tax_payments = []  # Track all tax payments
    tax_delays = []    # Track strategic delays
    
    print(f"{'Day':<4} {'Action':<10} {'Asset':<8} {'Days Since':<11} {'Strategic?'}")
    print("-" * 60)
    
    for day in range(1, 101):
        # Process actions for this day
        if day in daily_actions:
            for action in daily_actions[day]:
                if 'pay_tax' in action:
                    asset_id = action['pay_tax']
                    if asset_id in owned_assets:
                        days_since_payment = day - owned_assets[asset_id]['last_tax_payment']
                        
                        # Is this strategic timing?
                        strategic = "No" if days_since_payment == 1 else "YES"
                        
                        print(f"{day:<4} {'PAY_TAX':<10} {asset_id:<8} {days_since_payment:<11} {strategic}")
                        
                        tax_payments.append({
                            'day': day,
                            'asset_id': asset_id,
                            'days_since_payment': days_since_payment,
                            'strategic': days_since_payment > 1
                        })
                        
                        if days_since_payment > 1:
                            tax_delays.append({
                                'asset_id': asset_id,
                                'delay_days': days_since_payment,
                                'payment_day': day
                            })
                        
                        owned_assets[asset_id]['last_tax_payment'] = day
                
                elif 'sell' in action:
                    asset_id = action['sell']
                    if asset_id in owned_assets:
                        days_since_payment = day - owned_assets[asset_id]['last_tax_payment']
                        strategic = "N/A" if days_since_payment == 0 else "SELL+TAX"
                        
                        print(f"{day:<4} {'SELL':<10} {asset_id:<8} {days_since_payment:<11} {strategic}")
                        
                        if days_since_payment > 0:
                            tax_delays.append({
                                'asset_id': asset_id,
                                'delay_days': days_since_payment,
                                'payment_day': day,
                                'paid_on_sale': True
                            })
                        
                        del owned_assets[asset_id]
                
                elif 'buy' in action:
                    asset_id = action['buy']
                    owned_assets[asset_id] = {'buy_day': day, 'last_tax_payment': day}
                    print(f"{day:<4} {'BUY':<10} {asset_id:<8} {'0':<11} {'N/A'}")
    
    print(f"\n📊 TAX TIMING ANALYSIS:")
    
    total_payments = len(tax_payments)
    strategic_payments = len([p for p in tax_payments if p['strategic']])
    daily_payments = total_payments - strategic_payments
    
    print(f"Total explicit tax payments: {total_payments}")
    print(f"Daily payments (1 day): {daily_payments}")
    print(f"Strategic delays (>1 day): {strategic_payments}")
    print(f"Strategic percentage: {strategic_payments/total_payments*100 if total_payments > 0 else 0:.1f}%")
    
    if tax_delays:
        print(f"\n🎯 STRATEGIC TAX DELAYS:")
        for delay in tax_delays:
            delay_type = " (paid on sale)" if delay.get('paid_on_sale') else ""
            print(f"  {delay['asset_id']}: {delay['delay_days']} days delay on day {delay['payment_day']}{delay_type}")
        
        avg_delay = sum(d['delay_days'] for d in tax_delays) / len(tax_delays)
        print(f"Average strategic delay: {avg_delay:.1f} days")
    else:
        print("\n❌ NO STRATEGIC TAX DELAYS FOUND")
        print("Strategy appears to use mostly daily tax payments")
    
    # Analyze if delays were beneficial
    print(f"\n🧮 DELAY BENEFIT ANALYSIS:")
    for delay in tax_delays[:5]:  # Analyze first 5 delays
        asset_id = delay['asset_id']
        payment_day = delay['payment_day']
        delay_days = delay['delay_days']
        
        # Compare cost of paying daily vs waiting
        try:
            start_day = payment_day - delay_days + 1
            
            # Cost if paid daily
            daily_cost = 0
            for d in range(start_day, payment_day + 1):
                valuation = data_loader.get_asset_valuation(asset_id, d)
                daily_rate = data_loader.calculate_daily_tax(asset_id, valuation, d, 1)
                daily_cost += daily_rate
            
            # Cost of waiting (what we actually paid)
            delayed_cost = 0
            for d in range(start_day, payment_day + 1):
                valuation = data_loader.get_asset_valuation(asset_id, d)
                days_since = d - (start_day - 1)
                daily_rate = data_loader.calculate_daily_tax(asset_id, valuation, d, days_since)
                delayed_cost += daily_rate
            
            savings = daily_cost - delayed_cost
            print(f"  {asset_id}: Daily cost: {daily_cost:.0f}, Delayed cost: {delayed_cost:.0f}, Savings: {savings:.0f}")
            
        except Exception as e:
            print(f"  {asset_id}: Analysis error: {e}")

if __name__ == "__main__":
    analyze_tax_timing_strategy()