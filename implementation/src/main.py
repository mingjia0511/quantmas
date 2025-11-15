"""Main entry point for Year 1 solution."""
from pathlib import Path
from services.data_loader import DataLoader
from services.trading_engine import TradingEngine
from services.output_generator import OutputGenerator
from strategies.buy_and_hold_strategy import BuyAndHoldStrategy


def main() -> None:
    """Execute Year 1 trading strategy."""
    print("=== Quantmas Year 1: Sleigh the Market ===\n")

    # Configuration
    INITIAL_CASH = 1000000
    DATA_PATH = "../problems/year_1/data"
    OUTPUT_PATH = "../problems/year_1/output/output.yml"

    # Load data
    print("Loading market data...")
    loader = DataLoader(DATA_PATH)
    assets_df = loader.load_assets()
    print(f"Loaded {len(assets_df)} assets")

    # Generate strategy
    print("\nGenerating trading strategy...")
    strategy = BuyAndHoldStrategy(loader, initial_cash=INITIAL_CASH)
    trades = strategy.generate_trades()
    print(f"Generated {len(trades)} trades")

    # Display trades
    print("\nTrading Plan:")
    for trade in trades:
        price = loader.get_valuation_on_day(trade.asset_id, trade.day)
        print(f"  Day {trade.day:3d}: {trade.action.upper():4s} {trade.asset_id} at {price:,.0f} FSB")

    # Simulate execution to calculate final value
    print("\nSimulating execution...")
    engine = TradingEngine(initial_cash=INITIAL_CASH)

    for trade in trades:
        price = loader.get_valuation_on_day(trade.asset_id, trade.day)
        if trade.action == "buy":
            engine.buy_asset(trade.asset_id, price, trade.day)
        elif trade.action == "sell":
            engine.sell_asset(trade.asset_id, price, trade.day)

    # Calculate final portfolio value
    valuations_df = loader.load_valuations()
    day100_valuations = {}
    for asset_id in engine.holdings:
        day100_val = valuations_df[
            (valuations_df["asset_id"] == asset_id) & (valuations_df["day"] == 100)
        ]["valuation"].iloc[0]
        day100_valuations[asset_id] = float(day100_val)

    final_value = engine.calculate_total_value(day100_valuations)

    # Display results
    print("\n=== Final Portfolio (Day 100) ===")
    print(f"Cash remaining: {engine.cash:,.0f} FSB")
    print(f"\nAssets held:")
    for asset_id in sorted(engine.holdings.keys()):
        value = day100_valuations[asset_id]
        print(f"  {asset_id}: {value:,.0f} FSB")

    print(f"\n{'='*40}")
    print(f"Total Portfolio Value: {final_value:,.0f} FSB")
    print(f"Initial Investment:    {INITIAL_CASH:,.0f} FSB")
    print(f"Profit:                {final_value - INITIAL_CASH:,.0f} FSB")
    print(f"Return:                {((final_value - INITIAL_CASH) / INITIAL_CASH) * 100:.2f}%")
    print(f"{'='*40}")

    # Save output
    print(f"\nSaving output to {OUTPUT_PATH}...")
    OutputGenerator.save_output(trades, OUTPUT_PATH)
    print("✅ Output saved successfully!")


if __name__ == "__main__":
    main()
