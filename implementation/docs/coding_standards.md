# Coding Standards

## Python Code Style

### General Principles
- Follow PEP 8 guidelines for Python code style
- Use meaningful variable and function names
- Write docstrings for all classes and functions
- Keep functions focused and single-purpose

### Naming Conventions
- Classes: `PascalCase` (e.g., `OptimizedTradingStrategy`)
- Functions and variables: `snake_case` (e.g., `get_asset_price`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `STARTING_CAPITAL`)
- File names: `snake_case.py` (e.g., `optimized_trading.py`)

### Code Structure
- Maximum line length: 88 characters (Black formatter standard)
- Use type hints where appropriate
- Import organization:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports

### Documentation
- All public classes and functions must have docstrings
- Use Google-style docstrings
- Include parameter types and return types
- Provide usage examples for complex functions

### Error Handling
- Use specific exception types rather than generic `Exception`
- Provide meaningful error messages
- Log errors appropriately

### Testing
- Maintain >80% code coverage
- Write unit tests for all public methods
- Use descriptive test names that explain what is being tested
- Mock external dependencies in tests

## Example Code Structure

```python
"""
Module description here.
"""

import pandas as pd
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ExampleClass:
    """Class description."""
    
    value: float
    name: str = "default"


class ExampleStrategy:
    """
    Strategy class description.
    
    Attributes:
        data: DataFrame containing market data
        config: Dictionary of configuration parameters
    """
    
    def __init__(self, data_file: str):
        """Initialize strategy with data file."""
        self.data = pd.read_csv(data_file)
    
    def process_data(self, start_day: int, end_day: int) -> List[float]:
        """
        Process data for given date range.
        
        Args:
            start_day: First day to process (inclusive)
            end_day: Last day to process (inclusive)
            
        Returns:
            List of processed values
            
        Raises:
            ValueError: If start_day > end_day
        """
        if start_day > end_day:
            raise ValueError("start_day must be <= end_day")
        
        # Processing logic here
        return []
```