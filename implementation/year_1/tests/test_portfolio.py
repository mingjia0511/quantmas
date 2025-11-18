"""Tests for Portfolio class."""

import pytest
from src.portfolio import Portfolio


class TestPortfolio:
    """Test cases for Portfolio class."""
    
    def test_initial_state(self):
        """Test portfolio initialization."""
        portfolio = Portfolio(starting_cash=1_000_000)
        assert portfolio.cash == 1_000_000
        assert len(portfolio.owned_assets) == 0
        assert len(portfolio.transactions) == 0
    
    def test_can_buy_with_sufficient_cash(self):
        """Test buying with sufficient cash."""
        portfolio = Portfolio(starting_cash=500_000)
        assert portfolio.can_buy("asset_1", 300_000, 1, 1) is True
    
    def test_cannot_buy_with_insufficient_cash(self):
        """Test buying with insufficient cash."""
        portfolio = Portfolio(starting_cash=100_000)
        assert portfolio.can_buy("asset_1", 300_000, 1, 1) is False
    
    def test_cannot_buy_already_owned(self):
        """Test cannot buy asset already owned."""
        portfolio = Portfolio(starting_cash=1_000_000)
        portfolio.owned_assets.add("asset_1")
        assert portfolio.can_buy("asset_1", 300_000, 1, 1) is False
    
    def test_cannot_buy_before_available(self):
        """Test cannot buy before availability date."""
        portfolio = Portfolio(starting_cash=1_000_000)
        assert portfolio.can_buy("asset_1", 300_000, 10, 5) is False
    
    def test_buy_asset(self):
        """Test buying an asset."""
        portfolio = Portfolio(starting_cash=1_000_000)
        portfolio.buy("asset_1", 300_000, 1)
        
        assert portfolio.cash == 700_000
        assert "asset_1" in portfolio.owned_assets
        assert 1 in portfolio.transactions
        assert portfolio.transactions[1] == [{'buy': 'asset_1'}]
    
    def test_can_sell_owned_asset(self):
        """Test selling owned asset."""
        portfolio = Portfolio()
        portfolio.owned_assets.add("asset_1")
        assert portfolio.can_sell("asset_1") is True
    
    def test_cannot_sell_unowned_asset(self):
        """Test cannot sell unowned asset."""
        portfolio = Portfolio()
        assert portfolio.can_sell("asset_1") is False
    
    def test_sell_asset(self):
        """Test selling an asset."""
        portfolio = Portfolio(starting_cash=700_000)
        portfolio.owned_assets.add("asset_1")
        portfolio.sell("asset_1", 350_000, 5)
        
        assert portfolio.cash == 1_050_000
        assert "asset_1" not in portfolio.owned_assets
        assert 5 in portfolio.transactions
        assert portfolio.transactions[5] == [{'sell': 'asset_1'}]
    
    def test_calculate_final_value(self):
        """Test final portfolio value calculation."""
        portfolio = Portfolio(starting_cash=200_000)
        portfolio.owned_assets.add("asset_1")
        portfolio.owned_assets.add("asset_2")
        
        valuations = {
            "asset_1": {100: 325_000},
            "asset_2": {100: 564_000}
        }
        
        final_value = portfolio.calculate_final_value(valuations)
        assert final_value == 1_089_000  # 200k + 325k + 564k
    
    def test_multiple_transactions_same_day(self):
        """Test multiple transactions on same day."""
        portfolio = Portfolio(starting_cash=1_000_000)
        portfolio.buy("asset_1", 300_000, 1)
        portfolio.buy("asset_2", 200_000, 1)
        
        assert len(portfolio.transactions[1]) == 2
        assert portfolio.cash == 500_000
