"""Buy and hold trading strategy."""
from dataclasses import dataclass
from typing import List
from src.services.data_loader import DataLoader


@dataclass
class Trade:
    """Represents a trading action.

    Attributes:
        day: Trading day (1-100)
        action: Either 'buy' or 'sell'
        asset_id: Asset identifier
    """

    day: int
    action: str
    asset_id: str


class BuyAndHoldStrategy:
    """Implements a buy-and-hold strategy for profitable assets."""

    def __init__(self, data_loader: DataLoader, initial_cash: float):
        """Initialize strategy.

        Args:
            data_loader: Data loader for market data
            initial_cash: Starting cash amount in FSB
        """
        self._loader = data_loader
        self._initial_cash = initial_cash

    def generate_trades(self) -> List[Trade]:
        """Generate trading strategy.

        Strategy:
        - Identify top performing assets (by day 1 to day 100 return)
        - Buy them as they become available
        - Hold until day 100

        Returns:
            List of trades sorted by day

        Note:
            Assumes all assets have valuations for days 1 and 100.
            Assets without complete data are skipped with a warning.
        """
        assets_df = self._loader.load_assets()
        valuations_df = self._loader.load_valuations()

        # Calculate returns for each asset
        asset_returns = []
        for _, asset in assets_df.iterrows():
            asset_id = asset["id"]
            available_day = asset["available_on_day"]

            # Get day 1 and day 100 prices
            # Note: We use day 1 and day 100 as a standardized comparison metric
            # even though assets may not be available until later.
            # This gives us a consistent baseline to rank asset performance.
            day1_vals = valuations_df[
                (valuations_df["asset_id"] == asset_id) & (valuations_df["day"] == 1)
            ]
            day100_vals = valuations_df[
                (valuations_df["asset_id"] == asset_id) & (valuations_df["day"] == 100)
            ]

            # Skip assets with incomplete data
            if day1_vals.empty:
                print(f"Warning: {asset_id} missing day 1 valuation, skipping")
                continue

            if day100_vals.empty:
                print(f"Warning: {asset_id} missing day 100 valuation, skipping")
                continue

            day1_price = float(day1_vals["valuation"].iloc[0])
            day100_price = float(day100_vals["valuation"].iloc[0])
            return_pct = ((day100_price - day1_price) / day1_price) * 100

            asset_returns.append(
                {
                    "asset_id": asset_id,
                    "available_day": available_day,
                    "day1_price": day1_price,
                    "return_pct": return_pct,
                }
            )

        # Sort by return percentage (descending)
        asset_returns.sort(key=lambda x: x["return_pct"], reverse=True)

        # Select top profitable assets that fit budget
        trades = []
        cash = self._initial_cash
        purchased = set()

        for asset_info in asset_returns:
            if asset_info["return_pct"] <= 0:
                # Skip assets with negative returns
                continue

            asset_id = asset_info["asset_id"]
            available_day = asset_info["available_day"]

            # Get price on available day
            price = self._loader.get_valuation_on_day(asset_id, available_day)

            if price <= cash and asset_id not in purchased:
                trades.append(
                    Trade(day=available_day, action="buy", asset_id=asset_id)
                )
                cash -= price
                purchased.add(asset_id)

        # Sort trades by day
        trades.sort(key=lambda t: t.day)

        return trades
