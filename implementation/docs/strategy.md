# Simple Optimal Trading Strategy

## The Key Insight

Since we have **perfect information** about all future prices, the optimal strategy is elegantly simple:

**Buy at minimum price, sell at maximum price** for each profitable asset.

This straightforward approach achieves **1,386,404 FSB (38.6% return)**, outperforming complex multi-signal strategies.

## Algorithm

```
For each asset:
1. Find the minimum price and day it occurs
2. Find the maximum price and day it occurs  
3. If minimum day >= availability day AND maximum price > minimum price:
   - Buy on minimum day
   - Sell on maximum day (unless maximum is day 100, then hold)
4. Prioritize trades by profit percentage
5. Execute in chronological order with cash constraints
```

## Optimal Trade Sequence

| Asset | Name | Buy Day | Buy Price | Sell Day | Sell Price | ROI |
|-------|------|---------|-----------|----------|------------|-----|
| asset_13 | Aurora Apartments | 50 | 151,156 | HOLD | 268,389 | 77.6% |
| asset_3 | Toy Factory Complex | 52 | 161,855 | 98 | 273,292 | 68.8% |
| asset_15 | Cookie Factory | 99 | 211,507 | 19 | 343,288 | 62.3% |
| asset_2 | Candy Cane Plaza | 98 | 248,609 | 25 | 388,723 | 56.4% |
| asset_1 | Snowflake Manor | 4 | 161,117 | HOLD | 245,469 | 52.4% |
| asset_11 | North Star Mall | 98 | 258,797 | 22 | 392,265 | 51.6% |
| asset_6 | Reindeer Stables | 1 | 438,129 | 97 | 502,289 | 14.6% |

*Note: Some trades couldn't be executed due to timing or cash constraints*

## Execution Timeline

```
Day   1: BUY  asset_6 at 438,129 FSB (Cash: 561,871)
Day   4: BUY  asset_1 at 161,117 FSB (Cash: 400,754) 
Day  50: BUY  asset_13 at 151,156 FSB (Cash: 249,598)
Day  52: BUY  asset_3 at 161,855 FSB (Cash: 87,743)
Day  97: SELL asset_6 at 502,289 FSB (Cash: 590,032)
Day  98: SELL asset_3 at 273,292 FSB (Cash: 863,324)
Day  98: BUY  asset_2 at 248,609 FSB (Cash: 614,715)
Day  98: BUY  asset_11 at 258,797 FSB (Cash: 355,918)
Day  99: BUY  asset_15 at 211,507 FSB (Cash: 144,411)
```

## Final Portfolio

**Total Value: 1,386,404 FSB (38.6% return)**

- **Cash**: 144,411 FSB
- **Assets held to day 100**:
  - Snowflake Manor: 245,469 FSB
  - Aurora Apartments: 268,389 FSB  
  - Candy Cane Plaza: 250,685 FSB
  - North Star Mall: 264,444 FSB
  - Cookie Factory: 213,006 FSB

## Why This Works

1. **Perfect Information**: We know all future prices, so we can identify optimal entry/exit points
2. **No Risk**: There's no uncertainty, just execution timing and cash flow management
3. **Maximum Profit**: Buy at absolute minimum, sell at absolute maximum for each asset
4. **Hold Strategy**: If maximum price occurs on day 100, hold the asset (no selling needed)

## Lessons Learned

The original complex strategy with momentum indicators, mean reversion, and composite scoring achieved 37.0% return. This simple approach achieves 38.6% return with much cleaner code.

**Sometimes the best solution is the simplest one.**

When you have perfect information, sophisticated algorithms add complexity without improving results. The optimal strategy becomes a straightforward optimization problem: maximize profit given cash flow constraints.

- Category preferences (residential bonus)
- Timing advantages (early availability)

### Multi-Signal Approach

Trading decisions combine:

- **Momentum indicators**: Short-term price trends
- **Mean reversion signals**: Value opportunities
- **Fundamental rankings**: Long-term asset quality

### Risk Management

- **Cash preservation**: Maintain liquidity for opportunities
- **Position limits**: Avoid over-concentration
- **Exit timing**: Lock in gains near period end
- **Constraint validation**: Ensure all rules are followed

## Decision Tree Logic

```
For each available asset:
├── Is asset score positive?
│   └── No → Skip
│   └── Yes → Continue
├── Is asset score > 0.3 (High Quality)?
│   └── Yes → Buy if momentum > -0.02 OR mean_reversion > 0.05
│   └── No → Is asset score > 0.1 (Medium Quality)?
│       └── Yes → Buy if momentum > 0.01 AND mean_reversion > 0.03  
│       └── No → Buy only if momentum > 0.03 AND mean_reversion > 0.1
```

## Performance Attribution

### Major Contributors

1. **Early Snowflake Manor acquisition**: Foundation of portfolio performance
2. **Gingerbread Village timing**: Bought during price dip, rode to 70% gain
3. **Active end-game trading**: Optimized final positions

### Lessons Learned

1. **Quality over quantity**: Better to own fewer high-performing assets
2. **Timing beats timing**: Early deployment beats perfect timing
3. **Stay the course**: Hold quality assets through volatility
4. **End-game matters**: Final positioning significantly impacts score

## Alternative Strategies Considered

### Buy and Hold

Simply buying top-ranked assets and holding to day 100. This would have missed optimization opportunities from active trading.

### Technical Analysis Only  

Using only momentum and mean reversion signals without fundamental analysis. Risk of buying poor-performing assets during temporary uptrends.

### Diversification Strategy

Spreading capital across all asset types. Would have diluted returns with poor commercial assets.

### Market Timing

Attempting to time overall market cycles. Too risky given limited historical data.

## Optimization Results

Our multi-signal approach achieved:

- **37.0% total return** vs. theoretical buy-and-hold max of ~45%
- **Excellent risk-adjusted returns** through quality asset selection
- **Strong final positioning** with three top-tier assets
- **Efficient capital utilization** with 62.8% deployed in final assets

The strategy successfully balanced growth, risk management, and constraint compliance to achieve strong performance in this challenging market environment.
