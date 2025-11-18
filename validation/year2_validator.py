"""
Year 2 trading strategy validator for Quantmas.
Implements Year 2 specific validation rules including tax mechanics.
Uses Year 1 rules where applicable by calling Year1Validator methods.
"""

from typing import Dict, Any, List, Set
import pandas as pd
from .year1_validator import Year1Validator
from .base_validator import BaseValidator, ValidationResult


class Year2Validator(BaseValidator):
    """Validator for Year 2 trading strategies with tax mechanics"""
    
    def get_config(self) -> Dict[str, Any]:
        """Return Year 2 specific configuration from centralized config"""
        from .config import get_year_config
        return get_year_config(2)
    
    def get_additional_data_files(self) -> List:
        """Year 2 requires tax_rates.csv in addition to base files"""
        from pathlib import Path
        return [self.data_dir / "tax_rates.csv"]
    
    def validate_format(self, trades: Dict[int, List[Dict[str, str]]]) -> ValidationResult:
        """Validate Year 2 format including new pay_tax action"""
        result = ValidationResult(True, "Year 2 format validation passed")
        
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
                
                # Validate Year 2 actions (buy, sell, pay_tax)
                if action_type not in ['buy', 'sell', 'pay_tax']:
                    result.add_error(f"Day {day}, action {i+1}: Invalid action type '{action_type}'. Must be 'buy', 'sell', or 'pay_tax'")
                    continue
                
                if not isinstance(asset_id, str) or not asset_id.startswith('asset_'):
                    result.add_error(f"Day {day}, action {i+1}: Invalid asset_id '{asset_id}'. Must be string starting with 'asset_'")
                    continue
        
        return result
    
    def simulate_trading(self, trades: Dict[int, List[Dict[str, str]]], previous_year_results: Dict[str, Any] = None) -> ValidationResult:
        """Simulate Year 2 trading with tax mechanics, starting from Year 1 results

        Args:
            trades: Dictionary of day to actions
            previous_year_results: Year 1 results containing final_cash, final_assets, starting_cash, final_portfolio_value
        """
        result = ValidationResult(True, "Year 2 trading simulation completed successfully")

        # Validate previous year results
        if previous_year_results is None:
            result.add_error("Year 2 requires Year 1 results to start simulation")
            return result

        # Load data
        assets, valuations, load_result = self.load_data()
        if not load_result.success:
            result.add_error("Failed to load trading data")
            return result

        # Load tax rates
        tax_rates, tax_load_result = self.load_tax_rates()
        if not tax_load_result.success:
            result.add_error("Failed to load tax rates data")
            return result

        # Create Year1Validator instance for reusing validation methods
        year1_validator = Year1Validator(1, self.base_path)

        # Create lookup dictionaries
        asset_lookup = {row['id']: row for _, row in assets.iterrows()}
        valuation_lookup = {}
        for _, row in valuations.iterrows():
            valuation_lookup[(row['asset_id'], row['day'])] = row['valuation']

        # Initialize trading state from Year 1 results
        cash = previous_year_results['final_cash']
        portfolio_assets = [asset['asset_id'] for asset in previous_year_results['final_assets']]
        portfolio = set(portfolio_assets)
        transaction_count = 0
        daily_values = []
        transaction_log = []
        
        # Tax tracking state - initialize for inherited assets
        asset_tax_state = {}
        for asset_id in portfolio:
            # Start tracking taxes from day 1 for inherited assets
            asset_tax_state[asset_id] = {'last_payment_day': 0, 'unpaid_tax': 0.0}
        
        print(f"📊 Starting Year 2 simulation from Year 1 ending state:")
        print(f"💰 Cash: {self.format_currency(cash)}")
        print(f"🏠 Portfolio: {len(portfolio)} assets")
        print(f"📈 Loaded {len(assets)} assets, {len(valuations)} valuations, and {len(tax_rates)} tax rate records")
        print()
        
        # Simulate each day
        for day in range(1, self.total_days + 1):
            # Calculate and accrue taxes for all owned assets
            tax_validation_result = self._accrue_daily_taxes(day, portfolio, asset_lookup, valuation_lookup, tax_rates, asset_tax_state)
            if not tax_validation_result.success:
                for error in tax_validation_result.errors:
                    result.add_error(error)
                return result
            
            # Process day's actions
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
                    
                    if action_type == 'buy':
                        # Use Year 1 purchase validation
                        asset_info = asset_lookup[asset_id]
                        current_valuation = valuation_lookup.get((asset_id, day))

                        validation_result = year1_validator.validate_purchase(day, asset_id, asset_info, current_valuation, cash, portfolio)
                        if not validation_result.success:
                            for error in validation_result.errors:
                                result.add_error(error)
                            return result
                        
                        # Execute purchase
                        cash -= current_valuation
                        portfolio.add(asset_id)
                        transaction_count += 1
                        
                        # Initialize tax tracking for this asset
                        asset_tax_state[asset_id] = {'last_payment_day': day, 'unpaid_tax': 0.0}
                        
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
                        # Year 2 allows selling and paying tax on same day
                        # Use Year 1 sale validation
                        validation_result = year1_validator.validate_sale(day, asset_id, portfolio)
                        if not validation_result.success:
                            for error in validation_result.errors:
                                result.add_error(error)
                            return result
                        
                        current_valuation = valuation_lookup.get((asset_id, day))
                        cash += current_valuation
                        portfolio.remove(asset_id)
                        transaction_count += 1
                        
                        # Remove from tax tracking (taxes are implicitly settled with sale)
                        if asset_id in asset_tax_state:
                            del asset_tax_state[asset_id]
                        
                        action_desc = f"sold {asset_id} for {self.format_currency(current_valuation)}"
                        day_actions.append(action_desc)
                        transaction_log.append({
                            'day': day,
                            'action': 'sell',
                            'asset_id': asset_id,
                            'amount': current_valuation,
                            'cash_after': cash
                        })
                    
                    elif action_type == 'pay_tax':
                        validation_result = self._validate_tax_payment(day, asset_id, portfolio, asset_tax_state, cash)
                        if not validation_result.success:
                            for error in validation_result.errors:
                                result.add_error(error)
                            return result
                        
                        # Calculate and pay tax
                        tax_owed = asset_tax_state[asset_id]['unpaid_tax']
                        cash -= tax_owed
                        asset_tax_state[asset_id]['unpaid_tax'] = 0.0
                        asset_tax_state[asset_id]['last_payment_day'] = day
                        transaction_count += 1
                        
                        action_desc = f"paid tax on {asset_id} for {self.format_currency(tax_owed)}"
                        day_actions.append(action_desc)
                        transaction_log.append({
                            'day': day,
                            'action': 'pay_tax',
                            'asset_id': asset_id,
                            'amount': tax_owed,
                            'cash_after': cash
                        })
                
                if day_actions:
                    print(", ".join(day_actions))
            
            # Calculate daily portfolio value (including unpaid tax liabilities)
            portfolio_value = cash
            total_unpaid_tax = 0
            for asset_id in portfolio:
                portfolio_value += valuation_lookup.get((asset_id, day), 0)
                total_unpaid_tax += asset_tax_state.get(asset_id, {}).get('unpaid_tax', 0)
            
            # Portfolio value for scoring purposes includes tax liability
            net_portfolio_value = portfolio_value - total_unpaid_tax
            daily_values.append(net_portfolio_value)
        
        # Final validation: All taxes must be paid by day 100
        final_validation_result = self._validate_final_tax_state(asset_tax_state)
        if not final_validation_result.success:
            for error in final_validation_result.errors:
                result.add_error(error)
            return result

        # Calculate final results (Year 2 specific - includes tax considerations)
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

        # Store results in validation result
        result.data = {
            'final_cash': cash,
            'final_portfolio_value': final_portfolio_value,
            'final_assets': final_assets,
            'transaction_count': transaction_count,
            'daily_values': daily_values,
            'transaction_log': transaction_log,
            'return_percentage': ((final_portfolio_value / self.starting_cash) - 1) * 100,
            'total_unpaid_tax': sum(state.get('unpaid_tax', 0) for state in asset_tax_state.values()),
            'year1_starting_cash': previous_year_results.get('starting_cash', self.starting_cash),
            'year1_ending_value': previous_year_results['final_portfolio_value']
        }
        
        return result
    
    def load_tax_rates(self):
        """Load tax rates data for Year 2"""
        result = ValidationResult(True, "Tax rates loaded successfully")
        
        try:
            tax_rates = pd.read_csv(self.data_dir / "tax_rates.csv")
            return tax_rates, result
        except Exception as e:
            result.add_error(f"Failed to load tax rates: {e}")
            return pd.DataFrame(), result
    
    def _accrue_daily_taxes(self, day: int, portfolio: Set[str], asset_lookup: dict,
                           valuation_lookup: dict, tax_rates: pd.DataFrame, asset_tax_state: dict) -> ValidationResult:
        """Calculate and accrue daily taxes for all owned assets

        Returns:
            ValidationResult: success=True if valid, success=False with error message if invalid
        """
        result = ValidationResult(True, "Tax accrual validation passed")

        for asset_id in portfolio:
            if asset_id in asset_tax_state:
                current_valuation = valuation_lookup.get((asset_id, day), 0)
                asset_info = asset_lookup[asset_id]

                # Get current tax rate for this asset type
                current_tax_rate = self._get_current_tax_rate(asset_info, day, tax_rates)

                # Calculate days since last payment
                days_since_payment = day - asset_tax_state[asset_id]['last_payment_day']

                # CRITICAL VALIDATION: Check 30-day payment limit
                if days_since_payment > 30:
                    result.add_error(f"Day {day}: Asset '{asset_id}' has exceeded 30-day tax payment limit ({days_since_payment} days since last payment)")
                    return result

                # Tax penalty starts on day 2, not day 1 (corrected per user feedback)
                penalty_days = max(0, days_since_payment - 1)

                # Calculate effective tax rate
                effective_rate = current_tax_rate['tax_rate'] + (current_tax_rate['base_rate_modifier'] * penalty_days)

                # Calculate daily tax
                daily_tax = current_valuation * effective_rate

                # Add to unpaid tax
                asset_tax_state[asset_id]['unpaid_tax'] += daily_tax

        return result
    
    def _get_current_tax_rate(self, asset_info: dict, day: int, tax_rates: pd.DataFrame) -> dict:
        """Get the current tax rate for an asset on a given day"""
        asset_type = asset_info['type']
        asset_sub_type = asset_info['sub_type']
        
        # Find the most recent tax rate that applies
        applicable_rates = tax_rates[
            (tax_rates['asset_type'] == asset_type) & 
            (tax_rates['asset_sub_type'] == asset_sub_type) & 
            (tax_rates['day'] <= day)
        ].sort_values('day', ascending=False)
        
        if len(applicable_rates) > 0:
            latest_rate = applicable_rates.iloc[0]
            return {
                'tax_rate': latest_rate['tax_rate'],
                'base_rate_modifier': latest_rate['base_rate_modifier']
            }
        else:
            # Fallback to default rates if no specific rate found
            return {'tax_rate': 0.001, 'base_rate_modifier': 0.0005}
    
    def _validate_tax_payment(self, day: int, asset_id: str, portfolio: Set[str],
                             asset_tax_state: dict, cash: float) -> ValidationResult:
        """Validate tax payment action

        Returns:
            ValidationResult: success=True if valid, success=False with error message if invalid
        """
        result = ValidationResult(True, "Tax payment validation passed")

        # Check if we own the asset
        if asset_id not in portfolio:
            result.add_error(f"Day {day}: Cannot pay tax on '{asset_id}' - not owned")
            return result

        # Check if there's tax to pay
        if asset_id not in asset_tax_state or asset_tax_state[asset_id]['unpaid_tax'] <= 0:
            result.add_error(f"Day {day}: No taxes owed on '{asset_id}'")
            return result

        # Check if we have enough cash
        tax_owed = asset_tax_state[asset_id]['unpaid_tax']
        if cash < tax_owed:
            result.add_error(f"Day {day}: Insufficient funds to pay tax on '{asset_id}' (need {self.format_currency(tax_owed)}, have {self.format_currency(cash)})")
            return result

        # Check 30-day payment limit
        days_since_payment = day - asset_tax_state[asset_id]['last_payment_day']
        if days_since_payment > 30:
            result.add_error(f"Day {day}: Tax payment on '{asset_id}' is overdue (last payment {days_since_payment} days ago, maximum 30 days allowed)")
            return result

        return result

    def _validate_final_tax_state(self, asset_tax_state: dict) -> ValidationResult:
        """Validate that all taxes are paid by the end

        Returns:
            ValidationResult: success=True if all taxes paid, success=False with error message if unpaid taxes remain
        """
        result = ValidationResult(True, "Final tax state validation passed")

        unpaid_assets = []
        for asset_id, state in asset_tax_state.items():
            if state['unpaid_tax'] > 0.01:  # Small tolerance for rounding
                unpaid_assets.append(f"{asset_id} ({self.format_currency(state['unpaid_tax'])})")

        if unpaid_assets:
            result.add_error(f"Day {self.total_days}: Unpaid taxes remaining: {', '.join(unpaid_assets)}. All taxes must be paid by day {self.total_days}.")
            return result

        return result