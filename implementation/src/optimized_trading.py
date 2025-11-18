"""
Optimized Year 1 Asset Trading Solution

Based on market analysis, this implements a more effective strategy
that focuses on high-ROI assets and optimal timing.
"""

import pandas as pd
import yaml
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Asset:
    """Represents a tradeable asset with its properties."""
    id: str
    name: str
    type: str
    sub_type: str
    available_on_day: int
    region: str


@dataclass
class Portfolio:
    """Tracks current portfolio state."""
    cash: float = 1_000_000  # Starting with 1 million FSB
    owned_assets: Dict[str, int] = None  # asset_id -> quantity (always 1 for unique assets)
    
    def __post_init__(self):
        if self.owned_assets is None:
            self.owned_assets = {}


class OptimizedTradingStrategy:
    """
    Optimized trading strategy based on market analysis.
    
    Key insights from analysis:
    1. Focus on high-ROI assets (asset_13, asset_14, asset_3, asset_1, asset_4)
    2. Avoid negative ROI assets (asset_2, asset_11, asset_15)
    3. Buy and hold is often better than active trading
    4. Some assets benefit from timing (buy on dips, sell at peaks)
    """
    
    def __init__(self, assets_file: str, valuations_file: str):
        """Initialize with market data."""
        self.assets = self._load_assets(assets_file)
        self.valuations = self._load_valuations(valuations_file)
        self.portfolio = Portfolio()
        self.trading_log = {}
        
        # Pre-calculated asset priorities based on analysis
        self.target_assets = [
            'asset_13',  # 68.14% ROI - Aurora Apartments
            'asset_14',  # 59.29% ROI - Mistletoe Market  
            'asset_3',   # 58.51% ROI - Toy Factory Complex
            'asset_1',   # 51.72% ROI - Snowflake Manor
            'asset_4',   # 49.00% ROI - Gingerbread Village
            'asset_7',   # 30.62% ROI - Elf Quarters
            'asset_10',  # 26.78% ROI - Frozen Lake Resort
        ]
        
        # Assets to avoid (negative or very low ROI)
        self.avoid_assets = ['asset_2', 'asset_11', 'asset_15', 'asset_9']
        
    def _load_assets(self, filename: str) -> Dict[str, Asset]:
        """Load asset information from CSV."""
        df = pd.read_csv(filename)
        assets = {}
        for _, row in df.iterrows():
            asset = Asset(
                id=row['id'],
                name=row['name'],
                type=row['type'],
                sub_type=row['sub_type'],
                available_on_day=row['available_on_day'],
                region=row['region']
            )
            assets[asset.id] = asset
        return assets
    
    def _load_valuations(self, filename: str) -> pd.DataFrame:
        """Load daily valuations from CSV."""
        return pd.read_csv(filename)
    
    def get_asset_price(self, asset_id: str, day: int) -> float:
        """Get the price of an asset on a specific day."""
        mask = (self.valuations['asset_id'] == asset_id) & (self.valuations['day'] == day)
        result = self.valuations[mask]['valuation']
        if len(result) == 0:
            raise ValueError(f"No price data for {asset_id} on day {day}")
        return float(result.iloc[0])
    
    def get_asset_price_history(self, asset_id: str, start_day: int, end_day: int) -> List[Tuple[int, float]]:
        """Get price history for an asset over a date range."""
        mask = (self.valuations['asset_id'] == asset_id) & \
               (self.valuations['day'] >= start_day) & \
               (self.valuations['day'] <= end_day)
        data = self.valuations[mask]
        return [(int(row['day']), float(row['valuation'])) for _, row in data.iterrows()]
    
    def find_optimal_buy_day(self, asset_id: str) -> int:
        """Find the best day to buy an asset based on price analysis."""
        available_day = self.assets[asset_id].available_on_day
        
        # Get price history from available day to day 90 (leave some time to sell)
        price_history = self.get_asset_price_history(asset_id, available_day, 90)
        
        if not price_history:
            return available_day
        
        # Find the day with minimum price in the first 70% of available period
        min_price = float('inf')
        best_day = available_day
        
        for day, price in price_history:
            if day <= available_day + (90 - available_day) * 0.7:  # First 70% of period
                if price < min_price:
                    min_price = price
                    best_day = day
        
        return best_day
    
    def find_optimal_sell_day(self, asset_id: str, buy_day: int) -> int:
        """Find the best day to sell an asset."""
        # Get price history from buy day to day 100
        price_history = self.get_asset_price_history(asset_id, buy_day, 100)
        
        if not price_history:
            return 100
        
        # Find the day with maximum price after buy day
        max_price = 0
        best_day = 100
        
        for day, price in price_history:
            if day > buy_day and price > max_price:
                max_price = price
                best_day = day
        
        # If we don't find a better price, hold until day 100
        final_price = self.get_asset_price(asset_id, 100)
        if max_price <= final_price * 1.02:  # Only sell early if >2% better
            return 100
        
        return best_day
    
    def should_buy_asset(self, asset_id: str, day: int) -> bool:
        """Determine if we should buy an asset on a given day."""
        # Check if asset is available
        if day < self.assets[asset_id].available_on_day:
            return False
        
        # Check if we already own it
        if asset_id in self.portfolio.owned_assets:
            return False
        
        # Skip assets we want to avoid
        if asset_id in self.avoid_assets:
            return False
        
        # Check if we have enough cash
        current_price = self.get_asset_price(asset_id, day)
        if current_price > self.portfolio.cash:
            return False
        
        # For target assets, buy on optimal day or close to it
        if asset_id in self.target_assets:
            optimal_day = self.find_optimal_buy_day(asset_id)
            # Buy if we're within 5 days of optimal day or if it's getting late
            if abs(day - optimal_day) <= 5 or day > optimal_day + 10:
                return True
        
        return False
    
    def should_sell_asset(self, asset_id: str, day: int, buy_day: int) -> bool:
        """Determine if we should sell an asset on a given day."""
        if asset_id not in self.portfolio.owned_assets:
            return False
        
        # Always sell on day 100
        if day == 100:
            return True
        
        # For most target assets, hold until day 100 unless we find optimal sell point
        if asset_id in self.target_assets:
            optimal_sell_day = self.find_optimal_sell_day(asset_id, buy_day)
            return day >= optimal_sell_day
        
        # Sell other assets if they're not performing well
        return day >= 95  # Sell by day 95 to be safe
    
    def execute_day_trading(self, day: int) -> List[Dict[str, str]]:
        """Execute trading decisions for a given day."""
        actions = []
        
        # Track when we bought assets for sell decisions
        buy_days = getattr(self, '_buy_days', {})
        
        # First, check for sell opportunities
        for asset_id in list(self.portfolio.owned_assets.keys()):
            buy_day = buy_days.get(asset_id, day)
            if self.should_sell_asset(asset_id, day, buy_day):
                actions.append({'sell': asset_id})
                price = self.get_asset_price(asset_id, day)
                self.portfolio.cash += price
                del self.portfolio.owned_assets[asset_id]
                if asset_id in buy_days:
                    del buy_days[asset_id]
        
        # Then, check for buy opportunities (prioritize target assets)
        # Don't buy on the last day since there's no benefit
        if day < 100:
            for asset_id in self.target_assets:
                if self.should_buy_asset(asset_id, day):
                    actions.append({'buy': asset_id})
                    price = self.get_asset_price(asset_id, day)
                    self.portfolio.cash -= price
                    self.portfolio.owned_assets[asset_id] = 1
                    buy_days[asset_id] = day
                    break  # Only buy one asset per day to be conservative
        
        # Store buy days for future reference
        self._buy_days = buy_days
        
        return actions
    
    def run_simulation(self) -> Dict[int, List[Dict[str, str]]]:
        """Run the complete trading simulation for all 100 days."""
        trading_log = {}
        self._buy_days = {}
        
        for day in range(1, 101):
            actions = self.execute_day_trading(day)
            if actions:  # Only record days with actions
                trading_log[day] = actions
        
        self.trading_log = trading_log
        return trading_log
    
    def calculate_final_score(self) -> float:
        """Calculate final portfolio value on day 100."""
        total_value = self.portfolio.cash
        
        for asset_id in self.portfolio.owned_assets:
            final_price = self.get_asset_price(asset_id, 100)
            total_value += final_price
        
        return total_value
    
    def save_output(self, filename: str):
        """Save trading decisions to YAML file."""
        with open(filename, 'w') as f:
            yaml.dump(self.trading_log, f, default_flow_style=False)


def main():
    """Main execution function."""
    # File paths
    assets_file = "problems/year_1/data/assets.csv"
    valuations_file = "problems/year_1/data/valuations.csv"
    output_file = "problems/year_1/output/output.yml"
    
    # Initialize strategy
    strategy = OptimizedTradingStrategy(assets_file, valuations_file)
    
    # Run simulation
    print("Running optimized trading simulation...")
    trading_log = strategy.run_simulation()
    
    # Calculate and display results
    final_score = strategy.calculate_final_score()
    print(f"Final Portfolio Value: {final_score:,.2f} FSB")
    print(f"Starting Capital: 1,000,000 FSB")
    print(f"Total Return: {((final_score - 1_000_000) / 1_000_000) * 100:.2f}%")
    
    # Show final portfolio
    print(f"Final Cash: {strategy.portfolio.cash:,.2f} FSB")
    print("Final Assets:")
    total_asset_value = 0
    for asset_id in strategy.portfolio.owned_assets:
        price = strategy.get_asset_price(asset_id, 100)
        asset_name = strategy.assets[asset_id].name
        total_asset_value += price
        print(f"  - {asset_name} ({asset_id}): {price:,.2f} FSB")
    
    print(f"Total Asset Value: {total_asset_value:,.2f} FSB")
    
    # Save output
    Path("problems/year_1/output").mkdir(exist_ok=True)
    strategy.save_output(output_file)
    print(f"Trading decisions saved to {output_file}")
    
    # Show trading activity summary
    print(f"\nTrading Activity Summary:")
    total_actions = sum(len(actions) for actions in trading_log.values())
    print(f"Total trading actions: {total_actions}")
    print(f"Active trading days: {len(trading_log)}")
    
    # Show key trades
    print(f"\nKey Trades:")
    for day, actions in sorted(trading_log.items()):
        for action in actions:
            action_type = 'buy' if 'buy' in action else 'sell'
            asset_id = action[action_type]
            price = strategy.get_asset_price(asset_id, day)
            print(f"  Day {day}: {action_type.upper()} {asset_id} at ${price:,.0f}")


if __name__ == "__main__":
    main()