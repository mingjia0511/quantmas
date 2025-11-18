"""Main entry point for Year 1 challenge solution."""

from pathlib import Path
from .data_loader import DataLoader
from .strategy import TradingStrategy
from .output_writer import OutputWriter


def main():
    """Execute Year 1 trading strategy."""
    # Setup paths
    project_root = Path(__file__).parent.parent.parent.parent
    data_dir = project_root / "problems" / "year_1" / "data"
    output_dir = project_root / "problems" / "year_1" / "output"
    output_file = output_dir / "output.yml"
    
    print("Loading data...")
    loader = DataLoader(data_dir)
    assets, valuations = loader.load_all()
    
    print(f"Loaded {len(assets)} assets with {len(valuations)} valuation series")
    
    print("\nExecuting trading strategy...")
    strategy = TradingStrategy(assets, valuations)
    portfolio = strategy.execute_strategy()
    
    print(f"Executed {sum(len(txns) for txns in portfolio.transactions.values())} transactions")
    
    # Print summary
    OutputWriter.print_summary(portfolio, valuations)
    
    # Write output
    print(f"Writing output to {output_file}...")
    OutputWriter.write_output(portfolio.get_transactions(), output_file)
    
    print("✅ Done!")


if __name__ == "__main__":
    main()
