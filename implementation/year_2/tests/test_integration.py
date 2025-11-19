"""Integration tests for Year 2 solution."""

import pytest
from pathlib import Path
from src.data_loader import load_assets, load_valuations, load_tax_rates
from src.tax_calculator import TaxCalculator
from src.portfolio import Portfolio
from src.strategy import TaxOptimizedStrategy
from src.output_writer import write_output
import tempfile
import yaml


@pytest.fixture
def data_dir():
    """Get path to test data."""
    return Path(__file__).parent.parent.parent.parent / 'problems' / 'year_2' / 'data'


class TestIntegration:
    """Integration tests using real data."""
    
    def test_load_data(self, data_dir):
        """Test loading all data files."""
        assets = load_assets(data_dir)
        valuations = load_valuations(data_dir)
        tax_rates = load_tax_rates(data_dir)
        
        assert len(assets) > 0
        assert len(valuations) > 0
        assert len(tax_rates) > 0
        
        # Check data structure
        assert 'asset_id' in assets[0]
        assert 'asset_sub_type' in assets[0]
        
        # Check valuations have 100 days
        first_asset = list(valuations.keys())[0]
        assert len(valuations[first_asset]) == 100
        
        # Check tax rates have expected sub-types
        assert 'Residential' in tax_rates
        assert 'Commercial' in tax_rates
        assert 'Industrial' in tax_rates
    
    def test_portfolio_initialization(self, data_dir):
        """Test portfolio can be initialized with real data."""
        assets = load_assets(data_dir)
        valuations = load_valuations(data_dir)
        tax_rates = load_tax_rates(data_dir)
        
        asset_metadata = {asset['asset_id']: asset for asset in assets}
        calculator = TaxCalculator(tax_rates)
        portfolio = Portfolio(1_000_000, calculator, valuations, asset_metadata)
        
        assert portfolio.cash == 1_000_000
        assert len(portfolio.owned_assets) == 0
    
    def test_buy_and_pay_tax(self, data_dir):
        """Test buying asset and paying tax."""
        assets = load_assets(data_dir)
        valuations = load_valuations(data_dir)
        tax_rates = load_tax_rates(data_dir)
        
        asset_metadata = {asset['asset_id']: asset for asset in assets}
        calculator = TaxCalculator(tax_rates)
        portfolio = Portfolio(1_000_000, calculator, valuations, asset_metadata)
        
        # Buy first asset
        asset_id = assets[0]['asset_id']
        portfolio.buy_asset(asset_id, 1)
        
        assert asset_id in portfolio.owned_assets
        assert portfolio.cash < 1_000_000
        
        # Pay tax after 10 days
        tax_owed = portfolio.calculate_tax_owed(asset_id, 11)
        assert tax_owed > 0
        
        cash_before = portfolio.cash
        portfolio.pay_tax(asset_id, 11)
        assert portfolio.cash < cash_before
        assert portfolio.owned_assets[asset_id].last_payment_day == 11
    
    def test_strategy_execution(self, data_dir):
        """Test strategy can execute without errors."""
        assets = load_assets(data_dir)
        valuations = load_valuations(data_dir)
        tax_rates = load_tax_rates(data_dir)
        
        asset_metadata = {asset['asset_id']: asset for asset in assets}
        calculator = TaxCalculator(tax_rates)
        portfolio = Portfolio(1_000_000, calculator, valuations, asset_metadata)
        
        strategy = TaxOptimizedStrategy(portfolio, assets, num_days=100)
        actions = strategy.execute_strategy()
        
        # Check actions were generated
        assert len(actions) > 0
        assert 1 in actions  # Should have day 1 actions
        
        # Check final portfolio state
        final_value = portfolio.get_total_value(100)
        assert final_value > 0  # Should have positive value
    
    def test_output_writing(self, data_dir):
        """Test output file can be written."""
        # Create sample actions
        actions = {
            1: [{'buy': 'asset_1'}, {'buy': 'asset_2'}],
            10: [{'pay_tax': 'asset_1'}],
            20: [{'pay_tax': 'asset_1'}, {'pay_tax': 'asset_2'}]
        }
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            write_output(actions, temp_path)
            
            # Read back and verify
            with open(temp_path, 'r') as f:
                data = yaml.safe_load(f)
            
            assert len(data) == 5  # Total actions
            assert data[0]['day'] == 1
            assert 'buy' in data[0]
            assert data[2]['day'] == 10
            assert 'pay_tax' in data[2]
        finally:
            temp_path.unlink()
    
    def test_tax_calculation_accuracy(self, data_dir):
        """Test tax calculations match expected formula."""
        tax_rates = load_tax_rates(data_dir)
        calculator = TaxCalculator(tax_rates)
        
        # Test Residential tax for 10 days
        # Base rate = 0.001, modifier = 0.0005
        # Day 1: 0.001 + 0.0005*0 = 0.001
        # Day 2: 0.001 + 0.0005*1 = 0.0015
        # ...
        # Day 10: 0.001 + 0.0005*9 = 0.0055
        valuation = 100000
        tax = calculator.calculate_tax('Residential', valuation, 1, 11)
        
        expected = sum(valuation * (0.001 + 0.0005 * i) for i in range(10))
        assert abs(tax - expected) < 0.01
