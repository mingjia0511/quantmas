# Test-Driven Development (TDD) Guide

## The Red-Green-Refactor Cycle

TDD follows a simple three-step cycle that ensures code is tested, functional, and clean.

### 🔴 RED: Write a Failing Test

**Write the test FIRST, before any implementation code.**

```python
# test/test_services/test_trading_engine.py
def test_buy_asset_reduces_cash():
    """Buying an asset should reduce available cash by purchase price."""
    engine = TradingEngine(initial_cash=1000000)
    
    # This will fail - TradingEngine doesn't exist yet
    engine.buy_asset("asset_1", price=150000, day=1)
    
    assert engine.cash == 850000  # 1000000 - 150000
```

**Run the test - it should FAIL:**
```bash
pytest test/test_services/test_trading_engine.py::test_buy_asset_reduces_cash -v
```

**Expected output**: `ImportError` or `AttributeError`

This failure is GOOD - it confirms the test is actually testing something!

### 🟢 GREEN: Write Minimal Code to Pass

**Write just enough code to make the test pass. No more, no less.**

```python
# src/services/trading_engine.py
class TradingEngine:
    """Manages portfolio trading operations."""
    
    def __init__(self, initial_cash: float):
        self.cash = initial_cash
    
    def buy_asset(self, asset_id: str, price: float, day: int) -> None:
        """Purchase an asset at given price."""
        self.cash -= price
```

**Run the test - it should PASS:**
```bash
pytest test/test_services/test_trading_engine.py::test_buy_asset_reduces_cash -v
```

**Expected output**: `PASSED`

### 🔵 REFACTOR: Improve Code Quality

**Now improve the code without changing behavior.**

```python
# src/services/trading_engine.py
from typing import Dict

class TradingEngine:
    """Manages portfolio trading operations."""
    
    def __init__(self, initial_cash: float):
        self._cash = initial_cash
        self._holdings: Dict[str, int] = {}
    
    @property
    def cash(self) -> float:
        """Current available cash."""
        return self._cash
    
    def buy_asset(self, asset_id: str, price: float, day: int) -> None:
        """Purchase an asset at given price.
        
        Args:
            asset_id: Unique asset identifier
            price: Purchase price in FSB
            day: Trading day of purchase
        
        Raises:
            ValueError: If insufficient funds
        """
        if price > self._cash:
            raise ValueError(f"Insufficient funds: need {price}, have {self._cash}")
        
        self._cash -= price
        self._holdings[asset_id] = self._holdings.get(asset_id, 0) + 1
```

**Run ALL tests - they should still PASS:**
```bash
pytest -v
```

**Key point**: Tests protect your refactoring. If tests still pass, refactoring is safe!

---

## TDD Workflow for Quantmas

### Phase 1: Data Loading

#### 🔴 RED - Write Test
```python
# test/test_services/test_data_loader.py
import pytest
from src.services.data_loader import DataLoader

def test_load_assets_returns_correct_count():
    """Should load exactly 15 assets from CSV."""
    loader = DataLoader("problems/year_1/data")
    assets = loader.load_assets()
    assert len(assets) == 15
```

#### 🟢 GREEN - Minimal Implementation
```python
# src/services/data_loader.py
import pandas as pd

class DataLoader:
    def __init__(self, data_path: str):
        self.path = data_path
    
    def load_assets(self):
        return pd.read_csv(f"{self.path}/assets.csv")
```

#### 🔵 REFACTOR - Improve Quality
```python
# src/services/data_loader.py
from pathlib import Path
import pandas as pd

class DataLoader:
    """Handles loading and validation of market data."""
    
    def __init__(self, data_path: str):
        self._path = Path(data_path)
    
    def load_assets(self) -> pd.DataFrame:
        """Load assets from CSV with validation.
        
        Returns:
            DataFrame with columns: id, name, type, sub_type, 
                                   available_on_day, region
        
        Raises:
            FileNotFoundError: If assets.csv doesn't exist
            ValueError: If required columns are missing
        """
        file_path = self._path / "assets.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Assets file not found: {file_path}")
        
        df = pd.read_csv(file_path)
        self._validate_assets(df)
        return df
    
    def _validate_assets(self, df: pd.DataFrame) -> None:
        """Validate assets DataFrame has required columns."""
        required_columns = {'id', 'name', 'type', 'sub_type', 
                          'available_on_day', 'region'}
        missing = required_columns - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
```

### Phase 2: Trading Logic

#### 🔴 RED - Test Validation
```python
def test_cannot_buy_asset_already_owned():
    """Should raise error when trying to buy asset already in portfolio."""
    engine = TradingEngine(initial_cash=1000000)
    engine.buy_asset("asset_1", price=150000, day=1)
    
    with pytest.raises(ValueError, match="already owned"):
        engine.buy_asset("asset_1", price=150000, day=2)
```

#### 🟢 GREEN - Add Validation
```python
def buy_asset(self, asset_id: str, price: float, day: int) -> None:
    """Purchase an asset."""
    if asset_id in self._holdings:
        raise ValueError(f"Asset {asset_id} already owned")
    
    self._cash -= price
    self._holdings[asset_id] = 1
```

#### 🔵 REFACTOR - Extract Methods
```python
def buy_asset(self, asset_id: str, price: float, day: int) -> None:
    """Purchase an asset with full validation."""
    self._validate_can_buy(asset_id, price)
    self._execute_purchase(asset_id, price, day)

def _validate_can_buy(self, asset_id: str, price: float) -> None:
    """Validate purchase is allowed."""
    if asset_id in self._holdings:
        raise ValueError(f"Asset {asset_id} already owned")
    if price > self._cash:
        raise ValueError(f"Insufficient funds: need {price}, have {self._cash}")

def _execute_purchase(self, asset_id: str, price: float, day: int) -> None:
    """Execute the purchase transaction."""
    self._cash -= price
    self._holdings[asset_id] = 1
    self._log_transaction("BUY", asset_id, price, day)
```

### Phase 3: Strategy Implementation

#### 🔴 RED - Test Strategy Output
```python
def test_strategy_generates_valid_trades():
    """Strategy should generate trades within valid day range."""
    loader = DataLoader("problems/year_1/data")
    engine = TradingEngine(initial_cash=1000000)
    strategy = SimpleStrategy(loader, engine)
    
    trades = strategy.generate_trades()
    
    assert all(1 <= trade.day <= 100 for trade in trades)
    assert all(trade.action in ["buy", "sell"] for trade in trades)
    assert all(trade.asset_id.startswith("asset_") for trade in trades)
```

#### 🟢 GREEN - Basic Strategy
```python
from dataclasses import dataclass
from typing import List

@dataclass
class Trade:
    day: int
    action: str
    asset_id: str

class SimpleStrategy:
    def __init__(self, loader: DataLoader, engine: TradingEngine):
        self._loader = loader
        self._engine = engine
    
    def generate_trades(self) -> List[Trade]:
        """Generate simple buy-and-hold strategy."""
        return [Trade(day=1, action="buy", asset_id="asset_1")]
```

#### 🔵 REFACTOR - Add Real Logic
```python
class SimpleStrategy:
    """Implements a simple momentum-based trading strategy."""
    
    def __init__(self, loader: DataLoader, engine: TradingEngine):
        self._loader = loader
        self._engine = engine
        self._assets = loader.load_assets()
        self._valuations = loader.load_valuations()
    
    def generate_trades(self) -> List[Trade]:
        """Generate optimized trading strategy.
        
        Strategy:
        1. Identify assets with positive momentum
        2. Buy on local minima
        3. Sell on local maxima
        4. Hold best performers until day 100
        """
        trades = []
        
        for asset in self._identify_profitable_assets():
            entry_day = self._find_optimal_entry(asset)
            exit_day = self._find_optimal_exit(asset, entry_day)
            
            trades.append(Trade(day=entry_day, action="buy", asset_id=asset.id))
            if exit_day < 100:
                trades.append(Trade(day=exit_day, action="sell", asset_id=asset.id))
        
        return sorted(trades, key=lambda t: t.day)
    
    def _identify_profitable_assets(self) -> List[Asset]:
        """Identify assets with positive overall trend."""
        ...
    
    def _find_optimal_entry(self, asset: Asset) -> int:
        """Find best day to buy asset (local minimum)."""
        ...
    
    def _find_optimal_exit(self, asset: Asset, entry_day: int) -> int:
        """Find best day to sell asset (local maximum)."""
        ...
```

---

## TDD Best Practices

### 1. Test One Thing at a Time

❌ **BAD** - Tests multiple behaviors:
```python
def test_trading_engine():
    engine = TradingEngine(1000000)
    engine.buy_asset("asset_1", 150000, 1)
    engine.sell_asset("asset_1", 160000, 2)
    assert engine.cash == 1010000
    assert len(engine.holdings) == 0
    assert engine.profit == 10000
```

✅ **GOOD** - Separate, focused tests:
```python
def test_buy_asset_reduces_cash():
    engine = TradingEngine(1000000)
    engine.buy_asset("asset_1", 150000, 1)
    assert engine.cash == 850000

def test_sell_asset_increases_cash():
    engine = TradingEngine(1000000)
    engine.buy_asset("asset_1", 150000, 1)
    engine.sell_asset("asset_1", 160000, 2)
    assert engine.cash == 1010000

def test_sell_asset_removes_from_holdings():
    engine = TradingEngine(1000000)
    engine.buy_asset("asset_1", 150000, 1)
    engine.sell_asset("asset_1", 160000, 2)
    assert "asset_1" not in engine.holdings
```

### 2. Use Descriptive Test Names

Test names should describe WHAT is tested and WHAT is expected.

❌ **BAD**:
```python
def test_buy():
    ...

def test_error():
    ...
```

✅ **GOOD**:
```python
def test_buy_asset_with_sufficient_funds_succeeds():
    ...

def test_buy_asset_with_insufficient_funds_raises_value_error():
    ...

def test_buy_asset_already_owned_raises_value_error():
    ...
```

### 3. Arrange-Act-Assert (AAA) Pattern

Structure every test with three clear sections:

```python
def test_portfolio_value_calculation():
    # ARRANGE - Set up test data and preconditions
    engine = TradingEngine(initial_cash=500000)
    engine.buy_asset("asset_1", price=150000, day=1)
    valuations = {"asset_1": 160000}
    
    # ACT - Execute the behavior being tested
    total_value = engine.calculate_total_value(valuations)
    
    # ASSERT - Verify the outcome
    expected_value = 510000  # 350000 cash + 160000 asset
    assert total_value == expected_value
```

### 4. Use Fixtures for Common Setup

Avoid repetition with pytest fixtures:

```python
# test/conftest.py
import pytest

@pytest.fixture
def trading_engine():
    """Provide a fresh trading engine for each test."""
    return TradingEngine(initial_cash=1000000)

@pytest.fixture
def engine_with_asset(trading_engine):
    """Provide engine with one asset already purchased."""
    trading_engine.buy_asset("asset_1", 150000, 1)
    return trading_engine

# test/test_services/test_trading_engine.py
def test_buy_asset(trading_engine):
    """Use fixture - no setup needed in test."""
    trading_engine.buy_asset("asset_1", 150000, 1)
    assert trading_engine.cash == 850000

def test_sell_asset(engine_with_asset):
    """Use fixture with pre-purchased asset."""
    engine_with_asset.sell_asset("asset_1", 160000, 2)
    assert engine_with_asset.cash == 1010000
```

### 5. Test Edge Cases

Don't just test the happy path:

```python
def test_buy_asset_with_exact_cash_amount():
    """Should succeed when cash exactly equals price."""
    engine = TradingEngine(initial_cash=150000)
    engine.buy_asset("asset_1", price=150000, day=1)
    assert engine.cash == 0

def test_buy_asset_on_first_available_day():
    """Should allow purchase on exact available_on_day."""
    engine = TradingEngine(initial_cash=1000000)
    # asset_3 available on day 45
    engine.buy_asset("asset_3", price=200000, day=45)
    assert "asset_3" in engine.holdings

def test_buy_asset_before_available_day_raises_error():
    """Should reject purchase before available_on_day."""
    engine = TradingEngine(initial_cash=1000000)
    with pytest.raises(ValueError, match="not yet available"):
        engine.buy_asset("asset_3", price=200000, day=44)
```

---

## TDD Workflow Summary

For each new feature:

1. **🔴 RED**: Write a failing test
   - Think about the API you want
   - Write the test as if the code exists
   - Run it and watch it fail

2. **🟢 GREEN**: Make it pass
   - Write minimal code
   - Don't worry about perfection
   - Just make the test pass

3. **🔵 REFACTOR**: Clean it up
   - Improve names
   - Extract methods
   - Add documentation
   - Remove duplication
   - Run tests to ensure nothing broke

4. **Repeat**: Move to next test

## Benefits of TDD

- **Confidence**: Tests prove code works
- **Design**: Writing tests first improves API design
- **Documentation**: Tests show how to use the code
- **Regression**: Tests catch bugs when changing code
- **Coverage**: High coverage comes naturally
- **Refactoring**: Safe to improve code with test safety net

## Common TDD Mistakes to Avoid

❌ Writing tests after implementation
❌ Testing implementation details instead of behavior
❌ Making tests too complex
❌ Not running tests frequently
❌ Skipping the refactor step
❌ Writing tests that depend on each other

✅ Test behavior, not implementation
✅ Keep tests simple and focused
✅ Run tests after every change
✅ Refactor with confidence
✅ Make tests independent
