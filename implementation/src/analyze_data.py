"""
Data analysis script to understand asset price patterns.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from data_loader import DataLoader
import numpy as np


def analyze_asset_performance():
    """Analyze asset performance patterns."""
    # Load data
    data_loader = DataLoader("../../problems/year_1/data")
    assets_df, valuations_df = data_loader.load_data()
    
    print("=== ASSET ANALYSIS ===")
    print(f"Total assets: {len(assets_df)}")
    print("\nAsset types:")
    print(assets_df['sub_type'].value_counts())
    print("\nRegions:")
    print(assets_df['region'].value_counts())
    
    # Analyze performance for each asset
    performance_data = []
    
    for asset_id in assets_df['id']:
        asset_info = data_loader.get_asset_info(asset_id)
        price_history = data_loader.get_asset_price_history(asset_id)
        
        start_price = price_history['valuation'].iloc[0]
        end_price = price_history['valuation'].iloc[-1]
        min_price = price_history['valuation'].min()
        max_price = price_history['valuation'].max()
        mean_price = price_history['valuation'].mean()
        
        total_return = (end_price - start_price) / start_price * 100
        volatility = price_history['valuation'].std() / mean_price * 100
        
        performance_data.append({
            'asset_id': asset_id,
            'name': asset_info['name'],
            'sub_type': asset_info['sub_type'],
            'region': asset_info['region'],
            'available_day': asset_info['available_on_day'],
            'start_price': start_price,
            'end_price': end_price,
            'min_price': min_price,
            'max_price': max_price,
            'mean_price': mean_price,
            'total_return_pct': total_return,
            'volatility_pct': volatility,
            'max_gain_potential': (max_price - start_price) / start_price * 100
        })
    
    perf_df = pd.DataFrame(performance_data)
    
    print("\n=== PERFORMANCE ANALYSIS ===")
    print("Top performers by total return:")
    top_performers = perf_df.nlargest(5, 'total_return_pct')
    for _, row in top_performers.iterrows():
        print(f"{row['asset_id']}: {row['name']} ({row['total_return_pct']:.1f}%)")
    
    print("\nWorst performers:")
    worst_performers = perf_df.nsmallest(5, 'total_return_pct')
    for _, row in worst_performers.iterrows():
        print(f"{row['asset_id']}: {row['name']} ({row['total_return_pct']:.1f}%)")
    
    print("\nBest opportunities (max gain potential):")
    best_opportunities = perf_df.nlargest(5, 'max_gain_potential')
    for _, row in best_opportunities.iterrows():
        print(f"{row['asset_id']}: {row['name']} ({row['max_gain_potential']:.1f}%)")
    
    print("\nAverage returns by category:")
    print(perf_df.groupby('sub_type')['total_return_pct'].agg(['mean', 'std', 'count']))
    
    print("\nAverage returns by region:")
    print(perf_df.groupby('region')['total_return_pct'].agg(['mean', 'std', 'count']))
    
    return perf_df


def find_trading_opportunities(perf_df):
    """Identify potential trading strategies."""
    print("\n=== TRADING OPPORTUNITIES ===")
    
    # Assets that can be bought early and have good returns
    early_assets = perf_df[perf_df['available_day'] <= 10].copy()
    early_assets = early_assets.sort_values('total_return_pct', ascending=False)
    
    print("Early available assets with best returns:")
    for _, row in early_assets.head(10).iterrows():
        print(f"{row['asset_id']}: {row['name']} (day {row['available_day']}, {row['total_return_pct']:.1f}%)")
    
    # Identify potential buy-low-sell-high opportunities
    print("\nAssets with high volatility (potential trading opportunities):")
    volatile_assets = perf_df[perf_df['volatility_pct'] > 2.0].copy()
    volatile_assets = volatile_assets.sort_values('max_gain_potential', ascending=False)
    
    for _, row in volatile_assets.head(5).iterrows():
        print(f"{row['asset_id']}: {row['name']} (volatility: {row['volatility_pct']:.1f}%, max gain: {row['max_gain_potential']:.1f}%)")


if __name__ == "__main__":
    perf_df = analyze_asset_performance()
    find_trading_opportunities(perf_df)