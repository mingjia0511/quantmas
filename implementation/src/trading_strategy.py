"""
Trading strategy module for Quantmas Year 1 challenge.
Implements intelligent trading decisions based on market analysis.
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from data_loader import DataLoader
from portfolio_tracker import PortfolioTracker


class TradingStrategy:
    """Advanced trading strategy based on momentum, mean reversion, and value analysis."""
    
    def __init__(self, data_loader: DataLoader, portfolio: PortfolioTracker):
        """Initialize strategy with data loader and portfolio tracker."""
        self.data_loader = data_loader
        self.portfolio = portfolio
        self.asset_rankings = {}
        self._analyze_assets()
    
    def _analyze_assets(self):
        """Pre-analyze all assets to rank them by attractiveness."""
        all_assets = self.data_loader.get_all_assets()
        
        for asset_id in all_assets:
            asset_info = self.data_loader.get_asset_info(asset_id)
            price_history = self.data_loader.get_asset_price_history(asset_id)
            
            # Calculate performance metrics
            start_price = price_history['valuation'].iloc[0]
            end_price = price_history['valuation'].iloc[-1]
            max_price = price_history['valuation'].max()
            min_price = price_history['valuation'].min()
            
            total_return = (end_price - start_price) / start_price
            max_gain_potential = (max_price - start_price) / start_price
            volatility = price_history['valuation'].std() / price_history['valuation'].mean()
            
            # Score based on multiple factors
            score = self._calculate_asset_score(
                total_return, max_gain_potential, volatility,
                asset_info['sub_type'], asset_info['available_on_day']
            )
            
            self.asset_rankings[asset_id] = {
                'score': score,
                'total_return': total_return,
                'max_gain_potential': max_gain_potential,
                'volatility': volatility,
                'available_day': asset_info['available_on_day'],
                'sub_type': asset_info['sub_type'],
                'start_price': start_price,
                'end_price': end_price,
                'max_price': max_price,
                'min_price': min_price
            }
    
    def _calculate_asset_score(self, total_return: float, max_gain_potential: float, 
                              volatility: float, sub_type: str, available_day: int) -> float:
        """Calculate composite score for asset attractiveness."""
        score = 0.0
        
        # Heavily weight total return (40%)
        score += total_return * 0.4
        
        # Reward high gain potential (25%)
        score += max_gain_potential * 0.25
        
        # Slightly penalize volatility (10%)
        score -= volatility * 0.1
        
        # Bonus for residential assets (15%)
        if sub_type == "Residential":
            score += 0.15
        elif sub_type == "Commercial":
            score -= 0.1  # Penalty for poor performing commercial
        
        # Bonus for early availability (10%)
        early_availability_bonus = max(0, (20 - available_day) / 20 * 0.1)
        score += early_availability_bonus
        
        return score
    
    def _calculate_momentum(self, asset_id: str, current_day: int, window: int = 5) -> float:
        """Calculate price momentum over recent days."""
        if current_day < window:
            return 0.0
        
        try:
            recent_prices = []
            for day in range(max(1, current_day - window + 1), current_day + 1):
                price = self.data_loader.get_asset_valuation(asset_id, day)
                recent_prices.append(price)
            
            if len(recent_prices) < 2:
                return 0.0
            
            # Calculate price change rate
            momentum = (recent_prices[-1] - recent_prices[0]) / recent_prices[0]
            return momentum
        except ValueError:
            return 0.0
    
    def _calculate_mean_reversion_signal(self, asset_id: str, current_day: int) -> float:
        """Calculate mean reversion signal (buy when below average, sell when above)."""
        try:
            price_history = self.data_loader.get_asset_price_history(asset_id, current_day)
            if len(price_history) < 10:
                return 0.0
            
            current_price = self.data_loader.get_asset_valuation(asset_id, current_day)
            recent_mean = price_history['valuation'].tail(10).mean()
            
            # Signal strength based on deviation from mean
            deviation = (current_price - recent_mean) / recent_mean
            return -deviation  # Negative when price is high (sell signal), positive when low (buy signal)
        
        except ValueError:
            return 0.0
    
    def _should_buy_asset(self, asset_id: str, current_day: int) -> bool:
        """Determine if we should buy a specific asset."""
        try:
            asset_info = self.data_loader.get_asset_info(asset_id)
            current_price = self.data_loader.get_asset_valuation(asset_id, current_day)
            
            # Check basic constraints
            if not self.portfolio.can_buy(asset_id, current_price, asset_info['available_on_day'], current_day):
                return False
            
            # Get asset ranking
            asset_data = self.asset_rankings[asset_id]
            
            # Don't buy if overall score is negative
            if asset_data['score'] < 0:
                return False
            
            # Calculate signals
            momentum = self._calculate_momentum(asset_id, current_day)
            mean_reversion = self._calculate_mean_reversion_signal(asset_id, current_day)
            
            # For high-scoring assets, buy more aggressively
            if asset_data['score'] > 0.3:
                # Buy if momentum is positive or if price is significantly below average
                return momentum > -0.02 or mean_reversion > 0.05
            
            # For medium-scoring assets, be more selective
            elif asset_data['score'] > 0.1:
                # Buy if both momentum and mean reversion are favorable
                return momentum > 0.01 and mean_reversion > 0.03
            
            # For low-scoring assets, only buy if very favorable conditions
            else:
                return momentum > 0.03 and mean_reversion > 0.1
            
        except (ValueError, KeyError):
            return False
    
    def _should_sell_asset(self, asset_id: str, current_day: int) -> bool:
        """Determine if we should sell a specific asset."""
        if not self.portfolio.can_sell(asset_id):
            return False
        
        try:
            asset_data = self.asset_rankings[asset_id]
            current_price = self.data_loader.get_asset_valuation(asset_id, current_day)
            
            # Calculate signals
            momentum = self._calculate_momentum(asset_id, current_day)
            mean_reversion = self._calculate_mean_reversion_signal(asset_id, current_day)
            
            # Sell if close to end and we have gains to lock in
            days_remaining = 100 - current_day
            if days_remaining <= 5:
                return True  # Sell everything near the end
            
            # For poor-performing assets, sell quickly
            if asset_data['score'] < -0.1:
                return momentum < -0.01 or mean_reversion < -0.03
            
            # For good assets, hold unless momentum turns very negative
            if asset_data['score'] > 0.3:
                return momentum < -0.05 and mean_reversion < -0.1
            
            # For medium assets, sell on moderate negative signals
            return momentum < -0.03 and mean_reversion < -0.05
            
        except (ValueError, KeyError):
            return False
    
    def make_trading_decisions(self, current_day: int) -> List[Tuple[str, str]]:
        """Make trading decisions for the current day."""
        decisions = []
        
        # Get available assets for today
        available_assets = self.data_loader.get_available_assets(current_day)
        
        # Sort assets by score for prioritization
        sorted_assets = sorted(
            available_assets, 
            key=lambda x: self.asset_rankings.get(x, {}).get('score', -1), 
            reverse=True
        )
        
        # First, consider selling owned assets
        for asset_id in list(self.portfolio.owned_assets):
            if self._should_sell_asset(asset_id, current_day):
                try:
                    price = self.data_loader.get_asset_valuation(asset_id, current_day)
                    self.portfolio.sell_asset(asset_id, price, current_day)
                    decisions.append(('sell', asset_id))
                except ValueError:
                    continue
        
        # Then consider buying new assets
        for asset_id in sorted_assets:
            if asset_id not in self.portfolio.owned_assets and self._should_buy_asset(asset_id, current_day):
                try:
                    price = self.data_loader.get_asset_valuation(asset_id, current_day)
                    if self.portfolio.cash >= price:
                        self.portfolio.buy_asset(asset_id, price, current_day)
                        decisions.append(('buy', asset_id))
                        
                        # Limit to a few purchases per day to preserve cash
                        if len([d for d in decisions if d[0] == 'buy']) >= 3:
                            break
                except ValueError:
                    continue
        
        return decisions
    
    def get_asset_rankings(self) -> Dict:
        """Get the asset rankings for analysis."""
        return self.asset_rankings