"""
Portfolio tracking module for Quantmas challenges.
Manages cash, asset ownership, trading validation, and tax obligations.
"""
from typing import Dict, List, Set
from dataclasses import dataclass
from enum import Enum


class TradeAction(Enum):
    """Enumeration for trade actions."""
    BUY = "buy"
    SELL = "sell"
    PAY_TAX = "pay_tax"


@dataclass
class TaxObligation:
    """Represents tax owed on an asset."""
    asset_id: str
    accumulated_tax: float
    last_payment_day: int
    days_since_last_payment: int


@dataclass
class Trade:
    """Represents a trading action."""
    action: TradeAction
    asset_id: str
    day: int
    price: float


class PortfolioTracker:
    """Tracks portfolio state, validates trading actions, and manages tax obligations."""
    
    def __init__(self, initial_cash: float = 1_000_000, year: int = 1, starting_assets: Set[str] = None):
        """Initialize portfolio with starting cash and optionally starting assets."""
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.year = year
        self.owned_assets: Set[str] = starting_assets or set()
        self.trade_history: List[Trade] = []
        self.daily_trades: Dict[int, List[Dict[str, str]]] = {}
        
        # Tax tracking (Year 2+)
        self.tax_obligations: Dict[str, TaxObligation] = {}
        self.total_tax_paid: float = 0.0
        
        # Initialize tax obligations for starting assets
        if starting_assets:
            for asset_id in starting_assets:
                self.tax_obligations[asset_id] = TaxObligation(
                    asset_id=asset_id,
                    accumulated_tax=0.0,
                    last_payment_day=0,  # Never paid taxes
                    days_since_last_payment=1  # Start accumulating from day 1
                )
    
    def can_buy(self, asset_id: str, price: float, available_on_day: int, current_day: int) -> bool:
        """Check if an asset can be purchased."""
        # Check if we have enough cash
        if self.cash < price:
            return False
        
        # Check if asset is available for purchase
        if current_day < available_on_day:
            return False
        
        # Check if we don't already own the asset
        if asset_id in self.owned_assets:
            return False
        
        return True
    
    def can_sell(self, asset_id: str) -> bool:
        """Check if an asset can be sold (must have no outstanding taxes)."""
        if asset_id not in self.owned_assets:
            return False
        
        # In Year 2+, must settle all taxes before selling
        if self.year >= 2 and asset_id in self.tax_obligations:
            return self.tax_obligations[asset_id].accumulated_tax == 0
        
        return True
    
    def buy_asset(self, asset_id: str, price: float, day: int) -> bool:
        """Execute a buy order."""
        if self.cash < price:
            raise ValueError(f"Insufficient funds to buy {asset_id}. Need {price}, have {self.cash}")
        
        if asset_id in self.owned_assets:
            raise ValueError(f"Already own {asset_id}")
        
        self.cash -= price
        self.owned_assets.add(asset_id)
        
        # Initialize tax obligation for Year 2+
        if self.year >= 2:
            self.tax_obligations[asset_id] = TaxObligation(
                asset_id=asset_id,
                accumulated_tax=0.0,
                last_payment_day=day,
                days_since_last_payment=0
            )
        
        trade = Trade(TradeAction.BUY, asset_id, day, price)
        self.trade_history.append(trade)
        
        # Record for output format
        if day not in self.daily_trades:
            self.daily_trades[day] = []
        self.daily_trades[day].append({"buy": asset_id})
        
        return True
    
    def sell_asset(self, asset_id: str, price: float, day: int) -> bool:
        """Execute a sell order."""
        if asset_id not in self.owned_assets:
            raise ValueError(f"Don't own {asset_id}")
        
        # Must settle all taxes before selling in Year 2+
        if self.year >= 2 and asset_id in self.tax_obligations:
            if self.tax_obligations[asset_id].accumulated_tax > 0:
                raise ValueError(f"Must pay outstanding taxes on {asset_id} before selling")
        
        self.cash += price
        self.owned_assets.remove(asset_id)
        
        # Remove tax obligation
        if asset_id in self.tax_obligations:
            del self.tax_obligations[asset_id]
        
        trade = Trade(TradeAction.SELL, asset_id, day, price)
        self.trade_history.append(trade)
        
        # Record for output format
        if day not in self.daily_trades:
            self.daily_trades[day] = []
        self.daily_trades[day].append({"sell": asset_id})
        
        return True
    
    def can_pay_tax(self, asset_id: str, tax_amount: float) -> bool:
        """Check if we can pay tax for an asset."""
        if asset_id not in self.owned_assets:
            return False
        if self.cash < tax_amount:
            return False
        if asset_id not in self.tax_obligations:
            return False
        return True
    
    def pay_tax(self, asset_id: str, tax_amount: float, day: int) -> bool:
        """Pay tax for an asset."""
        if not self.can_pay_tax(asset_id, tax_amount):
            raise ValueError(f"Cannot pay tax for {asset_id}: insufficient funds or don't own asset")
        
        self.cash -= tax_amount
        self.total_tax_paid += tax_amount
        
        # Reset tax obligation
        self.tax_obligations[asset_id] = TaxObligation(
            asset_id=asset_id,
            accumulated_tax=0.0,
            last_payment_day=day,
            days_since_last_payment=0
        )
        
        trade = Trade(TradeAction.PAY_TAX, asset_id, day, tax_amount)
        self.trade_history.append(trade)
        
        # Record for output format
        if day not in self.daily_trades:
            self.daily_trades[day] = []
        self.daily_trades[day].append({"pay_tax": asset_id})
        
        return True
    
    def update_tax_obligations(self, day: int, data_loader):
        """Update daily tax obligations for all owned assets."""
        if self.year < 2 or not data_loader.tax_rates_df is not None:
            return
        
        for asset_id in self.owned_assets:
            if asset_id in self.tax_obligations:
                obligation = self.tax_obligations[asset_id]
                
                # Update days since last payment
                obligation.days_since_last_payment = day - obligation.last_payment_day
                
                # Skip if days since payment exceeds 30 (must pay by then)
                if obligation.days_since_last_payment > 30:
                    raise ValueError(f"Tax payment overdue for {asset_id}. Must pay within 30 days.")
                
                # Calculate daily tax and add to accumulated tax
                current_valuation = data_loader.get_asset_valuation(asset_id, day)
                daily_tax = data_loader.calculate_daily_tax(
                    asset_id, current_valuation, day, obligation.days_since_last_payment
                )
                obligation.accumulated_tax += daily_tax
    
    def get_tax_obligations_summary(self) -> Dict:
        """Get summary of tax obligations."""
        total_tax_owed = sum(obligation.accumulated_tax for obligation in self.tax_obligations.values())
        
        return {
            "total_tax_owed": total_tax_owed,
            "total_tax_paid": self.total_tax_paid,
            "obligations": {asset_id: {
                "accumulated_tax": obligation.accumulated_tax,
                "last_payment_day": obligation.last_payment_day,
                "days_since_last_payment": obligation.days_since_last_payment
            } for asset_id, obligation in self.tax_obligations.items()}
        }
    
    def get_portfolio_value(self, day_100_valuations: Dict[str, float], include_tax_penalty: bool = True) -> float:
        """Calculate total portfolio value on day 100."""
        asset_value = sum(day_100_valuations.get(asset_id, 0) for asset_id in self.owned_assets)
        
        # Apply tax penalties for unpaid taxes in Year 2+
        tax_penalty = 0.0
        if self.year >= 2 and include_tax_penalty:
            total_unpaid_tax = sum(obligation.accumulated_tax for obligation in self.tax_obligations.values())
            tax_penalty = total_unpaid_tax * 2  # 2x penalty
        
        return self.cash + asset_value - tax_penalty
    
    def get_trading_summary(self) -> Dict:
        """Get summary of trading activity."""
        buy_trades = [t for t in self.trade_history if t.action == TradeAction.BUY]
        sell_trades = [t for t in self.trade_history if t.action == TradeAction.SELL]
        tax_trades = [t for t in self.trade_history if t.action == TradeAction.PAY_TAX]
        
        summary = {
            "initial_cash": self.initial_cash,
            "current_cash": self.cash,
            "total_buys": len(buy_trades),
            "total_sells": len(sell_trades),
            "cash_spent": sum(t.price for t in buy_trades),
            "cash_gained": sum(t.price for t in sell_trades),
            "owned_assets": list(self.owned_assets),
            "net_cash_flow": sum(t.price for t in sell_trades) - sum(t.price for t in buy_trades)
        }
        
        if self.year >= 2:
            summary.update({
                "total_tax_payments": len(tax_trades),
                "total_tax_paid": self.total_tax_paid,
                "current_tax_obligations": sum(obligation.accumulated_tax for obligation in self.tax_obligations.values())
            })
        
        return summary
    
    def get_daily_trades_output(self) -> Dict[int, List[Dict[str, str]]]:
        """Get trades in the required output format."""
        return self.daily_trades
    
    def reset(self):
        """Reset portfolio to initial state."""
        self.cash = self.initial_cash
        self.owned_assets.clear()
        self.trade_history.clear()
        self.daily_trades.clear()
        
        if self.year >= 2:
            self.tax_obligations.clear()
            self.total_tax_paid = 0.0