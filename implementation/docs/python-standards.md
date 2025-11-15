# Python Coding Standards

## Type Hints (Mandatory)

All functions must have complete type hints for parameters and return values.

### Basic Types

```python
from typing import List, Dict, Optional, Tuple, Set
from pathlib import Path

def load_valuations(
    file_path: Path,
    asset_ids: Optional[List[str]] = None
) -> Dict[str, List[float]]:
    """Load asset valuations from CSV.
    
    Args:
        file_path: Path to valuations CSV file
        asset_ids: Optional list to filter specific assets
    
    Returns:
        Dictionary mapping asset_id to list of daily valuations
    """
    ...
```

### Complex Types

```python
from typing import Union, Callable, TypeVar, Generic

# Type aliases for clarity
AssetId = str
Price = float
Day = int

def get_price(asset_id: AssetId, day: Day) -> Price:
    """Get asset price on specific day."""
    ...

# Callable types
TransformFunc = Callable[[float], float]

def apply_transform(values: List[float], func: TransformFunc) -> List[float]:
    """Apply transformation function to all values."""
    return [func(v) for v in values]
```

### Generic Types

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class DataCache(Generic[T]):
    """Generic cache for any data type."""
    
    def __init__(self) -> None:
        self._cache: Dict[str, T] = {}
    
    def get(self, key: str) -> Optional[T]:
        """Retrieve cached value."""
        return self._cache.get(key)
    
    def set(self, key: str, value: T) -> None:
        """Store value in cache."""
        self._cache[key] = value
```

## Dataclasses

Use dataclasses for data structures.

### Immutable Data (frozen=True)

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Asset:
    """Immutable asset representation.
    
    Attributes:
        id: Unique asset identifier (e.g., 'asset_1')
        name: Human-readable asset name
        asset_type: Type of asset (e.g., 'Real Estate')
        sub_type: Asset subcategory (e.g., 'Residential')
        available_on_day: First day asset can be purchased (1-100)
        region: Geographic region
    """
    id: str
    name: str
    asset_type: str
    sub_type: str
    available_on_day: int
    region: str
    
    def is_available(self, day: int) -> bool:
        """Check if asset is available for purchase on given day."""
        return day >= self.available_on_day
```

### Mutable Data with Defaults

```python
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Portfolio:
    """Mutable portfolio state.
    
    Attributes:
        cash: Available cash in FSB
        holdings: Map of asset_id to quantity owned
        transaction_history: List of all transactions
    """
    cash: float
    holdings: Dict[str, int] = field(default_factory=dict)
    transaction_history: List['Transaction'] = field(default_factory=list)
    
    def total_value(self, valuations: Dict[str, float]) -> float:
        """Calculate total portfolio value."""
        asset_value = sum(
            self.holdings[aid] * valuations[aid]
            for aid in self.holdings
        )
        return self.cash + asset_value
```

### Post-Init Validation

```python
@dataclass
class Trade:
    """Represents a trading action."""
    day: int
    action: str
    asset_id: str
    price: float
    
    def __post_init__(self) -> None:
        """Validate trade data after initialization."""
        if not 1 <= self.day <= 100:
            raise ValueError(f"Invalid day: {self.day}")
        if self.action not in ("buy", "sell"):
            raise ValueError(f"Invalid action: {self.action}")
        if self.price <= 0:
            raise ValueError(f"Invalid price: {self.price}")
```

## Error Handling

### Custom Exceptions

```python
class TradingError(Exception):
    """Base exception for trading operations."""
    pass

class InsufficientFundsError(TradingError):
    """Raised when attempting to buy without enough cash."""
    pass

class AssetNotOwnedError(TradingError):
    """Raised when attempting to sell an asset not in portfolio."""
    pass

class AssetNotAvailableError(TradingError):
    """Raised when attempting to buy before available_on_day."""
    pass
```

### Proper Error Handling

```python
import logging

logger = logging.getLogger(__name__)

def buy_asset(self, asset_id: str, price: float, day: int) -> None:
    """Purchase asset with comprehensive error handling.
    
    Args:
        asset_id: Asset to purchase
        price: Purchase price in FSB
        day: Trading day
    
    Raises:
        InsufficientFundsError: If cash < price
        AssetNotAvailableError: If day < available_on_day
        AssetNotOwnedError: If asset already owned
    """
    try:
        self._validate_purchase(asset_id, price, day)
        self._execute_purchase(asset_id, price, day)
        logger.info(f"Day {day}: Purchased {asset_id} for {price} FSB")
    except InsufficientFundsError as e:
        logger.error(f"Purchase failed: {e}")
        raise
    except AssetNotAvailableError as e:
        logger.warning(f"Asset not available: {e}")
        raise
```

### Context Managers

```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def transaction_scope(engine: TradingEngine) -> Generator[None, None, None]:
    """Context manager for atomic transactions.
    
    Rolls back changes if exception occurs.
    """
    initial_state = engine.get_state()
    try:
        yield
    except Exception as e:
        logger.error(f"Transaction failed, rolling back: {e}")
        engine.restore_state(initial_state)
        raise
```

## Logging

### Logger Setup

```python
import logging
from pathlib import Path

def setup_logger(name: str, log_file: Path, level: int = logging.INFO) -> logging.Logger:
    """Configure logger with file and console handlers.
    
    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(level)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
```

### Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

class TradingEngine:
    def buy_asset(self, asset_id: str, price: float, day: int) -> None:
        """Purchase asset with appropriate logging."""
        logger.debug(f"Day {day}: Attempting to buy {asset_id} at {price} FSB")
        
        if price > self._cash:
            logger.warning(
                f"Insufficient funds for {asset_id}: "
                f"need {price} FSB, have {self._cash} FSB"
            )
            raise InsufficientFundsError()
        
        self._execute_purchase(asset_id, price)
        logger.info(
            f"Day {day}: Successfully purchased {asset_id} for {price} FSB. "
            f"Remaining cash: {self._cash} FSB"
        )
```

## Code Organization

### Module Structure

```python
"""
services/trading_engine.py

Manages portfolio trading operations including buy/sell transactions,
validation, and portfolio state tracking.
"""

# Standard library imports
import logging
from typing import Dict, List, Optional

# Third-party imports
import pandas as pd

# Local imports
from models.asset import Asset
from models.portfolio import Portfolio
from utils.validators import validate_trading_day

# Module-level constants
INITIAL_CASH = 1000000
MAX_TRADING_DAY = 100

# Logger setup
logger = logging.getLogger(__name__)


class TradingEngine:
    """Manages portfolio trading operations."""
    
    def __init__(self, initial_cash: float = INITIAL_CASH):
        """Initialize trading engine with starting cash."""
        self._portfolio = Portfolio(cash=initial_cash)
        logger.info(f"Initialized trading engine with {initial_cash} FSB")
    
    # Public methods
    def buy_asset(self, asset_id: str, price: float, day: int) -> None:
        """Purchase an asset."""
        ...
    
    def sell_asset(self, asset_id: str, price: float, day: int) -> None:
        """Sell an asset."""
        ...
    
    # Private methods
    def _validate_purchase(self, asset_id: str, price: float, day: int) -> None:
        """Validate purchase is allowed."""
        ...
    
    def _execute_purchase(self, asset_id: str, price: float, day: int) -> None:
        """Execute the purchase transaction."""
        ...
```

### Class Design

```python
class TradingEngine:
    """Manages portfolio trading operations.
    
    Responsibilities:
    - Track portfolio state (cash, holdings)
    - Execute buy/sell transactions
    - Validate trading rules
    - Maintain transaction history
    
    Example:
        >>> engine = TradingEngine(initial_cash=1000000)
        >>> engine.buy_asset("asset_1", price=150000, day=1)
        >>> engine.cash
        850000
    """
    
    def __init__(self, initial_cash: float):
        """Initialize trading engine.
        
        Args:
            initial_cash: Starting cash amount in FSB
        """
        self._cash = initial_cash
        self._holdings: Dict[str, int] = {}
        self._transactions: List[Transaction] = []
    
    @property
    def cash(self) -> float:
        """Current available cash."""
        return self._cash
    
    @property
    def holdings(self) -> Dict[str, int]:
        """Current asset holdings (read-only)."""
        return self._holdings.copy()
    
    def buy_asset(self, asset_id: str, price: float, day: int) -> None:
        """Purchase an asset.
        
        Args:
            asset_id: Asset to purchase
            price: Purchase price in FSB
            day: Trading day (1-100)
        
        Raises:
            InsufficientFundsError: If cash < price
            ValueError: If asset already owned
        """
        self._validate_can_buy(asset_id, price)
        self._execute_purchase(asset_id, price, day)
    
    def _validate_can_buy(self, asset_id: str, price: float) -> None:
        """Validate purchase is allowed (private helper)."""
        if asset_id in self._holdings:
            raise ValueError(f"Asset {asset_id} already owned")
        if price > self._cash:
            raise InsufficientFundsError(
                f"Need {price} FSB, have {self._cash} FSB"
            )
    
    def _execute_purchase(self, asset_id: str, price: float, day: int) -> None:
        """Execute the purchase (private helper)."""
        self._cash -= price
        self._holdings[asset_id] = 1
        self._transactions.append(
            Transaction(day=day, action="buy", asset_id=asset_id, price=price)
        )
```

## Naming Conventions

### Variables and Functions

```python
# snake_case for variables and functions
asset_count = 15
total_value = 1000000

def calculate_portfolio_value(cash: float, holdings: Dict[str, int]) -> float:
    """Calculate total portfolio value."""
    ...

def load_asset_data(file_path: Path) -> pd.DataFrame:
    """Load asset data from CSV."""
    ...
```

### Classes

```python
# PascalCase for classes
class TradingEngine:
    """Manages trading operations."""
    ...

class DataLoader:
    """Handles data loading."""
    ...

class SimpleStrategy:
    """Implements simple trading strategy."""
    ...
```

### Constants

```python
# UPPER_SNAKE_CASE for constants
INITIAL_CASH = 1000000
MAX_TRADING_DAY = 100
MIN_TRADING_DAY = 1
ASSET_COUNT = 15

# Module-level configuration
DEFAULT_DATA_PATH = Path("problems/year_1/data")
OUTPUT_PATH = Path("problems/year_1/output")
```

### Private Members

```python
class TradingEngine:
    def __init__(self):
        # Single underscore for "internal use"
        self._cash = 1000000
        self._holdings = {}
        
        # Double underscore for name mangling (rare)
        self.__secret_key = "abc123"
    
    def _validate_purchase(self):
        """Private method - single underscore."""
        ...
```

## List Comprehensions and Generators

### List Comprehensions

```python
# Simple transformation
prices = [100, 200, 300]
discounted = [p * 0.9 for p in prices]

# With filtering
high_prices = [p for p in prices if p > 150]

# Nested comprehension
matrix = [[i * j for j in range(3)] for i in range(3)]

# Dictionary comprehension
price_map = {f"asset_{i}": price for i, price in enumerate(prices, 1)}
```

### Generator Expressions

```python
# Memory-efficient for large datasets
total = sum(price * 0.9 for price in prices)

# Generator function
def load_valuations_lazy(file_path: Path) -> Generator[Dict[str, float], None, None]:
    """Yield valuations one day at a time."""
    df = pd.read_csv(file_path)
    for day in range(1, 101):
        day_data = df[df['day'] == day]
        yield dict(zip(day_data['asset_id'], day_data['valuation']))
```

## F-Strings for Formatting

```python
# Use f-strings for string formatting
asset_id = "asset_1"
price = 150000
day = 1

# Simple interpolation
message = f"Bought {asset_id} for {price} FSB on day {day}"

# With formatting
message = f"Price: {price:,.2f} FSB"  # "Price: 150,000.00 FSB"

# Multi-line
report = f"""
Portfolio Summary:
  Cash: {cash:,.2f} FSB
  Assets: {len(holdings)}
  Total Value: {total_value:,.2f} FSB
"""

# Expressions in f-strings
message = f"Profit: {sell_price - buy_price:,.2f} FSB"
```

## Pythonic Patterns

### Context Managers

```python
# File handling
with open("output.yml", "w") as f:
    yaml.dump(data, f)

# Multiple context managers
with open("input.csv") as infile, open("output.csv", "w") as outfile:
    process_data(infile, outfile)
```

### Unpacking

```python
# Tuple unpacking
asset_id, price = "asset_1", 150000

# Extended unpacking
first, *middle, last = [1, 2, 3, 4, 5]

# Dictionary unpacking
defaults = {"cash": 1000000, "day": 1}
config = {**defaults, "day": 5}  # Override day
```

### Enumerate and Zip

```python
# Enumerate for index + value
for i, asset in enumerate(assets, start=1):
    print(f"{i}. {asset.name}")

# Zip for parallel iteration
asset_ids = ["asset_1", "asset_2"]
prices = [150000, 300000]
for asset_id, price in zip(asset_ids, prices):
    print(f"{asset_id}: {price}")
```

### Default Dict and Counter

```python
from collections import defaultdict, Counter

# defaultdict for automatic initialization
holdings = defaultdict(int)
holdings["asset_1"] += 1  # No KeyError

# Counter for counting
actions = ["buy", "sell", "buy", "buy"]
action_counts = Counter(actions)  # Counter({'buy': 3, 'sell': 1})
```

## Code Quality Checklist

Before committing code, ensure:

- [ ] All functions have type hints
- [ ] All public functions have docstrings
- [ ] No unused imports
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] Consistent naming conventions
- [ ] Proper error handling
- [ ] Logging at appropriate levels
- [ ] Code formatted with black
- [ ] Imports sorted with isort
- [ ] Passes mypy type checking
- [ ] Passes flake8 linting
- [ ] Passes pylint with score ≥8.0
