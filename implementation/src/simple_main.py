"""
Simple optimal trading strategy: Buy low, sell high.
Since we have perfect information, find min/max for each asset and trade optimally.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import yaml
from data_loader import DataLoader


def create_optimal_trading_plan():
    """Create optimal trading plan using perfect information."""
    data_loader = DataLoader("../../problems/year_1/data")
    assets_df, valuations_df = data_loader.load_data()
    
    # Find min/max for each asset
    trades = []
    for asset_id in assets_df['id']:
        asset_info = data_loader.get_asset_info(asset_id)
        history = data_loader.get_asset_price_history(asset_id)
        
        min_price = history['valuation'].min()
        max_price = history['valuation'].max()
        min_day = int(history[history['valuation'] == min_price]['day'].iloc[0])
        max_day = int(history[history['valuation'] == max_price]['day'].iloc[0])
        
        # Only trade if asset is available at min day and profitable
        if (min_day >= asset_info['available_on_day'] and 
            max_price > min_price):
            
            profit_pct = (max_price - min_price) / min_price * 100
            
            trades.append({
                'asset_id': asset_id,
                'buy_day': min_day,
                'sell_day': max_day if max_day < 100 else None,  # Hold to end if max on day 100
                'buy_price': min_price,
                'sell_price': max_price,
                'profit_pct': profit_pct
            })
    
    # Sort by profit percentage (best first)
    trades.sort(key=lambda x: x['profit_pct'], reverse=True)
    
    return trades


def simulate_optimal_trading():
    """Simulate optimal trading with cash constraints."""
    trades = create_optimal_trading_plan()
    
    print("🎯 Simple Optimal Strategy: Buy Low, Sell High")
    print("=" * 60)
    
    cash = 1_000_000
    owned_assets = set()
    daily_actions = {}
    
    # Create timeline of all events
    events = []
    for trade in trades:
        events.append({
            'day': trade['buy_day'],
            'action': 'buy',
            'asset_id': trade['asset_id'],
            'price': trade['buy_price']
        })
        
        if trade['sell_day'] is not None:  # Don't sell if holding to day 100
            events.append({
                'day': trade['sell_day'],
                'action': 'sell',
                'asset_id': trade['asset_id'],
                'price': trade['sell_price']
            })
    
    # Sort by day
    events.sort(key=lambda x: x['day'])
    
    # Execute events
    for event in events:
        day = event['day']
        action = event['action']
        asset_id = event['asset_id']
        price = event['price']
        
        if action == 'buy':
            if cash >= price and asset_id not in owned_assets:
                cash -= price
                owned_assets.add(asset_id)
                
                if day not in daily_actions:
                    daily_actions[day] = []
                daily_actions[day].append({'buy': asset_id})
                
                print(f"Day {day:3d}: BUY  {asset_id} at {price:>8,.0f} FSB (Cash: {cash:>8,.0f})")
        
        elif action == 'sell':
            if asset_id in owned_assets:
                cash += price
                owned_assets.remove(asset_id)
                
                if day not in daily_actions:
                    daily_actions[day] = []
                daily_actions[day].append({'sell': asset_id})
                
                print(f"Day {day:3d}: SELL {asset_id} at {price:>8,.0f} FSB (Cash: {cash:>8,.0f})")
    
    # Calculate final value
    data_loader = DataLoader("../../problems/year_1/data")
    data_loader.load_data()
    day_100_valuations = data_loader.get_daily_valuations(100)
    
    final_asset_value = sum(day_100_valuations.get(asset_id, 0) for asset_id in owned_assets)
    final_total = cash + final_asset_value
    
    print("\n" + "=" * 60)
    print("🏆 FINAL RESULTS")
    print("=" * 60)
    print(f"Final Cash:        {cash:>12,.0f} FSB")
    print(f"Final Asset Value: {final_asset_value:>12,.0f} FSB") 
    print(f"TOTAL VALUE:       {final_total:>12,.0f} FSB")
    print(f"Total Return:      {(final_total - 1_000_000) / 1_000_000 * 100:>11.1f}%")
    
    # Save output - ensure all keys are plain integers
    output_data = {}
    for day, actions in daily_actions.items():
        output_data[int(day)] = actions
    
    output_path = "../../problems/year_1/output/output.yml"
    with open(output_path, 'w') as f:
        yaml.dump(output_data, f, default_flow_style=False, sort_keys=True)
    
    print(f"✅ Output saved to: {output_path}")
    
    return daily_actions, final_total


if __name__ == "__main__":
    daily_actions, final_value = simulate_optimal_trading()