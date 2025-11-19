# Year 1 Challenge - Example Scenarios

This document provides concrete examples of how the new rules work in practice.

## Example 1: Basic Buy with Transaction Costs

**Scenario**: You want to buy `asset_1` on day 1.

**Data**:
- Day 1 valuation of `asset_1`: 161,790 FSB
- Your cash: 1,000,000 FSB

**Calculation**:
```
Buy Price = 161,790 × 1.01 = 163,407.90 FSB
```

**Result**:
- ✅ Transaction valid (you have enough cash)
- Cash after purchase: 1,000,000 - 163,407.90 = 836,592.10 FSB
- You now own `asset_1`
- Earliest you can sell: Day 11 (10-day holding period)

---

## Example 2: Selling with Transaction Costs

**Scenario**: You bought `asset_1` on day 1, now selling on day 15.

**Data**:
- Day 15 valuation of `asset_1`: 168,234 FSB (hypothetical)
- You bought on day 1 for 163,407.90 FSB

**Calculation**:
```
Sell Proceeds = 168,234 × 0.99 = 166,551.66 FSB
```

**Result**:
- ✅ Transaction valid (held for 14 days ≥ 10 days)
- Cash received: 166,551.66 FSB
- Profit: 166,551.66 - 163,407.90 = 3,143.76 FSB
- Return: 1.92% over 14 days

---

## Example 3: Violating Holding Period

**Scenario**: You bought `asset_6` on day 20, trying to sell on day 25.

**Data**:
- Bought on day 20
- Current day: 25
- Days held: 5

**Result**:
- ❌ Transaction INVALID
- Reason: Must hold for at least 10 days
- Earliest valid sale date: Day 30

---

## Example 4: Transaction Costs Eating Profits

**Scenario**: Quick flip attempt (if holding period allowed).

**Data**:
- Buy on day 10 at valuation: 100,000 FSB
- Sell on day 20 at valuation: 102,000 FSB (2% gain)

**Calculation**:
```
Buy Price = 100,000 × 1.01 = 101,000 FSB
Sell Proceeds = 102,000 × 0.99 = 100,980 FSB
Net Result = 100,980 - 101,000 = -20 FSB (LOSS!)
```

**Lesson**: A 2% valuation increase results in a loss due to 2% round-trip transaction costs. You need valuations to rise by more than 2% to profit.

---

## Example 5: Macro-Driven Strategy

**Scenario**: Using macro indicators to guide decisions.

**Macro Data**:
- Day 1: Inflation = 100.21, Interest Rate = 2.53%
- Day 50: Inflation = 107.34, Interest Rate = 3.38%
- Day 100: Inflation = 115.27, Interest Rate = 4.55%

**Observation**:
- Inflation rising 15% → Residential assets likely to perform well
- Interest rates rising 2% → Commercial assets likely under pressure

**Strategy Example**:
```yaml
# Early days: Buy residential assets (inflation hedge)
1:
  - buy: asset_1  # Snowflake Manor (Residential)
  - buy: asset_4  # Gingerbread Village (Residential)

# Avoid or sell commercial assets as rates rise
30:
  - sell: asset_2  # Candy Cane Plaza (Commercial)

# Hold residential through year-end
# (No action needed, just hold)
```

**Actual Results** (from data):
- `asset_1` (Residential): +51.72% 📈
- `asset_4` (Residential): +70.09% 📈
- `asset_2` (Commercial): -19.36% 📉

---

## Example 6: Cash Management

**Scenario**: Running out of cash.

**Starting Position**:
- Cash: 50,000 FSB
- Own: asset_1, asset_4, asset_7

**Attempt**: Buy `asset_10` on day 30
- Day 30 valuation: 202,199 FSB
- Buy price: 202,199 × 1.01 = 204,220.99 FSB

**Result**:
- ❌ Transaction INVALID
- Reason: Insufficient cash (need 204,220.99, have 50,000)
- Solution: Sell an existing asset first (respecting holding period)

---

## Example 7: Complete Trading Sequence

**Full Example**:

```yaml
1:
  - buy: asset_1   # Cost: 163,407.90 FSB, Cash: 836,592.10 FSB
  
5:
  - buy: asset_6   # Cost: 448,986.87 FSB, Cash: 387,605.23 FSB
  
15:
  - buy: asset_4   # Cost: 136,726.85 FSB, Cash: 250,878.38 FSB
  - sell: asset_1  # Proceeds: ~166,551 FSB, Cash: ~417,429 FSB
  
30:
  - sell: asset_4  # Proceeds: ~226,356 FSB, Cash: ~643,785 FSB
  - buy: asset_10  # Cost: 204,220.99 FSB, Cash: ~439,564 FSB
```

**Key Points**:
- Each buy reduces cash by 1% more than valuation
- Each sell adds cash at 1% less than valuation
- Must wait 10 days between buy and sell
- Track cash carefully to avoid invalid transactions

---

## Example 8: Optimal vs Suboptimal Strategy

### Suboptimal: Day Trading (High Costs)
```yaml
1:
  - buy: asset_1
11:
  - sell: asset_1
12:
  - buy: asset_2
22:
  - sell: asset_2
# ... many more trades
```
**Problem**: 2% cost per round-trip × many trades = significant drag on returns

### Optimal: Strategic Long-Term Holds
```yaml
1:
  - buy: asset_1   # Residential (inflation hedge)
  - buy: asset_4   # Residential
  
15:
  - buy: asset_7   # Residential
  
# Hold through day 100
```
**Benefit**: Only pay transaction costs once, capture full appreciation of winning assets

---

## Key Takeaways

1. **Transaction costs are real**: 2% round-trip means you need >2% gains to profit
2. **Holding periods enforce patience**: Can't react to every market move
3. **Macro matters**: Asset class selection based on inflation/rates can drive performance
4. **Cash management is critical**: Plan your liquidity needs
5. **Quality over quantity**: Better to hold a few winners than trade frequently

