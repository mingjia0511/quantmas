# Quality Standards

## Testing Requirements

### Minimum Coverage: 80%

Use pytest with coverage plugin:

```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
```

### Test Structure

```python
# test/test_services/test_data_loader.py
import pytest
from src.services.data_loader import DataLoader

class TestDataLoader:
    """Test suite for DataLoader service."""
    
    def test_load_assets_returns_dataframe(self):
        """Should return pandas DataFrame with correct columns."""
        loader = DataLoader("problems/year_1/data")
        df = loader.load_assets()
        
        assert df is not None
        assert "id" in df.columns
        assert len(df) == 15
    
    def test_load_assets_invalid_path_raises_error(self):
        """Should raise FileNotFoundError for invalid path."""
        loader = DataLoader("invalid/path")
        
        with pytest.raises(FileNotFoundError):
            loader.load_assets()
```

### Test Categories

**1. Unit Tests** - Test individual functions/methods
- Mock external dependencies
- Fast execution (<1s per test)
- High coverage of edge cases

**2. Integration Tests** - Test component interactions
- Use real data files
- Test data flow between modules
- Validate outputs

**3. Validation Tests** - Test business rules
- Verify trading rules compliance
- Check output format correctness
- Test constraint enforcement

### pytest Configuration

```toml
# pyproject.toml
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
```

### Fixtures

Use `conftest.py` for shared test fixtures:

```python
# test/conftest.py
import pytest
import pandas as pd

@pytest.fixture
def sample_assets():
    """Provide sample asset data for tests."""
    return pd.DataFrame({
        'id': ['asset_1', 'asset_2'],
        'name': ['Snowflake Manor', 'Candy Cane Plaza'],
        'available_on_day': [1, 1],
        'region': ['Frostpeak', 'Tinseltown']
    })

@pytest.fixture
def trading_engine():
    """Provide a fresh trading engine for each test."""
    from src.services.trading_engine import TradingEngine
    return TradingEngine(initial_cash=1000000)

@pytest.fixture
def sample_valuations():
    """Provide sample valuation data."""
    return pd.DataFrame({
        'asset_id': ['asset_1', 'asset_1', 'asset_2', 'asset_2'],
        'day': [1, 2, 1, 2],
        'valuation': [150000, 155000, 300000, 305000]
    })
```

## Code Quality Tools

### Required Tools

Install via `requirements-dev.txt`:

```txt
# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0

# Code Quality
black>=23.7.0          # Code formatter
isort>=5.12.0          # Import sorter
flake8>=6.1.0          # Linter
mypy>=1.5.0            # Type checker
pylint>=2.17.0         # Code analyzer

# Development
ipython>=8.14.0
jupyter>=1.0.0
```

### Tool Configurations

#### Black (Code Formatter)

```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''
```

**Usage**:
```bash
black src/ test/
```

#### isort (Import Sorter)

```toml
# pyproject.toml
[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
```

**Usage**:
```bash
isort src/ test/
```

#### mypy (Type Checker)

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
```

**Usage**:
```bash
mypy src/
```

#### flake8 (Linter)

```ini
# .flake8
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    .venv,
    build,
    dist
```

**Usage**:
```bash
flake8 src/
```

#### pylint (Code Analyzer)

```toml
# pyproject.toml
[tool.pylint.messages_control]
max-line-length = 100
disable = [
    "C0111",  # missing-docstring (we use type hints)
    "R0903",  # too-few-public-methods (dataclasses)
]

[tool.pylint.basic]
good-names = ["i", "j", "k", "df", "id"]
```

**Usage**:
```bash
pylint src/
```

## Pre-commit Workflow

Run before each commit:

```bash
#!/bin/bash
# scripts/pre-commit.sh

echo "🔍 Running code quality checks..."

# Format code
echo "📝 Formatting with black..."
black src/ test/
isort src/ test/

# Type checking
echo "🔎 Type checking with mypy..."
mypy src/ || exit 1

# Linting
echo "🧹 Linting with flake8..."
flake8 src/ || exit 1

echo "🔬 Analyzing with pylint..."
pylint src/ || exit 1

# Testing
echo "🧪 Running tests..."
pytest --cov=src --cov-fail-under=80 || exit 1

echo "✅ All checks passed!"
```

**Usage**:
```bash
chmod +x scripts/pre-commit.sh
./scripts/pre-commit.sh
```

## Documentation Standards

### Docstring Format

Use Google-style docstrings:

```python
def calculate_portfolio_value(
    cash: float,
    holdings: Dict[str, int],
    valuations: Dict[str, float]
) -> float:
    """Calculate total portfolio value.
    
    Combines available cash with the current market value of all
    held assets to determine total portfolio worth.
    
    Args:
        cash: Available cash in FSB
        holdings: Map of asset_id to quantity owned
        valuations: Map of asset_id to current valuation
    
    Returns:
        Total portfolio value (cash + asset values)
    
    Raises:
        ValueError: If holdings contain assets not in valuations
        
    Example:
        >>> calculate_portfolio_value(
        ...     cash=500000,
        ...     holdings={"asset_1": 1},
        ...     valuations={"asset_1": 150000}
        ... )
        650000
    """
    if not all(asset_id in valuations for asset_id in holdings):
        raise ValueError("Holdings contain assets without valuations")
    
    asset_value = sum(
        holdings[asset_id] * valuations[asset_id]
        for asset_id in holdings
    )
    return cash + asset_value
```

### README.md Template

```markdown
# Quantmas Year X Solution

## Overview
Brief description of the problem and approach taken.

## Installation

### Prerequisites
- Python 3.11+
- pip

### Setup
\`\`\`bash
cd implementation
pip install -r requirements.txt
pip install -r requirements-dev.txt
\`\`\`

## Running the Solution

### Generate Output
\`\`\`bash
python -m src.main
\`\`\`

Output will be generated in `problems/year_X/output/`

### Run Tests
\`\`\`bash
pytest
\`\`\`

### Check Coverage
\`\`\`bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
\`\`\`

### Code Quality
\`\`\`bash
# Format
black src/ test/
isort src/ test/

# Type check
mypy src/

# Lint
flake8 src/
pylint src/
\`\`\`

## Algorithm

Describe your approach here:
- Data analysis findings
- Strategy chosen
- Optimization techniques
- Trade-offs made

## Results

Final score: X FSB

Key metrics:
- Number of trades: X
- Assets held at end: X
- Return on investment: X%
\`\`\`

## Coverage Report

Current test coverage: XX%

Run `pytest --cov=src --cov-report=html` to generate detailed report.
```

## Continuous Quality

### Coverage Tracking

Monitor coverage trends:

```bash
# Generate coverage badge
pytest --cov=src --cov-report=term-missing

# View detailed HTML report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Quality Metrics

Track these metrics:
- **Test Coverage**: ≥80% (mandatory)
- **Type Coverage**: 100% (all functions typed)
- **Pylint Score**: ≥8.0/10
- **Flake8**: 0 errors
- **Test Execution Time**: <10s for full suite

### Quality Checklist

Before considering code complete:

- [ ] All tests pass
- [ ] Coverage ≥80%
- [ ] All functions have type hints
- [ ] mypy passes with no errors
- [ ] flake8 passes with no errors
- [ ] pylint score ≥8.0
- [ ] All public functions documented
- [ ] README.md updated
- [ ] No commented-out code
- [ ] No debug print statements
