"""Trading strategy for Year 1 challenge."""

from typing import Dict, List, Tuple
from .portfolio import Portfolio


class TradingStrategy:
    """Implements trading strategy for maximizing returns."""
    
    def __init__(
        self,
        assets: Dict[str, Dict],
        valuations: Dict[str, Dict[int, int]]
    ):
        """Initialize strategy with market data.
        
        Args:
            assets: Asset metadata
            valuations: Asset valuations by day
        """
        self.assets = assets
        self.valuations = valuations
        self.portfolio = Portfolio()
    
    def calculate_future_return(self, asset_id: str, buy_day: int) -> float:
        """Calculate expected return from buying asset on given day.
        
        Args:
            asset_id: Asset identifier
            buy_day: Day to buy
            
        Returns:
            Return percentage (day 100 value / buy day value - 1)
        """
        buy_price = self.valuations[asset_id][buy_day]
        sell_price = self.valuations[asset_id][100]
        return (sell_price - buy_price) / buy_price
    
    def find_best_opportunities(self, day: int) -> List[Tuple[str, float]]:
        """Find best investment opportunities for given day.
        
        Args:
            day: Current trading day
            
        Returns:
            List of (asset_id, expected_return) sorted by return descending
        """
        opportunities = []
        
        for asset_id in self.assets:
            # Check if asset is available
            if day < self.assets[asset_id]['available_on_day']:
                continue
            
            # Check if we already own it
            if asset_id in self.portfolio.owned_assets:
                continue
            
            # Calculate expected return
            expected_return = self.calculate_future_return(asset_id, day)
            
            # Only consider positive returns
            if expected_return > 0:
                opportunities.append((asset_id, expected_return))
        
        # Sort by expected return (highest first)
        opportunities.sort(key=lambda x: x[1], reverse=True)
        return opportunities
    
    def execute_strategy(self) -> Portfolio:
        """Execute buy-and-hold strategy.
        
        Buy best assets when they become available, hold until day 100.
        Uses a greedy approach: select top N assets by return that fit within budget.
        
        Returns:
            Portfolio with all transactions
        """
        # Get all opportunities sorted by return
        all_opportunities = []
        for asset_id in self.assets:
            available_day = self.assets[asset_id]['available_on_day']
            expected_return = self.calculate_future_return(asset_id, available_day)
            buy_price = self.valuations[asset_id][available_day]
            if expected_return > 0:
                all_opportunities.append((asset_id, available_day, buy_price, expected_return))
        
        # Sort by expected return (highest first)
        all_opportunities.sort(key=lambda x: x[3], reverse=True)
        
        # Select assets that fit within budget
        selected_assets = []
        total_cost = 0
        for asset_id, available_day, buy_price, expected_return in all_opportunities:
            if total_cost + buy_price <= self.portfolio.cash:
                selected_assets.append((asset_id, available_day))
                total_cost += buy_price
        
        # Execute buys on each day
        for day in range(1, 101):
            # Buy selected assets that become available today
            for asset_id, available_day in selected_assets:
                if available_day == day and asset_id not in self.portfolio.owned_assets:
                    price = self.valuations[asset_id][day]
                    if self.portfolio.can_buy(asset_id, price, available_day, day):
                        self.portfolio.buy(asset_id, price, day)
        
        return self.portfolio
