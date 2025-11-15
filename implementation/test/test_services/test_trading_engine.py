"""Tests for TradingEngine service."""
import pytest
from src.services.trading_engine import TradingEngine, InsufficientFundsError, AssetAlreadyOwnedError, AssetNotOwnedError


class TestTradingEngine:
    """Test suite for TradingEngine."""

    def test_initial_cash(self) -> None:
        """Should start with correct cash amount."""
        engine = TradingEngine(initial_cash=1000000)
        assert engine.cash == 1000000

    def test_initial_holdings_empty(self) -> None:
        """Should start with no holdings."""
        engine = TradingEngine(initial_cash=1000000)
        assert len(engine.holdings) == 0

    def test_buy_asset_reduces_cash(self) -> None:
        """Should reduce cash by purchase price."""
        engine = TradingEngine(initial_cash=1000000)
        engine.buy_asset("asset_1", price=150000, day=1)
        assert engine.cash == 850000

    def test_buy_asset_adds_to_holdings(self) -> None:
        """Should add asset to holdings."""
        engine = TradingEngine(initial_cash=1000000)
        engine.buy_asset("asset_1", price=150000, day=1)
        assert "asset_1" in engine.holdings
        assert engine.holdings["asset_1"] == 1

    def test_buy_asset_insufficient_funds(self) -> None:
        """Should raise error when insufficient funds."""
        engine = TradingEngine(initial_cash=100000)
        with pytest.raises(InsufficientFundsError):
            engine.buy_asset("asset_1", price=150000, day=1)

    def test_buy_asset_already_owned(self) -> None:
        """Should raise error when trying to buy asset already owned."""
        engine = TradingEngine(initial_cash=1000000)
        engine.buy_asset("asset_1", price=150000, day=1)

        with pytest.raises(AssetAlreadyOwnedError):
            engine.buy_asset("asset_1", price=150000, day=2)

    def test_sell_asset_increases_cash(self) -> None:
        """Should increase cash by sale price."""
        engine = TradingEngine(initial_cash=1000000)
        engine.buy_asset("asset_1", price=150000, day=1)
        engine.sell_asset("asset_1", price=160000, day=2)
        assert engine.cash == 1010000

    def test_sell_asset_removes_from_holdings(self) -> None:
        """Should remove asset from holdings."""
        engine = TradingEngine(initial_cash=1000000)
        engine.buy_asset("asset_1", price=150000, day=1)
        engine.sell_asset("asset_1", price=160000, day=2)
        assert "asset_1" not in engine.holdings

    def test_sell_asset_not_owned(self) -> None:
        """Should raise error when trying to sell asset not owned."""
        engine = TradingEngine(initial_cash=1000000)
        with pytest.raises(AssetNotOwnedError):
            engine.sell_asset("asset_1", price=160000, day=1)

    def test_calculate_total_value(self) -> None:
        """Should calculate total portfolio value correctly."""
        engine = TradingEngine(initial_cash=1000000)
        engine.buy_asset("asset_1", price=150000, day=1)

        valuations = {"asset_1": 160000}
        total = engine.calculate_total_value(valuations)

        assert total == 1010000  # 850000 cash + 160000 asset value

    def test_calculate_total_value_multiple_assets(self) -> None:
        """Should handle multiple assets."""
        engine = TradingEngine(initial_cash=1000000)
        engine.buy_asset("asset_1", price=150000, day=1)
        engine.buy_asset("asset_2", price=300000, day=2)

        valuations = {"asset_1": 160000, "asset_2": 310000}
        total = engine.calculate_total_value(valuations)

        assert total == 1020000  # 550000 cash + 160000 + 310000

    def test_buy_and_rebuy_same_asset(self) -> None:
        """Should allow buying same asset after selling."""
        engine = TradingEngine(initial_cash=1000000)
        engine.buy_asset("asset_1", price=150000, day=1)
        engine.sell_asset("asset_1", price=160000, day=2)
        engine.buy_asset("asset_1", price=155000, day=3)

        assert "asset_1" in engine.holdings
        assert engine.cash == 855000  # 1000000 - 150000 + 160000 - 155000
