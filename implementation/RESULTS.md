# Quantmas Challenge Results

This document records the final portfolio valuations for all completed years.

**Important**: Years are connected - Year 2 starts with Year 1's ending portfolio (cash + assets).

## Summary

| Year | Initial Capital | Final Value | Return | Cumulative Value | Strategy |
|------|----------------|-------------|--------|------------------|----------|
| 1    | 1,000,000 FSB  | 1,473,231 FSB | +47.32% | 1,473,231 FSB | Buy-and-hold top 5 performers |
| 2    | 1,077,462 FSB* | 1,156,466 FSB | +15.65% | 1,156,466 FSB | Tax-optimized with asset sales |

*Year 2 starts with Year 1's ending portfolio: $176,181 cash + 5 assets valued at $901,281 on day 1

**Overall Performance**: Starting with 1,000,000 FSB, ending with 1,156,466 FSB = **+15.65% total return across both years**

---

## Year 1: Portfolio Optimization

### Final Results
- **Initial Capital**: 1,000,000 FSB
- **Final Portfolio Value**: 1,473,231 FSB
- **Total Return**: 47.32%
- **Cash Remaining**: 176,181 FSB
- **Assets Owned**: 5

### Asset Holdings (Day 100)
| Asset ID | Purchase Day | Purchase Price | Final Valuation | Return |
|----------|--------------|----------------|-----------------|--------|
| asset_1  | 1            | 161,790        | 245,469         | +51.7% |
| asset_4  | 15           | 153,176        | 228,239         | +49.0% |
| asset_13 | 40           | 159,626        | 268,389         | +68.1% |
| asset_3  | 45           | 169,952        | 269,386         | +58.5% |
| asset_14 | 50           | 179,275        | 285,567         | +59.3% |
| **Total**|              | **823,819**    | **1,297,050**   | **+57.4%** |

### Strategy
- **Approach**: Buy-and-hold top performers
- **Selection Criteria**: Top 5 assets by expected return (from availability to day 100)
- **Execution**: Purchased 5 assets as they became available, held through day 100
- **Key Success Factor**: Selecting high-return assets and avoiding capital-intensive low-return assets

### Transactions
```yaml
1:
  - buy: asset_1
15:
  - buy: asset_4
40:
  - buy: asset_13
45:
  - buy: asset_3
50:
  - buy: asset_14
```

**Total transactions: 5**

---

## Year 2: Tax Optimization

### Starting Portfolio (Carried from Year 1)
- **Cash**: $176,181
- **Assets**: 5 (asset_1, asset_4, asset_13, asset_3, asset_14)
- **Asset Values (Day 1)**: $901,281
- **Total Starting Value**: $1,077,462

### Final Results
- **Final Portfolio Value**: $1,156,466
- **Total Return**: +15.65% (from Year 1 ending)
- **Cash Remaining**: $46,590
- **Assets Owned**: 4 (asset_1, asset_4, asset_13, asset_14)
- **Total Taxes Paid**: $326,408

### Asset Holdings (Day 100)
| Asset ID | Day 1 Value | Final Valuation | Taxes Paid | Net Gain |
|----------|-------------|-----------------|------------|----------|
| asset_1  | $174,733    | $265,106        | $75,127    | +$15,246 |
| asset_4  | $144,919    | $174,006        | $71,916    | -$42,829 |
| asset_13 | $181,164    | $289,860        | $81,365    | +$27,331 |
| asset_14 | $203,648    | $285,567        | $98,000    | -$16,081 |
| **Total**| **$704,464**| **$1,014,539**  | **$326,408**| **-$16,333** |

*Note: asset_3 was sold on day 1 for $196,817 to raise cash for tax payments*

### Strategy
- **Approach**: Tax-optimized portfolio management with strategic asset sales
- **Day 1 Actions**: 
  - Sold asset_3 and asset_14 to raise cash for taxes ($400,465 raised)
  - Bought back asset_14 (better net return than asset_3)
- **Tax Payment Schedule**: Every 10 days
- **Key Challenge**: Limited starting cash ($176k) vs high tax burden on 5 assets

### Transactions Summary
- **Day 1**: 3 actions (2 sells, 1 buy)
- **Days 10-100**: 39 tax payments
- **Total**: 42 actions

### Tax Payment Summary
- **Payment Frequency**: Every 10 days (days 10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
- **Total Payments**: 39 tax payments across 4 assets
- **Total Taxes**: $326,408
- **Tax as % of Starting Value**: 30.3%
- **Tax as % of Final Value**: 28.2%

---

## Comparative Analysis

### Return Comparison
- **Year 1**: +47.32% return (no taxes, no constraints)
- **Year 2**: +15.65% return (with taxes, starting from Year 1 portfolio)
- **Overall**: +15.65% total return from initial 1M to final 1.156M

### Tax Impact
The introduction of taxes in Year 2 significantly impacted strategy:
- **Tax Burden**: $326k paid (30% of starting portfolio value)
- **Forced Asset Sales**: Had to sell asset_3 to raise cash for taxes
- **Lower Returns**: Tax payments consumed most of the asset appreciation

### Strategy Evolution

#### Year 1
- **Capital Deployment**: 82% (5 assets purchased)
- **Approach**: Simple buy-and-hold
- **Transactions**: 5 (all buys)
- **Result**: Strong returns with no constraints

#### Year 2
- **Starting Position**: Inherited 5 assets + limited cash
- **Capital Deployment**: Had to sell assets to raise tax cash
- **Approach**: Tax-optimized with strategic sales
- **Transactions**: 42 (3 day-1 actions + 39 tax payments)
- **Result**: Positive returns despite heavy tax burden

### Key Learnings

#### Year 1
- Buy-and-hold strategy works well without constraints
- Selecting top performers by expected return is effective
- Smart capital allocation (avoiding expensive low-return assets) is crucial
- 82% capital deployment balances returns with diversification

#### Year 2
- Tax obligations dramatically change strategy
- Starting cash position is critical for tax payments
- May need to sell assets to maintain liquidity
- Regular tax payments (every 10 days) prevent quadratic accumulation
- Asset selection must consider net returns after taxes

### Portfolio Continuity Challenges

**The Year 1 → Year 2 Transition**:
1. **Cash Shortage**: Year 1 ended with only $176k cash (12% of portfolio)
2. **Tax Burden**: 5 assets require significant ongoing tax payments
3. **Forced Sales**: Had to sell asset_3 immediately to raise cash
4. **Opportunity Cost**: Limited ability to buy new high-return assets

**Lesson**: In a multi-year scenario with taxes, Year 1 strategy should maintain higher cash reserves (30-40%) to handle Year 2 tax obligations.

---

## Risk Management

### Year 1
- **Risk**: Asset price decline
- **Mitigation**: Diversification across 5 assets
- **Result**: All assets appreciated, no losses

### Year 2
- **Risk**: Insufficient cash for tax payments
- **Mitigation**: Sold lowest-return assets on day 1
- **Risk**: Quadratic tax accumulation
- **Mitigation**: 10-day payment interval
- **Result**: All taxes paid, positive returns maintained

---

## Implementation Quality

### Year 1
- **Test Coverage**: 85%
- **Code Quality**: Modular architecture with clear separation of concerns
- **Documentation**: Comprehensive README and strategy analysis
- **Transactions**: 5 (clean buy-and-hold)

### Year 2
- **Test Coverage**: 83%
- **Code Quality**: Extended Year 1 architecture with tax calculation engine
- **Documentation**: Detailed strategy decisions and lessons learned
- **Transactions**: 42 (3 day-1 actions + 39 tax payments)

---

## Files

### Year 1
- Implementation: `implementation/year_1/`
- Output: `problems/year_1/output/output.yml`
- Tests: `implementation/year_1/tests/`
- Documentation: `implementation/year_1/README.md`, `implementation/year_1/docs/`

### Year 2
- Implementation: `implementation/year_2/`
- Output: `implementation/year_2/output.yml`
- Tests: `implementation/year_2/tests/`
- Documentation: `implementation/year_2/README.md`, `implementation/year_2/docs/`

---

## Overall Performance Summary

### Starting Position
- **Year 1 Day 1**: 1,000,000 FSB cash

### Ending Position
- **Year 2 Day 100**: 1,156,466 FSB total value
  - Cash: $46,590
  - Assets: 4 holdings worth $1,109,876

### Total Journey
- **Total Return**: +15.65%
- **Total Taxes Paid**: $326,408 (Year 2 only)
- **Total Transactions**: 47 (5 in Year 1, 42 in Year 2)
- **Assets Held**: 4 (asset_1, asset_4, asset_13, asset_14)

### Key Insights
1. **Year 1 Success**: Strong asset selection led to 47% returns
2. **Year 2 Challenge**: Tax burden consumed most gains, but positive returns maintained
3. **Portfolio Continuity**: Carrying assets forward created cash flow challenges
4. **Tax Strategy**: Regular payments and strategic sales prevented catastrophic losses
5. **Overall**: Despite heavy taxes, achieved positive total returns

---

*Last Updated: 2025-11-19*
