"""Tests for BuyAndHoldStrategy."""
import pytest
from src.strategies.buy_and_hold_strategy import BuyAndHoldStrategy, Trade
from src.services.data_loader import DataLoader


class TestBuyAndHoldStrategy:
    """Test suite for BuyAndHoldStrategy."""

    def test_generate_trades_returns_list(self) -> None:
        """Should return list of trades."""
        loader = DataLoader("../problems/year_1/data")
        strategy = BuyAndHoldStrategy(loader, initial_cash=1000000)

        trades = strategy.generate_trades()

        assert isinstance(trades, list)
        assert len(trades) > 0

    def test_all_trades_are_buys(self) -> None:
        """Should only generate buy actions (buy and hold)."""
        loader = DataLoader("../problems/year_1/data")
        strategy = BuyAndHoldStrategy(loader, initial_cash=1000000)

        trades = strategy.generate_trades()

        assert all(trade.action == "buy" for trade in trades)

    def test_trades_have_valid_days(self) -> None:
        """All trades should be within valid day range."""
        loader = DataLoader("../problems/year_1/data")
        strategy = BuyAndHoldStrategy(loader, initial_cash=1000000)

        trades = strategy.generate_trades()

        assert all(1 <= trade.day <= 100 for trade in trades)

    def test_trades_respect_available_on_day(self) -> None:
        """Should not buy assets before their available_on_day."""
        loader = DataLoader("../problems/year_1/data")
        strategy = BuyAndHoldStrategy(loader, initial_cash=1000000)

        trades = strategy.generate_trades()
        assets_df = loader.load_assets()

        for trade in trades:
            asset_info = assets_df[assets_df["id"] == trade.asset_id].iloc[0]
            assert trade.day >= asset_info["available_on_day"]

    def test_trades_respect_budget(self) -> None:
        """Should not exceed available cash."""
        loader = DataLoader("../problems/year_1/data")
        initial_cash = 1000000
        strategy = BuyAndHoldStrategy(loader, initial_cash=initial_cash)

        trades = strategy.generate_trades()

        # Simulate execution to verify budget
        cash = initial_cash
        for trade in trades:
            price = loader.get_valuation_on_day(trade.asset_id, trade.day)
            assert price <= cash, f"Trade on day {trade.day} exceeds budget"
            cash -= price

    def test_no_duplicate_assets(self) -> None:
        """Should not buy the same asset twice."""
        loader = DataLoader("../problems/year_1/data")
        strategy = BuyAndHoldStrategy(loader, initial_cash=1000000)

        trades = strategy.generate_trades()
        asset_ids = [trade.asset_id for trade in trades]

        assert len(asset_ids) == len(set(asset_ids)), "Duplicate assets found"

    def test_trades_sorted_by_day(self) -> None:
        """Trades should be sorted by day."""
        loader = DataLoader("../problems/year_1/data")
        strategy = BuyAndHoldStrategy(loader, initial_cash=1000000)

        trades = strategy.generate_trades()
        days = [trade.day for trade in trades]

        assert days == sorted(days), "Trades not sorted by day"
