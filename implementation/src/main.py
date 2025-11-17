"""
Main execution script for Quantmas Year 1 challenge.
Runs the trading simulation and generates output.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import yaml
from data_loader import DataLoader
from portfolio_tracker import PortfolioTracker
from trading_strategy import TradingStrategy


def run_trading_simulation():
    """Run the full trading simulation for 100 days."""
    print("🎅 Starting Quantmas Year 1 Trading Simulation! 🎄")
    
    # Initialize components
    data_loader = DataLoader("../../problems/year_1/data")
    portfolio = PortfolioTracker(initial_cash=1_000_000)
    
    # Load data
    print("📊 Loading market data...")
    data_loader.load_data()
    
    # Initialize strategy
    print("🧠 Initializing trading strategy...")
    strategy = TradingStrategy(data_loader, portfolio)
    
    # Show asset rankings
    print("\n📈 Asset Rankings (Top 10):")
    rankings = strategy.get_asset_rankings()
    sorted_rankings = sorted(rankings.items(), key=lambda x: x[1]['score'], reverse=True)
    for i, (asset_id, data) in enumerate(sorted_rankings[:10]):
        asset_info = data_loader.get_asset_info(asset_id)
        print(f"{i+1:2d}. {asset_id}: {asset_info['name']:<25} (Score: {data['score']:.3f}, Return: {data['total_return']*100:+.1f}%)")
    
    # Run simulation day by day
    print("\n🎯 Running trading simulation...")
    
    total_trades = 0
    for day in range(1, 101):
        decisions = strategy.make_trading_decisions(day)
        total_trades += len(decisions)
        
        if decisions:
            print(f"Day {day:3d}: {len(decisions)} trades")
            for action, asset_id in decisions:
                asset_info = data_loader.get_asset_info(asset_id)
                price = data_loader.get_asset_valuation(asset_id, day)
                print(f"  {action.upper()}: {asset_id} ({asset_info['name']}) at {price:,.0f} FSB")
        
        # Progress indicator
        if day % 20 == 0:
            print(f"📅 Completed {day}/100 days...")
    
    # Calculate final results
    day_100_valuations = data_loader.get_daily_valuations(100)
    final_portfolio_value = portfolio.get_portfolio_value(day_100_valuations)
    
    # Print final summary
    print("\n" + "="*60)
    print("🏆 FINAL RESULTS")
    print("="*60)
    
    summary = portfolio.get_trading_summary()
    print(f"Starting Cash:     {summary['initial_cash']:>12,.0f} FSB")
    print(f"Final Cash:        {summary['current_cash']:>12,.0f} FSB")
    print(f"Assets Owned:      {len(summary['owned_assets']):>12d}")
    print(f"Total Trades:      {total_trades:>12d}")
    print(f"Buy Trades:        {summary['total_buys']:>12d}")
    print(f"Sell Trades:       {summary['total_sells']:>12d}")
    print(f"Net Cash Flow:     {summary['net_cash_flow']:>12,.0f} FSB")
    
    # Show owned assets and their values
    if summary['owned_assets']:
        print(f"\n📋 Owned Assets on Day 100:")
        total_asset_value = 0
        for asset_id in summary['owned_assets']:
            asset_info = data_loader.get_asset_info(asset_id)
            value = day_100_valuations[asset_id]
            total_asset_value += value
            print(f"  {asset_id}: {asset_info['name']:<25} {value:>10,.0f} FSB")
        
        print(f"Total Asset Value: {total_asset_value:>12,.0f} FSB")
    
    print(f"FINAL SCORE:       {final_portfolio_value:>12,.0f} FSB")
    print(f"Total Return:      {(final_portfolio_value - summary['initial_cash']) / summary['initial_cash'] * 100:>11.1f}%")
    
    # Generate output file
    print(f"\n💾 Generating output file...")
    output_data = portfolio.get_daily_trades_output()
    
    output_path = "../../problems/year_1/output/output.yml"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        yaml.dump(output_data, f, default_flow_style=False, sort_keys=True)
    
    print(f"✅ Output saved to: {output_path}")
    print(f"🎄 Trading simulation complete! Final score: {final_portfolio_value:,.0f} FSB")
    
    return final_portfolio_value, summary


if __name__ == "__main__":
    final_score, summary = run_trading_simulation()