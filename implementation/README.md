# Quantmas Year 1 Solution: Sleigh the Market

## Overview

This solution implements a **buy-and-hold strategy** for the Year 1 Quantmas challenge. The strategy identifies the top-performing real estate assets based on their day 1 to day 100 returns and purchases them as they become available, holding until the end of the trading period.

## Strategy

### Approach
- Analyze all 15 assets for profitability (day 1 → day 100 return %)
- Rank assets by return percentage
- Purchase top performers as they become available
- Hold all assets until day 100

### Selected Assets
1. **asset_1** (Day 1): 51.72% return
2. **asset_4** (Day 15): 70.09% return  
3. **asset_10** (Day 30): 47.85% return
4. **asset_13** (Day 40): 60.00% return
5. **asset_14** (Day 50): 51.44% return

### Results
- **Total Invested**: 889,682 FSB
- **Cash Remaining**: 110,318 FSB
- **Assets Value (Day 100)**: 1,326,619 FSB
- **Final Portfolio Value**: 1,436,937 FSB
- **Profit**: 436,937 FSB
- **Return**: 43.69%

## Installation

### Prerequisites
- Python 3.11+
- pip

### Setup
```bash
cd implementation
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running the Solution

### Generate Output
```bash
cd implementation
python -m src.main
```

Output will be generated in `problems/year_1/output/output.yml`

### Run Tests
```bash
cd implementation
pytest
```

### Check Coverage
```bash
cd implementation
pytest --cov=src --cov-report=html --cov-report=term-missing
```

View detailed report:
```bash
open htmlcov/index.html
```

### Code Quality Checks
```bash
cd implementation

# Format code
black src/ test/
isort src/ test/

# Type check
mypy src/

# Lint
flake8 src/
pylint src/
```

## Project Structure

```
implementation/
├── src/
│   ├── models/
│   │   └── asset.py              # Asset data model
│   ├── services/
│   │   ├── data_loader.py        # Data loading and validation
│   │   ├── trading_engine.py     # Portfolio management
│   │   └── output_generator.py   # YAML output generation
│   ├── strategies/
│   │   └── buy_and_hold_strategy.py  # Trading strategy
│   └── main.py                   # Entry point
├── test/
│   ├── test_models/
│   ├── test_services/
│   └── test_strategies/
├── docs/
│   ├── project-structure.md      # Architecture
│   ├── quality-standards.md      # Testing & tooling
│   ├── tdd-guide.md             # TDD workflow
│   ├── python-standards.md       # Coding conventions
│   ├── workflow.md              # Problem-solving process
│   └── strategy-analysis.md      # Strategy analysis
└── README.md                     # This file
```

## Algorithm Details

### Data Analysis
1. Load all assets and valuations from CSV files
2. Calculate return percentage for each asset: `(day100_price - day1_price) / day1_price * 100`
3. Sort assets by return percentage (descending)
4. Filter out assets with negative returns

### Trade Generation
1. Iterate through sorted assets
2. For each profitable asset:
   - Check if purchase price fits within remaining budget
   - If affordable, add buy trade on asset's `available_on_day`
   - Deduct price from available budget
3. Sort all trades by day

### Execution Simulation
1. Initialize trading engine with 1,000,000 FSB
2. Execute each trade in order
3. Calculate final portfolio value:
   - Sum of day 100 valuations for all held assets
   - Plus remaining cash

## Design Decisions

### Why Buy-and-Hold?
- Simplest strategy with strong returns
- Avoids transaction complexity
- Focuses on identifying fundamentally strong assets
- No need to time market entry/exit beyond availability

### Why These 5 Assets?
- All have positive returns (>40%)
- Diversified availability dates (days 1, 15, 30, 40, 50)
- Fit within budget constraints
- Collectively provide 43.69% return

### Trade-offs
- **Not considered**: Intra-period volatility, selling opportunities
- **Prioritized**: Simplicity, strong fundamentals, budget efficiency
- **Risk**: Concentrated in 5 assets (but all profitable)

## Testing

### Test Coverage
- **Data Loading**: Validates CSV parsing, column presence, caching
- **Asset Model**: Tests immutability, availability logic
- **Trading Engine**: Buy/sell operations, validation, portfolio calculation
- **Strategy**: Trade generation, budget constraints, sorting
- **Output**: YAML formatting, file creation

### Running Specific Tests
```bash
# Test data loader only
pytest test/test_services/test_data_loader.py -v

# Test strategy only
pytest test/test_strategies/test_buy_and_hold_strategy.py -v

# Test with coverage
pytest --cov=src --cov-report=term-missing
```

## Output Format

The solution generates `output.yml` in the required format:

```yaml
1:
- buy: asset_1
15:
- buy: asset_4
30:
- buy: asset_10
40:
- buy: asset_13
50:
- buy: asset_14
```

Each day maps to a list of actions (buy/sell) with asset IDs.

## Future Improvements

Potential enhancements for better returns:
1. **Active Trading**: Sell assets at local maxima, rebuy at local minima
2. **Volatility Analysis**: Identify swing trading opportunities
3. **Correlation Analysis**: Optimize portfolio diversification
4. **Dynamic Rebalancing**: Adjust holdings based on performance
5. **Risk Management**: Set stop-losses for underperforming assets

## References

- Problem Statement: `../problems/year_1/problem.md`
- Strategy Analysis: `docs/strategy-analysis.md`
- TDD Guide: `docs/tdd-guide.md`
- Python Standards: `docs/python-standards.md`
