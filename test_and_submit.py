#!/usr/bin/env python3
"""
Quantmas Trading Strategy Validation System

A modular validation framework for trading strategy submissions across multiple years.
Validates output format, simulates trading, and provides detailed feedback.

Usage:
    python test_and_submit.py [year] [--base-path PATH]

Examples:
    python test_and_submit.py 1                    # Validate Year 1 in current directory
    python test_and_submit.py 2 --base-path /path  # Validate Year 2 with custom base path
"""

import argparse
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from validation.utils import (
    load_validator_for_year, 
    print_banner, 
    print_available_years,
    format_validation_summary
)
from validation.config import is_year_supported, get_implemented_years


def main():
    """Main entry point for the validation system"""
    parser = argparse.ArgumentParser(
        description="Quantmas Trading Strategy Validation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_and_submit.py 1                    # Validate Year 1
  python test_and_submit.py 2 --base-path /path  # Validate Year 2 with custom path
  python test_and_submit.py --list               # Show available years
        """
    )
    
    parser.add_argument(
        'year', 
        type=int, 
        nargs='?',
        help='Year to validate (1-5)'
    )
    
    parser.add_argument(
        '--base-path',
        default='.',
        help='Base path to the quantmas project directory (default: current directory)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available validation years and exit'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug output'
    )
    
    args = parser.parse_args()
    
    # Handle list option
    if args.list:
        print_available_years()
        return 0
    
    # Validate year argument
    if args.year is None:
        parser.print_help()
        print("\nError: Year argument is required (or use --list to see available years)")
        return 1
    
    year = args.year
    
    # Check if year is supported
    if not is_year_supported(year):
        print(f"❌ Error: Year {year} is not supported.")
        print_available_years()
        return 1
    
    # Check if year is implemented
    if year not in get_implemented_years():
        print(f"❌ Error: Year {year} validation is not yet implemented.")
        print_available_years()
        return 1
    
    # Validate base path
    base_path = Path(args.base_path).resolve()
    if not base_path.exists():
        print(f"❌ Error: Base path does not exist: {base_path}")
        return 1
    
    try:
        # Print banner
        print_banner(year)
        
        # Load and run validator
        print(f"🔧 Loading Year {year} validator...")
        validator = load_validator_for_year(year, base_path)
        
        print(f"📁 Working directory: {base_path}")
        print(f"📊 Target: problems/year_{year}/")
        print()
        
        # Run validation
        success = validator.validate()
        
        # Print summary
        print(format_validation_summary(success, year))
        
        # Return appropriate exit code
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Validation system error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


def validate_year_programmatically(year: int, base_path: str = ".") -> bool:
    """
    Programmatic interface for validation - useful for integration tests
    
    Args:
        year: Year to validate
        base_path: Path to quantmas project directory
        
    Returns:
        True if validation passed, False otherwise
    """
    try:
        validator = load_validator_for_year(year, base_path)
        return validator.validate()
    except Exception:
        return False


if __name__ == "__main__":
    sys.exit(main())