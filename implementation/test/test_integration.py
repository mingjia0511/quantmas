"""
Integration tests for the main trading simulation.
"""
import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from data_loader import DataLoader
from portfolio_tracker import PortfolioTracker
from trading_strategy import TradingStrategy


@pytest.fixture
def sample_market_data():
    """Create sample market data for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create assets.csv with diverse assets
        assets_data = """id,name,type,sub_type,available_on_day,region
asset_1,Good Residential,Real Estate,Residential,1,Region1
asset_2,Poor Commercial,Real Estate,Commercial,1,Region2
asset_3,Late Residential,Real Estate,Residential,50,Region1"""
        
        assets_path = Path(tmpdir) / "assets.csv"
        with open(assets_path, 'w') as f:
            f.write(assets_data)
        
        # Create valuations.csv with realistic price movements
        valuations_data = []
        valuations_data.append("asset_id,day,valuation")
        
        # Asset 1: Good performing residential (starts 100k, ends 150k)
        for day in range(1, 101):
            price = 100000 + (day - 1) * 500  # Linear increase
            valuations_data.append(f"asset_1,{day},{price}")
        
        # Asset 2: Poor performing commercial (starts 200k, ends 150k)
        for day in range(1, 101):
            price = 200000 - (day - 1) * 500  # Linear decrease
            valuations_data.append(f"asset_2,{day},{price}")
        
        # Asset 3: Late but good residential (starts 150k at day 50, ends 200k)
        for day in range(1, 101):
            if day < 50:
                price = 150000  # Not available but price exists
            else:
                price = 150000 + (day - 50) * 1000  # Strong growth
            valuations_data.append(f"asset_3,{day},{price}")
        
        valuations_path = Path(tmpdir) / "valuations.csv"
        with open(valuations_path, 'w') as f:
            f.write('\n'.join(valuations_data))
        
        yield tmpdir


class TestTradingIntegration:
    """Integration tests for the complete trading system."""
    
    def test_basic_trading_simulation(self, sample_market_data):
        """Test a basic trading simulation runs without errors."""
        data_loader = DataLoader(sample_market_data)
        portfolio = PortfolioTracker(initial_cash=1_000_000)
        
        data_loader.load_data()
        strategy = TradingStrategy(data_loader, portfolio)
        
        # Run simulation for first 10 days
        for day in range(1, 11):
            decisions = strategy.make_trading_decisions(day)
            assert isinstance(decisions, list)
        
        # Verify portfolio state is reasonable
        summary = portfolio.get_trading_summary()
        assert summary['current_cash'] >= 0
        assert summary['total_buys'] >= 0
        assert summary['total_sells'] >= 0
    
    def test_asset_ranking_logic(self, sample_market_data):
        """Test that asset ranking produces sensible results."""
        data_loader = DataLoader(sample_market_data)
        portfolio = PortfolioTracker()
        
        data_loader.load_data()
        strategy = TradingStrategy(data_loader, portfolio)
        
        rankings = strategy.get_asset_rankings()
        
        # Asset 1 (good residential) should rank higher than Asset 2 (poor commercial)
        assert rankings['asset_1']['score'] > rankings['asset_2']['score']
        
        # All assets should have calculated metrics
        for asset_id in ['asset_1', 'asset_2', 'asset_3']:
            assert 'score' in rankings[asset_id]
            assert 'total_return' in rankings[asset_id]
            assert 'max_gain_potential' in rankings[asset_id]
    
    def test_trading_constraints_respected(self, sample_market_data):
        """Test that all trading constraints are respected."""
        data_loader = DataLoader(sample_market_data)
        portfolio = PortfolioTracker(initial_cash=300_000)  # Limited cash
        
        data_loader.load_data()
        strategy = TradingStrategy(data_loader, portfolio)
        
        # Run simulation
        for day in range(1, 101):
            strategy.make_trading_decisions(day)
            
            # Check constraints after each day
            assert portfolio.cash >= 0, f"Negative cash on day {day}"
            
            # Verify all owned assets are available for the current day
            for asset_id in portfolio.owned_assets:
                asset_info = data_loader.get_asset_info(asset_id)
                assert asset_info['available_on_day'] <= day, f"Own unavailable asset {asset_id} on day {day}"
    
    def test_portfolio_value_calculation(self, sample_market_data):
        """Test portfolio value calculation accuracy."""
        data_loader = DataLoader(sample_market_data)
        portfolio = PortfolioTracker()
        
        data_loader.load_data()
        
        # Manually buy some assets
        portfolio.buy_asset("asset_1", 100_000, 1)
        portfolio.buy_asset("asset_2", 200_000, 1)
        
        # Calculate portfolio value at day 100
        day_100_valuations = data_loader.get_daily_valuations(100)
        final_value = portfolio.get_portfolio_value(day_100_valuations)
        
        # Expected: remaining cash + asset values
        expected_cash = 1_000_000 - 100_000 - 200_000  # 700k
        expected_asset_value = day_100_valuations['asset_1'] + day_100_valuations['asset_2']
        expected_total = expected_cash + expected_asset_value
        
        assert final_value == expected_total
    
    def test_yaml_output_format(self, sample_market_data):
        """Test that the output format matches requirements."""
        data_loader = DataLoader(sample_market_data)
        portfolio = PortfolioTracker()
        
        data_loader.load_data()
        
        # Manually perform some trades
        portfolio.buy_asset("asset_1", 100_000, 1)
        portfolio.sell_asset("asset_1", 110_000, 5)
        portfolio.buy_asset("asset_2", 200_000, 10)
        
        output = portfolio.get_daily_trades_output()
        
        # Verify structure
        assert isinstance(output, dict)
        assert 1 in output
        assert 5 in output
        assert 10 in output
        
        # Verify day 1 trades
        assert len(output[1]) == 1
        assert output[1][0] == {"buy": "asset_1"}
        
        # Verify day 5 trades
        assert len(output[5]) == 1
        assert output[5][0] == {"sell": "asset_1"}
        
        # Verify day 10 trades
        assert len(output[10]) == 1
        assert output[10][0] == {"buy": "asset_2"}
    
    def test_late_asset_availability(self, sample_market_data):
        """Test that late-available assets are handled correctly."""
        data_loader = DataLoader(sample_market_data)
        portfolio = PortfolioTracker()
        
        data_loader.load_data()
        strategy = TradingStrategy(data_loader, portfolio)
        
        # asset_3 is not available until day 50
        # Run simulation for days 1-49
        for day in range(1, 50):
            strategy.make_trading_decisions(day)
            assert "asset_3" not in portfolio.owned_assets, f"Owned asset_3 before availability on day {day}"
        
        # asset_3 should be available from day 50
        available_day_50 = data_loader.get_available_assets(50)
        assert "asset_3" in available_day_50


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_insufficient_cash_scenario(self):
        """Test behavior when portfolio runs out of cash."""
        portfolio = PortfolioTracker(initial_cash=100)  # Very limited cash
        
        # Should not be able to buy expensive assets
        can_buy = portfolio.can_buy("asset_1", 1000, 1, 1)
        assert can_buy is False
        
        with pytest.raises(ValueError):
            portfolio.buy_asset("asset_1", 1000, 1)
    
    def test_empty_portfolio_value(self):
        """Test portfolio value calculation with no assets."""
        portfolio = PortfolioTracker()
        
        final_value = portfolio.get_portfolio_value({})
        assert final_value == portfolio.initial_cash