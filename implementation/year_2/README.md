# Year 2: Tax Optimization Solution

This directory contains the solution for Year 2 of the Quantmas Challenge, which introduces tax obligations on asset holdings.

## Quick Start

```bash
# Install dependencies
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# Run the solution
python3 -m src.main

# Run tests
./venv/bin/python -m pytest tests/ -v

# Check test coverage
./venv/bin/python -m pytest tests/ --cov=src --cov-report=term
```

## Results

**Final Portfolio Value**: $1,045,537.03  
**Total Return**: 4.55%  
**Total Taxes Paid**: $255,110.97  
**Assets Held**: 3 (asset_1, asset_4, asset_13)

## Strategy Overview

The Year 2 solution extends Year 1 with tax optimization:

### Key Approach

1. **Net Return Calculation**: Evaluates assets based on gross returns minus estimated tax burden
2. **Conservative Cash Reserve**: Maintains 35% cash reserve for tax payments
3. **Regular Tax Payments**: Pays taxes every 10 days to prevent excessive accumulation
4. **Buy-and-Hold**: Focuses on high net-return assets and holds them through day 100

### Tax Payment Strategy

- **Payment Interval**: Every 10 days
- **Maximum Delay**: 28 days (safety margin before 30-day limit)
- **Final Settlement**: All remaining taxes paid on day 100

### Why This Works

The tax formula `Daily Tax = Valuation × (Base Rate + Modifier × Days Since Last Payment)` creates quadratic growth in tax burden. By paying every 10 days:

- **10-day accumulation**: ~$2,750 tax on $500k asset
- **20-day accumulation**: ~$11,000 tax (4× more!)
- **30-day accumulation**: ~$24,750 tax (9× more!)

Regular payments minimize the quadratic penalty while preserving capital for returns.

## Project Structure

```
year_2/
├── src/
│   ├── __init__.py
│   ├── data_loader.py       # CSV loading utilities
│   ├── tax_calculator.py    # Tax calculation engine
│   ├── portfolio.py         # Portfolio with tax tracking
│   ├── strategy.py          # Tax-optimized trading strategy
│   ├── output_writer.py     # YAML output generation
│   └── main.py              # Entry point
├── tests/
│   ├── __init__.py
│   ├── test_tax_calculator.py    # Tax calculation tests
│   ├── test_portfolio.py         # Portfolio management tests
│   └── test_integration.py       # Integration tests
├── docs/
│   └── strategy-decisions.md     # Detailed strategy analysis
├── output.yml               # Final strategy output
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Key Components

### TaxCalculator
Implements the tax formula with time-varying rates:
```python
Daily Tax = Valuation × (Base Rate + Modifier × Days Since Last Payment)
```

Features:
- Handles rate changes at days 1, 25, 50, 75
- Cumulative tax calculation over periods
- Supports different asset sub-types (Residential, Commercial, Industrial)

### AssetTaxTracker
Tracks tax payment history for each owned asset:
- Last payment date
- Total taxes paid
- Payment history
- 30-day constraint checking

### Portfolio
Extends Year 1 portfolio with:
- Tax calculation and payment
- Tax obligation tracking
- Net value calculation (including unpaid tax penalties)
- Asset-level tax management

### TaxOptimizedStrategy
Implements the trading strategy:
- Net return evaluation (gross return - tax burden)
- Conservative cash management (35% reserve)
- Regular tax payment schedule (every 10 days)
- Final settlement on day 100

## Tax Rate Analysis

Tax rates increase over time, affecting strategy:

| Sub-Type    | Day 1 Base | Day 75 Base | Day 1 Modifier | Day 75 Modifier |
|-------------|------------|-------------|----------------|-----------------|
| Residential | 0.10%      | 0.13%       | 0.05%          | 0.065%          |
| Commercial  | 0.15%      | 0.18%       | 0.07%          | 0.085%          |
| Industrial  | 0.12%      | 0.15%       | 0.06%          | 0.075%          |

**Insight**: Residential assets have the lowest tax burden, making them attractive for long-term holds.

## Testing

The solution includes comprehensive tests:

- **Unit Tests**: Tax calculator, portfolio operations
- **Integration Tests**: Data loading, strategy execution, output generation
- **Coverage**: 83% (exceeds 80% requirement)

Run tests with:
```bash
./venv/bin/python -m pytest tests/ -v --cov=src
```

## Performance Metrics

| Metric                    | Value        |
|---------------------------|--------------|
| Initial Capital           | $1,000,000   |
| Final Portfolio Value     | $1,045,537   |
| Total Return              | 4.55%        |
| Assets Purchased          | 3            |
| Total Tax Payments        | 27           |
| Total Taxes Paid          | $255,111     |
| Cash Remaining            | $244,073     |
| Test Coverage             | 83%          |

## Design Decisions

### Why 35% Cash Reserve?

Initial testing with 20% reserve led to insufficient cash for final tax payments. 35% provides adequate buffer while still allowing meaningful asset purchases.

### Why 10-Day Payment Interval?

Balances two competing factors:
1. **Frequent payments** reduce quadratic tax accumulation
2. **Infrequent payments** preserve cash for returns

10 days is optimal: short enough to limit tax growth, long enough to maintain liquidity.

### Why Buy-and-Hold?

With tax obligations, frequent trading becomes expensive:
- Each sale triggers final tax payment
- Repurchasing starts new tax cycle
- Transaction costs (implicit in valuations) add up

Buy-and-hold minimizes these costs while capturing asset appreciation.

## Future Improvements

Potential enhancements for better returns:

1. **Dynamic Tax Scheduling**: Adjust payment frequency based on cash levels
2. **Asset Rebalancing**: Sell underperformers, buy better assets mid-period
3. **Tax Rate Arbitrage**: Favor Residential over Commercial/Industrial
4. **Valuation Forecasting**: Predict future valuations to optimize timing
5. **Multi-Objective Optimization**: Balance return, risk, and tax burden

## References

- Problem Statement: `../../problems/year_2/README.md`
- Strategy Analysis: `docs/strategy-decisions.md`
- Test Coverage Report: `htmlcov/index.html` (after running tests with coverage)
