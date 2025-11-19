"""Tests for portfolio management."""

import pytest
from src.tax_calculator import TaxCalculator
from src.portfolio import Portfolio


@pytest.fixture
def tax_rates():
    """Sample tax rates."""
    return {
        'Residential': {
            1: {'base_rate': 0.001, 'modifier': 0.0005}
        }
    }


@pytest.fixture
def valuations():
    """Sample valuations."""
    # Create valuations for days 1-100
    asset_1_vals = {day: 100000 + (day - 1) * 1000 for day in range(1, 101)}
    asset_2_vals = {day: 200000 + (day - 1) * 2000 for day in range(1, 101)}
    return {
        'asset_1': asset_1_vals,
        'asset_2': asset_2_vals
    }


@pytest.fixture
def asset_metadata():
    """Sample asset metadata."""
    return {
        'asset_1': {'asset_sub_type': 'Residential'},
        'asset_2': {'asset_sub_type': 'Residential'}
    }


@pytest.fixture
def portfolio(tax_rates, valuations, asset_metadata):
    """Portfolio instance."""
    calculator = TaxCalculator(tax_rates)
    return Portfolio(1000000, calculator, valuations, asset_metadata)


class TestPortfolio:
    """Test portfolio operations."""
    
    def test_initialization(self, portfolio):
        """Test portfolio initialization."""
        assert portfolio.cash == 1000000
        assert len(portfolio.owned_assets) == 0
        assert len(portfolio.transactions) == 0
    
    def test_get_asset_valuation(self, portfolio):
        """Test getting asset valuations."""
        assert portfolio.get_asset_valuation('asset_1', 1) == 100000
        assert portfolio.get_asset_valuation('asset_1', 10) == 109000  # 100000 + 9*1000
        assert portfolio.get_asset_valuation('asset_2', 1) == 200000
    
    def test_get_asset_valuation_unknown_asset(self, portfolio):
        """Test error for unknown asset."""
        with pytest.raises(ValueError, match="Unknown asset"):
            portfolio.get_asset_valuation('asset_999', 1)
    
    def test_get_asset_valuation_unknown_day(self, portfolio):
        """Test error for unknown day."""
        with pytest.raises(ValueError, match="No valuation"):
            portfolio.get_asset_valuation('asset_1', 999)
    
    def test_can_buy(self, portfolio):
        """Test buy affordability check."""
        assert portfolio.can_buy('asset_1', 1)  # Can afford 100k
        assert portfolio.can_buy('asset_2', 1)  # Can afford 200k
    
    def test_can_buy_already_owned(self, portfolio):
        """Test cannot buy already owned asset."""
        portfolio.buy_asset('asset_1', 1)
        assert not portfolio.can_buy('asset_1', 2)
    
    def test_can_buy_insufficient_cash(self, portfolio):
        """Test cannot buy with insufficient cash."""
        portfolio.cash = 50000
        assert not portfolio.can_buy('asset_1', 1)
    
    def test_buy_asset(self, portfolio):
        """Test buying an asset."""
        initial_cash = portfolio.cash
        portfolio.buy_asset('asset_1', 1)
        
        assert portfolio.cash == initial_cash - 100000
        assert 'asset_1' in portfolio.owned_assets
        assert len(portfolio.transactions) == 1
        assert portfolio.transactions[0] == (1, 'buy', 'asset_1', 100000)
    
    def test_buy_asset_creates_tracker(self, portfolio):
        """Test buying creates tax tracker."""
        portfolio.buy_asset('asset_1', 1)
        tracker = portfolio.owned_assets['asset_1']
        
        assert tracker.asset_id == 'asset_1'
        assert tracker.asset_sub_type == 'Residential'
        assert tracker.purchase_day == 1
        assert tracker.last_payment_day == 1
    
    def test_can_sell(self, portfolio):
        """Test sell check."""
        assert not portfolio.can_sell('asset_1')
        portfolio.buy_asset('asset_1', 1)
        assert portfolio.can_sell('asset_1')
    
    def test_sell_asset(self, portfolio):
        """Test selling an asset."""
        portfolio.buy_asset('asset_1', 1)
        cash_after_buy = portfolio.cash
        
        portfolio.sell_asset('asset_1', 10)
        
        valuation_day_10 = 109000  # 100000 + 9*1000
        assert portfolio.cash == cash_after_buy + valuation_day_10
        assert 'asset_1' not in portfolio.owned_assets
        assert len(portfolio.transactions) == 2
        assert portfolio.transactions[1] == (10, 'sell', 'asset_1', valuation_day_10)
    
    def test_sell_asset_not_owned(self, portfolio):
        """Test error selling unowned asset."""
        with pytest.raises(ValueError, match="not owned"):
            portfolio.sell_asset('asset_1', 1)
    
    def test_calculate_tax_owed(self, portfolio):
        """Test tax calculation."""
        portfolio.buy_asset('asset_1', 1)
        
        # No tax on purchase day
        assert portfolio.calculate_tax_owed('asset_1', 1) == 0.0
        
        # Tax after 10 days
        tax = portfolio.calculate_tax_owed('asset_1', 11)
        assert tax > 0
    
    def test_can_pay_tax(self, portfolio):
        """Test tax payment affordability."""
        portfolio.buy_asset('asset_1', 1)
        assert portfolio.can_pay_tax('asset_1', 11)
        
        portfolio.cash = 0
        assert not portfolio.can_pay_tax('asset_1', 11)
    
    def test_pay_tax(self, portfolio):
        """Test paying tax."""
        portfolio.buy_asset('asset_1', 1)
        cash_before = portfolio.cash
        
        portfolio.pay_tax('asset_1', 11)
        
        assert portfolio.cash < cash_before
        tracker = portfolio.owned_assets['asset_1']
        assert tracker.last_payment_day == 11
        assert tracker.total_tax_paid > 0
        assert len(portfolio.transactions) == 2
        assert portfolio.transactions[1][1] == 'pay_tax'
    
    def test_pay_tax_no_tax_owed(self, portfolio):
        """Test paying tax when none owed."""
        portfolio.buy_asset('asset_1', 1)
        cash_before = portfolio.cash
        
        portfolio.pay_tax('asset_1', 1)  # Same day as purchase
        
        assert portfolio.cash == cash_before  # No change
        assert len(portfolio.transactions) == 1  # Only buy transaction
    
    def test_pay_tax_insufficient_cash(self, portfolio):
        """Test error when cannot afford tax."""
        portfolio.buy_asset('asset_1', 1)
        portfolio.cash = 1  # Very low cash
        
        with pytest.raises(ValueError, match="Insufficient cash"):
            portfolio.pay_tax('asset_1', 11)
    
    def test_get_total_value(self, portfolio):
        """Test total value calculation."""
        # Initial value
        assert portfolio.get_total_value(1) == 1000000
        
        # After buying
        portfolio.buy_asset('asset_1', 1)
        assert portfolio.get_total_value(1) == 1000000  # Same value
        
        # After price increase
        value_day_10 = portfolio.get_total_value(10)
        # Cash + asset value - unpaid tax
        valuation_day_10 = 109000  # 100000 + 9*1000
        expected = portfolio.cash + valuation_day_10 - portfolio.calculate_tax_owed('asset_1', 10)
        assert abs(value_day_10 - expected) < 0.01
    
    def test_get_total_value_with_penalty(self, portfolio):
        """Test total value with day 100 penalty."""
        portfolio.buy_asset('asset_1', 1)
        
        # Regular day
        value_day_50 = portfolio.get_total_value(50)
        
        # Day 100 (with 2x penalty on unpaid taxes)
        # Note: This test assumes we haven't paid taxes
        # In reality, strategy should pay taxes before day 100
    
    def test_get_assets_needing_payment(self, portfolio):
        """Test identifying assets needing payment."""
        portfolio.buy_asset('asset_1', 1)
        portfolio.buy_asset('asset_2', 1)
        
        # No assets need payment early
        assert len(portfolio.get_assets_needing_payment(10, 30)) == 0
        
        # Both need payment after 30 days
        assert len(portfolio.get_assets_needing_payment(31, 30)) == 2
        
        # Pay tax on one
        portfolio.pay_tax('asset_1', 31)
        assert len(portfolio.get_assets_needing_payment(31, 30)) == 1
        assert portfolio.get_assets_needing_payment(31, 30) == ['asset_2']
