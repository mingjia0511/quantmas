"""
Base validator class for Quantmas trading strategy submissions.
Provides common interface and shared functionality for year-specific validators.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import yaml
from pathlib import Path


class ValidationResult:
    """Container for validation results"""
    
    def __init__(self, success: bool, message: str = "", data: Optional[Dict[str, Any]] = None):
        self.success = success
        self.message = message
        self.data = data or {}
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def add_error(self, error: str):
        self.errors.append(error)
        self.success = False
    
    def add_warning(self, warning: str):
        self.warnings.append(warning)


class BaseValidator(ABC):
    """Base class for year-specific validators"""

    def __init__(self, year: int, base_path: Path):
        self.year = year
        self.base_path = Path(base_path)
        self.problem_dir = self.base_path / "problems" / f"year_{year}"
        self.data_dir = self.problem_dir / "data"
        self.output_dir = self.problem_dir / "output"

        # Will be set by config
        self.starting_cash = None
        self.total_days = None
    
    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """Return year-specific configuration"""
        pass
    
    @abstractmethod
    def validate_format(self, trades: Dict[int, List[Dict[str, str]]]) -> ValidationResult:
        """Validate the format of the output file"""
        pass
    
    @abstractmethod
    def simulate_trading(self, trades: Dict[int, List[Dict[str, str]]]) -> ValidationResult:
        """Simulate the trading strategy and validate business rules"""
        pass
    
    def get_additional_data_files(self) -> List[Path]:
        """Override in subclasses to specify additional data files beyond base requirements"""
        return []

    def check_files_exist(self) -> ValidationResult:
        """Check if required files exist"""
        result = ValidationResult(True, "File check passed")
        
        required_files = self.get_required_files()
        missing_files = []
        
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(str(file_path))
        
        if missing_files:
            result.success = False
            result.message = f"Missing required files: {', '.join(missing_files)}"
            
        return result
    
    def get_required_files(self) -> List[Path]:
        """Get list of required files for this year"""
        base_files = [
            self.output_dir / "output.yml",
            self.data_dir / "assets.csv",
            self.data_dir / "valuations.csv"
        ]
        # Add any additional files specified by the specific year validator
        additional_files = self.get_additional_data_files()
        return base_files + additional_files
    
    def load_output(self) -> Tuple[Dict[int, List[Dict[str, str]]], ValidationResult]:
        """Load and parse output.yml"""
        output_file = self.output_dir / "output.yml"
        result = ValidationResult(True, "Output loaded successfully")
        
        try:
            with open(output_file, 'r') as f:
                trades = yaml.safe_load(f) or {}
            return trades, result
        except yaml.YAMLError as e:
            result.add_error(f"Invalid YAML format: {e}")
            return {}, result
        except FileNotFoundError:
            result.add_error("output.yml not found")
            return {}, result
    
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, ValidationResult]:
        """Load assets and valuations data"""
        result = ValidationResult(True, "Data loaded successfully")
        
        try:
            assets = pd.read_csv(self.data_dir / "assets.csv")
            valuations = pd.read_csv(self.data_dir / "valuations.csv")
            return assets, valuations, result
        except Exception as e:
            result.add_error(f"Failed to load data: {e}")
            return pd.DataFrame(), pd.DataFrame(), result
    
    def format_currency(self, amount: float) -> str:
        """Format currency amounts consistently"""
        return f"{amount:,.0f} FSB"
    
    def print_results(self, validation_results: List[ValidationResult]):
        """Print formatted validation results"""
        print(f"\n🎯 YEAR {self.year} VALIDATION RESULTS")
        print("=" * 50)
        
        all_success = all(r.success for r in validation_results)
        
        for result in validation_results:
            if result.success:
                print(f"✅ {result.message}")
            else:
                print(f"❌ {result.message}")
                for error in result.errors:
                    print(f"   • {error}")
            
            for warning in result.warnings:
                print(f"⚠️  {warning}")
        
        # Print final results if simulation was successful
        simulation_result = None
        for result in validation_results:
            if hasattr(result, 'data') and 'final_portfolio_value' in result.data:
                simulation_result = result
                break
        
        if simulation_result and all_success:
            self._print_final_results(simulation_result.data)
        
        if all_success:
            print(f"\n🎉 Year {self.year} validation completed successfully!")
            print(f"Your Year {self.year} submission is ready for the North Pole! 🎅")
            return True
        else:
            print(f"\n❌ Year {self.year} validation failed. Please fix the issues above.")
            return False
    
    def _print_final_results(self, data: Dict[str, Any]):
        """Print detailed final results"""
        print()
        print("🎯 FINAL RESULTS")
        print("=" * 40)
        print(f"Final Cash: {self.format_currency(data['final_cash'])}")
        print(f"Final Portfolio Value: {self.format_currency(data['final_portfolio_value'])}")
        print(f"Total Transactions: {data['transaction_count']}")
        print(f"Return: {data['return_percentage']:.2f}%")
        
        if data['final_assets']:
            print("\n📋 Final Portfolio:")
            for asset in data['final_assets']:
                print(f"  • {asset['asset_id']} ({asset['name']}): {self.format_currency(asset['final_value'])}")
        else:
            print("\n📋 Final Portfolio: All cash, no assets")
        
        print(f"\nSCORE: {data['final_portfolio_value']}")
    
    def validate(self) -> bool:
        """Run complete validation for this year"""
        # Load configuration from centralized config system
        config = self.get_config()
        self.starting_cash = config.get('starting_cash')
        self.total_days = config.get('total_days')

        # Validate that required config values are set
        if self.starting_cash is None or self.total_days is None:
            config_error_result = ValidationResult(False, "Configuration error")
            config_error_result.add_error(
                f"Year {self.year} is missing required config values: "
                f"starting_cash={self.starting_cash}, total_days={self.total_days}"
            )
            return self.print_results([config_error_result])

        results = []

        # Check files exist
        file_result = self.check_files_exist()
        results.append(file_result)
        if not file_result.success:
            return self.print_results(results)

        # Load data
        trades, load_result = self.load_output()
        results.append(load_result)
        if not load_result.success:
            return self.print_results(results)

        # For Year N > 1, run Year N-1 validation first and get results
        previous_year_results = None
        if self.year > 1:
            previous_year_results = self._run_previous_year_validation()
            if previous_year_results is None:
                prev_year_error = ValidationResult(False, f"Year {self.year - 1} validation failed")
                prev_year_error.add_error(f"Year {self.year} requires Year {self.year - 1} to validate successfully first")
                results.append(prev_year_error)
                return self.print_results(results)

        # Validate format (current year's format rules)
        format_result = self.validate_format(trades)
        results.append(format_result)
        if not format_result.success:
            return self.print_results(results)

        # Simulate trading (pass previous year results if applicable)
        if self.year > 1:
            simulation_result = self.simulate_trading(trades, previous_year_results)
        else:
            simulation_result = self.simulate_trading(trades)
        results.append(simulation_result)

        return self.print_results(results)

    def _run_previous_year_validation(self) -> Optional[Dict[str, Any]]:
        """Run previous year validation and return results for sequential validation"""
        from .utils import load_validator_for_year

        try:
            prev_year = self.year - 1
            prev_validator = load_validator_for_year(prev_year, str(self.base_path))

            # Load previous year's config
            prev_config = prev_validator.get_config()
            prev_validator.starting_cash = prev_config.get('starting_cash')
            prev_validator.total_days = prev_config.get('total_days')

            if prev_validator.starting_cash is None or prev_validator.total_days is None:
                print(f"⚠️  Year {prev_year} config missing values")
                return None

            # Load previous year's output
            prev_trades, prev_load_result = prev_validator.load_output()
            if not prev_load_result.success:
                print(f"⚠️  Year {prev_year} output.yml not found or invalid")
                return None

            # Run previous year simulation
            print(f"📊 Running Year {prev_year} validation first...")
            prev_simulation = prev_validator.simulate_trading(prev_trades)
            if not prev_simulation.success:
                print(f"❌ Year {prev_year} validation failed")
                return None

            print(f"✅ Year {prev_year} validation successful\n")

            # Return data needed by next year
            return {
                'final_cash': prev_simulation.data['final_cash'],
                'final_assets': prev_simulation.data['final_assets'],
                'final_portfolio_value': prev_simulation.data['final_portfolio_value'],
                'starting_cash': prev_validator.starting_cash
            }

        except Exception as e:
            print(f"❌ Error running Year {self.year - 1} validation: {e}")
            return None