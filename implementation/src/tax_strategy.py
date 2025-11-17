"""
Tax strategy module for Quantmas Year 2+ challenges.
Handles optimal tax payment timing decisions.
"""
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TaxDecision:
    """Represents a tax payment decision."""
    asset_id: str
    pay_now: bool
    estimated_cost: float
    days_to_wait: int = 0
    reason: str = ""


class TaxStrategy:
    """Handles tax payment timing optimization."""
    
    def __init__(self, data_loader, portfolio_tracker):
        """Initialize with data loader and portfolio tracker."""
        self.data_loader = data_loader
        self.portfolio = portfolio_tracker
        self.max_delay_days = 30
    
    def should_pay_tax_now(self, asset_id: str, current_day: int) -> TaxDecision:
        """Determine if we should pay tax now or wait."""
        if asset_id not in self.portfolio.tax_obligations:
            return TaxDecision(asset_id, False, 0.0, 0, "No tax obligation")
        
        obligation = self.portfolio.tax_obligations[asset_id]
        
        # Must pay if approaching 30-day limit
        if obligation.days_since_last_payment >= 25:
            return TaxDecision(
                asset_id, True, obligation.accumulated_tax, 0,
                f"Approaching 30-day limit ({obligation.days_since_last_payment} days)"
            )
        
        # Calculate cost of paying now vs waiting
        current_tax_cost = obligation.accumulated_tax
        
        # Estimate future costs if we wait different amounts of days
        best_wait_days = 0
        lowest_cost = current_tax_cost
        
        for wait_days in range(1, min(self.max_delay_days - obligation.days_since_last_payment, 10)):
            future_day = current_day + wait_days
            if future_day > 100:
                break
            
            try:
                # Estimate future valuation (simple trend analysis)
                future_valuation = self._estimate_future_valuation(asset_id, current_day, future_day)
                
                # Calculate total tax if we wait
                total_future_tax = self._calculate_future_tax_cost(
                    asset_id, current_day, future_day, future_valuation, obligation.days_since_last_payment
                )
                
                if total_future_tax < lowest_cost:
                    lowest_cost = total_future_tax
                    best_wait_days = wait_days
                    
            except Exception:
                # If we can't estimate, don't wait
                break
        
        # Decision logic
        if best_wait_days > 0 and lowest_cost < current_tax_cost * 0.95:  # At least 5% savings
            return TaxDecision(
                asset_id, False, lowest_cost, best_wait_days,
                f"Wait {best_wait_days} days for estimated savings of {current_tax_cost - lowest_cost:,.0f} FSB"
            )
        else:
            return TaxDecision(
                asset_id, True, current_tax_cost, 0,
                f"Pay now to avoid escalating costs"
            )
    
    def _estimate_future_valuation(self, asset_id: str, current_day: int, future_day: int) -> float:
        """Estimate asset valuation on future day using trend analysis."""
        # Get recent price history
        history = self.data_loader.get_asset_price_history(asset_id, current_day)
        
        if len(history) < 5:
            # Not enough history, assume current price
            return self.data_loader.get_asset_valuation(asset_id, current_day)
        
        # Simple linear trend estimation
        recent_history = history.tail(5)
        days = recent_history['day'].values
        prices = recent_history['valuation'].values
        
        # Calculate simple slope
        if len(days) >= 2:
            slope = (prices[-1] - prices[0]) / (days[-1] - days[0])
            current_price = prices[-1]
            days_ahead = future_day - current_day
            estimated_price = current_price + (slope * days_ahead)
            
            # Don't let estimate go negative or be too extreme
            current_price = self.data_loader.get_asset_valuation(asset_id, current_day)
            estimated_price = max(estimated_price, current_price * 0.5)  # Not below 50% of current
            estimated_price = min(estimated_price, current_price * 1.5)  # Not above 150% of current
            
            return estimated_price
        
        return self.data_loader.get_asset_valuation(asset_id, current_day)
    
    def _calculate_future_tax_cost(self, asset_id: str, current_day: int, future_day: int, 
                                 future_valuation: float, current_days_since_payment: int) -> float:
        """Calculate total tax cost if we wait until future_day to pay."""
        total_tax = 0.0
        
        # Add accumulated tax up to current day
        obligation = self.portfolio.tax_obligations[asset_id]
        total_tax += obligation.accumulated_tax
        
        # Add estimated daily taxes from current_day + 1 to future_day
        for day in range(current_day + 1, future_day + 1):
            days_since_payment = current_days_since_payment + (day - current_day)
            if days_since_payment > 30:
                # Would exceed limit
                return float('inf')
            
            # Use linear interpolation for valuation between current and future
            if future_day > current_day:
                current_valuation = self.data_loader.get_asset_valuation(asset_id, current_day)
                progress = (day - current_day) / (future_day - current_day)
                estimated_valuation = current_valuation + progress * (future_valuation - current_valuation)
            else:
                estimated_valuation = future_valuation
            
            daily_tax = self.data_loader.calculate_daily_tax(
                asset_id, estimated_valuation, day, days_since_payment
            )
            total_tax += daily_tax
        
        return total_tax
    
    def get_tax_payment_recommendations(self, current_day: int) -> List[TaxDecision]:
        """Get tax payment recommendations for all owned assets."""
        recommendations = []
        
        for asset_id in self.portfolio.owned_assets:
            if asset_id in self.portfolio.tax_obligations:
                decision = self.should_pay_tax_now(asset_id, current_day)
                recommendations.append(decision)
        
        return recommendations
    
    def prioritize_tax_payments(self, current_day: int, available_cash: float) -> List[str]:
        """Prioritize which taxes to pay given limited cash."""
        recommendations = self.get_tax_payment_recommendations(current_day)
        
        # Sort by urgency (days since last payment) and cost efficiency
        urgent_payments = []
        optional_payments = []
        
        for decision in recommendations:
            if decision.pay_now:
                obligation = self.portfolio.tax_obligations[decision.asset_id]
                if obligation.days_since_last_payment >= 25:
                    urgent_payments.append((decision.asset_id, obligation.accumulated_tax))
                else:
                    optional_payments.append((decision.asset_id, obligation.accumulated_tax))
        
        # Sort urgent by cost (pay cheapest first to preserve cash)
        urgent_payments.sort(key=lambda x: x[1])
        optional_payments.sort(key=lambda x: x[1])
        
        # Build priority list
        priority_list = []
        remaining_cash = available_cash
        
        # Pay urgent taxes first
        for asset_id, cost in urgent_payments:
            if remaining_cash >= cost:
                priority_list.append(asset_id)
                remaining_cash -= cost
        
        # Pay optional taxes if we have cash
        for asset_id, cost in optional_payments:
            if remaining_cash >= cost:
                priority_list.append(asset_id)
                remaining_cash -= cost
        
        return priority_list