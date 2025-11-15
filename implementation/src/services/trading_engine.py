"""Trading engine for portfolio management."""
from typing import Dict


class InsufficientFundsError(Exception):
    """Raised when attempting to buy without enough cash."""

    pass


class AssetAlreadyOwnedError(Exception):
    """Raised when attempting to buy an asset already owned."""

    pass


class AssetNotOwnedError(Exception):
    """Raised when attempting to sell an asset not owned."""

    pass


class TradingEngine:
    """Manages portfolio trading operations."""

    def __init__(self, initial_cash: float):
        """Initialize trading engine.

        Args:
            initial_cash: Starting cash amount in FSB
        """
        self._cash = initial_cash
        self._holdings: Dict[str, int] = {}

    @property
    def cash(self) -> float:
        """Current available cash."""
        return self._cash

    @property
    def holdings(self) -> Dict[str, int]:
        """Current asset holdings (read-only copy)."""
        return self._holdings.copy()

    def buy_asset(self, asset_id: str, price: float, day: int) -> None:
        """Purchase an asset.

        Args:
            asset_id: Asset to purchase
            price: Purchase price in FSB
            day: Trading day (1-100)

        Raises:
            InsufficientFundsError: If cash < price
            AssetAlreadyOwnedError: If asset already owned
        """
        if asset_id in self._holdings:
            raise AssetAlreadyOwnedError(f"Asset {asset_id} already owned")

        if price > self._cash:
            raise InsufficientFundsError(
                f"Insufficient funds: need {price} FSB, have {self._cash} FSB"
            )

        self._cash -= price
        self._holdings[asset_id] = 1

    def sell_asset(self, asset_id: str, price: float, day: int) -> None:
        """Sell an asset.

        Args:
            asset_id: Asset to sell
            price: Sale price in FSB
            day: Trading day (1-100)

        Raises:
            AssetNotOwnedError: If asset not owned
        """
        if asset_id not in self._holdings:
            raise AssetNotOwnedError(f"Asset {asset_id} not owned")

        self._cash += price
        del self._holdings[asset_id]

    def calculate_total_value(self, valuations: Dict[str, float]) -> float:
        """Calculate total portfolio value.

        Args:
            valuations: Map of asset_id to current valuation

        Returns:
            Total portfolio value (cash + asset values)
        """
        asset_value = sum(valuations[asset_id] for asset_id in self._holdings)
        return self._cash + asset_value
