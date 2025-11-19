"""Tests for tax calculator."""

import pytest
from src.tax_calculator import TaxCalculator, AssetTaxTracker


@pytest.fixture
def tax_rates():
    """Sample tax rates for testing."""
    return {
        'Residential': {
            1: {'base_rate': 0.001, 'modifier': 0.0005},
            25: {'base_rate': 0.0011, 'modifier': 0.00055}
        },
        'Commercial': {
            1: {'base_rate': 0.0015, 'modifier': 0.0007}
        }
    }


@pytest.fixture
def calculator(tax_rates):
    """Tax calculator instance."""
    return TaxCalculator(tax_rates)


class TestTaxCalculator:
    """Test tax calculation logic."""
    
    def test_get_rates_for_day_early(self, calculator):
        """Test getting rates for early days."""
        rates = calculator.get_rates_for_day('Residential', 10)
        assert rates['base_rate'] == 0.001
        assert rates['modifier'] == 0.0005
    
    def test_get_rates_for_day_after_change(self, calculator):
        """Test getting rates after rate change."""
        rates = calculator.get_rates_for_day('Residential', 30)
        assert rates['base_rate'] == 0.0011
        assert rates['modifier'] == 0.00055
    
    def test_get_rates_for_day_on_change_day(self, calculator):
        """Test getting rates on exact change day."""
        rates = calculator.get_rates_for_day('Residential', 25)
        assert rates['base_rate'] == 0.0011
        assert rates['modifier'] == 0.00055
    
    def test_calculate_tax_single_day(self, calculator):
        """Test tax calculation for single day."""
        # Day 1 to day 2: 1 day
        # Rate = 0.001 + 0.0005 * 0 = 0.001
        # Tax = 100000 * 0.001 = 100
        tax = calculator.calculate_tax('Residential', 100000, 1, 2)
        assert abs(tax - 100) < 0.01
    
    def test_calculate_tax_multiple_days(self, calculator):
        """Test tax calculation over multiple days."""
        # Days 1-11: 10 days
        # Day 1: rate = 0.001 + 0.0005*0 = 0.001, tax = 100
        # Day 2: rate = 0.001 + 0.0005*1 = 0.0015, tax = 150
        # Day 3: rate = 0.001 + 0.0005*2 = 0.002, tax = 200
        # ...
        # Day 10: rate = 0.001 + 0.0005*9 = 0.0055, tax = 550
        # Total = 100 + 150 + 200 + ... + 550 = 2750
        tax = calculator.calculate_tax('Residential', 100000, 1, 11)
        expected = sum(100000 * (0.001 + 0.0005 * i) for i in range(10))
        assert abs(tax - expected) < 0.01
    
    def test_calculate_tax_zero_days(self, calculator):
        """Test tax calculation for zero days."""
        tax = calculator.calculate_tax('Residential', 100000, 5, 5)
        assert tax == 0.0
    
    def test_calculate_tax_across_rate_change(self, calculator):
        """Test tax calculation across rate change boundary."""
        # Days 20-30: crosses rate change at day 25
        tax = calculator.calculate_tax('Residential', 100000, 20, 30)
        
        # Days 21-25 use old rates (0.001, 0.0005)
        # Days 26-30 use new rates (0.0011, 0.00055)
        expected = 0
        for day in range(21, 31):
            days_since = day - 20 - 1
            if day < 25:
                rate = 0.001 + 0.0005 * days_since
            else:
                rate = 0.0011 + 0.00055 * days_since
            expected += 100000 * rate
        
        assert abs(tax - expected) < 0.01
    
    def test_unknown_asset_type(self, calculator):
        """Test error handling for unknown asset type."""
        with pytest.raises(ValueError, match="Unknown asset sub-type"):
            calculator.get_rates_for_day('Unknown', 1)


class TestAssetTaxTracker:
    """Test asset tax tracking."""
    
    def test_initialization(self):
        """Test tracker initialization."""
        tracker = AssetTaxTracker('asset_1', 'Residential', 1)
        assert tracker.asset_id == 'asset_1'
        assert tracker.asset_sub_type == 'Residential'
        assert tracker.purchase_day == 1
        assert tracker.last_payment_day == 1
        assert tracker.total_tax_paid == 0.0
    
    def test_days_since_last_payment(self):
        """Test days calculation."""
        tracker = AssetTaxTracker('asset_1', 'Residential', 1)
        assert tracker.days_since_last_payment(1) == 0
        assert tracker.days_since_last_payment(10) == 9
        assert tracker.days_since_last_payment(31) == 30
    
    def test_record_payment(self):
        """Test recording payments."""
        tracker = AssetTaxTracker('asset_1', 'Residential', 1)
        tracker.record_payment(10, 100.0)
        
        assert tracker.last_payment_day == 10
        assert tracker.total_tax_paid == 100.0
        assert len(tracker.payment_history) == 1
        assert tracker.payment_history[0] == (10, 100.0)
    
    def test_multiple_payments(self):
        """Test multiple payments."""
        tracker = AssetTaxTracker('asset_1', 'Residential', 1)
        tracker.record_payment(10, 100.0)
        tracker.record_payment(20, 150.0)
        tracker.record_payment(30, 200.0)
        
        assert tracker.last_payment_day == 30
        assert tracker.total_tax_paid == 450.0
        assert len(tracker.payment_history) == 3
    
    def test_needs_payment(self):
        """Test payment need detection."""
        tracker = AssetTaxTracker('asset_1', 'Residential', 1)
        
        assert not tracker.needs_payment(1, 30)
        assert not tracker.needs_payment(29, 30)
        assert tracker.needs_payment(31, 30)
        assert tracker.needs_payment(50, 30)
    
    def test_needs_payment_after_payment(self):
        """Test payment need after making payment."""
        tracker = AssetTaxTracker('asset_1', 'Residential', 1)
        tracker.record_payment(10, 100.0)
        
        assert not tracker.needs_payment(10, 30)
        assert not tracker.needs_payment(39, 30)
        assert tracker.needs_payment(40, 30)
