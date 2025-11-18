"""Tests for TradingStrategy class."""

import pytest
from src.strategy import TradingStrategy


class TestTradingStrategy:
    """Test cases for TradingStrategy class."""
    
    @pytest.fixture
    def sample_assets(self):
        """Create sample asset data."""
        return {
            "asset_1": {
                "name": "Test Asset 1",
                "type": "Real Estate",
                "sub_type": "Residential",
                "available_on_day": 1,
                "region": "Frostpeak"
            },
            "asset_2": {
                "name": "Test Asset 2",
                "type": "Real Estate",
                "sub_type": "Commercial",
                "available_on_day": 10,
                "region": "Tinseltown"
            }
        }
    
    @pytest.fixture
    def sample_valuations(self):
        """Create sample valuation data."""
        return {
            "asset_1": {day: 100_000 + (day * 1_000) for day in range(1, 101)},
            "asset_2": {day: 200_000 - (day * 500) for day in range(1, 101)}
        }
    
    def test_calculate_future_return_positive(self, sample_assets, sample_valuations):
        """Test calculating positive future return."""
        strategy = TradingStrategy(sample_assets, sample_valuations)
        
        # asset_1 goes from 101k to 200k
        return_pct = strategy.calculate_future_return("asset_1", 1)
        assert return_pct > 0
        assert abs(return_pct - 0.98) < 0.01  # ~98% return
    
    def test_calculate_future_return_negative(self, sample_assets, sample_valuations):
        """Test calculating negative future return."""
        strategy = TradingStrategy(sample_assets, sample_valuations)
        
        # asset_2 goes from 199.5k to 150k
        return_pct = strategy.calculate_future_return("asset_2", 1)
        assert return_pct < 0
    
    def test_find_best_opportunities(self, sample_assets, sample_valuations):
        """Test finding best investment opportunities."""
        strategy = TradingStrategy(sample_assets, sample_valuations)
        
        opportunities = strategy.find_best_opportunities(1)
        
        # Only asset_1 should be available and profitable on day 1
        assert len(opportunities) == 1
        assert opportunities[0][0] == "asset_1"
        assert opportunities[0][1] > 0
    
    def test_find_opportunities_respects_availability(self, sample_assets, sample_valuations):
        """Test that opportunities respect availability dates."""
        strategy = TradingStrategy(sample_assets, sample_valuations)
        
        # On day 5, asset_2 is not yet available
        opportunities = strategy.find_best_opportunities(5)
        asset_ids = [opp[0] for opp in opportunities]
        assert "asset_2" not in asset_ids
        
        # On day 10, asset_2 becomes available
        opportunities = strategy.find_best_opportunities(10)
        asset_ids = [opp[0] for opp in opportunities]
        # asset_2 has negative return, so won't be in opportunities
        assert "asset_1" in asset_ids
    
    def test_should_sell_when_price_drops(self, sample_assets, sample_valuations):
        """Test selling when price will drop."""
        strategy = TradingStrategy(sample_assets, sample_valuations)
        
        # asset_2 price drops every day
        assert strategy.should_sell("asset_2", 50) is True
    
    def test_should_not_sell_when_price_rises(self, sample_assets, sample_valuations):
        """Test not selling when price will rise."""
        strategy = TradingStrategy(sample_assets, sample_valuations)
        
        # asset_1 price rises every day
        assert strategy.should_sell("asset_1", 50) is False
    
    def test_execute_strategy_basic(self, sample_assets, sample_valuations):
        """Test basic strategy execution."""
        strategy = TradingStrategy(sample_assets, sample_valuations)
        portfolio = strategy.execute_strategy()
        
        # Should have made some transactions
        assert len(portfolio.transactions) > 0
        
        # Should have positive final value
        final_value = portfolio.calculate_final_value(sample_valuations)
        assert final_value > 0
