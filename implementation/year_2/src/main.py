"""Main entry point for Year 2 solution."""

from pathlib import Path
from .data_loader import load_assets, load_valuations, load_tax_rates
from .tax_calculator import TaxCalculator
from .portfolio import Portfolio
from .strategy import TaxOptimizedStrategy
from .output_writer import write_output


def main():
    """Run Year 2 solution."""
    # Setup paths
    project_root = Path(__file__).parent.parent.parent.parent
    data_dir = project_root / 'problems' / 'year_2' / 'data'
    output_dir = project_root / 'implementation' / 'year_2'
    
    print("=== Year 2: Tax Optimization Challenge ===\n")
    
    # Load data
    print("Loading data...")
    assets = load_assets(data_dir)
    valuations = load_valuations(data_dir)
    tax_rates = load_tax_rates(data_dir)
    
    print(f"Loaded {len(assets)} assets")
    print(f"Loaded valuations for {len(valuations)} assets")
    print(f"Tax rate periods: {len(next(iter(tax_rates.values())))}\n")
    
    # Create asset metadata lookup
    asset_metadata = {
        asset['asset_id']: asset
        for asset in assets
    }
    
    # Year 1 ending portfolio (carried over to Year 2)
    year1_ending_cash = 176_181
    year1_ending_assets = ['asset_1', 'asset_4', 'asset_13', 'asset_3', 'asset_14']
    
    print("Starting with Year 1 ending portfolio:")
    print(f"  Cash: ${year1_ending_cash:,}")
    print(f"  Assets: {year1_ending_assets}")
    
    # Calculate total portfolio value at Year 2 day 1
    total_value = year1_ending_cash
    for asset_id in year1_ending_assets:
        if asset_id in valuations:
            total_value += valuations[asset_id][1]
    print(f"  Total portfolio value: ${total_value:,}\n")
    
    # Initialize components
    tax_calculator = TaxCalculator(tax_rates)
    portfolio = Portfolio(
        initial_cash=year1_ending_cash,
        tax_calculator=tax_calculator,
        valuations=valuations,
        asset_metadata=asset_metadata
    )
    
    # Add Year 1 assets to portfolio (already owned, start paying taxes from day 1)
    for asset_id in year1_ending_assets:
        if asset_id in asset_metadata:
            portfolio.add_existing_asset(asset_id, purchase_day=0)  # Day 0 = carried from Year 1
    
    # Execute strategy
    strategy = TaxOptimizedStrategy(portfolio, assets)
    actions = strategy.execute_strategy()
    
    # Write output
    output_file = output_dir / 'output.yml'
    write_output(actions, output_file)


if __name__ == '__main__':
    main()
