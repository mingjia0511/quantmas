"""Tax calculation logic for Year 2."""

from typing import Dict


class TaxCalculator:
    """Handles tax calculations for assets with time-varying rates."""
    
    def __init__(self, tax_rates: Dict[str, Dict[int, Dict]]):
        """
        Initialize tax calculator with tax rate data.
        
        Args:
            tax_rates: Dict mapping asset_sub_type -> {day: {base_rate, modifier}}
        """
        self.tax_rates = tax_rates
        
        # Pre-compute rate change days for efficiency
        self.rate_change_days = {}
        for sub_type in tax_rates:
            self.rate_change_days[sub_type] = sorted(tax_rates[sub_type].keys())
    
    def get_rates_for_day(self, asset_sub_type: str, day: int) -> Dict:
        """
        Get tax rates applicable on a specific day.
        
        Args:
            asset_sub_type: Type of asset
            day: Day to get rates for
        
        Returns:
            Dict with base_rate and modifier
        """
        if asset_sub_type not in self.tax_rates:
            raise ValueError(f"Unknown asset sub-type: {asset_sub_type}")
        
        # Find the most recent rate change day <= current day
        change_days = self.rate_change_days[asset_sub_type]
        applicable_day = change_days[0]  # Default to first
        
        for change_day in change_days:
            if change_day <= day:
                applicable_day = change_day
            else:
                break
        
        return self.tax_rates[asset_sub_type][applicable_day]
    
    def calculate_tax(
        self,
        asset_sub_type: str,
        valuation: float,
        start_day: int,
        end_day: int
    ) -> float:
        """
        Calculate cumulative tax over a period.
        
        Formula: Daily Tax = Valuation × (Base Rate + Modifier × Days Since Start)
        
        Args:
            asset_sub_type: Type of asset
            valuation: Asset valuation (assumed constant for simplicity)
            start_day: First day of tax period (last payment day)
            end_day: Last day of tax period (current day)
        
        Returns:
            Total tax owed
        """
        if end_day <= start_day:
            return 0.0
        
        total_tax = 0.0
        
        # Calculate tax for each day in the period
        for day in range(start_day + 1, end_day + 1):
            days_since_start = day - start_day
            rates = self.get_rates_for_day(asset_sub_type, day)
            
            daily_rate = rates['base_rate'] + (rates['modifier'] * (days_since_start - 1))
            daily_tax = valuation * daily_rate
            total_tax += daily_tax
        
        return total_tax


class AssetTaxTracker:
    """Tracks tax payment history for individual assets."""
    
    def __init__(self, asset_id: str, asset_sub_type: str, purchase_day: int):
        """
        Initialize tax tracker for an asset.
        
        Args:
            asset_id: Asset identifier
            asset_sub_type: Type of asset
            purchase_day: Day asset was purchased
        """
        self.asset_id = asset_id
        self.asset_sub_type = asset_sub_type
        self.purchase_day = purchase_day
        self.last_payment_day = purchase_day
        self.total_tax_paid = 0.0
        self.payment_history = []  # List of (day, amount) tuples
    
    def days_since_last_payment(self, current_day: int) -> int:
        """Calculate days since last tax payment."""
        return current_day - self.last_payment_day
    
    def record_payment(self, day: int, amount: float):
        """
        Record a tax payment.
        
        Args:
            day: Day of payment
            amount: Amount paid
        """
        self.last_payment_day = day
        self.total_tax_paid += amount
        self.payment_history.append((day, amount))
    
    def needs_payment(self, current_day: int, max_days: int = 30) -> bool:
        """
        Check if tax payment is needed.
        
        Args:
            current_day: Current day
            max_days: Maximum days allowed between payments
        
        Returns:
            True if payment is needed
        """
        return self.days_since_last_payment(current_day) >= max_days
