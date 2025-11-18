"""Output file generation for Year 1 challenge."""

import yaml
from pathlib import Path
from typing import Dict, List


class OutputWriter:
    """Writes trading decisions to YAML output file."""
    
    @staticmethod
    def write_output(transactions: Dict[int, List[Dict]], output_path: Path) -> None:
        """Write transactions to YAML file.
        
        Args:
            transactions: Dict mapping day to list of transactions
            output_path: Path to output file
        """
        # Convert to format expected by challenge
        output = {}
        for day in sorted(transactions.keys()):
            output[day] = transactions[day]
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write YAML file
        with open(output_path, 'w') as f:
            yaml.dump(output, f, default_flow_style=False, sort_keys=False)
    
    @staticmethod
    def print_summary(portfolio, valuations: Dict[str, Dict[int, int]]) -> None:
        """Print portfolio summary.
        
        Args:
            portfolio: Portfolio object
            valuations: Asset valuations
        """
        final_value = portfolio.calculate_final_value(valuations)
        
        print("\n" + "="*60)
        print("PORTFOLIO SUMMARY")
        print("="*60)
        print(f"Cash on hand: {portfolio.cash:,} FSB")
        print(f"Assets owned: {len(portfolio.owned_assets)}")
        
        if portfolio.owned_assets:
            print("\nAsset Holdings:")
            total_asset_value = 0
            for asset_id in sorted(portfolio.owned_assets):
                value = valuations[asset_id][100]
                total_asset_value += value
                print(f"  {asset_id}: {value:,} FSB")
            print(f"  Total: {total_asset_value:,} FSB")
        
        print(f"\nFinal Portfolio Value: {final_value:,} FSB")
        print(f"Return: {((final_value / 1_000_000) - 1) * 100:.2f}%")
        print("="*60 + "\n")
