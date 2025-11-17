"""
Simple optimal strategy: Buy at min, sell at max.
Since we have perfect information, this is the optimal approach.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from data_loader import DataLoader
import numpy as np


def find_optimal_trades():
    """Find optimal buy/sell points for each asset."""
    data_loader = DataLoader("../../problems/year_1/data")
    assets_df, valuations_df = data_loader.load_data()
    
    optimal_trades = []
    
    print("=== OPTIMAL TRADING ANALYSIS ===")
    
    for asset_id in assets_df['id']:
        asset_info = data_loader.get_asset_info(asset_id)
        price_history = data_loader.get_asset_price_history(asset_id)
        
        # Find min and max prices and their days
        min_price = price_history['valuation'].min()
        max_price = price_history['valuation'].max()
        
        min_day = price_history[price_history['valuation'] == min_price]['day'].iloc[0]
        max_day = price_history[price_history['valuation'] == max_price]['day'].iloc[0]
        
        # Only consider if asset is available at min_day
        if min_day >= asset_info['available_on_day']:
            profit = max_price - min_price
            roi_pct = (profit / min_price) * 100
            
            # If max is on day 100, we hold (don't sell)
            sell_day = max_day if max_day < 100 else None
            
            optimal_trades.append({
                'asset_id': asset_id,
                'name': asset_info['name'],
                'available_day': asset_info['available_on_day'],
                'buy_day': min_day,
                'buy_price': min_price,
                'sell_day': sell_day,
                'sell_price': max_price if sell_day else max_price,
                'profit': profit,
                'roi_pct': roi_pct,
                'hold_to_end': sell_day is None
            })
    
    # Sort by ROI
    optimal_trades.sort(key=lambda x: x['roi_pct'], reverse=True)
    
    print(f"\nOptimal trades (sorted by ROI):")
    print(f"{'Asset':<8} {'Name':<25} {'Buy Day':<8} {'Buy Price':<10} {'Sell Day':<9} {'Sell Price':<11} {'ROI %':<8}")
    print("-" * 90)
    
    for trade in optimal_trades:
        sell_day_str = str(trade['sell_day']) if trade['sell_day'] else "HOLD"
        print(f"{trade['asset_id']:<8} {trade['name']:<25} {trade['buy_day']:<8} {trade['buy_price']:<10,.0f} "
              f"{sell_day_str:<9} {trade['sell_price']:<11,.0f} {trade['roi_pct']:<8.1f}")
    
    return optimal_trades


def calculate_optimal_portfolio(max_cash=1_000_000):
    """Calculate the optimal portfolio given cash constraints."""
    optimal_trades = find_optimal_trades()
    
    # Simulate optimal trading with cash constraints
    cash = max_cash
    portfolio = {}
    trades_executed = []
    daily_actions = {}
    
    print(f"\n=== OPTIMAL PORTFOLIO SIMULATION ===")
    print(f"Starting cash: {cash:,.0f} FSB")
    
    # Create a timeline of all buy/sell events
    events = []
    
    for trade in optimal_trades:
        # Add buy event
        if trade['buy_day'] >= trade['available_day'] and trade['buy_price'] <= cash:
            events.append({
                'day': trade['buy_day'],
                'action': 'buy',
                'asset_id': trade['asset_id'],
                'price': trade['buy_price'],
                'trade_info': trade
            })
        
        # Add sell event if applicable
        if trade['sell_day'] is not None:
            events.append({
                'day': trade['sell_day'],
                'action': 'sell', 
                'asset_id': trade['asset_id'],
                'price': trade['sell_price'],
                'trade_info': trade
            })
    
    # Sort events by day
    events.sort(key=lambda x: x['day'])
    
    # Execute events in order
    for event in events:
        day = event['day']
        action = event['action']
        asset_id = event['asset_id']
        price = event['price']
        
        if action == 'buy' and cash >= price and asset_id not in portfolio:
            cash -= price
            portfolio[asset_id] = event['trade_info']
            trades_executed.append(event)
            
            if day not in daily_actions:
                daily_actions[day] = []
            daily_actions[day].append({'buy': asset_id})
            
            print(f"Day {day:3d}: BUY  {asset_id} at {price:,.0f} FSB (Cash: {cash:,.0f})")
        
        elif action == 'sell' and asset_id in portfolio:
            cash += price
            del portfolio[asset_id] 
            trades_executed.append(event)
            
            if day not in daily_actions:
                daily_actions[day] = []
            daily_actions[day].append({'sell': asset_id})
            
            print(f"Day {day:3d}: SELL {asset_id} at {price:,.0f} FSB (Cash: {cash:,.0f})")
    
    # Calculate final portfolio value
    data_loader = DataLoader("../../problems/year_1/data")
    data_loader.load_data()
    day_100_valuations = data_loader.get_daily_valuations(100)
    
    final_asset_value = sum(day_100_valuations.get(asset_id, 0) for asset_id in portfolio.keys())
    final_total = cash + final_asset_value
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Final cash:        {cash:>12,.0f} FSB")
    print(f"Final asset value: {final_asset_value:>12,.0f} FSB")
    print(f"TOTAL VALUE:       {final_total:>12,.0f} FSB")
    print(f"Total return:      {(final_total - max_cash) / max_cash * 100:>11.1f}%")
    
    if portfolio:
        print(f"\nAssets held to day 100:")
        for asset_id in portfolio.keys():
            asset_info = data_loader.get_asset_info(asset_id)
            value = day_100_valuations[asset_id]
            print(f"  {asset_id}: {asset_info['name']:<25} {value:>10,.0f} FSB")
    
    return daily_actions, final_total


if __name__ == "__main__":
    daily_actions, final_value = calculate_optimal_portfolio()