"""
Test suite for the portfolio_tracker module.
"""
import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from portfolio_tracker import PortfolioTracker, TradeAction, Trade


class TestPortfolioTracker:
    """Test cases for PortfolioTracker class."""
    
    def test_init_default(self):
        """Test PortfolioTracker initialization with default values."""
        portfolio = PortfolioTracker()
        assert portfolio.initial_cash == 1_000_000
        assert portfolio.cash == 1_000_000
        assert len(portfolio.owned_assets) == 0
        assert len(portfolio.trade_history) == 0
        assert len(portfolio.daily_trades) == 0
    
    def test_init_custom(self):
        """Test PortfolioTracker initialization with custom initial cash."""
        portfolio = PortfolioTracker(initial_cash=500_000)
        assert portfolio.initial_cash == 500_000
        assert portfolio.cash == 500_000
    
    def test_can_buy_success(self):
        """Test can_buy returns True when all conditions are met."""
        portfolio = PortfolioTracker()
        result = portfolio.can_buy("asset_1", 100_000, 1, 5)
        assert result is True
    
    def test_can_buy_insufficient_funds(self):
        """Test can_buy returns False when insufficient funds."""
        portfolio = PortfolioTracker(initial_cash=50_000)
        result = portfolio.can_buy("asset_1", 100_000, 1, 5)
        assert result is False
    
    def test_can_buy_not_available(self):
        """Test can_buy returns False when asset not yet available."""
        portfolio = PortfolioTracker()
        result = portfolio.can_buy("asset_1", 100_000, 10, 5)
        assert result is False
    
    def test_can_buy_already_owned(self):
        """Test can_buy returns False when asset already owned."""
        portfolio = PortfolioTracker()
        portfolio.owned_assets.add("asset_1")
        result = portfolio.can_buy("asset_1", 100_000, 1, 5)
        assert result is False
    
    def test_can_sell_success(self):
        """Test can_sell returns True when asset is owned."""
        portfolio = PortfolioTracker()
        portfolio.owned_assets.add("asset_1")
        result = portfolio.can_sell("asset_1")
        assert result is True
    
    def test_can_sell_not_owned(self):
        """Test can_sell returns False when asset not owned."""
        portfolio = PortfolioTracker()
        result = portfolio.can_sell("asset_1")
        assert result is False
    
    def test_buy_asset_success(self):
        """Test successful asset purchase."""
        portfolio = PortfolioTracker()
        initial_cash = portfolio.cash
        price = 100_000
        
        result = portfolio.buy_asset("asset_1", price, 1)
        
        assert result is True
        assert portfolio.cash == initial_cash - price
        assert "asset_1" in portfolio.owned_assets
        assert len(portfolio.trade_history) == 1
        assert portfolio.trade_history[0].action == TradeAction.BUY
        assert portfolio.trade_history[0].asset_id == "asset_1"
        assert portfolio.trade_history[0].price == price
        assert 1 in portfolio.daily_trades
        assert portfolio.daily_trades[1] == [{"buy": "asset_1"}]
    
    def test_buy_asset_insufficient_funds(self):
        """Test asset purchase with insufficient funds."""
        portfolio = PortfolioTracker(initial_cash=50_000)
        
        with pytest.raises(ValueError, match="Insufficient funds"):
            portfolio.buy_asset("asset_1", 100_000, 1)
    
    def test_buy_asset_already_owned(self):
        """Test asset purchase when already owned."""
        portfolio = PortfolioTracker()
        portfolio.owned_assets.add("asset_1")
        
        with pytest.raises(ValueError, match="Already own"):
            portfolio.buy_asset("asset_1", 100_000, 1)
    
    def test_sell_asset_success(self):
        """Test successful asset sale."""
        portfolio = PortfolioTracker()
        portfolio.owned_assets.add("asset_1")
        initial_cash = portfolio.cash
        price = 100_000
        
        result = portfolio.sell_asset("asset_1", price, 1)
        
        assert result is True
        assert portfolio.cash == initial_cash + price
        assert "asset_1" not in portfolio.owned_assets
        assert len(portfolio.trade_history) == 1
        assert portfolio.trade_history[0].action == TradeAction.SELL
        assert portfolio.trade_history[0].asset_id == "asset_1"
        assert portfolio.trade_history[0].price == price
        assert 1 in portfolio.daily_trades
        assert portfolio.daily_trades[1] == [{"sell": "asset_1"}]
    
    def test_sell_asset_not_owned(self):
        """Test asset sale when not owned."""
        portfolio = PortfolioTracker()
        
        with pytest.raises(ValueError, match="Don't own"):
            portfolio.sell_asset("asset_1", 100_000, 1)
    
    def test_get_portfolio_value(self):
        """Test portfolio value calculation."""
        portfolio = PortfolioTracker()
        portfolio.cash = 500_000
        portfolio.owned_assets = {"asset_1", "asset_2"}
        
        day_100_valuations = {"asset_1": 200_000, "asset_2": 300_000}
        
        total_value = portfolio.get_portfolio_value(day_100_valuations)
        assert total_value == 1_000_000  # 500k cash + 200k + 300k
    
    def test_get_portfolio_value_missing_asset(self):
        """Test portfolio value calculation with missing asset valuation."""
        portfolio = PortfolioTracker()
        portfolio.cash = 500_000
        portfolio.owned_assets = {"asset_1", "asset_2"}
        
        day_100_valuations = {"asset_1": 200_000}  # asset_2 missing
        
        total_value = portfolio.get_portfolio_value(day_100_valuations)
        assert total_value == 700_000  # 500k cash + 200k + 0 for missing
    
    def test_get_trading_summary(self):
        """Test trading summary generation."""
        portfolio = PortfolioTracker()
        
        # Perform some trades
        portfolio.buy_asset("asset_1", 100_000, 1)
        portfolio.buy_asset("asset_2", 200_000, 2)
        portfolio.sell_asset("asset_1", 150_000, 3)
        
        summary = portfolio.get_trading_summary()
        
        assert summary['initial_cash'] == 1_000_000
        assert summary['current_cash'] == 850_000  # 1M - 100k - 200k + 150k
        assert summary['total_buys'] == 2
        assert summary['total_sells'] == 1
        assert summary['cash_spent'] == 300_000
        assert summary['cash_gained'] == 150_000
        assert set(summary['owned_assets']) == {"asset_2"}
        assert summary['net_cash_flow'] == -150_000
    
    def test_multiple_trades_same_day(self):
        """Test multiple trades on the same day."""
        portfolio = PortfolioTracker()
        
        portfolio.buy_asset("asset_1", 100_000, 1)
        portfolio.buy_asset("asset_2", 200_000, 1)
        
        assert len(portfolio.daily_trades[1]) == 2
        assert {"buy": "asset_1"} in portfolio.daily_trades[1]
        assert {"buy": "asset_2"} in portfolio.daily_trades[1]
    
    def test_reset(self):
        """Test portfolio reset functionality."""
        portfolio = PortfolioTracker()
        
        # Perform some trades
        portfolio.buy_asset("asset_1", 100_000, 1)
        portfolio.owned_assets.add("asset_2")
        
        # Reset
        portfolio.reset()
        
        assert portfolio.cash == portfolio.initial_cash
        assert len(portfolio.owned_assets) == 0
        assert len(portfolio.trade_history) == 0
        assert len(portfolio.daily_trades) == 0


class TestTrade:
    """Test cases for Trade dataclass."""
    
    def test_trade_creation(self):
        """Test Trade dataclass creation."""
        trade = Trade(TradeAction.BUY, "asset_1", 1, 100_000)
        
        assert trade.action == TradeAction.BUY
        assert trade.asset_id == "asset_1"
        assert trade.day == 1
        assert trade.price == 100_000


class TestTradeAction:
    """Test cases for TradeAction enum."""
    
    def test_trade_action_values(self):
        """Test TradeAction enum values."""
        assert TradeAction.BUY.value == "buy"
        assert TradeAction.SELL.value == "sell"