"""
Optimal strategy for Year 2: Buy at min, sell at max, with tax optimization.
Since we have perfect information, we can compute the globally optimal strategy.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import yaml
from data_loader import DataLoader
from portfolio_tracker import PortfolioTracker
import numpy as np


def calculate_optimal_with_taxes():
    """Calculate optimal strategy for Year 2 including tax considerations."""
    
    # Load Year 2 data
    data_loader = DataLoader("../problems/year_2/data", year=2)
    assets_df, valuations_df, tax_rates_df = data_loader.load_data()
    
    print("=== YEAR 2 OPTIMAL STRATEGY WITH TAXES ===")
    
    # Starting position from Year 1
    starting_cash = 144_411
    starting_assets = {'asset_1', 'asset_13', 'asset_2', 'asset_11', 'asset_15'}
    
    print(f"Starting cash: {starting_cash:,.0f} FSB")
    print(f"Starting assets: {', '.join(starting_assets)}")
    
    # Initialize portfolio tracker
    portfolio = PortfolioTracker(
        initial_cash=starting_cash, 
        year=2, 
        starting_assets=starting_assets
    )
    
    # For each asset, calculate net profit considering taxes
    asset_analysis = {}
    
    for asset_id in assets_df['id']:
        asset_info = data_loader.get_asset_info(asset_id)
        price_history = data_loader.get_asset_price_history(asset_id)
        
        # Calculate basic buy/sell optimal points
        min_price = price_history['valuation'].min()
        max_price = price_history['valuation'].max()
        min_day = price_history[price_history['valuation'] == min_price]['day'].iloc[0]
        max_day = price_history[price_history['valuation'] == max_price]['day'].iloc[0]
        
        # Calculate tax burden if we hold this asset
        tax_burden = calculate_holding_tax_burden(asset_id, min_day, max_day, data_loader, price_history)
        
        # Net profit after taxes
        gross_profit = max_price - min_price
        net_profit = gross_profit - tax_burden
        net_roi = (net_profit / min_price) * 100 if min_price > 0 else 0
        
        asset_analysis[asset_id] = {
            'asset_id': asset_id,
            'name': asset_info['name'],
            'sub_type': asset_info['sub_type'],
            'available_day': asset_info['available_on_day'],
            'buy_day': min_day,
            'buy_price': min_price,
            'sell_day': max_day if max_day < 100 else None,
            'sell_price': max_price,
            'gross_profit': gross_profit,
            'tax_burden': tax_burden,
            'net_profit': net_profit,
            'net_roi': net_roi,
            'hold_to_end': max_day >= 100
        }
    
    # Sort by net ROI (profit after taxes)
    sorted_assets = sorted(asset_analysis.values(), key=lambda x: x['net_roi'], reverse=True)
    
    print(f"\nAsset Analysis (sorted by net ROI after taxes):")
    print(f"{'Asset':<8} {'Type':<11} {'Buy Day':<8} {'Buy Price':<10} {'Sell Day':<9} {'Gross Profit':<13} {'Tax Burden':<11} {'Net Profit':<11} {'Net ROI%':<8}")
    print("-" * 110)
    
    for asset in sorted_assets:
        sell_day_str = str(asset['sell_day']) if asset['sell_day'] else "HOLD"
        print(f"{asset['asset_id']:<8} {asset['sub_type']:<11} {asset['buy_day']:<8} {asset['buy_price']:<10,.0f} "
              f"{sell_day_str:<9} {asset['gross_profit']:<13,.0f} {asset['tax_burden']:<11,.0f} "
              f"{asset['net_profit']:<11,.0f} {asset['net_roi']:<8.1f}")
    
    return sorted_assets, data_loader, portfolio


def calculate_optimal_tax_payment_day(asset_id: str, last_payment_day: int, current_day: int, data_loader: DataLoader, max_hold_day: int = 100):
    """
    Calculate the mathematically optimal day to pay taxes using perfect valuation data.
    Returns the day (relative to last_payment_day) that minimizes total tax cost.
    """
    min_total_cost = float('inf')
    optimal_payment_day = 1  # Default to paying immediately
    
    # Try all possible payment days (1 to 30 days from last payment, or until max_hold_day)
    for days_to_wait in range(1, min(31, max_hold_day - last_payment_day + 1)):
        payment_day = last_payment_day + days_to_wait
        
        if payment_day > max_hold_day:
            break
            
        # Calculate total tax cost if we pay on this day
        total_cost = 0.0
        
        for day in range(last_payment_day + 1, payment_day + 1):
            if day > max_hold_day:
                break
                
            try:
                valuation = data_loader.get_asset_valuation(asset_id, day)
                days_since_payment = day - last_payment_day
                daily_tax = data_loader.calculate_daily_tax(asset_id, valuation, day, days_since_payment)
                total_cost += daily_tax
            except:
                # If we can't get valuation, skip this day
                continue
        
        # Track the minimum cost option
        if total_cost < min_total_cost:
            min_total_cost = total_cost
            optimal_payment_day = days_to_wait
    
    return optimal_payment_day, min_total_cost


def calculate_holding_tax_burden(asset_id: str, buy_day: int, sell_day: int, data_loader: DataLoader, price_history: pd.DataFrame):
    """Calculate total tax burden for holding an asset from buy_day to sell_day using optimal payment timing."""
    if sell_day is None:
        sell_day = 100  # Hold to end
    
    total_tax = 0.0
    last_payment_day = buy_day
    current_day = buy_day + 1  # Tax starts accruing the day after purchase
    
    while current_day <= sell_day:
        # Calculate optimal payment day for this period
        days_to_wait, period_tax_cost = calculate_optimal_tax_payment_day(
            asset_id, last_payment_day, current_day, data_loader, sell_day
        )
        
        # Add this period's optimal tax cost
        total_tax += period_tax_cost
        
        # Move to next payment period
        last_payment_day = last_payment_day + days_to_wait
        current_day = last_payment_day + 1
        
        if last_payment_day >= sell_day:
            break
    
    return total_tax


def generate_optimal_year2_actions():
    """Generate the complete optimal action sequence for Year 2 with perfect tax timing."""
    sorted_assets, data_loader, portfolio = calculate_optimal_with_taxes()
    
    print(f"\n=== GENERATING OPTIMAL YEAR 2 ACTION PLAN ===")
    
    # Track actions by day
    daily_actions = {}
    
    # Starting assets from Year 1
    starting_assets = {'asset_1', 'asset_13', 'asset_2', 'asset_11', 'asset_15'}
    
    # Track tax payment schedule for starting assets
    tax_schedule = {}
    for asset_id in starting_assets:
        tax_schedule[asset_id] = {'last_payment_day': 0}  # Never paid taxes before
    
    # Track owned assets and cash
    owned_assets = starting_assets.copy()
    cash = 144411  # Starting cash from Year 1
    
    print(f"Starting position: {cash:,.0f} FSB cash + {len(owned_assets)} assets")
    
    # Simulate day by day
    for day in range(1, 101):
        day_actions = []
        
        # 1. Handle tax payments for owned assets
        for asset_id in list(owned_assets):
            if asset_id in tax_schedule:
                last_payment = tax_schedule[asset_id]['last_payment_day']
                
                # Calculate optimal payment day
                days_to_wait, tax_cost = calculate_optimal_tax_payment_day(
                    asset_id, last_payment, day, data_loader, 100
                )
                
                optimal_payment_day = last_payment + days_to_wait
                
                # Pay taxes if this is the optimal day
                if day == optimal_payment_day:
                    if cash >= tax_cost:
                        day_actions.append({'pay_tax': asset_id})
                        cash -= tax_cost
                        tax_schedule[asset_id]['last_payment_day'] = day
                        print(f"Day {day}: Pay tax on {asset_id}: {tax_cost:,.0f} FSB (cash left: {cash:,.0f})")
                    else:
                        print(f"Day {day}: WARNING - Cannot afford tax on {asset_id}: {tax_cost:,.0f} FSB (only have {cash:,.0f})")
        
        # 2. Check for optimal sells
        assets_to_sell = []
        for asset_data in sorted_assets:
            asset_id = asset_data['asset_id']
            if asset_id in owned_assets and asset_data['sell_day'] == day:
                # Make sure all taxes are paid first
                if asset_id in tax_schedule and tax_schedule[asset_id]['last_payment_day'] < day:
                    print(f"Day {day}: WARNING - Cannot sell {asset_id} - taxes not up to date")
                else:
                    assets_to_sell.append(asset_id)
        
        for asset_id in assets_to_sell:
            sell_price = data_loader.get_asset_valuation(asset_id, day)
            day_actions.append({'sell': asset_id})
            cash += sell_price
            owned_assets.remove(asset_id)
            if asset_id in tax_schedule:
                del tax_schedule[asset_id]
            print(f"Day {day}: Sell {asset_id} for {sell_price:,.0f} FSB (cash: {cash:,.0f})")
        
        # 3. Check for optimal buys
        for asset_data in sorted_assets:
            asset_id = asset_data['asset_id']
            if (asset_id not in owned_assets and 
                asset_data['buy_day'] == day and 
                asset_data['net_roi'] > 0):  # Only buy profitable assets
                
                buy_price = asset_data['buy_price']
                if cash >= buy_price:
                    day_actions.append({'buy': asset_id})
                    cash -= buy_price
                    owned_assets.add(asset_id)
                    tax_schedule[asset_id] = {'last_payment_day': day}  # Just bought, no taxes yet
                    print(f"Day {day}: Buy {asset_id} for {buy_price:,.0f} FSB (cash: {cash:,.0f})")
        
        # Store actions for this day
        if day_actions:
            daily_actions[day] = day_actions
    
    # Final summary
    final_asset_value = sum(
        data_loader.get_asset_valuation(asset_id, 100) 
        for asset_id in owned_assets
    )
    final_wealth = cash + final_asset_value
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Final cash: {cash:,.0f} FSB")
    print(f"Final asset value: {final_asset_value:,.0f} FSB") 
    print(f"Total wealth: {final_wealth:,.0f} FSB")
    print(f"Improvement from Year 1: {final_wealth - 1386404:,.0f} FSB")
    
    return daily_actions


def simulate_optimal_year2_trading():
    """Simulate optimal trading for Year 2 with perfect information and tax optimization."""
    sorted_assets, data_loader, portfolio = calculate_optimal_with_taxes()
    
    print(f"\n=== SIMULATING OPTIMAL YEAR 2 TRADING ===")
    
    # Track daily actions
    daily_actions = {}
    
    # Calculate current portfolio value and taxes owed on starting assets
    print(f"\nStarting portfolio analysis:")
    for asset_id in portfolio.owned_assets:
        day_1_valuation = data_loader.get_asset_valuation(asset_id, 1)
        asset_info = data_loader.get_asset_info(asset_id)
        print(f"  {asset_id} ({asset_info['name']}): {day_1_valuation:,.0f} FSB")
    
    # Strategy: Sell existing assets if they're not optimal, buy optimal assets
    
    # First, identify which existing assets we should keep vs sell
    existing_asset_decisions = {}
    for asset_id in portfolio.owned_assets:
        asset_data = next((a for a in sorted_assets if a['asset_id'] == asset_id), None)
        if asset_data and asset_data['net_roi'] > 5:  # Keep if decent return expected
            existing_asset_decisions[asset_id] = 'keep'
            print(f"DECISION: Keep {asset_id} (net ROI: {asset_data['net_roi']:.1f}%)")
        else:
            existing_asset_decisions[asset_id] = 'sell_when_optimal'
            print(f"DECISION: Sell {asset_id} when optimal")
    
    # Create timeline of all optimal events
    events = []
    
    # Add sell events for existing assets
    for asset_id in portfolio.owned_assets:
        asset_data = next((a for a in sorted_assets if a['asset_id'] == asset_id), None)
        if asset_data and existing_asset_decisions[asset_id] == 'sell_when_optimal':
            if asset_data['sell_day'] and asset_data['sell_day'] < 100:
                events.append({
                    'day': asset_data['sell_day'],
                    'action': 'sell',
                    'asset_id': asset_id,
                    'price': asset_data['sell_price'],
                    'type': 'existing'
                })
    
    # Add buy events for new profitable assets
    for asset_data in sorted_assets:
        asset_id = asset_data['asset_id']
        # Only buy if we don't own it and it's profitable after taxes
        if asset_id not in portfolio.owned_assets and asset_data['net_roi'] > 10:
            if asset_data['buy_day'] >= asset_data['available_day']:
                events.append({
                    'day': asset_data['buy_day'],
                    'action': 'buy',
                    'asset_id': asset_id,
                    'price': asset_data['buy_price'],
                    'type': 'new'
                })
                
                # Add corresponding sell event if not holding to end
                if asset_data['sell_day'] and asset_data['sell_day'] < 100:
                    events.append({
                        'day': asset_data['sell_day'],
                        'action': 'sell',
                        'asset_id': asset_id,
                        'price': asset_data['sell_price'],
                        'type': 'new'
                    })
    
    # Sort events by day
    events.sort(key=lambda x: (x['day'], x['action'] == 'buy'))  # Sells before buys on same day
    
    # Execute events and track cash flow
    cash = portfolio.cash
    current_portfolio = set(portfolio.owned_assets)
    
    print(f"\n=== EXECUTING OPTIMAL TRADING PLAN ===")
    print(f"Day   0: Starting cash: {cash:,.0f} FSB")
    
    for event in events:
        day = event['day']
        action = event['action']
        asset_id = event['asset_id']
        price = event['price']
        
        # Add tax payment events (pay every 5 days to minimize escalating rates)
        if day % 5 == 0 and day > 0:
            # Pay taxes on all owned assets
            for owned_asset in current_portfolio:
                if day not in daily_actions:
                    daily_actions[day] = []
                daily_actions[day].append({'pay_tax': owned_asset})
                print(f"Day {day:3d}: PAY TAX {owned_asset}")
        
        if action == 'buy' and cash >= price and asset_id not in current_portfolio:
            cash -= price
            current_portfolio.add(asset_id)
            
            if day not in daily_actions:
                daily_actions[day] = []
            daily_actions[day].append({'buy': asset_id})
            
            asset_info = data_loader.get_asset_info(asset_id)
            print(f"Day {day:3d}: BUY  {asset_id} ({asset_info['name'][:20]:<20}) for {price:>10,.0f} FSB (Cash: {cash:>10,.0f})")
        
        elif action == 'sell' and asset_id in current_portfolio:
            cash += price
            current_portfolio.remove(asset_id)
            
            if day not in daily_actions:
                daily_actions[day] = []
            daily_actions[day].append({'sell': asset_id})
            
            asset_info = data_loader.get_asset_info(asset_id)
            print(f"Day {day:3d}: SELL {asset_id} ({asset_info['name'][:20]:<20}) for {price:>10,.0f} FSB (Cash: {cash:>10,.0f})")
    
    # Final tax payments on day 100
    if 100 not in daily_actions:
        daily_actions[100] = []
    for asset_id in current_portfolio:
        daily_actions[100].append({'pay_tax': asset_id})
        print(f"Day 100: PAY TAX {asset_id} (final payment)")
    
    # Calculate final portfolio value
    day_100_valuations = data_loader.get_daily_valuations(100)
    final_asset_value = sum(day_100_valuations.get(asset_id, 0) for asset_id in current_portfolio)
    final_total = cash + final_asset_value
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Final cash:        {cash:>12,.0f} FSB")
    print(f"Final asset value: {final_asset_value:>12,.0f} FSB")
    print(f"TOTAL VALUE:       {final_total:>12,.0f} FSB")
    
    starting_total = 144_411 + sum(data_loader.get_asset_valuation(aid, 1) for aid in ['asset_1', 'asset_13', 'asset_2', 'asset_11', 'asset_15'])
    print(f"Starting value:    {starting_total:>12,.0f} FSB")
    print(f"Total return:      {(final_total - starting_total):>12,.0f} FSB ({(final_total - starting_total) / starting_total * 100:>7.1f}%)")
    
    if current_portfolio:
        print(f"\nAssets held to day 100:")
        for asset_id in current_portfolio:
            asset_info = data_loader.get_asset_info(asset_id)
            value = day_100_valuations[asset_id]
            print(f"  {asset_id}: {asset_info['name']:<25} {value:>10,.0f} FSB")
    
    return daily_actions, final_total


def save_year2_output(daily_actions):
    """Save the Year 2 trading plan to output.yml file."""
    output_dir = "../problems/year_2/output"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/output.yml"
    
    with open(output_file, 'w') as f:
        yaml.dump(daily_actions, f, default_flow_style=False)
    
    print(f"\nOutput saved to: {output_file}")


if __name__ == "__main__":
    # Generate the optimal action plan with perfect tax timing
    print("🎄 Generating Optimal Year 2 Strategy with Perfect Tax Timing 🎄")
    daily_actions = generate_optimal_year2_actions()
    
    # Save the output
    save_year2_output(daily_actions)
    
    print(f"\n🎄 Year 2 Optimal Strategy Complete! 🎄")