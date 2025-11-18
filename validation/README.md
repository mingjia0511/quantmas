# Quantmas Validation System

A modular Python validation framework for trading strategy submissions across multiple years of the Quantmas challenge.

## Features

- 🎯 **Modular Design**: Each year has its own validator that can inherit rules from previous years
- 🔗 **Rule Inheritance**: Year 2+ validators automatically inherit and enforce rules from previous years
- 📊 **Comprehensive Validation**: Format checking, business rule validation, and trading simulation
- 🎨 **Rich Output**: Colorful, detailed feedback with clear error messages
- 🔧 **Extensible**: Easy to add new years and validation rules

## Quick Start

### Install Requirements

```bash
pip install -r validation_requirements.txt
```

### Basic Usage

```bash
# Validate Year 1 submission
python3 test_and_submit.py 1

# Show available years
python3 test_and_submit.py --list

# Get help
python3 test_and_submit.py --help
```

### Advanced Usage

```bash
# Validate with custom base path
python3 test_and_submit.py 1 --base-path /path/to/project

# Enable debug output
python3 test_and_submit.py 1 --debug
```

## Architecture

### Core Components

- **`base_validator.py`**: Abstract base class with common validation logic
- **`year1_validator.py`**: Year 1 specific validation rules  
- **`config.py`**: Centralized configuration for all years
- **`utils.py`**: Common utilities and helper functions
- **`test_and_submit.py`**: Main entry point and CLI interface

### Rule Inheritance

The system supports progressive rule inheritance:

```
Year 1: Base trading rules
Year 2: Year 1 rules + new Year 2 rules  
Year 3: Year 1 + Year 2 + new Year 3 rules
...and so on
```

Each year validator automatically inherits and enforces rules from all previous years.

## Directory Structure

```
validation/
├── __init__.py
├── base_validator.py      # Base validator class
├── year1_validator.py     # Year 1 implementation  
├── config.py             # Configuration settings
└── utils.py              # Utilities and helpers

test_and_submit.py        # Main CLI script
validation_requirements.txt  # Python dependencies
```

## Adding New Years

To add a new year (e.g., Year 2):

1. **Update config.py**: Add Year 2 configuration
2. **Create year2_validator.py**: Implement Year2Validator class
3. **Update config.py**: Mark Year 2 as implemented
4. **Test**: The inheritance system will automatically work

### Example Year 2 Validator

```python
from .year1_validator import Year1Validator

class Year2Validator(Year1Validator):
    def get_config(self):
        return {
            'starting_cash': 750000,  # Year 2 specific config
            'total_days': 150
        }
    
    def get_additional_data_files(self):
        return [
            self.data_dir / "tax_rates.csv"  # Year 2 specific file
        ]
    
    def simulate_trading(self, trades):
        # Call parent to get Year 1 validation
        result = super().simulate_trading(trades)
        if not result.success:
            return result
        
        # Add Year 2 specific logic here
        # ...
        
        return result
```

## Validation Process

1. **File Check**: Verifies all required files exist
2. **Data Loading**: Loads and parses output.yml and data files
3. **Inheritance Check**: Validates rules from previous years
4. **Format Validation**: Checks output format compliance
5. **Trading Simulation**: Simulates strategy and validates business rules
6. **Results**: Provides detailed feedback and final score

## Output Format

The validator produces rich, colorful output:

```
🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅
🎄 Quantmas Year 1 Submission Validation 🎄  
🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅🎅

🔧 Loading Year 1 validator...
📁 Working directory: /path/to/project
📊 Target: problems/year_1/

📊 Starting simulation with 500,000 FSB
📈 Loaded 15 assets and 1500 valuation records

Day 1: bought asset_6 for 438,129 FSB
Day 2: sold asset_6 for 445,200 FSB

🎯 FINAL RESULTS
========================================
Final Cash: 507,071 FSB
Final Portfolio Value: 507,071 FSB  
Total Transactions: 2
Return: 1.41%

✅ Year 1 validation completed successfully!
🎉 Your Year 1 submission is ready for the North Pole! 🎅
```

## Programmatic Usage

The system also provides a programmatic interface:

```python
from validation.utils import validate_year_programmatically

# Returns True/False
success = validate_year_programmatically(1, "/path/to/project")
```

## Migration from Bash Script

The original `test-and-submit.sh` has been replaced by this Python system. The bash script now shows migration instructions but can still be run with `--legacy` flag for backward compatibility.

## Requirements

- Python 3.7+
- pandas >= 1.3.0
- PyYAML >= 6.0
