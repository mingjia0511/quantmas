"""
Year 1 Asset Trading Solution

This module implements a trading strategy to maximize portfolio value
by analyzing asset price trends and making optimal buy/sell decisions.
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


class TradingStrategy:
    """
    Implements a trading strategy based on price trend analysis.
    
    Strategy:
    1. Calculate return potential for each asset (day 100 price vs current price)
    2. Identify assets with strong upward trends
    3. Buy when prices are relatively low in the trend
    4. Sell when prices peak or before day 100 to lock in gains
    """
    
    def __init__(self, assets_file: str, valuations_file: str):
        """Initialize with market data."""
        self.assets = self._load_assets(assets_file)
        self.valuations = self._load_valuations(valuations_file)
        self.portfolio = Portfolio()
        self.trading_log = {}
        
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
    
    def calculate_asset_roi(self, asset_id: str, current_day: int) -> float:
        """Calculate potential ROI from current day to day 100."""
        current_price = self.get_asset_price(asset_id, current_day)
        final_price = self.get_asset_price(asset_id, 100)
        return (final_price - current_price) / current_price
    
    def get_price_trend(self, asset_id: str, end_day: int, lookback_days: int = 10) -> float:
        """Calculate price trend (slope) over the last N days."""
        start_day = max(1, end_day - lookback_days + 1)
        prices = []
        days = []
        
        for day in range(start_day, end_day + 1):
            try:
                price = self.get_asset_price(asset_id, day)
                prices.append(price)
                days.append(day)
            except ValueError:
                continue
        
        if len(prices) < 2:
            return 0.0
        
        # Simple linear trend calculation
        n = len(prices)
        sum_x = sum(days)
        sum_y = sum(prices)
        sum_xy = sum(d * p for d, p in zip(days, prices))
        sum_x2 = sum(d * d for d in days)
        
        # Calculate slope (trend)
        if n * sum_x2 - sum_x * sum_x == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        return slope
    
    def is_good_buy_opportunity(self, asset_id: str, day: int) -> bool:
        """Determine if this is a good time to buy an asset."""
        # Check if asset is available
        if day < self.assets[asset_id].available_on_day:
            return False
        
        # Check if we already own it
        if asset_id in self.portfolio.owned_assets:
            return False
        
        # Check if we have enough cash
        current_price = self.get_asset_price(asset_id, day)
        if current_price > self.portfolio.cash:
            return False
        
        # Check ROI potential
        roi = self.calculate_asset_roi(asset_id, day)
        if roi < 0.1:  # Require at least 10% return potential
            return False
        
        # Check recent trend - prefer buying on dips in upward trends
        if day > 5:  # Need some history
            trend = self.get_price_trend(asset_id, day, 5)
            # Look for assets with positive long-term trend but recent dip
            long_trend = self.get_price_trend(asset_id, day, 10)
            if long_trend > 0 and trend < 0:  # Overall up but recent dip
                return True
        
        return roi > 0.2  # Otherwise require higher return threshold
    
    def is_good_sell_opportunity(self, asset_id: str, day: int) -> bool:
        """Determine if this is a good time to sell an asset."""
        if asset_id not in self.portfolio.owned_assets:
            return False
        
        # Always sell on day 100 (last day)
        if day == 100:
            return True
        
        # Sell if we're near the end and have good gains
        if day >= 90:
            roi = self.calculate_asset_roi(asset_id, day)
            if roi < 0.05:  # Less than 5% potential remaining
                return True
        
        # Sell if trend is strongly negative
        if day > 10:
            trend = self.get_price_trend(asset_id, day, 5)
            if trend < -1000:  # Strong downward trend
                return True
        
        return False
    
    def execute_day_trading(self, day: int) -> List[Dict[str, str]]:
        """Execute trading decisions for a given day."""
        actions = []
        
        # First, check for sell opportunities
        for asset_id in list(self.portfolio.owned_assets.keys()):
            if self.is_good_sell_opportunity(asset_id, day):
                actions.append({'sell': asset_id})
                price = self.get_asset_price(asset_id, day)
                self.portfolio.cash += price
                del self.portfolio.owned_assets[asset_id]
        
        # Then, check for buy opportunities
        for asset_id in self.assets.keys():
            if self.is_good_buy_opportunity(asset_id, day):
                actions.append({'buy': asset_id})
                price = self.get_asset_price(asset_id, day)
                self.portfolio.cash -= price
                self.portfolio.owned_assets[asset_id] = 1
        
        return actions
    
    def run_simulation(self) -> Dict[int, List[Dict[str, str]]]:
        """Run the complete trading simulation for all 100 days."""
        trading_log = {}
        
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
    strategy = TradingStrategy(assets_file, valuations_file)
    
    # Run simulation
    print("Running trading simulation...")
    trading_log = strategy.run_simulation()
    
    # Calculate and display results
    final_score = strategy.calculate_final_score()
    print(f"Final Portfolio Value: {final_score:,.2f} FSB")
    print(f"Starting Capital: 1,000,000 FSB")
    print(f"Total Return: {((final_score - 1_000_000) / 1_000_000) * 100:.2f}%")
    
    # Show final portfolio
    print(f"Final Cash: {strategy.portfolio.cash:,.2f} FSB")
    print("Final Assets:")
    for asset_id in strategy.portfolio.owned_assets:
        price = strategy.get_asset_price(asset_id, 100)
        asset_name = strategy.assets[asset_id].name
        print(f"  - {asset_name} ({asset_id}): {price:,.2f} FSB")
    
    # Save output
    Path("problems/year_1/output").mkdir(exist_ok=True)
    strategy.save_output(output_file)
    print(f"Trading decisions saved to {output_file}")
    
    # Show some trading activity
    print("\nTrading Activity Summary:")
    total_actions = sum(len(actions) for actions in trading_log.values())
    print(f"Total trading actions: {total_actions}")
    print(f"Active trading days: {len(trading_log)}")


if __name__ == "__main__":
    main()