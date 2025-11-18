"""
Utility functions for the Quantmas validation system.
Provides common functionality used across validators.
"""

import importlib
from pathlib import Path
from typing import Type
from .base_validator import BaseValidator
from .config import get_year_config, get_implemented_years


def load_validator_for_year(year: int, base_path: str = ".") -> BaseValidator:
    """Dynamically load and instantiate the validator for a specific year"""
    if year not in get_implemented_years():
        raise ValueError(f"Year {year} validator is not yet implemented. Implemented years: {get_implemented_years()}")

    config = get_year_config(year)
    module_name = config['module']
    class_name = config['validator_class']

    try:
        # Import the module
        module = importlib.import_module(module_name)
        # Get the validator class
        validator_class: Type[BaseValidator] = getattr(module, class_name)
        # Instantiate with year and base path
        validator = validator_class(year, Path(base_path))

        return validator
    except (ImportError, AttributeError) as e:
        raise RuntimeError(f"Failed to load validator for year {year}: {e}")


def print_banner(year: int):
    """Print a festive banner for the validation"""
    print("🎅" * 20)
    print(f"🎄 Quantmas Year {year} Submission Validation 🎄")
    print("🎅" * 20)
    print()


def print_available_years():
    """Print information about available years"""
    implemented = get_implemented_years()
    print("Available validation years:")
    for year in range(1, 6):
        if year in implemented:
            print(f"  ✅ Year {year} - Ready")
        else:
            print(f"  🚧 Year {year} - Coming soon")
    print()


def format_validation_summary(success: bool, year: int):
    """Format a final validation summary"""
    if success:
        return f"""
✨ VALIDATION COMPLETE ✨
{'=' * 30}
🎉 Year {year} submission validation PASSED!
🚀 Your solution is ready for the North Pole!
🎅 Ho ho ho, well done!
"""
    else:
        return f"""
❌ VALIDATION FAILED ❌
{'=' * 30}
⚠️  Year {year} submission has issues that need fixing.
🔧 Please review the errors above and try again.
🎄 Don't give up - Santa believes in you!
"""