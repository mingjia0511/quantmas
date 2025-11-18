"""
Data Analysis Script for Year 1 Trading
Analyze the market data to understand price patterns and optimize strategy.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def analyze_market_data():
    """Analyze the market data to find optimal trading opportunities."""
    # Load data
    assets_df = pd.read_csv("problems/year_1/data/assets.csv")
    valuations_df = pd.read_csv("problems/year_1/data/valuations.csv")
    
    print("Asset Information:")
    print("================")
    for _, asset in assets_df.iterrows():
        print(f"{asset['id']}: {asset['name']} ({asset['sub_type']}, {asset['region']})")
        print(f"  Available from day: {asset['available_on_day']}")
    
    print("\nPrice Analysis:")
    print("==============")
    
    # Calculate ROI for each asset from first available day to day 100
    results = []
    
    for asset_id in assets_df['id']:
        asset_info = assets_df[assets_df['id'] == asset_id].iloc[0]
        asset_data = valuations_df[valuations_df['asset_id'] == asset_id].copy()
        
        if len(asset_data) == 0:
            continue
            
        # Get prices on first available day and day 100
        available_day = asset_info['available_on_day']
        
        first_price = asset_data[asset_data['day'] == available_day]['valuation'].iloc[0]
        final_price = asset_data[asset_data['day'] == 100]['valuation'].iloc[0]
        
        roi = (final_price - first_price) / first_price
        
        # Calculate volatility (standard deviation of daily returns)
        asset_data = asset_data.sort_values('day')
        asset_data['daily_return'] = asset_data['valuation'].pct_change()
        volatility = asset_data['daily_return'].std()
        
        # Find best buy and sell days
        min_price = asset_data['valuation'].min()
        max_price = asset_data['valuation'].max()
        min_day = asset_data[asset_data['valuation'] == min_price]['day'].iloc[0]
        max_day = asset_data[asset_data['valuation'] == max_price]['day'].iloc[0]
        
        optimal_roi = (max_price - min_price) / min_price if min_day <= max_day else 0
        
        results.append({
            'asset_id': asset_id,
            'name': asset_info['name'],
            'available_day': available_day,
            'first_price': first_price,
            'final_price': final_price,
            'roi': roi,
            'volatility': volatility,
            'min_price': min_price,
            'max_price': max_price,
            'min_day': min_day,
            'max_day': max_day,
            'optimal_roi': optimal_roi
        })
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('optimal_roi', ascending=False)
    
    print("\nAsset Performance Ranking (by optimal ROI):")
    print("==========================================")
    for _, row in results_df.iterrows():
        print(f"{row['asset_id']}: {row['name']}")
        print(f"  Available day: {row['available_day']}")
        print(f"  Buy-and-hold ROI: {row['roi']:.2%}")
        print(f"  Optimal ROI: {row['optimal_roi']:.2%} (buy day {row['min_day']}, sell day {row['max_day']})")
        print(f"  Price range: ${row['min_price']:.0f} - ${row['max_price']:.0f}")
        print()
    
    # Find the best simple strategy
    print("Best Simple Strategy (one asset, buy and hold):")
    print("=============================================")
    best_simple = results_df.iloc[0]
    profit = (best_simple['final_price'] - best_simple['first_price'])
    print(f"Buy {best_simple['asset_id']} on day {best_simple['available_day']}")
    print(f"Cost: ${best_simple['first_price']:.0f}")
    print(f"Value on day 100: ${best_simple['final_price']:.0f}")
    print(f"Profit: ${profit:.0f}")
    print(f"ROI: {best_simple['roi']:.2%}")
    print(f"Final portfolio: ${1_000_000 - best_simple['first_price'] + best_simple['final_price']:.0f}")
    
    return results_df


def find_multi_asset_strategy():
    """Find the best multi-asset strategy."""
    assets_df = pd.read_csv("problems/year_1/data/assets.csv")
    valuations_df = pd.read_csv("problems/year_1/data/valuations.csv")
    
    print("\nMulti-Asset Strategy Analysis:")
    print("=============================")
    
    # Simple greedy approach: buy assets in order of ROI that we can afford
    cash = 1_000_000
    portfolio = []
    
    # Calculate ROI for all assets
    asset_rois = []
    for _, asset in assets_df.iterrows():
        asset_id = asset['id']
        available_day = asset['available_on_day']
        
        asset_data = valuations_df[valuations_df['asset_id'] == asset_id]
        first_price = asset_data[asset_data['day'] == available_day]['valuation'].iloc[0]
        final_price = asset_data[asset_data['day'] == 100]['valuation'].iloc[0]
        
        roi = (final_price - first_price) / first_price
        profit = final_price - first_price
        
        asset_rois.append({
            'asset_id': asset_id,
            'name': asset['name'],
            'available_day': available_day,
            'price': first_price,
            'final_price': final_price,
            'roi': roi,
            'profit': profit
        })
    
    # Sort by ROI
    asset_rois.sort(key=lambda x: x['roi'], reverse=True)
    
    print("Asset ROI ranking:")
    for asset in asset_rois:
        print(f"  {asset['asset_id']}: {asset['roi']:.2%} (${asset['profit']:.0f} profit)")
    
    # Greedy selection
    for asset in asset_rois:
        if asset['price'] <= cash and asset['roi'] > 0:
            portfolio.append(asset)
            cash -= asset['price']
            print(f"Buy {asset['asset_id']} for ${asset['price']:.0f} (remaining cash: ${cash:.0f})")
    
    total_value = cash
    total_profit = 0
    print(f"\nFinal Portfolio (day 100):")
    print(f"Cash: ${cash:.0f}")
    for asset in portfolio:
        total_value += asset['final_price']
        total_profit += asset['profit']
        print(f"{asset['asset_id']}: ${asset['final_price']:.0f}")
    
    print(f"\nTotal Portfolio Value: ${total_value:.0f}")
    print(f"Total Profit: ${total_profit:.0f}")
    print(f"Total ROI: {(total_value - 1_000_000) / 1_000_000:.2%}")


if __name__ == "__main__":
    analyze_market_data()
    find_multi_asset_strategy()