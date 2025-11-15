# Problem-Solving Workflow

## Overview

This document outlines the step-by-step process for tackling Quantmas challenges using TDD and best practices.

---

## Step 1: Understand the Problem

### Read Problem Statement
- Read `problems/year_X/problem.md` thoroughly
- Identify the objective and scoring criteria
- Note all constraints and rules
- Understand input/output formats

### Examine Data Files
```bash
# Check data structure
head -20 problems/year_1/data/assets.csv
head -20 problems/year_1/data/valuations.csv

# Count records
wc -l problems/year_1/data/*.csv

# Check for data quality issues
python -c "import pandas as pd; df = pd.read_csv('problems/year_1/data/assets.csv'); print(df.info())"
```

### Clarify Ambiguities
- List any unclear requirements
- Ask user for clarification
- Document assumptions in `.agent_log/2025.log`

---

## Step 2: Set Up Project Structure

### Create Directory Structure
```bash
cd implementation

# Create source directories
mkdir -p src/{models,services,strategies,utils}
touch src/__init__.py
touch src/{models,services,strategies,utils}/__init__.py

# Create test directories
mkdir -p test/{test_models,test_services,test_strategies}
touch test/__init__.py
touch test/conftest.py

# Create docs directory
mkdir -p docs
```

### Initialize Configuration Files

**requirements.txt**:
```txt
pandas>=2.0.0
numpy>=1.24.0
pyyaml>=6.0
```

**requirements-dev.txt**:
```txt
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
black>=23.7.0
isort>=5.12.0
flake8>=6.1.0
mypy>=1.5.0
pylint>=2.17.0
```

**pyproject.toml**:
```toml
[tool.pytest.ini_options]
testpaths = ["test"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--verbose",
    "--cov=src",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=80"
]

[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.11"
warn_return_any = true
disallow_untyped_defs = true
```

### Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## Step 3: Data Exploration (TDD)

### 🔴 RED: Write Data Loading Tests

```python
# test/test_services/test_data_loader.py
import pytest
from src.services.data_loader import DataLoader

class TestDataLoader:
    def test_load_assets_returns_dataframe(self):
        """Should load assets as DataFrame."""
        loader = DataLoader("problems/year_1/data")
        df = loader.load_assets()
        assert df is not None
        assert len(df) == 15
    
    def test_load_valuations_returns_dataframe(self):
        """Should load valuations as DataFrame."""
        loader = DataLoader("problems/year_1/data")
        df = loader.load_valuations()
        assert df is not None
        assert len(df) == 1500  # 15 assets * 100 days
```

### 🟢 GREEN: Implement Data Loading

```python
# src/services/data_loader.py
from pathlib import Path
import pandas as pd

class DataLoader:
    def __init__(self, data_path: str):
        self._path = Path(data_path)
    
    def load_assets(self) -> pd.DataFrame:
        return pd.read_csv(self._path / "assets.csv")
    
    def load_valuations(self) -> pd.DataFrame:
        return pd.read_csv(self._path / "valuations.csv")
```

### 🔵 REFACTOR: Add Validation

```python
# src/services/data_loader.py
from pathlib import Path
from typing import Dict, List
import pandas as pd

class DataLoader:
    """Handles loading and validation of market data."""
    
    def __init__(self, data_path: str):
        self._path = Path(data_path)
    
    def load_assets(self) -> pd.DataFrame:
        """Load assets with validation."""
        df = pd.read_csv(self._path / "assets.csv")
        self._validate_assets(df)
        return df
    
    def load_valuations(self) -> pd.DataFrame:
        """Load valuations with validation."""
        df = pd.read_csv(self._path / "valuations.csv")
        self._validate_valuations(df)
        return df
    
    def _validate_assets(self, df: pd.DataFrame) -> None:
        """Validate assets DataFrame."""
        required = {'id', 'name', 'type', 'sub_type', 'available_on_day', 'region'}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")
    
    def _validate_valuations(self, df: pd.DataFrame) -> None:
        """Validate valuations DataFrame."""
        required = {'asset_id', 'day', 'valuation'}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")
```

### Analyze Data

Create a Jupyter notebook for exploration:

```python
# notebooks/data_exploration.ipynb
import pandas as pd
import matplotlib.pyplot as plt

# Load data
assets = pd.read_csv("../problems/year_1/data/assets.csv")
valuations = pd.read_csv("../problems/year_1/data/valuations.csv")

# Analyze assets
print(assets.info())
print(assets['sub_type'].value_counts())
print(assets['region'].value_counts())

# Analyze valuations
for asset_id in assets['id']:
    asset_vals = valuations[valuations['asset_id'] == asset_id]
    plt.plot(asset_vals['day'], asset_vals['valuation'], label=asset_id)

plt.legend()
plt.xlabel('Day')
plt.ylabel('Valuation (FSB)')
plt.title('Asset Valuations Over Time')
plt.show()

# Calculate returns
for asset_id in assets['id']:
    asset_vals = valuations[valuations['asset_id'] == asset_id]
    start_price = asset_vals[asset_vals['day'] == 1]['valuation'].values[0]
    end_price = asset_vals[asset_vals['day'] == 100]['valuation'].values[0]
    return_pct = ((end_price - start_price) / start_price) * 100
    print(f"{asset_id}: {return_pct:.2f}%")
```

---

## Step 4: Build Core Models (TDD)

### 🔴 RED: Write Model Tests

```python
# test/test_models/test_asset.py
from src.models.asset import Asset

def test_asset_creation():
    """Should create asset with all attributes."""
    asset = Asset(
        id="asset_1",
        name="Snowflake Manor",
        asset_type="Real Estate",
        sub_type="Residential",
        available_on_day=1,
        region="Frostpeak"
    )
    assert asset.id == "asset_1"
    assert asset.available_on_day == 1

def test_asset_is_available():
    """Should correctly determine availability."""
    asset = Asset(
        id="asset_3",
        name="Test",
        asset_type="Real Estate",
        sub_type="Residential",
        available_on_day=45,
        region="Test"
    )
    assert not asset.is_available(44)
    assert asset.is_available(45)
    assert asset.is_available(46)
```

### 🟢 GREEN: Implement Models

```python
# src/models/asset.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Asset:
    """Immutable asset representation."""
    id: str
    name: str
    asset_type: str
    sub_type: str
    available_on_day: int
    region: str
    
    def is_available(self, day: int) -> bool:
        """Check if asset is available on given day."""
        return day >= self.available_on_day
```

---

## Step 5: Build Trading Engine (TDD)

### 🔴 RED: Write Trading Tests

```python
# test/test_services/test_trading_engine.py
import pytest
from src.services.trading_engine import TradingEngine

def test_initial_cash():
    """Should start with correct cash amount."""
    engine = TradingEngine(initial_cash=1000000)
    assert engine.cash == 1000000

def test_buy_asset_reduces_cash():
    """Should reduce cash by purchase price."""
    engine = TradingEngine(initial_cash=1000000)
    engine.buy_asset("asset_1", price=150000, day=1)
    assert engine.cash == 850000

def test_buy_asset_insufficient_funds():
    """Should raise error when insufficient funds."""
    engine = TradingEngine(initial_cash=100000)
    with pytest.raises(ValueError, match="Insufficient funds"):
        engine.buy_asset("asset_1", price=150000, day=1)
```

### 🟢 GREEN: Implement Trading Engine

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
        return self._cash
    
    def buy_asset(self, asset_id: str, price: float, day: int) -> None:
        """Purchase an asset."""
        if price > self._cash:
            raise ValueError("Insufficient funds")
        self._cash -= price
        self._holdings[asset_id] = 1
```

### 🔵 REFACTOR: Add Full Validation

Continue with sell logic, validation, etc.

---

## Step 6: Develop Strategy (TDD)

### Start Simple

```python
# src/strategies/simple_strategy.py
class SimpleStrategy:
    """Buy-and-hold strategy."""
    
    def generate_trades(self) -> List[Trade]:
        """Buy best asset on day 1, hold until day 100."""
        # Identify best performing asset
        best_asset = self._find_best_asset()
        return [Trade(day=1, action="buy", asset_id=best_asset.id)]
```

### Iterate and Improve

1. Analyze which assets perform best
2. Identify optimal entry/exit points
3. Test different strategies
4. Measure performance

---

## Step 7: Generate Output

### 🔴 RED: Write Output Tests

```python
# test/test_services/test_output_generator.py
def test_generate_yaml_output():
    """Should generate valid YAML format."""
    trades = [
        Trade(day=1, action="buy", asset_id="asset_1"),
        Trade(day=50, action="sell", asset_id="asset_1")
    ]
    output = OutputGenerator.generate_yaml(trades)
    
    assert "1:" in output
    assert "buy: asset_1" in output
```

### 🟢 GREEN: Implement Output Generation

```python
# src/services/output_generator.py
import yaml
from typing import List, Dict
from models.trade import Trade

class OutputGenerator:
    @staticmethod
    def generate_yaml(trades: List[Trade]) -> str:
        """Generate YAML output from trades."""
        output: Dict[int, List[Dict[str, str]]] = {}
        
        for trade in trades:
            if trade.day not in output:
                output[trade.day] = []
            output[trade.day].append({trade.action: trade.asset_id})
        
        return yaml.dump(output, sort_keys=True)
    
    @staticmethod
    def save_output(trades: List[Trade], file_path: str) -> None:
        """Save trades to YAML file."""
        yaml_content = OutputGenerator.generate_yaml(trades)
        with open(file_path, 'w') as f:
            f.write(yaml_content)
```

---

## Step 8: Integration and Validation

### Create Main Entry Point

```python
# src/main.py
from pathlib import Path
from services.data_loader import DataLoader
from services.trading_engine import TradingEngine
from strategies.simple_strategy import SimpleStrategy
from services.output_generator import OutputGenerator

def main():
    """Main entry point for solution."""
    # Load data
    loader = DataLoader("problems/year_1/data")
    
    # Initialize engine
    engine = TradingEngine(initial_cash=1000000)
    
    # Generate strategy
    strategy = SimpleStrategy(loader, engine)
    trades = strategy.generate_trades()
    
    # Execute trades and calculate final value
    final_value = engine.execute_all(trades)
    print(f"Final portfolio value: {final_value:,.2f} FSB")
    
    # Generate output
    output_path = Path("problems/year_1/output/output.yml")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    OutputGenerator.save_output(trades, str(output_path))
    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    main()
```

### Run Full Test Suite

```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
```

---

## Step 9: Quality Checks

### Run All Quality Tools

```bash
# Format code
black src/ test/
isort src/ test/

# Type check
mypy src/

# Lint
flake8 src/
pylint src/

# Test
pytest --cov=src --cov-fail-under=80
```

### Verify Output

```bash
# Generate output
python -m src.main

# Validate output format
python -c "import yaml; yaml.safe_load(open('problems/year_1/output/output.yml'))"

# Check output location
ls -la problems/year_1/output/
```

---

## Step 10: Documentation

### Update README.md

Document:
- Installation steps
- How to run solution
- How to run tests
- Algorithm explanation
- Final results

### Update docs/

Create:
- `docs/architecture.md` - System design
- `docs/algorithm.md` - Strategy explanation
- `docs/decisions.md` - Design decisions and trade-offs

---

## Step 11: Submit

### Final Checklist

- [ ] All tests pass
- [ ] Coverage ≥ 80%
- [ ] mypy passes
- [ ] flake8 passes
- [ ] pylint score ≥ 8.0
- [ ] Output file generated
- [ ] Output in correct location
- [ ] README.md complete
- [ ] Documentation complete
- [ ] `.agent_log/2025.log` updated

### Run Submission Script

```bash
bash ./test-and-submit.sh
```

---

## Iterative Improvement

After initial submission:

1. **Analyze Results**: Review score and identify weaknesses
2. **Hypothesis**: Form hypothesis about improvements
3. **Test**: Write tests for new approach
4. **Implement**: Build improvement
5. **Measure**: Compare new vs old performance
6. **Iterate**: Repeat until satisfied

---

## Troubleshooting

### Tests Failing
- Read error messages carefully
- Check test assumptions
- Verify test data
- Use debugger or print statements

### Coverage Too Low
- Identify uncovered lines: `pytest --cov=src --cov-report=term-missing`
- Write tests for uncovered code
- Remove dead code

### Type Errors
- Add missing type hints
- Fix incorrect types
- Use `reveal_type()` for debugging

### Output Invalid
- Validate against problem specification
- Check YAML syntax
- Verify all business rules followed

---

## Time Management

Suggested time allocation for a challenge:

- **20%** - Understanding problem and data exploration
- **30%** - Building core infrastructure (models, services)
- **30%** - Strategy development and optimization
- **10%** - Output generation and validation
- **10%** - Documentation and quality checks

---

## Collaboration with User

### When to Ask Questions
- Problem statement ambiguity
- Unclear business rules
- Trade-off decisions (performance vs simplicity)
- Before major architectural changes

### What to Report
- Completion of major milestones
- Test coverage status
- Issues encountered
- Performance metrics
- Final results

### What to Log
Everything in `.agent_log/2025.log`:
- User instructions
- Questions and answers
- Assumptions made
- Issues and resolutions
- Key decisions and rationale
- Test results
- Final scores and learnings
