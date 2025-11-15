# Trading Strategy Analysis

## Data Assumptions

### Valuation Coverage
**Verified Assumption**: All assets have complete valuation data for days 1-100.

- ✅ All 15 assets have valuations for all 100 days
- ✅ Day 1 valuations exist for all assets (even those not available until later)
- ✅ Day 100 valuations exist for all assets

**Why this matters**: Our strategy uses day 1 and day 100 prices to rank assets by performance, even though some assets aren't available until later (e.g., asset_14 available on day 50). The data includes "theoretical" valuations for days before availability, allowing standardized comparison.

**Implication**: If an asset is available on day 50, we still use its day 1 valuation (theoretical price if it existed) to calculate return %, but we purchase it at the actual day 50 price.

## Data Analysis Results

### Top Performers (by return %)
1. **asset_4**: 70.09% return (134,185 → 228,239) - Available day 15
2. **asset_13**: 60.00% return (167,745 → 268,389) - Available day 40
3. **asset_1**: 51.72% return (161,790 → 245,469) - Available day 1
4. **asset_14**: 51.44% return (188,563 → 285,567) - Available day 50
5. **asset_10**: 47.85% return (202,199 → 298,955) - Available day 30

### Worst Performers
- **asset_15**: -23.94% return - Available day 5
- **asset_2**: -19.36% return - Available day 1
- **asset_11**: -17.65% return - Available day 1

## Strategy: Multi-Asset Buy-and-Hold

### Approach
Buy multiple profitable assets as they become available, hold until day 100.

### Execution Plan
1. **Day 1**: Buy asset_1 (161,790 FSB) - Best available day 1
2. **Day 15**: Buy asset_4 (134,185 FSB) - Best overall performer
3. **Day 30**: Buy asset_10 (202,199 FSB) - Strong performer
4. **Day 40**: Buy asset_13 (167,745 FSB) - Second best performer
5. **Day 50**: Buy asset_14 (188,563 FSB) - Strong performer

### Capital Requirements
- Day 1: 161,790 FSB (remaining: 838,210)
- Day 15: 134,185 FSB (remaining: 704,025)
- Day 30: 202,199 FSB (remaining: 501,826)
- Day 40: 167,745 FSB (remaining: 334,081)
- Day 50: 188,563 FSB (remaining: 145,518)

Total invested: 854,482 FSB
Cash remaining: 145,518 FSB

### Expected Day 100 Value
- asset_1: 245,469 FSB
- asset_4: 228,239 FSB
- asset_10: 298,955 FSB
- asset_13: 268,389 FSB
- asset_14: 285,567 FSB
- Cash: 145,518 FSB

**Total: 1,472,137 FSB**
**Profit: 472,137 FSB (47.2% return)**

## Alternative: Focus on Top 3

Buy only the top 3 performers:
- Day 1: asset_1 (161,790)
- Day 15: asset_4 (134,185)
- Day 40: asset_13 (167,745)

Total invested: 463,720 FSB
Cash remaining: 536,280 FSB

Day 100 value:
- Assets: 742,097 FSB
- Cash: 536,280 FSB
- **Total: 1,278,377 FSB (27.8% return)**

## Chosen Strategy

**Multi-Asset Buy-and-Hold** - Better diversification and higher expected return.
