"""Portfolio management with tax tracking for Year 2."""

from typing import Dict, List, Tuple
from .tax_calculator import TaxCalculator, AssetTaxTracker


class Portfolio:
    """Manages portfolio state including cash, assets, and tax obligations."""
    
    def __init__(
        self,
        initial_cash: float,
        tax_calculator: TaxCalculator,
        valuations: Dict[str, Dict[int, float]],
        asset_metadata: Dict[str, Dict]
    ):
        """
        Initialize portfolio.
        
        Args:
            initial_cash: Starting cash amount
            tax_calculator: Tax calculation engine
            valuations: Dict mapping asset_id -> {day: valuation}
            asset_metadata: Dict mapping asset_id -> {sub_type, etc}
        """
        self.cash = initial_cash
        self.tax_calculator = tax_calculator
        self.valuations = valuations
        self.asset_metadata = asset_metadata
        
        # Track owned assets and their tax status
        self.owned_assets: Dict[str, AssetTaxTracker] = {}
        
        # Transaction history
        self.transactions: List[Tuple[int, str, str, float]] = []  # (day, action, asset_id, amount)
    
    def get_asset_valuation(self, asset_id: str, day: int) -> float:
        """Get asset valuation on a specific day."""
        if asset_id not in self.valuations:
            raise ValueError(f"Unknown asset: {asset_id}")
        if day not in self.valuations[asset_id]:
            raise ValueError(f"No valuation for {asset_id} on day {day}")
        return self.valuations[asset_id][day]
    
    def can_buy(self, asset_id: str, day: int) -> bool:
        """Check if we can afford to buy an asset."""
        if asset_id in self.owned_assets:
            return False  # Already own it
        
        valuation = self.get_asset_valuation(asset_id, day)
        return self.cash >= valuation
    
    def buy_asset(self, asset_id: str, day: int):
        """
        Buy an asset.
        
        Args:
            asset_id: Asset to buy
            day: Day of purchase
        """
        if not self.can_buy(asset_id, day):
            raise ValueError(f"Cannot buy {asset_id} on day {day}")
        
        valuation = self.get_asset_valuation(asset_id, day)
        self.cash -= valuation
        
        # Create tax tracker for this asset
        asset_sub_type = self.asset_metadata[asset_id]['asset_sub_type']
        self.owned_assets[asset_id] = AssetTaxTracker(asset_id, asset_sub_type, day)
        
        self.transactions.append((day, 'buy', asset_id, valuation))
    
    def add_existing_asset(self, asset_id: str, purchase_day: int):
        """
        Add an asset that was already owned (carried over from previous period).
        
        Args:
            asset_id: Asset to add
            purchase_day: Original purchase day (0 for carried over assets)
        """
        if asset_id in self.owned_assets:
            raise ValueError(f"Already own {asset_id}")
        
        if asset_id not in self.asset_metadata:
            raise ValueError(f"Unknown asset: {asset_id}")
        
        # Create tax tracker for this asset
        asset_sub_type = self.asset_metadata[asset_id]['asset_sub_type']
        self.owned_assets[asset_id] = AssetTaxTracker(asset_id, asset_sub_type, purchase_day)
    
    def can_sell(self, asset_id: str) -> bool:
        """Check if we can sell an asset."""
        return asset_id in self.owned_assets
    
    def sell_asset(self, asset_id: str, day: int):
        """
        Sell an asset.
        
        Args:
            asset_id: Asset to sell
            day: Day of sale
        """
        if not self.can_sell(asset_id):
            raise ValueError(f"Cannot sell {asset_id} on day {day} - not owned")
        
        valuation = self.get_asset_valuation(asset_id, day)
        self.cash += valuation
        
        # Remove from owned assets
        del self.owned_assets[asset_id]
        
        self.transactions.append((day, 'sell', asset_id, valuation))
    
    def calculate_tax_owed(self, asset_id: str, day: int) -> float:
        """
        Calculate tax owed for an asset.
        
        Args:
            asset_id: Asset to calculate tax for
            day: Current day
        
        Returns:
            Tax amount owed
        """
        if asset_id not in self.owned_assets:
            raise ValueError(f"Don't own {asset_id}")
        
        tracker = self.owned_assets[asset_id]
        
        if tracker.last_payment_day >= day:
            return 0.0
        
        valuation = self.get_asset_valuation(asset_id, day)
        return self.tax_calculator.calculate_tax(
            tracker.asset_sub_type,
            valuation,
            tracker.last_payment_day,
            day
        )
    
    def can_pay_tax(self, asset_id: str, day: int) -> bool:
        """Check if we can afford to pay tax on an asset."""
        if asset_id not in self.owned_assets:
            return False
        
        tax_owed = self.calculate_tax_owed(asset_id, day)
        return self.cash >= tax_owed
    
    def pay_tax(self, asset_id: str, day: int):
        """
        Pay tax on an asset.
        
        Args:
            asset_id: Asset to pay tax on
            day: Day of payment
        """
        if asset_id not in self.owned_assets:
            raise ValueError(f"Cannot pay tax on {asset_id} - not owned")
        
        tax_owed = self.calculate_tax_owed(asset_id, day)
        
        if tax_owed == 0:
            return  # No tax to pay
        
        if self.cash < tax_owed:
            raise ValueError(f"Insufficient cash to pay tax on {asset_id}: need ${tax_owed:.2f}, have ${self.cash:.2f}")
        
        self.cash -= tax_owed
        self.owned_assets[asset_id].record_payment(day, tax_owed)
        
        self.transactions.append((day, 'pay_tax', asset_id, tax_owed))
    
    def get_total_value(self, day: int) -> float:
        """
        Calculate total portfolio value.
        
        Args:
            day: Day to calculate value for
        
        Returns:
            Total value (cash + asset valuations - unpaid taxes with penalty if day 100)
        """
        total = self.cash
        
        # Add asset valuations
        for asset_id in self.owned_assets:
            total += self.get_asset_valuation(asset_id, day)
        
        # Subtract unpaid taxes (with 2x penalty if on day 100)
        for asset_id in self.owned_assets:
            tax_owed = self.calculate_tax_owed(asset_id, day)
            if day == 100:
                total -= (2 * tax_owed)  # Penalty
            else:
                total -= tax_owed
        
        return total
    
    def get_assets_needing_payment(self, day: int, max_days: int = 30) -> List[str]:
        """
        Get list of assets that need tax payment.
        
        Args:
            day: Current day
            max_days: Maximum days between payments
        
        Returns:
            List of asset IDs needing payment
        """
        return [
            asset_id
            for asset_id, tracker in self.owned_assets.items()
            if tracker.needs_payment(day, max_days)
        ]
