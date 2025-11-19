# Year 1 Implementation

## Quick Start

### Run the Solution

```bash
# Install dependencies
pip install -r requirements.txt

# Generate output
python -m src.main
```

Output will be generated at: `../../problems/year_1/output/output.yml`

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing
```

## Strategy

**Approach**: Buy top 5 assets by expected return, hold until day 100

**Transactions**: 5  
**Actual Return**: 47.32%

See `docs/strategy-decisions.md` for detailed strategy explanation.

## Documentation

- **`docs/strategy-decisions.md`** - Strategy rationale and trade-offs
- **`docs/development-process.md`** - Development workflow and lessons learned

## Project Structure

```
year_1/
├── src/                    # Source code
│   ├── data_loader.py      # CSV data loading
│   ├── portfolio.py        # Portfolio management
│   ├── strategy.py         # Trading strategy
│   ├── output_writer.py    # YAML output
│   └── main.py             # Entry point
├── tests/                  # Unit tests
├── docs/                   # Documentation
└── requirements.txt        # Dependencies
```

## Results

**Final Portfolio**:
- Cash: 176,181 FSB
- Assets: 5 (asset_1, asset_3, asset_4, asset_13, asset_14)
- Total Value: 1,473,231 FSB
- **Return: 47.32%**
