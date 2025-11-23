# Data Consistency Standards - Quantmas Challenges

## Overview

This document defines the data consistency standards across all 5 years of Quantmas challenges.

## Assets (assets.csv)

**Status**: ✅ Identical across all years

- **MD5 Hash**: `140dda04da4687be69d75297cef53ae4`
- **Rows**: 16 (15 assets + header)
- **Assets**: 15 real estate properties
  - 7 Residential
  - 5 Commercial  
  - 3 Industrial
- **Regions**: Frostpeak, Tinseltown, Evergreen Valley, Mistletoe Meadows

**Rationale**: Same asset universe across all years provides consistency and allows players to learn asset characteristics over time.

## Valuations (valuations.csv)

**Status**: ⚠️ Varies by year (intentional)

### Year 1
- **Rows**: 1,501 (1,500 valuations + header)
- **Starting Capital**: 1,000,000 FSB
- **Market**: Volatile housing boom
- **Performance**:
  - Residential: +51.7% (asset_1: 161,790 → 245,469)
  - Industrial: +13.9% (asset_6: 438,129 → 498,898)
  - Commercial: -19.4% (asset_2: 310,871 → 250,685)

### Year 2
- **Rows**: 1,501
- **Continuity**: Starts from Year 1 ending values
- **Market**: Matured, tax-dampened
- **Performance**:
  - Residential: +10.1% (asset_1: 245,679 → 270,495)
  - Industrial: +13.0% (asset_6: 499,463 → 564,189)
  - Commercial: -12.7% (asset_2: 252,764 → 220,544)

### Year 3
- **Rows**: 1,501
- **Continuity**: Starts from Year 2 ending values
- **Market**: Stable growth with SPV structure
- **Performance**:
  - Residential: +9.5% (asset_1: 270,495 → 296,227)
  - Industrial: +13.0% (asset_6: 564,189 → 637,884)
  - Commercial: -7.0% (asset_2: 220,544 → 205,210)

### Year 4
- **Rows**: 1,501
- **Continuity**: Uses Year 2 data (standalone challenge)
- **Market**: Same as Year 2 (treasury management focus)
- **Performance**: Identical to Year 2

**Rationale**: Year 4 is a standalone treasury management challenge, so it reuses Year 2 market data to focus on cash flow optimization rather than market timing.

### Year 5
- **Rows**: 1,501
- **Continuity**: Starts from Year 4 ending values
- **Market**: Election-driven volatility
- **Performance**:
  - Residential: -8.6% (asset_1: 270,095 → 246,778) - Santa loses
  - Industrial: +23.4% (asset_6: 563,263 → 694,806) - Grinch wins
  - Commercial: +19.5% (asset_2: 224,057 → 267,772) - Both favor

## Tax Rates (tax_rates.csv)

**Years**: 2, 3

**Status**: ✅ Identical

- **Rows**: 13 (12 rates + header)
- **Structure**: Rates change on days 1, 25, 50, 75
- **Base Rates** (per day):
  - Residential: 0.10% - 0.13%
  - Commercial: 0.15% - 0.18%
  - Industrial: 0.12% - 0.15%
- **Modifiers**: 0.05% - 0.085% per day of delay

**Rationale**: Year 3 builds on Year 2 tax mechanics, so rates remain consistent.

## SPV Rules (spv_rules.csv)

**Year**: 3 only

- **Rows**: 2 (1 rule + header)
- **Base Tax Rate**: 0.8% per day (8x higher than asset rates)
- **Tax Modifier**: 0.4% per day of delay
- **Min Capital**: 2% of SPV asset value
- **Liquidation Cost**: 1% of SPV value

**Rationale**: Higher SPV tax rates create meaningful trade-offs for structuring decisions. The 8x multiplier reflects the complexity and regulatory burden of SPV structures.

## Treasury Products (treasury_products.csv)

**Year**: 4 only

- **Rows**: 6 (5 products + header)
- **Products**:
  - Overnight Snowbank: 1 day, 2.5% annual
  - Frosty Money Market: 1 day, 2.8% annual
  - Weekly Icicle Bond: 7 days, 3.2% annual
  - Fortnight Frost Note: 14 days, 3.5% annual
  - Monthly Blizzard Bill: 30 days, 4.0% annual

**Rationale**: Normal yield curve (longer tenor = higher yield) reflects real-world treasury markets.

## Cash Flows (cash_flows.csv)

**Year**: 4 only

- **Rows**: 28 (27 flows + header)
- **Total Income**: 598,622 FSB
- **Total Expenses**: -1,256,618 FSB
- **Net Cash Flow**: -657,996 FSB

**Rationale**: Negative net cash flow forces players to actively manage liquidity through asset sales and treasury investments.

## Election Data (Year 5)

### polls.csv
- **Rows**: 13 (12 polls + header)
- **Pattern**: Close race, Grinch slight edge
- **Final**: 50-50 tie

### news.csv
- **Rows**: 9 (8 events + header)
- **Balance**: 4 positive, 4 negative (2 each candidate)
- **Sentiment Range**: -0.28 to +0.35

### election_info.csv
- **Rows**: 3 (2 candidates + header)
- **Santa**: 20% tax reduction, 25% valuation boost
- **Grinch**: 35% tax reduction, 40% valuation boost

**Rationale**: Balanced election with Grinch offering better economics but Santa offering tradition. Close polls create uncertainty.

## Continuity Rules

### Sequential Years (Build on Previous)
- **Year 1 → Year 2**: Continuous (ending values become starting values)
- **Year 2 → Year 3**: Continuous (ending values become starting values)
- **Year 4 → Year 5**: Continuous (ending values become starting values)

### Standalone Years (Reset)
- **Year 4**: Reuses Year 2 data (treasury focus, not market timing)

### Justification for Changes

**Year 1 → Year 2**:
- Market maturation after housing boom
- Tax introduction dampens speculation
- More stable, lower returns

**Year 2 → Year 3**:
- Continued market stability
- SPV structure adds complexity, not market change
- Similar performance patterns

**Year 4 (Standalone)**:
- Treasury management challenge
- Market data secondary to cash flow management
- Reusing Year 2 data allows focus on liquidity

**Year 4 → Year 5**:
- Election introduces new volatility
- Asset class performance shifts based on political winds
- Residential declines (Santa loses), Industrial surges (Grinch wins)

## Validation Checklist

✅ All assets.csv files identical (MD5 match)
✅ Valuations continuity maintained where intended
✅ Tax rates consistent between Years 2-3
✅ SPV rates balanced (8x multiplier justified)
✅ Treasury yields follow normal curve
✅ Cash flows create meaningful liquidity challenge
✅ Election data balanced and fair
✅ All CSV files have correct row counts
✅ No missing or duplicate data
✅ Performance patterns match problem descriptions

## Last Updated

2025-11-23 - Initial documentation after data consistency review
