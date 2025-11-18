"""
Year 1 trading strategy validator for Quantmas.
Implements specific validation rules and simulation logic for Year 1 challenges.
"""

from typing import Dict, Any, List
import pandas as pd
from .base_validator import BaseValidator, ValidationResult
from .config import get_year_config


class Year1Validator(BaseValidator):
    """Validator for Year 1 trading strategies"""
    
    def get_config(self) -> Dict[str, Any]:
        """Return Year 1 specific configuration from centralized config"""
        return get_year_config(1)
    
    def validate_format(self, trades: Dict[int, List[Dict[str, str]]]) -> ValidationResult:
        """Validate the format of Year 1 output file"""
        result = ValidationResult(True, "Format validation passed")
        
        if not isinstance(trades, dict):
            result.add_error("Output must be a dictionary with day numbers as keys")
            return result
        
        for day, actions in trades.items():
            if not isinstance(day, int) or day < 1 or day > self.total_days:
                result.add_error(f"Invalid day: {day}. Must be integer between 1 and {self.total_days}")
                continue
            
            if not isinstance(actions, list):
                result.add_error(f"Day {day}: Actions must be a list")
                continue
            
            for i, action in enumerate(actions):
                if not isinstance(action, dict):
                    result.add_error(f"Day {day}, action {i+1}: Each action must be a dictionary")
                    continue
                
                if len(action) != 1:
                    result.add_error(f"Day {day}, action {i+1}: Each action must have exactly one key-value pair")
                    continue
                
                action_type = list(action.keys())[0]
                asset_id = list(action.values())[0]
                
                if action_type not in ['buy', 'sell']:
                    result.add_error(f"Day {day}, action {i+1}: Invalid action type '{action_type}'. Must be 'buy' or 'sell'")
                    continue
                
                if not isinstance(asset_id, str) or not asset_id.startswith('asset_'):
                    result.add_error(f"Day {day}, action {i+1}: Invalid asset_id '{asset_id}'. Must be string starting with 'asset_'")
                    continue
        
        return result
    
    def simulate_trading(self, trades: Dict[int, List[Dict[str, str]]]) -> ValidationResult:
        """Simulate Year 1 trading strategy and validate business rules"""
        result = ValidationResult(True, "Trading simulation completed")
        
        # Load data
        assets, valuations, load_result = self.load_data()
        if not load_result.success:
            result.add_error("Failed to load trading data")
            return result
        
        # Create lookup dictionaries
        asset_lookup = {row['id']: row for _, row in assets.iterrows()}
        valuation_lookup = {}
        for _, row in valuations.iterrows():
            valuation_lookup[(row['asset_id'], row['day'])] = row['valuation']
        
        # Initialize trading state
        cash = self.starting_cash
        portfolio = set()
        transaction_count = 0
        daily_values = []
        transaction_log = []
        
        print(f"📊 Starting simulation with {self.format_currency(cash)}")
        print(f"📈 Loaded {len(assets)} assets and {len(valuations)} valuation records")
        print()
        
        # Simulate each day
        for day in range(1, self.total_days + 1):
            if day in trades:
                print(f"Day {day}:", end=" ")
                day_actions = []
                
                for action in trades[day]:
                    action_type = list(action.keys())[0]
                    asset_id = list(action.values())[0]
                    
                    # Validate asset exists
                    if asset_id not in asset_lookup:
                        result.add_error(f"Day {day}: Unknown asset '{asset_id}'")
                        return result
                    
                    asset_info = asset_lookup[asset_id]
                    current_valuation = valuation_lookup.get((asset_id, day))
                    
                    if current_valuation is None:
                        result.add_error(f"Day {day}: No valuation data for '{asset_id}' on day {day}")
                        return result
                    
                    if action_type == 'buy':
                        # Validate purchase
                        validation_result = self.validate_purchase(day, asset_id, asset_info, current_valuation, cash, portfolio)
                        if not validation_result.success:
                            for error in validation_result.errors:
                                result.add_error(error)
                            return result

                        # Execute purchase
                        cash -= current_valuation
                        portfolio.add(asset_id)
                        transaction_count += 1
                        action_desc = f"bought {asset_id} for {self.format_currency(current_valuation)}"
                        day_actions.append(action_desc)
                        transaction_log.append({
                            'day': day,
                            'action': 'buy',
                            'asset_id': asset_id,
                            'amount': current_valuation,
                            'cash_after': cash
                        })

                    elif action_type == 'sell':
                        # Validate sale
                        validation_result = self.validate_sale(day, asset_id, portfolio)
                        if not validation_result.success:
                            for error in validation_result.errors:
                                result.add_error(error)
                            return result
                        
                        # Execute sale
                        cash += current_valuation
                        portfolio.remove(asset_id)
                        transaction_count += 1
                        action_desc = f"sold {asset_id} for {self.format_currency(current_valuation)}"
                        day_actions.append(action_desc)
                        transaction_log.append({
                            'day': day,
                            'action': 'sell',
                            'asset_id': asset_id,
                            'amount': current_valuation,
                            'cash_after': cash
                        })
                
                if day_actions:
                    print(", ".join(day_actions))
            
            # Calculate daily portfolio value
            portfolio_value = cash
            for asset_id in portfolio:
                portfolio_value += valuation_lookup.get((asset_id, day), 0)
            daily_values.append(portfolio_value)
        
        # Calculate final results
        final_results = self.calculate_final_results(cash, portfolio, asset_lookup, valuation_lookup)
        
        # Store results in validation result
        result.data = {
            'final_cash': final_results['final_cash'],
            'final_portfolio_value': final_results['final_portfolio_value'],
            'final_assets': final_results['final_assets'],
            'transaction_count': transaction_count,
            'daily_values': daily_values,
            'transaction_log': transaction_log,
            'return_percentage': ((final_results['final_portfolio_value'] / self.starting_cash) - 1) * 100
        }
        
        # Store final results for printing by base validator
        result.message = "Trading simulation completed successfully"
        
        return result
    
    def validate_purchase(self, day: int, asset_id: str, asset_info: dict, current_valuation: float, cash: float, portfolio: set) -> ValidationResult:
        """Validate a purchase action.

        Returns:
            ValidationResult: success=True if valid, success=False with error message if invalid
        """
        result = ValidationResult(True, "Purchase validation passed")

        # Check if asset is available
        if day < asset_info['available_on_day']:
            result.add_error(f"Day {day}: Asset '{asset_id}' not available until day {asset_info['available_on_day']}")
            return result

        # Check if we already own it
        if asset_id in portfolio:
            result.add_error(f"Day {day}: Cannot buy '{asset_id}' - already owned")
            return result

        # Check if we have enough cash
        if cash < current_valuation:
            result.add_error(f"Day {day}: Insufficient funds to buy '{asset_id}' (need {self.format_currency(current_valuation)}, have {self.format_currency(cash)})")
            return result

        return result
    
    def validate_sale(self, day: int, asset_id: str, portfolio: set) -> ValidationResult:
        """Validate a sale action.

        Returns:
            ValidationResult: success=True if valid, success=False with error message if invalid
        """
        result = ValidationResult(True, "Sale validation passed")

        # Check if we own it
        if asset_id not in portfolio:
            result.add_error(f"Day {day}: Cannot sell '{asset_id}' - not owned")
            return result

        return result
    
    def calculate_final_results(self, cash: float, portfolio: set, asset_lookup: dict, valuation_lookup: dict) -> dict:
        """Calculate final portfolio value and asset breakdown"""
        final_portfolio_value = cash
        final_assets = []
        
        for asset_id in portfolio:
            final_valuation = valuation_lookup.get((asset_id, self.total_days), 0)
            final_portfolio_value += final_valuation
            final_assets.append({
                'asset_id': asset_id,
                'name': asset_lookup[asset_id]['name'],
                'final_value': final_valuation
            })
        
        return {
            'final_cash': cash,
            'final_portfolio_value': final_portfolio_value,
            'final_assets': final_assets
        }