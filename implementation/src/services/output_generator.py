"""Output generation service."""
import yaml
from typing import List, Dict, Any
from pathlib import Path
from src.strategies.buy_and_hold_strategy import Trade


class OutputGenerator:
    """Handles generation of output files."""

    @staticmethod
    def generate_yaml(trades: List[Trade]) -> str:
        """Generate YAML output from trades.

        Args:
            trades: List of trades to convert

        Returns:
            YAML string representation
        """
        output: Dict[int, List[Dict[str, str]]] = {}

        for trade in trades:
            if trade.day not in output:
                output[trade.day] = []
            output[trade.day].append({trade.action: trade.asset_id})

        # Sort by day
        sorted_output = dict(sorted(output.items()))

        return yaml.dump(sorted_output, sort_keys=False, default_flow_style=False)

    @staticmethod
    def save_output(trades: List[Trade], file_path: str) -> None:
        """Save trades to YAML file.

        Args:
            trades: List of trades to save
            file_path: Path to output file
        """
        yaml_content = OutputGenerator.generate_yaml(trades)

        # Ensure directory exists
        output_path = Path(file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w") as f:
            f.write(yaml_content)
