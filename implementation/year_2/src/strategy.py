"""Trading strategy with tax optimization for Year 2."""

from typing import Dict, List, Tuple
from .portfolio import Portfolio


class TaxOptimizedStrategy:
    """
    Strategy that optimizes for returns while managing tax burden.
    
    Approach:
    1. Calculate net returns (gross return - estimated tax burden)
    2. Buy assets with best net returns on day 1
    3. Pay taxes every 10 days to balance cash vs tax accumulation
    4. Ensure all taxes paid by day 100
    """
    
    def __init__(
        self,
        portfolio: Portfolio,
        assets: List[Dict],
        num_days: int = 100
    ):
        """
        Initialize strategy.
        
        Args:
            portfolio: Portfolio to manage
            assets: List of available assets
            num_days: Trading period length
        """
        self.portfolio = portfolio
        self.assets = assets
        self.num_days = num_days
        
        # Strategy parameters
        self.tax_payment_interval = 10  # Pay tax every N days
        self.max_tax_delay = 28  # Never let tax go beyond this (safety margin before 30)
    
    def calculate_net_return(
        self,
        asset_id: str,
        buy_day: int,
        sell_day: int = 100
    ) -> float:
        """
        Calculate net return after taxes.
        
        Args:
            asset_id: Asset to evaluate
            buy_day: Day to buy
            sell_day: Day to sell
        
        Returns:
            Net return as percentage
        """
        buy_price = self.portfolio.get_asset_valuation(asset_id, buy_day)
        sell_price = self.portfolio.get_asset_valuation(asset_id, sell_day)
        
        # Estimate tax burden (assume we pay every 10 days)
        asset_sub_type = self.portfolio.asset_metadata[asset_id]['asset_sub_type']
        holding_days = sell_day - buy_day
        
        # Calculate tax for periodic payments
        total_tax = 0.0
        last_payment = buy_day
        
        for payment_day in range(buy_day + self.tax_payment_interval, sell_day + 1, self.tax_payment_interval):
            # Use average valuation for estimation
            avg_valuation = (buy_price + sell_price) / 2
            tax = self.portfolio.tax_calculator.calculate_tax(
                asset_sub_type,
                avg_valuation,
                last_payment,
                payment_day
            )
            total_tax += tax
            last_payment = payment_day
        
        # Add final tax payment
        if last_payment < sell_day:
            avg_valuation = (buy_price + sell_price) / 2
            final_tax = self.portfolio.tax_calculator.calculate_tax(
                asset_sub_type,
                avg_valuation,
                last_payment,
                sell_day
            )
            total_tax += final_tax
        
        # Calculate net return
        gross_profit = sell_price - buy_price
        net_profit = gross_profit - total_tax
        net_return = (net_profit / buy_price) * 100
        
        return net_return
    
    def find_best_assets(self, day: int, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Find assets with best net returns.
        
        Args:
            day: Current day
            top_n: Number of top assets to return
        
        Returns:
            List of (asset_id, net_return) tuples, sorted by net return
        """
        asset_returns = []
        
        for asset in self.assets:
            asset_id = asset['asset_id']
            
            # Skip if already owned
            if asset_id in self.portfolio.owned_assets:
                continue
            
            # Skip if can't afford
            if not self.portfolio.can_buy(asset_id, day):
                continue
            
            # Calculate net return
            try:
                net_return = self.calculate_net_return(asset_id, day)
                asset_returns.append((asset_id, net_return))
            except Exception as e:
                print(f"Warning: Could not calculate return for {asset_id}: {e}")
                continue
        
        # Sort by net return (descending)
        asset_returns.sort(key=lambda x: x[1], reverse=True)
        
        return asset_returns[:top_n]
    
    def execute_strategy(self) -> Dict[int, List[Dict[str, str]]]:
        """
        Execute the trading strategy.
        
        Returns:
            Dict mapping day -> list of actions
        """
        actions = {}
        
        print("=== Year 2: Tax Optimization Strategy ===\n")
        print(f"Initial Cash: ${self.portfolio.cash:,.2f}")
        
        # Show carried assets from Year 1
        if self.portfolio.owned_assets:
            print(f"Carried assets from Year 1: {len(self.portfolio.owned_assets)}")
            for asset_id in self.portfolio.owned_assets:
                valuation = self.portfolio.get_asset_valuation(asset_id, 1)
                print(f"  {asset_id}: ${valuation:,.0f}")
        print()
        
        # Day 1: Assess portfolio and potentially sell assets to build cash reserves
        print("Day 1: Assessing portfolio...")
        day_1_actions = []
        
        # Calculate total portfolio value
        total_value = self.portfolio.cash
        for asset_id in self.portfolio.owned_assets:
            total_value += self.portfolio.get_asset_valuation(asset_id, 1)
        
        # We need ~40% cash for tax payments over 100 days
        target_cash = total_value * 0.40
        cash_needed = target_cash - self.portfolio.cash
        
        if cash_needed > 0:
            print(f"  Need ${cash_needed:,.0f} more cash for tax payments")
            print(f"  Selling assets with lowest net returns...")
            
            # Calculate net returns for owned assets
            owned_returns = []
            for asset_id in list(self.portfolio.owned_assets.keys()):
                net_return = self.calculate_net_return(asset_id, 1, 100)
                owned_returns.append((asset_id, net_return))
            
            # Sort by net return (lowest first - sell worst performers)
            owned_returns.sort(key=lambda x: x[1])
            
            # Sell assets until we have enough cash
            for asset_id, net_return in owned_returns:
                if self.portfolio.cash >= target_cash:
                    break
                valuation = self.portfolio.get_asset_valuation(asset_id, 1)
                self.portfolio.sell_asset(asset_id, 1)
                day_1_actions.append({'sell': asset_id})
                print(f"  Sold {asset_id}: ${valuation:,.0f} (net return: {net_return:.2f}%)")
        
        # Now consider buying new assets
        print("\n  Analyzing new assets to buy...")
        best_assets = self.find_best_assets(1, top_n=15)
        
        # Reserve cash for taxes
        tax_reserve = self.portfolio.cash * 0.35
        
        for asset_id, net_return in best_assets:
            valuation = self.portfolio.get_asset_valuation(asset_id, 1)
            if self.portfolio.cash - valuation >= tax_reserve:
                self.portfolio.buy_asset(asset_id, 1)
                day_1_actions.append({'buy': asset_id})
                print(f"  Bought {asset_id}: ${valuation:,.0f} (net return: {net_return:.2f}%)")
        
        if day_1_actions:
            actions[1] = day_1_actions
        
        print(f"\nDay 1 Summary:")
        print(f"  Actions: {len(day_1_actions)}")
        print(f"  Cash: ${self.portfolio.cash:,.2f}")
        print(f"  Assets owned: {len(self.portfolio.owned_assets)}")
        print(f"  Portfolio value: ${self.portfolio.get_total_value(1):,.2f}\n")
        
        # Days 2-100: Manage taxes
        for day in range(2, self.num_days + 1):
            day_actions = []
            
            # Check for assets needing urgent tax payment (approaching 30-day limit)
            urgent_assets = self.portfolio.get_assets_needing_payment(day, self.max_tax_delay)
            
            if urgent_assets:
                print(f"Day {day}: Urgent tax payments needed for {len(urgent_assets)} assets")
                for asset_id in urgent_assets:
                    if self.portfolio.can_pay_tax(asset_id, day):
                        tax_owed = self.portfolio.calculate_tax_owed(asset_id, day)
                        self.portfolio.pay_tax(asset_id, day)
                        day_actions.append({'pay_tax': asset_id})
                        print(f"  Paid tax on {asset_id}: ${tax_owed:,.2f}")
                    else:
                        # Need to sell asset to avoid 30-day penalty
                        tax_owed = self.portfolio.calculate_tax_owed(asset_id, day)
                        print(f"  WARNING: Cannot afford tax on {asset_id} (${tax_owed:,.2f})")
                        print(f"  Selling {asset_id} to avoid 30-day penalty")
                        self.portfolio.sell_asset(asset_id, day)
                        day_actions.append({'sell': asset_id})
                        print(f"  Sold {asset_id} for ${self.portfolio.get_asset_valuation(asset_id, day):,.2f}")
            
            # Regular tax payment schedule (every N days)
            if day % self.tax_payment_interval == 0:
                assets_to_pay = []
                for asset_id in list(self.portfolio.owned_assets.keys()):
                    tracker = self.portfolio.owned_assets[asset_id]
                    days_since = tracker.days_since_last_payment(day)
                    
                    # Pay if we've accumulated some days and not already paid today
                    if days_since >= self.tax_payment_interval:
                        assets_to_pay.append((asset_id, days_since))
                
                if assets_to_pay:
                    print(f"Day {day}: Regular tax payment cycle")
                    for asset_id, days_since in assets_to_pay:
                        if self.portfolio.can_pay_tax(asset_id, day):
                            tax_owed = self.portfolio.calculate_tax_owed(asset_id, day)
                            self.portfolio.pay_tax(asset_id, day)
                            day_actions.append({'pay_tax': asset_id})
                            print(f"  Paid tax on {asset_id}: ${tax_owed:,.2f} ({days_since} days)")
            
            # Final day: Pay all remaining taxes
            if day == 100:
                print(f"\nDay {day}: Final tax settlement")
                for asset_id in list(self.portfolio.owned_assets.keys()):
                    tax_owed = self.portfolio.calculate_tax_owed(asset_id, day)
                    if tax_owed > 0:
                        if self.portfolio.can_pay_tax(asset_id, day):
                            self.portfolio.pay_tax(asset_id, day)
                            day_actions.append({'pay_tax': asset_id})
                            tracker = self.portfolio.owned_assets[asset_id]
                            days_since = day - tracker.payment_history[-2][0] if len(tracker.payment_history) > 1 else day - tracker.purchase_day
                            print(f"  Final tax on {asset_id}: ${tax_owed:,.2f}")
                        else:
                            print(f"  ERROR: Cannot pay final tax on {asset_id} (${tax_owed:,.2f})")
            
            if day_actions:
                actions[day] = day_actions
        
        # Print final results
        final_value = self.portfolio.get_total_value(100)
        initial_value = 1_000_000
        total_return = ((final_value - initial_value) / initial_value) * 100
        
        print(f"\n=== Final Results ===")
        print(f"Final Portfolio Value: ${final_value:,.2f}")
        print(f"Total Return: {total_return:.2f}%")
        print(f"Cash Remaining: ${self.portfolio.cash:,.2f}")
        print(f"Assets Owned: {len(self.portfolio.owned_assets)}")
        
        # Calculate total taxes paid
        total_tax = sum(
            tracker.total_tax_paid
            for tracker in self.portfolio.owned_assets.values()
        )
        print(f"Total Taxes Paid: ${total_tax:,.2f}")
        
        return actions
