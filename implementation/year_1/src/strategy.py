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
    
    def should_sell(self, asset_id: str, day: int) -> bool:
        """Determine if asset should be sold on given day.
        
        Args:
            asset_id: Asset identifier
            day: Current trading day
            
        Returns:
            True if asset should be sold
        """
        if day >= 100:
            return False  # Hold until end
        
        current_price = self.valuations[asset_id][day]
        future_price = self.valuations[asset_id][day + 1] if day < 100 else current_price
        
        # Sell if price will drop tomorrow
        return future_price < current_price
    
    def execute_strategy(self) -> Portfolio:
        """Execute trading strategy across all 100 days.
        
        Returns:
            Portfolio with all transactions
        """
        for day in range(1, 101):
            # Check for sell opportunities first
            assets_to_sell = [
                asset_id for asset_id in list(self.portfolio.owned_assets)
                if self.should_sell(asset_id, day)
            ]
            
            for asset_id in assets_to_sell:
                price = self.valuations[asset_id][day]
                self.portfolio.sell(asset_id, price, day)
            
            # Look for buy opportunities
            opportunities = self.find_best_opportunities(day)
            
            for asset_id, expected_return in opportunities:
                price = self.valuations[asset_id][day]
                available_day = self.assets[asset_id]['available_on_day']
                
                if self.portfolio.can_buy(asset_id, price, available_day, day):
                    self.portfolio.buy(asset_id, price, day)
        
        return self.portfolio
