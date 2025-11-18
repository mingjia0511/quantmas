"""Portfolio management for Year 1 challenge."""

from typing import Dict, List, Set


class Portfolio:
    """Manages portfolio state and transactions."""
    
    def __init__(self, starting_cash: int = 1_000_000):
        """Initialize portfolio with starting cash."""
        self.cash = starting_cash
        self.owned_assets: Set[str] = set()
        self.transactions: Dict[int, List[Dict]] = {}
    
    def can_buy(self, asset_id: str, price: int, available_day: int, current_day: int) -> bool:
        """Check if asset can be purchased.
        
        Args:
            asset_id: Asset identifier
            price: Purchase price
            available_day: Day asset becomes available
            current_day: Current trading day
            
        Returns:
            True if purchase is valid
        """
        return (
            self.cash >= price and
            asset_id not in self.owned_assets and
            current_day >= available_day
        )
    
    def can_sell(self, asset_id: str) -> bool:
        """Check if asset can be sold.
        
        Args:
            asset_id: Asset identifier
            
        Returns:
            True if sale is valid
        """
        return asset_id in self.owned_assets
    
    def buy(self, asset_id: str, price: int, day: int) -> None:
        """Purchase an asset.
        
        Args:
            asset_id: Asset to purchase
            price: Purchase price
            day: Trading day
        """
        self.cash -= price
        self.owned_assets.add(asset_id)
        self._record_transaction(day, 'buy', asset_id)
    
    def sell(self, asset_id: str, price: int, day: int) -> None:
        """Sell an asset.
        
        Args:
            asset_id: Asset to sell
            price: Sale price
            day: Trading day
        """
        self.cash += price
        self.owned_assets.remove(asset_id)
        self._record_transaction(day, 'sell', asset_id)
    
    def _record_transaction(self, day: int, action: str, asset_id: str) -> None:
        """Record a transaction.
        
        Args:
            day: Trading day
            action: 'buy' or 'sell'
            asset_id: Asset identifier
        """
        if day not in self.transactions:
            self.transactions[day] = []
        self.transactions[day].append({action: asset_id})
    
    def calculate_final_value(self, valuations: Dict[str, Dict[int, int]]) -> int:
        """Calculate total portfolio value at day 100.
        
        Args:
            valuations: Asset valuations by day
            
        Returns:
            Total wealth (cash + asset values)
        """
        asset_value = sum(
            valuations[asset_id][100]
            for asset_id in self.owned_assets
        )
        return self.cash + asset_value
    
    def get_transactions(self) -> Dict[int, List[Dict]]:
        """Get all recorded transactions.
        
        Returns:
            Dict mapping day to list of transactions
        """
        return self.transactions
