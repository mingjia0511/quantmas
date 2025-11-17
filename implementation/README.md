# Quantmas Year 1 Trading Solution

## Overview

This solution implements an intelligent trading system for the Quantmas Year 1 challenge. The system analyzes North Pole real estate assets and makes strategic buy/sell decisions to maximize portfolio value over 100 trading days.

## Solution Architecture

### Core Components

1. **DataLoader** (`src/data_loader.py`)
   - Loads and parses asset and valuation data from CSV files
   - Provides convenient methods to access asset information and historical prices
   - Handles data validation and error cases

2. **PortfolioTracker** (`src/portfolio_tracker.py`)
   - Tracks cash balance and owned assets
   - Validates trading rules (sufficient funds, asset availability, ownership constraints)
   - Records all trading activity and generates output in required format

3. **TradingStrategy** (`src/trading_strategy.py`)
   - Implements advanced trading algorithm based on multiple signals
   - Ranks assets by attractiveness using composite scoring
   - Makes buy/sell decisions using momentum and mean reversion analysis

4. **Main Execution** (`src/main.py`)
   - Orchestrates the complete trading simulation
   - Runs day-by-day trading decisions for 100 days
   - Generates final results and output file

## Trading Strategy

### Asset Ranking System

Assets are scored based on multiple factors:

- **Total Return (40% weight)**: End-to-end price performance
- **Max Gain Potential (25% weight)**: Highest achievable return during the period  
- **Volatility Penalty (10% weight)**: Risk adjustment for price stability
- **Asset Type Bonus (15% weight)**:
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
