#!/usr/bin/env python3
"""
Complete Year 2 optimal strategy considering cash constraints and tax payments.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import yaml
from pathlib import Path
from data_loader import DataLoader

def calculate_daily_tax(asset_id, valuation, day, days_since_payment, data_loader):
    """Calculate daily tax for an asset."""
    try:
        return data_loader.calculate_daily_tax(asset_id, valuation, day, days_since_payment)
    except:
        return 0.0

def simulate_strategy(strategies, starting_cash, data_loader):
    """Simulate the complete strategy with cash flow and tax management."""
    
    # Initialize portfolio state
    cash = starting_cash
    owned_assets = {
        'asset_1': {'buy_day': 0, 'last_tax_payment': 0},
        'asset_2': {'buy_day': 0, 'last_tax_payment': 0},
        'asset_11': {'buy_day': 0, 'last_tax_payment': 0},
        'asset_13': {'buy_day': 0, 'last_tax_payment': 0},
        'asset_15': {'buy_day': 0, 'last_tax_payment': 0}
    }
    
    # Track all actions day by day
    daily_actions = {}
    
    print(f"Starting simulation with {cash:,.0f} FSB and 5 owned assets")
    
    # Process each day
    for day in range(1, 101):
        if day not in daily_actions:
            daily_actions[day] = []
        
        # 1. Pay taxes on owned assets (daily payments for optimal rates)
        taxes_paid_today = 0
        for asset_id in list(owned_assets.keys()):
            if asset_id in owned_assets:
                days_since_payment = day - owned_assets[asset_id]['last_tax_payment']
                
                if days_since_payment > 0:  # Tax is owed
                    try:
                        valuation = data_loader.get_asset_valuation(asset_id, day)
                        daily_tax = calculate_daily_tax(asset_id, valuation, day, days_since_payment, data_loader)
                        
                        if cash >= daily_tax:
                            cash -= daily_tax
                            taxes_paid_today += daily_tax
                            owned_assets[asset_id]['last_tax_payment'] = day
                            daily_actions[day].append({"pay_tax": asset_id})
                        else:
                            print(f"⚠️ Day {day}: Cannot afford tax for {asset_id} ({daily_tax:,.0f} FSB needed, {cash:,.0f} available)")
                    except Exception as e:
                        print(f"Error calculating tax for {asset_id} on day {day}: {e}")
        
        # 2. Execute sell orders (must have paid all taxes first)
        for strategy in strategies:
            if (strategy['sell_day'] == day and 
                strategy['asset_id'] in owned_assets):
                
                try:
                    sell_price = data_loader.get_asset_valuation(strategy['asset_id'], day)
                    cash += sell_price
                    del owned_assets[strategy['asset_id']]
                    daily_actions[day].append({"sell": strategy['asset_id']})
                    print(f"📤 Day {day}: Sold {strategy['asset_id']} for {sell_price:,.0f} FSB")
                except Exception as e:
                    print(f"Error selling {strategy['asset_id']} on day {day}: {e}")
        
        # 3. Execute buy orders (if we have enough cash)
        for strategy in strategies:
            if (strategy['buy_day'] == day and 
                not strategy['currently_owned'] and
                strategy['asset_id'] not in owned_assets):
                
                try:
                    buy_price = data_loader.get_asset_valuation(strategy['asset_id'], day)
                    
                    # Estimate tax burden for this asset to ensure we can afford it
                    hold_days = strategy['sell_day'] - strategy['buy_day']
                    estimated_daily_tax = buy_price * 0.02  # Rough estimate: 2% daily
                    estimated_tax_reserve = estimated_daily_tax * min(hold_days, 10)  # Reserve for 10 days
                    
                    total_cost = buy_price + estimated_tax_reserve
                    
                    if cash >= total_cost:
                        cash -= buy_price
                        owned_assets[strategy['asset_id']] = {
                            'buy_day': day,
                            'last_tax_payment': day
                        }
                        daily_actions[day].append({"buy": strategy['asset_id']})
                        print(f"📥 Day {day}: Bought {strategy['asset_id']} for {buy_price:,.0f} FSB (reserved {estimated_tax_reserve:,.0f} for taxes)")
                    else:
                        print(f"⚠️ Day {day}: Cannot afford {strategy['asset_id']} ({total_cost:,.0f} needed, {cash:,.0f} available)")
                except Exception as e:
                    print(f"Error buying {strategy['asset_id']} on day {day}: {e}")
        
        # 4. Daily summary (only show if something happened)
        if daily_actions[day] or taxes_paid_today > 0:
            print(f"Day {day}: Cash {cash:,.0f} FSB, Tax paid: {taxes_paid_today:,.0f}, Assets: {len(owned_assets)}")
    
    # Calculate final portfolio value
    final_asset_value = 0
    for asset_id in owned_assets:
        try:
            day_100_value = data_loader.get_asset_valuation(asset_id, 100)
            final_asset_value += day_100_value
            print(f"Final: {asset_id} worth {day_100_value:,.0f} FSB")
        except:
            print(f"Error getting final value for {asset_id}")
    
    total_wealth = cash + final_asset_value
    
    print(f"\n🏆 FINAL RESULTS:")
    print(f"Final Cash: {cash:,.0f} FSB")
    print(f"Final Assets Value: {final_asset_value:,.0f} FSB") 
    print(f"Total Wealth: {total_wealth:,.0f} FSB")
    
    return daily_actions, total_wealth

def main():
    """Generate the complete Year 2 strategy."""
    print("🎯 Year 2 Complete Strategy Generation 🎯")
    
    # Load data
    data_loader = DataLoader("../problems/year_2/data", year=2)
    data_loader.load_data()
    
    starting_cash = 144411
    
    # Define optimal strategies from our analysis
    strategies = [
        # Existing assets - keep profitable ones, sell others at optimal times
        {'asset_id': 'asset_1', 'currently_owned': True, 'buy_day': 0, 'sell_day': 100, 'net_profit': 53642, 'roi': 30.7},
        {'asset_id': 'asset_2', 'currently_owned': True, 'buy_day': 0, 'sell_day': 25, 'net_profit': 63533, 'roi': 18.9},
        {'asset_id': 'asset_11', 'currently_owned': True, 'buy_day': 0, 'sell_day': 22, 'net_profit': 58252, 'roi': 16.8},
        {'asset_id': 'asset_13', 'currently_owned': True, 'buy_day': 0, 'sell_day': 100, 'net_profit': 73692, 'roi': 40.7},
        {'asset_id': 'asset_15', 'currently_owned': True, 'buy_day': 0, 'sell_day': 19, 'net_profit': 54318, 'roi': 18.0},
        
        # New assets - prioritize by net profit and cash requirements
        {'asset_id': 'asset_3', 'currently_owned': False, 'buy_day': 52, 'sell_day': 98, 'net_profit': 100163, 'roi': 57.3},
        {'asset_id': 'asset_14', 'currently_owned': False, 'buy_day': 51, 'sell_day': 98, 'net_profit': 98007, 'roi': 51.3},
        {'asset_id': 'asset_4', 'currently_owned': False, 'buy_day': 49, 'sell_day': 99, 'net_profit': 77979, 'roi': 51.7},
        {'asset_id': 'asset_10', 'currently_owned': False, 'buy_day': 51, 'sell_day': 100, 'net_profit': 76052, 'roi': 34.3},
        {'asset_id': 'asset_7', 'currently_owned': False, 'buy_day': 53, 'sell_day': 100, 'net_profit': 65073, 'roi': 31.9},
        
        # Lower profit opportunities (if cash allows)
        {'asset_id': 'asset_5', 'currently_owned': False, 'buy_day': 41, 'sell_day': 70, 'net_profit': 28625, 'roi': 9.5},
        {'asset_id': 'asset_9', 'currently_owned': False, 'buy_day': 46, 'sell_day': 71, 'net_profit': 19723, 'roi': 5.7},
        {'asset_id': 'asset_12', 'currently_owned': False, 'buy_day': 68, 'sell_day': 69, 'net_profit': 9502, 'roi': 1.6},
        {'asset_id': 'asset_8', 'currently_owned': False, 'buy_day': 17, 'sell_day': 20, 'net_profit': 8270, 'roi': 1.6},
        {'asset_id': 'asset_6', 'currently_owned': False, 'buy_day': 56, 'sell_day': 57, 'net_profit': 7489, 'roi': 1.5}
    ]
    
    # Sort strategies by execution order (sells first, then buys by day)
    strategies.sort(key=lambda x: (x['buy_day'] if not x['currently_owned'] else 0, 
                                  -x['net_profit'] if x['currently_owned'] else x['net_profit']))
    
    print(f"Strategy includes {len(strategies)} actions")
    for s in strategies:
        action = "HOLD/SELL" if s['currently_owned'] else "BUY/SELL"
        print(f"  {s['asset_id']}: {action} Days {s['buy_day']}→{s['sell_day']} for {s['net_profit']:,.0f} FSB profit")
    
    # Simulate the strategy
    daily_actions, final_wealth = simulate_strategy(strategies, starting_cash, data_loader)
    
    # Generate output file
    output_file = Path("../problems/year_2/output/output.yml")
    output_file.parent.mkdir(exist_ok=True)
    
    # Filter out empty days
    filtered_actions = {day: actions for day, actions in daily_actions.items() if actions}
    
    with open(output_file, 'w') as f:
        yaml.dump(filtered_actions, f, default_flow_style=False, sort_keys=True)
    
    print(f"\n📄 Output saved to: {output_file}")
    print(f"🎯 Strategy projects final wealth of {final_wealth:,.0f} FSB")
    
    return filtered_actions, final_wealth

if __name__ == "__main__":
    main()