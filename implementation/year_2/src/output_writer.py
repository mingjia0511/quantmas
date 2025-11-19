"""Output file generation for Year 2."""

import yaml
from pathlib import Path
from typing import Dict, List


def write_output(actions: Dict[int, List[Dict[str, str]]], output_file: Path):
    """
    Write actions to YAML output file.
    
    Args:
        actions: Dict mapping day -> list of actions
        output_file: Path to output file
    """
    # Convert to required format
    output_data = []
    
    for day in sorted(actions.keys()):
        day_actions = actions[day]
        for action in day_actions:
            # Each action is a dict with one key (buy/sell/pay_tax) and asset_id as value
            output_data.append({
                'day': day,
                **action  # Spread the action dict (e.g., {'buy': 'asset_1'})
            })
    
    # Write to file
    with open(output_file, 'w') as f:
        yaml.dump(output_data, f, default_flow_style=False, sort_keys=False)
    
    print(f"\nWrote {len(output_data)} actions to {output_file}")
