# Project Structure

## Directory Layout

```
/workspaces/quantmas/
├── implementation/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── models/              # Data models (dataclasses/Pydantic)
│   │   │   ├── __init__.py
│   │   │   ├── asset.py
│   │   │   └── portfolio.py
│   │   ├── services/            # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── data_loader.py
│   │   │   └── trading_engine.py
│   │   ├── strategies/          # Trading strategies
│   │   │   ├── __init__.py
│   │   │   └── optimizer.py
│   │   └── utils/               # Helper functions
│   │       ├── __init__.py
│   │       └── validators.py
│   ├── test/
│   │   ├── __init__.py
│   │   ├── conftest.py          # pytest fixtures
│   │   ├── test_models/
│   │   │   └── test_asset.py
│   │   ├── test_services/
│   │   │   └── test_data_loader.py
│   │   └── test_strategies/
│   │       └── test_optimizer.py
│   ├── docs/
│   │   ├── project-structure.md # This file
│   │   ├── quality-standards.md # Testing & tooling
│   │   ├── tdd-guide.md         # Red-Green-Refactor
│   │   ├── python-standards.md  # Coding conventions
│   │   └── workflow.md          # Problem-solving process
│   ├── requirements.txt         # Production dependencies
│   ├── requirements-dev.txt     # Development dependencies
│   ├── pyproject.toml           # Project configuration
│   ├── setup.py                 # Package setup
│   └── README.md                # How to run
├── problems/
│   └── year_X/
│       ├── data/                # Input CSV files
│       ├── output/              # Generated YAML/JSON
│       └── problem.md
└── .agent_log/
    └── 2025.log
```

## Module Organization

### models/
**Purpose**: Data structures and domain models

**Guidelines**:
- Use `@dataclass` for simple data containers
- Use Pydantic for validation-heavy models
- Type hints on all attributes
- Immutable where possible (`frozen=True`)

**Example**:
```python
# models/asset.py
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
```

### services/
**Purpose**: Business logic and core operations

**Guidelines**:
- Single responsibility per service
- Dependency injection for testability
- Clear interfaces
- No direct I/O in business logic (delegate to utils)

**Example**:
```python
# services/trading_engine.py
class TradingEngine:
    """Manages portfolio trading operations."""
    
    def __init__(self, initial_cash: float):
        self._cash = initial_cash
        self._holdings: Dict[str, int] = {}
    
    def buy_asset(self, asset_id: str, price: float, day: int) -> None:
        """Purchase an asset with validation."""
        ...
```

### strategies/
**Purpose**: Algorithm implementations

**Guidelines**:
- Strategy pattern for different approaches
- Easy to swap and compare
- Separate strategy logic from execution
- Document algorithm decisions

**Example**:
```python
# strategies/optimizer.py
class TradingOptimizer:
    """Implements trading strategy."""
    
    def generate_trades(self) -> List[Trade]:
        """Generate optimized trading strategy."""
        ...
```

### utils/
**Purpose**: Shared utilities and helpers

**Guidelines**:
- Pure functions where possible
- Well-tested helper functions
- No business logic
- Reusable across modules

**Example**:
```python
# utils/validators.py
def validate_trading_day(day: int) -> None:
    """Validate trading day is within valid range."""
    if not 1 <= day <= 100:
        raise ValueError(f"Invalid trading day: {day}")
```

## Test Organization

Tests mirror the source structure:

```
test/
├── test_models/
│   ├── test_asset.py
│   └── test_portfolio.py
├── test_services/
│   ├── test_data_loader.py
│   └── test_trading_engine.py
└── test_strategies/
    └── test_optimizer.py
```

**Guidelines**:
- One test file per source file
- Use `conftest.py` for shared fixtures
- Group related tests in classes
- Name tests descriptively: `test_<what>_<condition>_<expected>`

## Configuration Files

### requirements.txt
Production dependencies only:
```txt
pandas>=2.0.0
numpy>=1.24.0
pyyaml>=6.0
```

### requirements-dev.txt
Development and testing tools:
```txt
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.7.0
mypy>=1.5.0
```

### pyproject.toml
Project configuration for all tools:
```toml
[tool.pytest.ini_options]
testpaths = ["test"]
addopts = ["--cov=src", "--cov-fail-under=80"]

[tool.black]
line-length = 100
target-version = ['py311']

[tool.mypy]
python_version = "3.11"
disallow_untyped_defs = true
```

## File Naming Conventions

- **Source files**: `snake_case.py` (e.g., `data_loader.py`)
- **Test files**: `test_<module>.py` (e.g., `test_data_loader.py`)
- **Classes**: `PascalCase` (e.g., `TradingEngine`)
- **Functions/methods**: `snake_case` (e.g., `buy_asset`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `INITIAL_CASH`)

## Import Organization

Use `isort` with black profile:

```python
# Standard library
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Third-party
import pandas as pd
import numpy as np

# Local
from models.asset import Asset
from services.data_loader import DataLoader
```
