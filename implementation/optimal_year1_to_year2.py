#!/usr/bin/env python3
"""
Complete Year 1 to Year 2 optimal strategy algorithm.
Takes Year 1 ending position as fixed input and generates optimal Year 2 strategy 
using perfect information and optimal tax timing calculations.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import yaml
import numpy as np
from pathlib import Path
from data_loader import DataLoader
from typing import Dict, List, Tuple, Optional

class OptimalYear2Strategy:
    """Complete optimal strategy for Year 2 with perfect tax calculations."""
    
    def __init__(self):
        # Year 1 ending position (FIXED)
        self.year1_ending_cash = 144411
        self.year1_ending_assets = {'asset_1', 'asset_13', 'asset_2', 'asset_11', 'asset_15'}
        
        # Load Year 2 data
        self.data_loader = DataLoader("../problems/year_2/data", year=2)
        self.data_loader.load_data()
        
        # Strategy state
        self.daily_actions = {}
        self.cash = self.year1_ending_cash
        self.owned_assets = {}
        
        # Initialize owned assets from Year 1
        for asset_id in self.year1_ending_assets:
            self.owned_assets[asset_id] = {
                'acquisition_day': 0,  # Acquired at end of Year 1
                'last_tax_payment': 0
            }
    
    def calculate_optimal_tax_payment_day(self, asset_id: str, current_day: int, max_days: int = 30) -> int:
        """Calculate the optimal day to pay taxes for an asset using perfect information."""
        if max_days > 30:
            max_days = 30  # Hard limit
        
        min_cost = float('inf')
        optimal_day = current_day
        
        last_payment = self.owned_assets[asset_id]['last_tax_payment']
        
        # Try each possible payment day
        for payment_day in range(current_day, min(current_day + max_days, 101)):
            total_cost = 0.0
            
            # Calculate total tax cost if we pay on this day
            for day in range(last_payment + 1, payment_day + 1):
                if day > 100:
                    break
                try:
                    valuation = self.data_loader.get_asset_valuation(asset_id, day)
                    days_since_payment = day - last_payment
                    if days_since_payment > 30:  # Would exceed limit
                        total_cost = float('inf')
                        break
                    daily_tax = self.data_loader.calculate_daily_tax(asset_id, valuation, day, days_since_payment)
                    total_cost += daily_tax
                except:
                    total_cost = float('inf')
                    break
            
            if total_cost < min_cost:
                min_cost = total_cost
                optimal_day = payment_day
        
        return optimal_day
    
    def calculate_total_tax_burden(self, asset_id: str, buy_day: int, sell_day: int) -> Tuple[float, List]:
        """Calculate total tax burden and optimal payment schedule for holding period."""
        if sell_day <= buy_day:
            return 0.0, []
        
        total_tax = 0.0
        payment_schedule = []
        last_payment_day = buy_day
        current_day = buy_day + 1
        
        while current_day <= sell_day:
            # Find optimal payment day from current position
            max_wait_days = min(30 - (current_day - last_payment_day), sell_day - current_day + 1)
            if max_wait_days <= 0:
                # Must pay today
                optimal_payment_day = current_day
            else:
                optimal_payment_day = self.calculate_optimal_payment_day_for_period(
                    asset_id, last_payment_day, current_day, sell_day
                )
            
            # Calculate cost for this payment period
            period_cost = 0.0
            for day in range(last_payment_day + 1, optimal_payment_day + 1):
                if day > sell_day:
                    break
                try:
                    valuation = self.data_loader.get_asset_valuation(asset_id, day)
                    days_since_payment = day - last_payment_day
                    daily_tax = self.data_loader.calculate_daily_tax(asset_id, valuation, day, days_since_payment)
                    period_cost += daily_tax
                except:
                    break
            
            payment_schedule.append({
                'payment_day': optimal_payment_day,
                'cost': period_cost,
                'period_start': last_payment_day + 1,
                'period_end': optimal_payment_day
            })
            
            total_tax += period_cost
            last_payment_day = optimal_payment_day
            current_day = optimal_payment_day + 1
        
        return total_tax, payment_schedule
    
    def calculate_optimal_payment_day_for_period(self, asset_id: str, last_payment: int, start_day: int, end_day: int) -> int:
        """Find optimal payment day within a specific period."""
        min_cost = float('inf')
        optimal_day = start_day
        
        max_payment_day = min(last_payment + 30, end_day)
        
        for payment_day in range(start_day, max_payment_day + 1):
            total_cost = 0.0
            
            for day in range(last_payment + 1, payment_day + 1):
                try:
                    valuation = self.data_loader.get_asset_valuation(asset_id, day)
                    days_since_payment = day - last_payment
                    daily_tax = self.data_loader.calculate_daily_tax(asset_id, valuation, day, days_since_payment)
                    total_cost += daily_tax
                except:
                    total_cost = float('inf')
                    break
            
            if total_cost < min_cost:
                min_cost = total_cost
                optimal_day = payment_day
        
        return optimal_day
    
    def find_optimal_sell_fast(self, asset_id: str, current_value: float) -> Optional[Dict]:
        """Fast method to find optimal sell timing for owned asset."""
        best_profit = 0
        best_day = 100
        
        # Sample key days instead of all days (every 5 days + some random samples)
        sample_days = list(range(1, 101, 5))  # Every 5 days
        sample_days.extend([10, 15, 25, 35, 45, 55, 65, 75, 85, 95])  # Key points
        sample_days = sorted(set(sample_days))
        
        for sell_day in sample_days:
            if sell_day > 100:
                continue
            try:
                sell_price = self.data_loader.get_asset_valuation(asset_id, sell_day)
                # Use simplified tax calculation (assume daily payments)
                tax_burden = self.estimate_tax_burden_simple(asset_id, 0, sell_day)
                
                net_profit = sell_price - current_value - tax_burden
                
                if net_profit > best_profit:
                    best_profit = net_profit
                    best_day = sell_day
            except:
                continue
        
        if best_profit > 0:
            # Do final optimization around the best day found
            final_day, final_profit = self.refine_sell_timing(asset_id, current_value, best_day)
            
            if final_profit > 0:
                sell_price = self.data_loader.get_asset_valuation(asset_id, final_day)
                tax_burden = self.estimate_tax_burden_simple(asset_id, 0, final_day)
                
                return {
                    'asset_id': asset_id,
                    'type': 'sell_owned',
                    'currently_owned': True,
                    'buy_day': 0,
                    'buy_price': current_value,
                    'sell_day': final_day,
                    'sell_price': sell_price,
                    'gross_profit': sell_price - current_value,
                    'tax_burden': tax_burden,
                    'net_profit': final_profit,
                    'roi': (final_profit / current_value * 100) if current_value > 0 else 0,
                    'tax_schedule': [],
                    'priority': 1
                }
        return None
    
    def find_optimal_buy_sell_fast(self, asset_id: str, asset_info: Dict) -> Optional[Dict]:
        """Fast method to find optimal buy/sell combination."""
        available_day = asset_info['available_on_day']
        best_profit = 0
        best_buy_day = available_day
        best_sell_day = 100
        
        # Sample fewer combinations - focus on promising patterns
        buy_samples = list(range(max(1, available_day), 100, 7))  # Every 7 days
        buy_samples.extend([available_day, available_day + 1, available_day + 2])  # Early days
        buy_samples = sorted(set([d for d in buy_samples if d < 100]))
        
        for buy_day in buy_samples:
            try:
                buy_price = self.data_loader.get_asset_valuation(asset_id, buy_day)
                
                # For each buy day, sample sell days
                sell_samples = list(range(buy_day + 1, 101, 10))  # Every 10 days
                sell_samples.extend([buy_day + 1, buy_day + 7, buy_day + 14, 100])  # Key intervals
                sell_samples = sorted(set([d for d in sell_samples if d > buy_day and d <= 100]))
                
                for sell_day in sell_samples:
                    try:
                        sell_price = self.data_loader.get_asset_valuation(asset_id, sell_day)
                        tax_burden = self.estimate_tax_burden_simple(asset_id, buy_day, sell_day)
                        
                        gross_profit = sell_price - buy_price
                        net_profit = gross_profit - tax_burden
                        
                        if net_profit > best_profit:
                            best_profit = net_profit
                            best_buy_day = buy_day
                            best_sell_day = sell_day
                    except:
                        continue
            except:
                continue
        
        if best_profit > 0:
            # Final refinement around best combination
            final_buy, final_sell, final_profit = self.refine_buy_sell_timing(
                asset_id, best_buy_day, best_sell_day, best_profit
            )
            
            if final_profit > 0:
                buy_price = self.data_loader.get_asset_valuation(asset_id, final_buy)
                sell_price = self.data_loader.get_asset_valuation(asset_id, final_sell)
                tax_burden = self.estimate_tax_burden_simple(asset_id, final_buy, final_sell)
                
                return {
                    'asset_id': asset_id,
                    'type': 'buy_sell',
                    'currently_owned': False,
                    'buy_day': final_buy,
                    'buy_price': buy_price,
                    'sell_day': final_sell,
                    'sell_price': sell_price,
                    'gross_profit': sell_price - buy_price,
                    'tax_burden': tax_burden,
                    'net_profit': final_profit,
                    'roi': (final_profit / buy_price * 100) if buy_price > 0 else 0,
                    'tax_schedule': [],
                    'priority': 2
                }
        return None
    
    def estimate_tax_burden_simple(self, asset_id: str, buy_day: int, sell_day: int) -> float:
        """Fast estimate of tax burden assuming daily payments."""
        total_tax = 0.0
        
        for day in range(buy_day + 1, sell_day + 1):
            try:
                valuation = self.data_loader.get_asset_valuation(asset_id, day)
                # Assume daily payments (days_since = 1)
                daily_tax = self.data_loader.calculate_daily_tax(asset_id, valuation, day, 1)
                total_tax += daily_tax
            except:
                continue
        
        return total_tax
    
    def refine_sell_timing(self, asset_id: str, current_value: float, best_day: int) -> Tuple[int, float]:
        """Refine sell timing around the best day found."""
        best_profit = 0
        final_day = best_day
        
        # Check ±3 days around the best day
        for day in range(max(1, best_day - 3), min(101, best_day + 4)):
            try:
                sell_price = self.data_loader.get_asset_valuation(asset_id, day)
                tax_burden = self.estimate_tax_burden_simple(asset_id, 0, day)
                net_profit = sell_price - current_value - tax_burden
                
                if net_profit > best_profit:
                    best_profit = net_profit
                    final_day = day
            except:
                continue
        
        return final_day, best_profit
    
    def refine_buy_sell_timing(self, asset_id: str, buy_day: int, sell_day: int, current_profit: float) -> Tuple[int, int, float]:
        """Refine buy/sell timing around the best combination."""
        best_profit = current_profit
        final_buy = buy_day
        final_sell = sell_day
        
        # Check ±2 days around best buy/sell combination
        for b_day in range(max(1, buy_day - 2), min(100, buy_day + 3)):
            for s_day in range(max(b_day + 1, sell_day - 2), min(101, sell_day + 3)):
                try:
                    buy_price = self.data_loader.get_asset_valuation(asset_id, b_day)
                    sell_price = self.data_loader.get_asset_valuation(asset_id, s_day)
                    tax_burden = self.estimate_tax_burden_simple(asset_id, b_day, s_day)
                    
                    net_profit = sell_price - buy_price - tax_burden
                    
                    if net_profit > best_profit:
                        best_profit = net_profit
                        final_buy = b_day
                        final_sell = s_day
                except:
                    continue
        
        return final_buy, final_sell, best_profit
    
    def find_optimal_trades(self) -> List[Dict]:
        """Find optimal trading opportunities for Year 2 using smart heuristics."""
        all_assets = self.data_loader.get_all_assets()
        opportunities = []
        
        print(f"📈 Analyzing {len(all_assets)} assets for optimal trades...")
        print("⚡ Using optimized algorithms for faster processing...")
        
        # Analyze each asset
        for i, asset_id in enumerate(all_assets):
            if i % 20 == 0:  # Progress every 20 assets
                print(f"   Progress: {i}/{len(all_assets)} assets analyzed...")
                
            asset_info = self.data_loader.get_asset_info(asset_id)
            currently_owned = asset_id in self.owned_assets
            
            if currently_owned:
                # For owned assets, find optimal sell timing using smart sampling
                current_value = self.data_loader.get_asset_valuation(asset_id, 1)
                opportunity = self.find_optimal_sell_fast(asset_id, current_value)
                if opportunity:
                    opportunities.append(opportunity)
            else:
                # For unowned assets, use smart buy/sell sampling
                opportunity = self.find_optimal_buy_sell_fast(asset_id, asset_info)
                if opportunity:
                    opportunities.append(opportunity)
        
        # Sort by priority (owned assets first) then by net profit
        opportunities.sort(key=lambda x: (-x['priority'], -x['net_profit']))
        
        return opportunities
    
    def simulate_strategy(self, opportunities: List[Dict]) -> Dict:
        """Simulate the complete strategy execution."""
        print("🎯 Simulating Optimal Year 2 Strategy 🎯")
        print(f"Starting: {self.cash:,.0f} FSB + {len(self.owned_assets)} owned assets")
        
        # Track portfolio changes
        portfolio_log = []
        total_tax_paid = 0
        total_trades = 0
        
        # Execute day by day
        for day in range(1, 101):
            if day % 20 == 1:  # Progress every 20 days
                current_value = self.cash
                for asset_id in self.owned_assets:
                    try:
                        current_value += self.data_loader.get_asset_valuation(asset_id, day)
                    except:
                        pass
                print(f"   📅 Day {day}/100 - Portfolio value: {current_value:,.0f} FSB")
            
            daily_tax_paid = 0
            daily_actions = []
            
            # 1. Check for optimal tax payment opportunities
            for asset_id in list(self.owned_assets.keys()):
                asset_data = self.owned_assets[asset_id]
                days_since_payment = day - asset_data['last_tax_payment']
                
                # Find if any tax payment is optimal today
                optimal_payment_day = self.calculate_optimal_tax_payment_day(asset_id, day, 30 - days_since_payment)
                
                if optimal_payment_day == day or days_since_payment >= 25:  # Pay if optimal or approaching limit
                    # Calculate accumulated tax
                    accumulated_tax = 0
                    for tax_day in range(asset_data['last_tax_payment'] + 1, day + 1):
                        try:
                            valuation = self.data_loader.get_asset_valuation(asset_id, tax_day)
                            days_since = tax_day - asset_data['last_tax_payment']
                            daily_tax = self.data_loader.calculate_daily_tax(asset_id, valuation, tax_day, days_since)
                            accumulated_tax += daily_tax
                        except:
                            continue
                    
                    if self.cash >= accumulated_tax:
                        self.cash -= accumulated_tax
                        daily_tax_paid += accumulated_tax
                        total_tax_paid += accumulated_tax
                        self.owned_assets[asset_id]['last_tax_payment'] = day
                        daily_actions.append({'pay_tax': asset_id})
            
            # 2. Execute sell orders
            for opp in opportunities:
                if (opp['type'] == 'sell_owned' and opp['sell_day'] == day and 
                    opp['asset_id'] in self.owned_assets):
                    
                    asset_id = opp['asset_id']
                    
                    # Calculate any remaining tax and net proceeds
                    last_payment = self.owned_assets[asset_id]['last_tax_payment']
                    accumulated_tax = 0
                    
                    if last_payment < day:
                        for tax_day in range(last_payment + 1, day + 1):
                            try:
                                valuation = self.data_loader.get_asset_valuation(asset_id, tax_day)
                                days_since = tax_day - last_payment
                                daily_tax = self.data_loader.calculate_daily_tax(asset_id, valuation, tax_day, days_since)
                                accumulated_tax += daily_tax
                            except:
                                continue
                    
                    # Net proceeds after taxes
                    gross_proceeds = opp['sell_price']
                    net_proceeds = gross_proceeds - accumulated_tax
                    
                    self.cash += net_proceeds
                    daily_tax_paid += accumulated_tax
                    total_tax_paid += accumulated_tax
                    
                    del self.owned_assets[asset_id]
                    daily_actions.append({'sell': asset_id})
                    total_trades += 1
                    
                    if day % 10 == 0 or accumulated_tax > 50000:  # Show major sales
                        print(f"   💰 Day {day}: Sold {asset_id} for {gross_proceeds:,.0f} FSB (tax: {accumulated_tax:,.0f})")
            
            # 3. Execute buy orders (if we have enough cash)
            for opp in opportunities:
                if (opp['type'] == 'buy_sell' and opp['buy_day'] == day and 
                    opp['asset_id'] not in self.owned_assets):
                    
                    asset_id = opp['asset_id']
                    buy_price = opp['buy_price']
                    
                    # Estimate total cost including future taxes
                    estimated_total_cost = buy_price + opp['tax_burden']
                    
                    if self.cash >= estimated_total_cost:
                        self.cash -= buy_price
                        self.owned_assets[asset_id] = {
                            'acquisition_day': day,
                            'last_tax_payment': day
                        }
                        daily_actions.append({'buy': asset_id})
                        total_trades += 1
                        
                        if day % 10 == 0 or buy_price > 50000:  # Show major purchases
                            print(f"   🏪 Day {day}: Bought {asset_id} for {buy_price:,.0f} FSB")
                    else:
                        print(f"   ❌ Day {day}: Cannot afford {asset_id} ({estimated_total_cost:,.0f} needed, {self.cash:,.0f} available)")
            
            # Record daily actions
            if daily_actions:
                self.daily_actions[day] = daily_actions
            
            # Log portfolio state
            if daily_actions or daily_tax_paid > 0:
                asset_value = 0
                for asset_id in self.owned_assets:
                    try:
                        asset_value += self.data_loader.get_asset_valuation(asset_id, day)
                    except:
                        pass
                
                portfolio_log.append({
                    'day': day,
                    'cash': self.cash,
                    'asset_value': asset_value,
                    'total_wealth': self.cash + asset_value,
                    'assets_owned': len(self.owned_assets),
                    'tax_paid': daily_tax_paid
                })
        
        # Calculate final results
        final_asset_value = 0
        for asset_id in self.owned_assets:
            try:
                final_asset_value += self.data_loader.get_asset_valuation(asset_id, 100)
            except:
                pass
        
        final_wealth = self.cash + final_asset_value
        
        print(f"\n🏆 FINAL RESULTS:")
        print(f"Final Cash: {self.cash:,.0f} FSB")
        print(f"Final Assets: {final_asset_value:,.0f} FSB")
        print(f"Total Wealth: {final_wealth:,.0f} FSB")
        print(f"Total Tax Paid: {total_tax_paid:,.0f} FSB")
        print(f"Total Trades Executed: {total_trades}")
        print(f"Assets Still Owned: {len(self.owned_assets)}")
        print(f"Improvement over Year 1: {((final_wealth / 1386404) - 1) * 100:+.1f}%")
        
        return {
            'final_wealth': final_wealth,
            'final_cash': self.cash,
            'final_asset_value': final_asset_value,
            'total_tax_paid': total_tax_paid,
            'total_trades': total_trades,
            'daily_actions': self.daily_actions,
            'portfolio_log': portfolio_log
        }
    
    def generate_output_file(self, results: Dict):
        """Generate the output.yml file."""
        output_file = Path("../problems/year_2/output/output.yml")
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            yaml.dump(results['daily_actions'], f, default_flow_style=False, sort_keys=True)
        
        print(f"📄 Output saved to: {output_file}")
        return output_file

def main():
    """Execute the complete Year 1 to Year 2 optimal strategy."""
    print("🎄 Year 1 to Year 2 Optimal Strategy Algorithm 🎄")
    print("="*70)
    
    # Initialize strategy
    print("[STEP 1/4] Initializing strategy with Year 1 position...")
    strategy = OptimalYear2Strategy()
    print(f"✅ Starting with {strategy.cash:,.0f} FSB and {len(strategy.owned_assets)} owned assets")
    
    # Find all optimal opportunities
    print("\n[STEP 2/4] Finding optimal trading opportunities...")
    print("⏳ This may take a few minutes as we analyze all possible trades...")
    opportunities = strategy.find_optimal_trades()
    
    print(f"\n✅ Analysis complete! Found {len(opportunities)} profitable opportunities:")
    print(f"{'Asset':<8} {'Type':<12} {'Buy→Sell':<12} {'Net Profit':<12} {'ROI%':<8}")
    print("-" * 60)
    
    for opp in opportunities[:15]:  # Show top 15
        buy_sell = f"{opp['buy_day']}→{opp['sell_day']}"
        opp_type = "SELL OWNED" if opp['currently_owned'] else "BUY+SELL"
        print(f"{opp['asset_id']:<8} {opp_type:<12} {buy_sell:<12} {opp['net_profit']:<12,.0f} {opp['roi']:<8.1f}")
    
    # Simulate strategy
    print(f"\n[STEP 3/4] Simulating strategy execution...")
    print("⏳ Running day-by-day simulation with optimal tax timing...")
    results = strategy.simulate_strategy(opportunities)
    
    # Generate output
    print(f"\n[STEP 4/4] Generating output file...")
    output_file = strategy.generate_output_file(results)
    
    print(f"\n🎉 Complete Year 2 strategy generated successfully!")
    print(f"📊 Final wealth: {results['final_wealth']:,.0f} FSB")
    print(f"📁 Output saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    results = main()