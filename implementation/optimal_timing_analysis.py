#!/usr/bin/env python3
"""
Optimal buy/sell timing analysis considering tax burden.
For each asset, test all possible buy/sell combinations to find the most profitable.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import yaml
from pathlib import Path
from data_loader import DataLoader

def calculate_tax_for_period(asset_id, buy_day, sell_day, data_loader):
    """Calculate optimal tax cost for holding asset from buy_day to sell_day."""
    if sell_day <= buy_day:
        return 0.0
    
    # For simplicity, assume daily tax payments (optimal strategy)
    total_tax = 0.0
    
    for day in range(buy_day + 1, sell_day + 1):
        try:
            valuation = data_loader.get_asset_valuation(asset_id, day)
            days_since_payment = 1  # Daily payments
            daily_tax = data_loader.calculate_daily_tax(asset_id, valuation, day, days_since_payment)
            total_tax += daily_tax
        except:
            continue
    
    return total_tax

def find_optimal_buy_sell(asset_id, data_loader, currently_owned=False, available_day=1):
    """Find the optimal buy/sell combination for an asset."""
    price_history = data_loader.get_asset_price_history(asset_id)
    
    best_profit = float('-inf')
    best_strategy = None
    
    # If currently owned, we start from day 0 (already own it)
    if currently_owned:
        start_day = 0
        buy_price = data_loader.get_asset_valuation(asset_id, 1)  # Current value
    else:
        start_day = max(available_day, 1)
        buy_price = None
    
    # Test all possible buy/sell combinations
    for buy_day in range(start_day, 100):
        if currently_owned:
            buy_day = 0  # We already own it
            buy_price = data_loader.get_asset_valuation(asset_id, 1)
        else:
            if buy_day < available_day:
                continue
            try:
                buy_price = data_loader.get_asset_valuation(asset_id, buy_day)
            except:
                continue
        
        # Test all possible sell days after buy day
        for sell_day in range(buy_day + 1, 101):
            try:
                sell_price = data_loader.get_asset_valuation(asset_id, sell_day)
                
                # Calculate tax burden for this holding period
                tax_cost = calculate_tax_for_period(asset_id, buy_day, sell_day, data_loader)
                
                # Calculate profit
                gross_profit = sell_price - buy_price
                net_profit = gross_profit - tax_cost
                
                if net_profit > best_profit:
                    best_profit = net_profit
                    best_strategy = {
                        'buy_day': buy_day,
                        'buy_price': buy_price,
                        'sell_day': sell_day,
                        'sell_price': sell_price,
                        'gross_profit': gross_profit,
                        'tax_cost': tax_cost,
                        'net_profit': net_profit,
                        'hold_days': sell_day - buy_day,
                        'roi': (net_profit / buy_price * 100) if buy_price > 0 else 0
                    }
                
            except:
                continue
        
        if currently_owned:
            break  # Only test once for owned assets
    
    return best_strategy

def analyze_optimal_strategies():
    """Analyze optimal buy/sell strategies for all assets."""
    print("🎯 Optimal Buy/Sell Timing Analysis (Tax-Aware) 🎯")
    
    # Load data
    data_loader = DataLoader("../problems/year_2/data", year=2)
    data_loader.load_data()
    
    # Assets we currently own
    owned_assets = {'asset_1', 'asset_13', 'asset_2', 'asset_11', 'asset_15'}
    
    # Get all assets
    all_assets = data_loader.get_all_assets()
    
    results = []
    
    print(f"\nAnalyzing optimal strategies for {len(all_assets)} assets...")
    print(f"{'Asset':<8} {'Status':<6} {'Type':<11} {'Buy Day':<8} {'Sell Day':<9} {'Hold Days':<10} {'Gross':<10} {'Tax':<8} {'Net':<8} {'ROI%':<6}")
    print("-" * 110)
    
    for asset_id in all_assets:
        asset_info = data_loader.get_asset_info(asset_id)
        currently_owned = asset_id in owned_assets
        
        strategy = find_optimal_buy_sell(
            asset_id, data_loader, currently_owned, asset_info['available_on_day']
        )
        
        if strategy and strategy['net_profit'] > 0:
            status = "OWN" if currently_owned else "BUY"
            
            print(f"{asset_id:<8} {status:<6} {asset_info['sub_type']:<11} "
                  f"{strategy['buy_day']:<8} {strategy['sell_day']:<9} "
                  f"{strategy['hold_days']:<10} {strategy['gross_profit']:<10,.0f} "
                  f"{strategy['tax_cost']:<8,.0f} {strategy['net_profit']:<8,.0f} "
                  f"{strategy['roi']:<6.1f}")
            
            # Add asset info to strategy
            strategy['asset_id'] = asset_id
            strategy['name'] = asset_info['name']
            strategy['sub_type'] = asset_info['sub_type']
            strategy['currently_owned'] = currently_owned
            strategy['available_day'] = asset_info['available_on_day']
            
            results.append(strategy)
    
    # Sort by net profit
    results.sort(key=lambda x: x['net_profit'], reverse=True)
    
    print(f"\n🏆 TOP STRATEGIES (by net profit):")
    print(f"{'Asset':<8} {'Status':<6} {'Net Profit':<10} {'ROI%':<6} {'Strategy'}")
    print("-" * 70)
    
    for strategy in results[:10]:
        status = "OWNED" if strategy['currently_owned'] else "NEW"
        strategy_desc = f"Hold {strategy['hold_days']} days (Day {strategy['buy_day']}→{strategy['sell_day']})"
        
        print(f"{strategy['asset_id']:<8} {status:<6} {strategy['net_profit']:<10,.0f} "
              f"{strategy['roi']:<6.1f} {strategy_desc}")
    
    # Compare with traditional min/max approach
    print(f"\n📊 STRATEGY COMPARISON:")
    print("Comparing optimal timing vs traditional min/max approach...")
    
    return results

if __name__ == "__main__":
    analyze_optimal_strategies()