#!/usr/bin/env python3
"""
Asset-by-asset analysis for Year 2 with optimal tax strategy.
For each asset, calculate optimal buy/sell and tax payment timing.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import yaml
from pathlib import Path
from data_loader import DataLoader
from portfolio_tracker import PortfolioTracker

def calculate_optimal_tax_payments(asset_id, buy_day, sell_day, data_loader):
    """Calculate optimal tax payment schedule for holding an asset from buy_day to sell_day."""
    if sell_day is None:
        sell_day = 100
    
    # Track when to pay taxes and total cost
    payment_schedule = []
    total_tax_cost = 0.0
    last_payment_day = buy_day
    
    current_day = buy_day + 1  # Tax starts day after purchase
    
    while current_day <= sell_day:
        # Calculate cost for each possible payment day (1 to 30 days from last payment)
        min_cost = float('inf')
        optimal_payment_day = current_day
        
        max_wait = min(30, sell_day - last_payment_day)
        
        for wait_days in range(1, max_wait + 1):
            payment_day = last_payment_day + wait_days
            if payment_day > sell_day:
                break
                
            # Calculate total tax cost if we pay on this day
            period_cost = 0.0
            for day in range(last_payment_day + 1, payment_day + 1):
                try:
                    valuation = data_loader.get_asset_valuation(asset_id, day)
                    days_since_payment = day - last_payment_day
                    daily_tax = data_loader.calculate_daily_tax(asset_id, valuation, day, days_since_payment)
                    period_cost += daily_tax
                except:
                    break
            
            if period_cost < min_cost:
                min_cost = period_cost
                optimal_payment_day = payment_day
        
        # Record this payment
        payment_schedule.append({
            'day': optimal_payment_day,
            'cost': min_cost
        })
        total_tax_cost += min_cost
        last_payment_day = optimal_payment_day
        current_day = optimal_payment_day + 1
    
    return payment_schedule, total_tax_cost

def analyze_asset(asset_id, data_loader, currently_owned=False):
    """Analyze a single asset for optimal strategy."""
    try:
        asset_info = data_loader.get_asset_info(asset_id)
        price_history = data_loader.get_asset_price_history(asset_id)
        
        # Find optimal buy/sell days
        min_price = price_history['valuation'].min()
        max_price = price_history['valuation'].max()
        min_day = price_history[price_history['valuation'] == min_price]['day'].iloc[0]
        max_day = price_history[price_history['valuation'] == max_price]['day'].iloc[0]
        
        # For currently owned assets, we "bought" them at end of Year 1 (day 0) at Year 1 day 100 price
        if currently_owned:
            # Get the Year 2 day 1 price as our "purchase" price
            buy_day = 0  # We already own it
            buy_price = data_loader.get_asset_valuation(asset_id, 1)  # Current value
            # But check if we should sell immediately or hold
            day_1_price = data_loader.get_asset_valuation(asset_id, 1)
            if max_day == 1:  # Peak is day 1, sell immediately
                sell_day = 1
                sell_price = max_price
            else:
                sell_day = max_day if max_day < 100 else 100
                sell_price = data_loader.get_asset_valuation(asset_id, sell_day)
        else:
            # Check if available and worth buying
            if min_day < asset_info['available_on_day']:
                # Can't buy at min price, adjust
                available_day = asset_info['available_on_day']
                available_price = data_loader.get_asset_valuation(asset_id, available_day)
                buy_day = available_day
                buy_price = available_price
            else:
                buy_day = min_day
                buy_price = min_price
            
            sell_day = max_day if max_day < 100 else 100
            sell_price = data_loader.get_asset_valuation(asset_id, sell_day)
        
        # Calculate optimal tax strategy
        if currently_owned or buy_day < 100:
            payment_schedule, total_tax_cost = calculate_optimal_tax_payments(
                asset_id, buy_day, sell_day, data_loader
            )
        else:
            payment_schedule = []
            total_tax_cost = 0.0
        
        # Calculate profitability
        if currently_owned:
            # We already own it, so profit is just sell_price minus taxes
            gross_profit = sell_price - buy_price  # Current value to sell value
            net_profit = gross_profit - total_tax_cost
            investment = buy_price  # Current value as our "investment"
        else:
            gross_profit = sell_price - buy_price
            net_profit = gross_profit - total_tax_cost
            investment = buy_price
        
        net_roi = (net_profit / investment * 100) if investment > 0 else 0
        
        return {
            'asset_id': asset_id,
            'name': asset_info['name'],
            'sub_type': asset_info['sub_type'],
            'currently_owned': currently_owned,
            'available_day': asset_info['available_on_day'],
            'buy_day': buy_day,
            'buy_price': buy_price,
            'sell_day': sell_day,
            'sell_price': sell_price,
            'gross_profit': gross_profit,
            'total_tax_cost': total_tax_cost,
            'net_profit': net_profit,
            'net_roi': net_roi,
            'payment_schedule': payment_schedule,
            'worth_trading': net_roi > 0
        }
        
    except Exception as e:
        return {
            'asset_id': asset_id,
            'error': str(e)
        }

def main():
    """Analyze all assets for Year 2."""
    print("🎄 Year 2 Asset-by-Asset Analysis 🎄")
    
    # Load data
    data_loader = DataLoader("../problems/year_2/data", year=2)
    data_loader.load_data()
    
    # Assets we currently own from Year 1
    owned_assets = {'asset_1', 'asset_13', 'asset_2', 'asset_11', 'asset_15'}
    
    # Get all assets
    all_assets = data_loader.get_all_assets()
    
    results = []
    
    print(f"\nAnalyzing {len(all_assets)} assets...")
    print(f"Currently owned: {len(owned_assets)} assets")
    print("-" * 120)
    
    for asset_id in all_assets:
        currently_owned = asset_id in owned_assets
        result = analyze_asset(asset_id, data_loader, currently_owned)
        results.append(result)
        
        if 'error' not in result:
            status = "OWN" if currently_owned else "NEW"
            worth = "✅" if result['worth_trading'] else "❌"
            
            print(f"{asset_id:<8} {status:<4} {worth} {result['sub_type']:<11} "
                  f"Buy: Day {result['buy_day']:<3} @{result['buy_price']:<8,.0f} "
                  f"Sell: Day {result['sell_day']:<3} @{result['sell_price']:<8,.0f} "
                  f"Tax: {result['total_tax_cost']:<8,.0f} "
                  f"Net: {result['net_profit']:<8,.0f} "
                  f"ROI: {result['net_roi']:<6.1f}%")
        else:
            print(f"{asset_id:<8} ERROR: {result['error']}")
    
    # Sort by net ROI
    profitable_assets = [r for r in results if 'error' not in r and r['worth_trading']]
    profitable_assets.sort(key=lambda x: x['net_roi'], reverse=True)
    
    print(f"\n🏆 TOP PROFITABLE ASSETS:")
    print(f"{'Asset':<8} {'Status':<6} {'Type':<11} {'Net Profit':<10} {'ROI%':<8} {'Tax Payments'}")
    print("-" * 80)
    
    for asset in profitable_assets[:10]:  # Top 10
        status = "OWNED" if asset['currently_owned'] else "BUY"
        num_payments = len(asset['payment_schedule'])
        print(f"{asset['asset_id']:<8} {status:<6} {asset['sub_type']:<11} "
              f"{asset['net_profit']:<10,.0f} {asset['net_roi']:<8.1f} {num_payments} payments")
    
    # Save detailed results
    output_file = Path("year2_asset_analysis.yml")
    with open(output_file, 'w') as f:
        yaml.dump(results, f, default_flow_style=False)
    
    print(f"\n📊 Detailed analysis saved to: {output_file}")
    
    # Create summary
    summary = {
        'total_assets': len(all_assets),
        'owned_assets': len(owned_assets),
        'profitable_trades': len(profitable_assets),
        'total_potential_profit': sum(r['net_profit'] for r in profitable_assets),
        'best_assets': profitable_assets[:5]
    }
    
    print(f"\n📈 SUMMARY:")
    print(f"  Total assets analyzed: {summary['total_assets']}")
    print(f"  Currently owned: {summary['owned_assets']}")
    print(f"  Profitable opportunities: {summary['profitable_trades']}")
    print(f"  Total potential profit: {summary['total_potential_profit']:,.0f} FSB")

if __name__ == "__main__":
    main()