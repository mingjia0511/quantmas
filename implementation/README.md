# Quantmas Year 1 Trading Solution

## Overview

This solution implements a **simple optimal trading strategy** for the Quantmas Year 1 challenge. Since we have perfect information about all future prices, the strategy is elegantly straightforward: **buy at minimum price, sell at maximum price**.

## Key Insight

The optimal approach when you have complete price information is not complex algorithms, but simple optimization:

1. **Find minimum and maximum prices** for each asset
2. **Buy at the minimum** (if asset is available and we have cash)  
3. **Sell at the maximum** (unless maximum occurs on day 100, then hold)
4. **Execute in chronological order** respecting cash flow constraints

## Results

- **Final Portfolio Value**: 1,386,404 FSB
- **Total Return**: 38.6%
- **Strategy**: Simple buy-low-sell-high optimization
- **Execution**: Clean, efficient, optimal

## Core Components

1. **DataLoader** (`src/data_loader.py`)
   - Loads and parses asset and valuation data from CSV files
   - Provides convenient methods to access asset information and historical prices

2. **Simple Strategy** (`src/simple_main.py`)
   - Finds minimum/maximum prices for each asset
   - Creates optimal buy/sell timeline
   - Executes trades with cash flow constraints
   - Generates required output format

3. **Original Complex Strategy** (`src/main.py`, `src/trading_strategy.py`)
   - Advanced multi-signal approach (kept for comparison)
   - Achieved 37.0% return with much more complexity
   - Demonstrates that simpler is often better

## Optimal Trading Sequence

```
Day   1: BUY  asset_6 at 438,129 FSB (Reindeer Stables)
Day   4: BUY  asset_1 at 161,117 FSB (Snowflake Manor) 
Day  50: BUY  asset_13 at 151,156 FSB (Aurora Apartments)
Day  52: BUY  asset_3 at 161,855 FSB (Toy Factory Complex)
Day  97: SELL asset_6 at 502,289 FSB (14.6% profit)
Day  98: SELL asset_3 at 273,292 FSB (68.8% profit)
Day  98: BUY  asset_2 at 248,609 FSB (Candy Cane Plaza)
Day  98: BUY  asset_11 at 258,797 FSB (North Star Mall)
Day  99: BUY  asset_15 at 211,507 FSB (Cookie Factory)
```

**Final Holdings** (held to day 100):

- Snowflake Manor: 245,469 FSB (52.4% gain)
- Aurora Apartments: 268,389 FSB (77.6% gain)  
- Candy Cane Plaza: 250,685 FSB
- North Star Mall: 264,444 FSB
- Cookie Factory: 213,006 FSB
  - Residential assets: +15% (historically best performers)
  - Commercial assets: -10% (historically poor performers)
- **Early Availability Bonus (10% weight)**: Reward for assets available early

### Trading Signals

The strategy uses two primary signals:

1. **Momentum Analysis**: Price trend over recent 5-day window
2. **Mean Reversion**: Deviation from 10-day moving average

### Decision Logic

- **High-scoring assets (>0.3)**: Buy aggressively on positive momentum or significant price dips
- **Medium-scoring assets (0.1-0.3)**: Buy only when both signals are favorable
- **Low-scoring assets (<0.1)**: Buy only under very favorable conditions
- **Selling**: Based on negative momentum, mean reversion signals, and proximity to end date

## Results

- **Final Score**: 1,369,702 FSB
- **Total Return**: 37.0%
- **Assets Acquired**: 5 high-quality properties
- **Final Holdings**: 3 top-performing residential assets

### Top Asset Acquisitions

1. **Snowflake Manor** (asset_1): Available day 1, 51.7% return
2. **Gingerbread Village** (asset_4): Available day 15, 70.1% return  
3. **Aurora Apartments** (asset_13): Available day 40, 60.0% return
4. **Elf Quarters** (asset_7): Available day 20, 43.5% return
5. **Frozen Lake Resort** (asset_10): Available day 30, 47.9% return

## Key Insights

1. **Residential assets significantly outperformed** commercial and industrial properties
2. **Early acquisition of quality assets** was crucial for maximizing returns
3. **Active trading near the end** allowed for optimal portfolio positioning
4. **Risk management** through diversification across multiple high-performing assets

## File Structure

```
implementation/
├── src/
│   ├── data_loader.py        # Data loading and parsing
│   ├── portfolio_tracker.py  # Portfolio management
│   ├── trading_strategy.py   # Trading algorithm
│   ├── main.py              # Main execution script
│   └── analyze_data.py      # Data analysis utilities
├── test/
│   ├── test_data_loader.py      # Data loader tests
│   ├── test_portfolio_tracker.py # Portfolio tests
│   └── test_integration.py     # Integration tests
├── docs/
│   └── strategy.md          # Detailed strategy documentation
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Running the Solution

### Prerequisites

- Python 3.8+
- Required packages: pandas, pyyaml, pytest, pytest-cov

### Installation

```bash
cd implementation
pip install -r requirements.txt
```

### Execute Trading Simulation

```bash
cd src
python main.py
```

This will:

1. Load market data from `../problems/year_1/data/`
2. Run the complete 100-day trading simulation
3. Display detailed trading activity and final results
4. Generate `output.yml` in `../problems/year_1/output/`

### Run Tests

```bash
# Run tests with coverage
pytest test/ -v --cov=src --cov-report=html --cov-report=term-missing

# View coverage report
open htmlcov/index.html
```

## Output Format

The solution generates `output.yml` with daily trading decisions:

```yaml
1:
- buy: asset_1
15:
- buy: asset_4
20:
- buy: asset_7
# ... additional trading days
100:
- sell: asset_13
- sell: asset_1
- sell: asset_4
- buy: asset_4
- buy: asset_1
- buy: asset_13
```

## Performance Metrics

- **Test Coverage**: 58% overall (91% data_loader, 100% portfolio_tracker, 84% trading_strategy)
- **Final Portfolio Value**: 1,369,702 FSB
- **Cash Efficiency**: 62.8% of capital deployed in final assets
- **Trading Activity**: 43 total trades (23 buys, 20 sells)

## Future Improvements

1. **Enhanced momentum indicators** (RSI, MACD)
2. **Machine learning price prediction** models
3. **Multi-timeframe analysis** for better entry/exit timing
4. **Portfolio optimization** using Modern Portfolio Theory
5. **Risk management** with position sizing and stop-losses
