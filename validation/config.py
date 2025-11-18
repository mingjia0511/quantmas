"""
Configuration module for Quantmas validation system.
Centralizes year-specific settings and constants.
"""

from typing import Dict, Any

# Global constants
DEFAULT_BASE_PATH = "."
SUPPORTED_YEARS = [1, 2, 3, 4, 5]

# Year-specific configurations
YEAR_CONFIGS: Dict[int, Dict[str, Any]] = {
    1: {
        'starting_cash': 1000000,
        'total_days': 100,
        'validator_class': 'Year1Validator',
        'module': 'validation.year1_validator'
    },
    # Future years will be added here
    2: {
        'starting_cash': 1000000,  # Same as Year 1 for now - can be adjusted
        'total_days': 100,         # Same structure as Year 1
        'validator_class': 'Year2Validator',
        'module': 'validation.year2_validator'
    },
    3: {
        'starting_cash': None,  # TBD
        'total_days': None,     # TBD
        'validator_class': 'Year3Validator',
        'module': 'validation.year3_validator'
    },
    4: {
        'starting_cash': None,  # TBD
        'total_days': None,     # TBD
        'validator_class': 'Year4Validator',
        'module': 'validation.year4_validator'
    },
    5: {
        'starting_cash': None,  # TBD
        'total_days': None,     # TBD
        'validator_class': 'Year5Validator',
        'module': 'validation.year5_validator'
    }
}

def get_year_config(year: int) -> Dict[str, Any]:
    """Get configuration for a specific year"""
    if year not in YEAR_CONFIGS:
        raise ValueError(f"Year {year} is not supported. Supported years: {SUPPORTED_YEARS}")
    return YEAR_CONFIGS[year].copy()

def is_year_supported(year: int) -> bool:
    """Check if a year is supported"""
    return year in SUPPORTED_YEARS

def get_implemented_years() -> list:
    """Get list of years with implemented validators"""
    # Year 1 and Year 2 are now implemented
    return [1, 2]