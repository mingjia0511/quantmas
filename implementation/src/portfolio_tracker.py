"""
Portfolio tracking module for Quantmas Year 1 challenge.
Manages cash, asset ownership, and trading validation.
"""
from typing import Dict, List, Set
from dataclasses import dataclass
from enum import Enum


class TradeAction(Enum):
    """Enumeration for trade actions."""
    BUY = "buy"
    SELL = "sell"


@dataclass
class Trade:
    """Represents a trading action."""
    action: TradeAction
    asset_id: str
    day: int
    price: float


class PortfolioTracker:
    """Tracks portfolio state and validates trading actions."""
    
    def __init__(self, initial_cash: float = 1_000_000):
        """Initialize portfolio with starting cash."""
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.owned_assets: Set[str] = set()
        self.trade_history: List[Trade] = []
        self.daily_trades: Dict[int, List[Dict[str, str]]] = {}
    
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
        """Check if an asset can be sold."""
        return asset_id in self.owned_assets
    
    def buy_asset(self, asset_id: str, price: float, day: int) -> bool:
        """Execute a buy order."""
        if self.cash < price:
            raise ValueError(f"Insufficient funds to buy {asset_id}. Need {price}, have {self.cash}")
        
        if asset_id in self.owned_assets:
            raise ValueError(f"Already own {asset_id}")
        
        self.cash -= price
        self.owned_assets.add(asset_id)
        
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
        
        self.cash += price
        self.owned_assets.remove(asset_id)
        
        trade = Trade(TradeAction.SELL, asset_id, day, price)
        self.trade_history.append(trade)
        
        # Record for output format
        if day not in self.daily_trades:
            self.daily_trades[day] = []
        self.daily_trades[day].append({"sell": asset_id})
        
        return True
    
    def get_portfolio_value(self, day_100_valuations: Dict[str, float]) -> float:
        """Calculate total portfolio value on day 100."""
        asset_value = sum(day_100_valuations.get(asset_id, 0) for asset_id in self.owned_assets)
        return self.cash + asset_value
    
    def get_trading_summary(self) -> Dict:
        """Get summary of trading activity."""
        buy_trades = [t for t in self.trade_history if t.action == TradeAction.BUY]
        sell_trades = [t for t in self.trade_history if t.action == TradeAction.SELL]
        
        return {
            "initial_cash": self.initial_cash,
            "current_cash": self.cash,
            "total_buys": len(buy_trades),
            "total_sells": len(sell_trades),
            "cash_spent": sum(t.price for t in buy_trades),
            "cash_gained": sum(t.price for t in sell_trades),
            "owned_assets": list(self.owned_assets),
            "net_cash_flow": sum(t.price for t in sell_trades) - sum(t.price for t in buy_trades)
        }
    
    def get_daily_trades_output(self) -> Dict[int, List[Dict[str, str]]]:
        """Get trades in the required output format."""
        return self.daily_trades
    
    def reset(self):
        """Reset portfolio to initial state."""
        self.cash = self.initial_cash
        self.owned_assets.clear()
        self.trade_history.clear()
        self.daily_trades.clear()