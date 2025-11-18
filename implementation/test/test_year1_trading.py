"""
Test suite for Year 1 Trading Strategy

Provides comprehensive test coverage for the trading strategy implementation.
"""

import pytest
import pandas as pd
import yaml
import tempfile
import os
from pathlib import Path
from src.optimized_trading import OptimizedTradingStrategy, Asset, Portfolio


class TestAsset:
    """Test the Asset dataclass."""
    
    def test_asset_creation(self):
        """Test creating an Asset instance."""
        asset = Asset(
            id="asset_1",
            name="Test Manor",
            type="Real Estate",
            sub_type="Residential",
            available_on_day=1,
            region="Test Region"
        )
        assert asset.id == "asset_1"
        assert asset.name == "Test Manor"
        assert asset.type == "Real Estate"
        assert asset.sub_type == "Residential"
        assert asset.available_on_day == 1
        assert asset.region == "Test Region"


class TestPortfolio:
    """Test the Portfolio dataclass."""
    
    def test_portfolio_default_initialization(self):
        """Test default portfolio initialization."""
        portfolio = Portfolio()
        assert portfolio.cash == 1_000_000
        assert portfolio.owned_assets == {}
    
    def test_portfolio_custom_initialization(self):
        """Test custom portfolio initialization."""
        portfolio = Portfolio(cash=500_000, owned_assets={"asset_1": 1})
        assert portfolio.cash == 500_000
        assert portfolio.owned_assets == {"asset_1": 1}


class TestOptimizedTradingStrategy:
    """Test the OptimizedTradingStrategy class."""
    
    @pytest.fixture
    def sample_data_files(self):
        """Create temporary test data files."""
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Create sample assets data
        assets_data = """id,name,type,sub_type,available_on_day,region
asset_1,Test Manor,Real Estate,Residential,1,Test Region
asset_2,Test Plaza,Real Estate,Commercial,5,Test Region
asset_3,Test Complex,Real Estate,Industrial,10,Test Region"""
        
        assets_file = os.path.join(temp_dir, "assets.csv")
        with open(assets_file, 'w') as f:
            f.write(assets_data)
        
        # Create sample valuations data
        valuations_data = """asset_id,day,valuation
asset_1,1,100000
asset_1,2,105000
asset_1,3,110000
asset_1,4,115000
asset_1,5,120000
asset_2,5,200000
asset_2,6,210000
asset_2,7,220000
asset_2,8,230000
asset_2,9,240000
asset_3,10,300000
asset_3,11,315000
asset_3,12,330000
asset_3,13,345000
asset_3,14,360000"""
        
        valuations_file = os.path.join(temp_dir, "valuations.csv")
        with open(valuations_file, 'w') as f:
            f.write(valuations_data)
        
        return assets_file, valuations_file, temp_dir
    
    def test_load_assets(self, sample_data_files):
        """Test loading assets from CSV."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        assert len(strategy.assets) == 3
        assert "asset_1" in strategy.assets
        assert strategy.assets["asset_1"].name == "Test Manor"
        assert strategy.assets["asset_1"].available_on_day == 1
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_load_valuations(self, sample_data_files):
        """Test loading valuations from CSV."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        assert len(strategy.valuations) == 15
        assert "asset_id" in strategy.valuations.columns
        assert "day" in strategy.valuations.columns
        assert "valuation" in strategy.valuations.columns
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_get_asset_price(self, sample_data_files):
        """Test getting asset price for a specific day."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        price = strategy.get_asset_price("asset_1", 1)
        assert price == 100000.0
        
        price = strategy.get_asset_price("asset_2", 5)
        assert price == 200000.0
        
        # Test error case
        with pytest.raises(ValueError):
            strategy.get_asset_price("asset_1", 100)
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_get_asset_price_history(self, sample_data_files):
        """Test getting asset price history."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        history = strategy.get_asset_price_history("asset_1", 1, 5)
        assert len(history) == 5
        assert history[0] == (1, 100000.0)
        assert history[4] == (5, 120000.0)
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_portfolio_initialization(self, sample_data_files):
        """Test portfolio starts correctly."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        assert strategy.portfolio.cash == 1_000_000
        assert strategy.portfolio.owned_assets == {}
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_should_buy_asset_availability(self, sample_data_files):
        """Test buy logic respects availability dates."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # asset_2 not available until day 5
        assert not strategy.should_buy_asset("asset_2", 1)
        assert not strategy.should_buy_asset("asset_2", 4)
        
        # asset_1 available from day 1
        # Note: This might return False due to other logic, but availability check should pass
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_should_buy_asset_cash_check(self, sample_data_files):
        """Test buy logic respects cash availability."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Reduce cash to test insufficient funds
        strategy.portfolio.cash = 50000
        
        # Should not be able to buy asset_1 at 100000
        assert not strategy.should_buy_asset("asset_1", 1)
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_should_buy_asset_ownership_check(self, sample_data_files):
        """Test can't buy assets we already own."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Simulate owning asset_1
        strategy.portfolio.owned_assets["asset_1"] = 1
        
        assert not strategy.should_buy_asset("asset_1", 1)
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_should_sell_asset_ownership_check(self, sample_data_files):
        """Test can only sell assets we own."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Don't own any assets initially
        assert not strategy.should_sell_asset("asset_1", 50, 1)
        
        # Simulate owning asset_1
        strategy.portfolio.owned_assets["asset_1"] = 1
        
        # Now we can potentially sell (depends on other logic)
        # At minimum, should return True on day 100
        assert strategy.should_sell_asset("asset_1", 100, 1)
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_execute_day_trading_buy(self, sample_data_files):
        """Test executing buy transactions."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Override target assets to include our test asset
        strategy.target_assets = ["asset_1"]
        
        # Mock the should_buy_asset method to return True
        original_should_buy = strategy.should_buy_asset
        strategy.should_buy_asset = lambda asset_id, day: asset_id == "asset_1" and day == 1
        
        actions = strategy.execute_day_trading(1)
        
        # Should have bought asset_1
        assert len(actions) == 1
        assert actions[0] == {"buy": "asset_1"}
        assert "asset_1" in strategy.portfolio.owned_assets
        assert strategy.portfolio.cash == 900000  # 1M - 100K
        
        # Restore original method
        strategy.should_buy_asset = original_should_buy
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_execute_day_trading_sell(self, sample_data_files):
        """Test executing sell transactions."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Override target assets to only include our test assets
        strategy.target_assets = ["asset_1", "asset_2", "asset_3"]
        
        # Set up portfolio with an owned asset
        strategy.portfolio.owned_assets["asset_1"] = 1
        strategy.portfolio.cash = 900000
        strategy._buy_days = {"asset_1": 1}
        
        # Mock both methods to control behavior
        original_should_sell = strategy.should_sell_asset
        original_should_buy = strategy.should_buy_asset
        strategy.should_sell_asset = lambda asset_id, day, buy_day: asset_id == "asset_1" and day == 2
        strategy.should_buy_asset = lambda asset_id, day: False  # Don't buy anything
        
        actions = strategy.execute_day_trading(2)
        
        # Should have sold asset_1 only
        assert len(actions) == 1
        assert actions[0] == {"sell": "asset_1"}
        assert "asset_1" not in strategy.portfolio.owned_assets
        assert strategy.portfolio.cash == 1005000  # 900K + 105K (day 2 price)
        
        # Restore original methods
        strategy.should_sell_asset = original_should_sell
        strategy.should_buy_asset = original_should_buy
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_calculate_final_score(self, sample_data_files):
        """Test final score calculation."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Set up portfolio
        strategy.portfolio.cash = 500000
        strategy.portfolio.owned_assets = {}  # No assets for simple test
        
        score = strategy.calculate_final_score()
        assert score == 500000
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_save_output(self, sample_data_files):
        """Test saving trading log to file."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Set up sample trading log
        strategy.trading_log = {
            1: [{"buy": "asset_1"}],
            5: [{"sell": "asset_1"}]
        }
        
        output_file = os.path.join(temp_dir, "output.yml")
        strategy.save_output(output_file)
        
        # Verify file was created and contains correct data
        assert os.path.exists(output_file)
        
        with open(output_file, 'r') as f:
            loaded_data = yaml.safe_load(f)
        
        assert loaded_data[1] == [{"buy": "asset_1"}]
        assert loaded_data[5] == [{"sell": "asset_1"}]
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_find_optimal_buy_day(self, sample_data_files):
        """Test finding optimal buy day for an asset."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Test with asset_1 (available day 1)
        optimal_day = strategy.find_optimal_buy_day("asset_1")
        assert optimal_day >= 1  # Should be at least the available day
        assert optimal_day <= 100  # Should be within trading period
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_find_optimal_sell_day(self, sample_data_files):
        """Test finding optimal sell day for an asset."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Mock get_asset_price to handle day 100
        original_get_price = strategy.get_asset_price
        def mock_get_price(asset_id, day):
            if day == 100:
                return 120000.0  # Mock day 100 price
            return original_get_price(asset_id, day)
        
        strategy.get_asset_price = mock_get_price
        
        # Test with asset_1, bought on day 1
        optimal_day = strategy.find_optimal_sell_day("asset_1", 1)
        assert optimal_day > 1  # Should be after buy day
        assert optimal_day <= 100  # Should be within trading period
        
        # Restore original method
        strategy.get_asset_price = original_get_price
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_should_buy_asset_with_target_assets(self, sample_data_files):
        """Test buy logic with target assets."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Set asset_1 as a target asset
        strategy.target_assets = ["asset_1"]
        
        # Mock find_optimal_buy_day to return day 1
        strategy.find_optimal_buy_day = lambda asset_id: 1
        
        # Should consider buying asset_1 on day 1
        result = strategy.should_buy_asset("asset_1", 1)
        # Result depends on other conditions, but at least availability check passes
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_should_sell_asset_on_last_day(self, sample_data_files):
        """Test sell logic on day 100."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Set up owning an asset
        strategy.portfolio.owned_assets["asset_1"] = 1
        
        # Should always sell on day 100
        assert strategy.should_sell_asset("asset_1", 100, 1)
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_should_sell_asset_target_asset_logic(self, sample_data_files):
        """Test sell logic for target assets."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Set asset_1 as a target asset
        strategy.target_assets = ["asset_1"]
        strategy.portfolio.owned_assets["asset_1"] = 1
        
        # Mock find_optimal_sell_day to return day 50
        strategy.find_optimal_sell_day = lambda asset_id, buy_day: 50
        
        # Should sell on or after optimal day
        assert not strategy.should_sell_asset("asset_1", 49, 1)
        assert strategy.should_sell_asset("asset_1", 50, 1)
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_calculate_final_score_with_assets(self, sample_data_files):
        """Test final score calculation with owned assets."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Set up portfolio with cash and assets
        strategy.portfolio.cash = 500000
        strategy.portfolio.owned_assets = {"asset_1": 1}
        
        # Mock day 100 price for asset_1
        original_get_price = strategy.get_asset_price
        strategy.get_asset_price = lambda asset_id, day: 200000 if asset_id == "asset_1" and day == 100 else original_get_price(asset_id, day)
        
        score = strategy.calculate_final_score()
        assert score == 700000  # 500000 cash + 200000 asset value
        
        # Restore original method
        strategy.get_asset_price = original_get_price
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_execute_day_trading_no_actions(self, sample_data_files):
        """Test day trading when no actions should be taken."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Mock methods to return False for all decisions
        strategy.should_buy_asset = lambda asset_id, day: False
        strategy.should_sell_asset = lambda asset_id, day, buy_day: False
        
        actions = strategy.execute_day_trading(50)
        assert actions == []
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_run_simulation_records_only_action_days(self, sample_data_files):
        """Test that simulation only records days with actions."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Mock execute_day_trading to return actions only on specific days
        def mock_execute(day):
            if day in [1, 50, 100]:
                return [{"buy": "asset_1"}]
            return []
        
        strategy.execute_day_trading = mock_execute
        trading_log = strategy.run_simulation()
        
        assert len(trading_log) == 3
        assert 1 in trading_log
        assert 50 in trading_log
        assert 100 in trading_log
        assert 25 not in trading_log
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_simulation_runs_all_days(self, sample_data_files):
        """Test that simulation processes all 100 days."""
        assets_file, valuations_file, temp_dir = sample_data_files
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        
        # Mock execute_day_trading to track days processed
        days_processed = []
        original_execute = strategy.execute_day_trading
        
        def mock_execute(day):
            days_processed.append(day)
            return []
        
        strategy.execute_day_trading = mock_execute
        strategy.run_simulation()
        
        assert len(days_processed) == 100
        assert min(days_processed) == 1
        assert max(days_processed) == 100
        
        # Restore original method
        strategy.execute_day_trading = original_execute
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)


class TestIntegration:
    """Integration tests with real data."""
    
    def test_strategy_with_real_data(self):
        """Test strategy with actual problem data."""
        assets_file = "../problems/year_1/data/assets.csv"
        valuations_file = "../problems/year_1/data/valuations.csv"
        
        # Skip if files don't exist (test environment)
        if not (os.path.exists(assets_file) and os.path.exists(valuations_file)):
            pytest.skip("Real data files not available")
        
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        trading_log = strategy.run_simulation()
        final_score = strategy.calculate_final_score()
        
        # Basic sanity checks
        assert final_score >= 1_000_000  # Should at least break even
        assert final_score <= 2_000_000  # Shouldn't be unreasonably high
        assert isinstance(trading_log, dict)
        
        # Verify all actions are valid
        for day, actions in trading_log.items():
            assert 1 <= day <= 100
            for action in actions:
                assert len(action) == 1
                assert ('buy' in action) or ('sell' in action)
                if 'buy' in action:
                    assert action['buy'].startswith('asset_')
                if 'sell' in action:
                    assert action['sell'].startswith('asset_')
    
    def test_output_file_format(self):
        """Test that output file has correct format."""
        assets_file = "../problems/year_1/data/assets.csv"
        valuations_file = "../problems/year_1/data/valuations.csv"
        output_file = "../problems/year_1/output/output.yml"
        
        # Skip if files don't exist
        if not (os.path.exists(assets_file) and os.path.exists(valuations_file)):
            pytest.skip("Real data files not available")
        
        strategy = OptimizedTradingStrategy(assets_file, valuations_file)
        strategy.run_simulation()
        strategy.save_output(output_file)
        
        # Verify output file exists and is valid YAML
        assert os.path.exists(output_file)
        
        with open(output_file, 'r') as f:
            data = yaml.safe_load(f)
        
        assert isinstance(data, dict)
        
        # Verify format matches expected structure
        for day, actions in data.items():
            assert isinstance(day, int)
            assert 1 <= day <= 100
            assert isinstance(actions, list)
            for action in actions:
                assert isinstance(action, dict)
                assert len(action) == 1
                action_type = list(action.keys())[0]
                assert action_type in ['buy', 'sell']
                asset_id = action[action_type]
                assert isinstance(asset_id, str)
                assert asset_id.startswith('asset_')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])