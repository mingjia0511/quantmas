# Year 3 - Treasury Elf Training Manual 🎄

*Your guide to becoming a Cash Management Master!* 💰✨

This document provides detailed examples of treasury strategies and liquidity management. Think of it as your Treasury Elf handbook—full of tips, tricks, and cautionary tales of lazy Frosty Bucks! 🧝‍♂️

**Remember**: Idle cash gets coal! 🎅

## Example 1: The Tale of Lazy Larry vs Smart Sally 🧝‍♂️🧝‍♀️

**Scenario**: Day 1, you have 1,000,000 FSB starting capital and no immediate obligations.

**Lazy Larry's Approach** (Idle Cash - DON'T DO THIS!):
```yaml
1:
  # Do nothing, hold cash
```
**Result**:
- Idle cash: 1,000,000 FSB
- Penalty: 1,000,000 × 0.001 = 1,000 FSB per day
- Over 100 days: 100,000 FSB lost! ❌

**Smart Sally's Approach** (Zero-Cash Mandate - BE LIKE SALLY!):
```yaml
1:
  - invest_treasury: t_bill_30d, 700000   # Monthly Blizzard Bill - highest yield!
  - invest_treasury: t_bill_7d, 200000    # Weekly Icicle Bond - medium flexibility
  - invest_treasury: repo_overnight, 100000  # Overnight Snowbank - daily flexibility
```
**Result**:
- Zero idle cash ✅ (Santa is proud!)
- Treasury returns:
  - Monthly Blizzard Bill: 700,000 × (0.04/365) × 30 = 2,301 FSB 🎉
  - Weekly Icicle Bond: 200,000 × (0.032/365) × 7 = 123 FSB
  - Overnight Snowbank: 100,000 × (0.025/365) × 1 = 6.85 FSB per day
- **Sally beats Larry by**: 100,000+ FSB over 100 days! 💰

**Moral**: Don't be like Lazy Larry! Be like Smart Sally! 🌟

---

## Example 2: Liquidity Planning with Known Obligations

**Scenario**: Day 1, you know you have operational expenses on day 10 (40,000 FSB).

**Bad Strategy** (All Long-Term):
```yaml
1:
  - invest_treasury: t_bill_30d, 1000000  # Locks all cash for 30 days
```
**Problem**: On day 10, you can't pay 40,000 FSB obligation!
- Liquidity shortfall: 40,000 FSB
- Penalty: 40,000 × 2 = 80,000 FSB ❌

**Good Strategy** (Match Maturities):
```yaml
1:
  - invest_treasury: t_bill_7d, 100000    # Matures day 8, covers day 10
  - invest_treasury: t_bill_30d, 900000   # Rest in highest yield
```
**Result**:
```yaml
8:
  - redeem_treasury: t_bill_7d, 100000    # Get cash back
  - invest_treasury: repo_overnight, 100000  # Keep flexible until day 10

10:
  - redeem_treasury: repo_overnight, 100000
  # 40,000 used for operations (automatic)
  - invest_treasury: t_bill_7d, 60000     # Reinvest remainder
```
- Zero idle cash ✅
- No liquidity shortfall ✅
- Maximized treasury returns ✅

---

## Example 3: Coordinating Asset Sales with Liquidity Needs

**Scenario**: Day 50, you need 200,000 FSB for taxes on day 60, but only have 50,000 FSB in maturing instruments.

**Option A: Sell Asset Early**
```yaml
50:
  - sell: asset_2  # Generates ~220,000 FSB (after transaction costs)
  - invest_treasury: t_bill_7d, 220000  # Matures day 57

57:
  - redeem_treasury: t_bill_7d, 220000
  - invest_treasury: repo_overnight, 220000  # Keep flexible

60:
  - redeem_treasury: repo_overnight, 220000
  - pay_tax: asset_1  # 200,000 FSB
  - invest_treasury: repo_overnight, 20000  # Remainder
```

**Option B: Use Short-Term Instruments**
```yaml
50:
  - redeem_treasury: t_bill_30d, 150000  # Maturing from day 20
  - invest_treasury: t_bill_7d, 150000   # Matures day 57

57:
  - redeem_treasury: t_bill_7d, 150000
  # Still short 50,000 FSB!
  - sell: asset_5  # Emergency sale
  - invest_treasury: repo_overnight, 200000

60:
  - redeem_treasury: repo_overnight, 200000
  - pay_tax: asset_1
```

**Lesson**: Plan asset sales in advance to avoid emergency liquidations.

---

## Example 4: Laddering Strategy

**Scenario**: You want to maintain continuous liquidity while maximizing yields.

**Laddering Approach**:
```yaml
1:
  - invest_treasury: t_bill_7d, 200000    # Matures day 8
  - invest_treasury: t_bill_14d, 200000   # Matures day 15
  - invest_treasury: t_bill_30d, 200000   # Matures day 31
  - invest_treasury: repo_overnight, 400000  # Daily flexibility

8:
  - redeem_treasury: t_bill_7d, 200000
  - invest_treasury: t_bill_7d, 200000    # Roll over, matures day 15

15:
  - redeem_treasury: t_bill_7d, 200000
  - redeem_treasury: t_bill_14d, 200000
  - invest_treasury: t_bill_7d, 200000    # Matures day 22
  - invest_treasury: t_bill_14d, 200000   # Matures day 29

# Continue rolling over...
```

**Benefits**:
- Regular maturity dates provide liquidity
- Captures higher yields from longer tenors
- Reduces reinvestment risk
- Maintains flexibility

---

## Example 5: Dividend Capture Strategy

**Scenario**: You own industrial assets that pay dividends on days 25, 50, 75.

**Cash Flow Planning**:
```yaml
# Day 20: Prepare for dividend
20:
  - redeem_treasury: t_bill_7d, 300000
  - invest_treasury: repo_overnight, 300000  # Stay flexible

25:
  # Dividend arrives: +166,237 FSB (automatic)
  - redeem_treasury: repo_overnight, 300000
  # Total cash: 466,237 FSB
  - invest_treasury: t_bill_30d, 400000     # Lock in high yield
  - invest_treasury: t_bill_7d, 66237       # Remainder

# Repeat for days 50 and 75
```

**Lesson**: Dividends are predictable inflows—plan to deploy them immediately into higher-yielding instruments.

---

## Example 6: Idle Cash Penalty Calculation

**Scenario**: You forgot to invest 100,000 FSB on day 50.

**Penalty Calculation**:
```
Idle cash: 100,000 FSB
Daily penalty: 100,000 × 0.001 = 100 FSB
```

**Opportunity Cost**:
```
If invested in 30-day T-bill:
  Return: 100,000 × (0.04/365) × 30 = 329 FSB

Total cost of idle cash:
  Penalty: 100 FSB
  Lost return: 329 FSB
  Total: 429 FSB for one day! ❌
```

**Lesson**: Even one day of idle cash is expensive. Always invest excess cash.

---

## Example 7: Liquidity Shortfall Scenario

**Scenario**: Day 30, you have 150,000 FSB obligation but only 100,000 FSB available.

**What Happens**:
```
Required: 150,000 FSB
Available: 100,000 FSB
Shortfall: 50,000 FSB

Penalty: 50,000 × 2 = 100,000 FSB ❌
```

**How to Avoid**:
1. **Forecast ahead**: Check cash_flows.csv for upcoming obligations
2. **Maintain buffer**: Keep 50-100k in overnight repo
3. **Plan asset sales**: Sell assets 3-5 days before major obligations
4. **Ladder maturities**: Ensure instruments mature before obligations

---

## Example 8: Yield Optimization

**Scenario**: You have 500,000 FSB excess cash for 30 days with no obligations.

**Option A: All Overnight Repo**
```yaml
1:
  - invest_treasury: repo_overnight, 500000
# Roll over daily for 30 days
```
**Return**: 500,000 × (0.025/365) × 30 = 1,027 FSB

**Option B: All 30-Day T-Bill**
```yaml
1:
  - invest_treasury: t_bill_30d, 500000
```
**Return**: 500,000 × (0.04/365) × 30 = 1,644 FSB

**Difference**: 617 FSB (60% higher return!)

**Lesson**: If you're certain about 30-day horizon, use 30-day T-bills. The yield pickup is significant.

---

## Example 9: Mixed Strategy for Uncertain Timing

**Scenario**: You think you'll need cash around day 20-25, but not sure exactly when.

**Flexible Strategy**:
```yaml
1:
  - invest_treasury: t_bill_14d, 300000   # Matures day 15 (before window)
  - invest_treasury: t_bill_7d, 200000    # Matures day 8 (early)

8:
  - redeem_treasury: t_bill_7d, 200000
  - invest_treasury: repo_overnight, 200000  # Daily flexibility

15:
  - redeem_treasury: t_bill_14d, 300000
  - invest_treasury: repo_overnight, 300000  # Wait for clarity

# Days 20-25: Redeem as needed
```

**Lesson**: When timing is uncertain, use shorter tenors and overnight instruments for flexibility.

---

## Example 10: Full 100-Day Treasury Strategy

**Comprehensive Example**:

```yaml
1:
  - buy: asset_1  # 270,000 FSB (Residential, tax-efficient)
  - buy: asset_6  # 564,000 FSB (Industrial, pays dividends)
  # Remaining cash: 166,000 FSB
  - invest_treasury: t_bill_7d, 100000
  - invest_treasury: repo_overnight, 66000

5:
  # Settlement inflow: +150,000 FSB (from cash_flows.csv)
  - invest_treasury: t_bill_30d, 150000  # Matures day 35

8:
  - redeem_treasury: t_bill_7d, 100000
  - invest_treasury: t_bill_7d, 100000  # Roll over

10:
  # Operations: -33,648 FSB (automatic)
  - redeem_treasury: repo_overnight, 66000
  - invest_treasury: repo_overnight, 32352  # Remainder after operations

15:
  # Tax estimate: -135,302 FSB
  - redeem_treasury: t_bill_7d, 100000
  - redeem_treasury: repo_overnight, 32352
  - pay_tax: asset_1  # 135,302 FSB
  # Cash deficit: need to sell asset or use reserves

20:
  # Operations + maintenance: -90,819 FSB
  - sell: asset_2  # Generate cash (if owned)
  - invest_treasury: t_bill_7d, 150000

25:
  # Dividend: +166,237 FSB
  - redeem_treasury: t_bill_7d, 150000
  - invest_treasury: t_bill_30d, 300000  # Lock in high yield
  - invest_treasury: repo_overnight, 16237

# Continue through day 100...
```

**Key Principles**:
1. Always invest excess cash immediately
2. Match maturities to known obligations
3. Use overnight repo for uncertain timing
4. Maximize 30-day T-bills when horizon is clear
5. Coordinate asset sales with liquidity needs
6. Capture dividends and redeploy immediately

---

## Example 11: Break-Even Analysis

**Question**: Is it worth locking cash in 30-day T-bill vs rolling overnight repo?

**30-Day T-Bill**:
- Yield: 4.00% annual
- Return on 100,000 FSB: 100,000 × (0.04/365) × 30 = 329 FSB

**Overnight Repo (30 days)**:
- Yield: 2.50% annual
- Return on 100,000 FSB: 100,000 × (0.025/365) × 30 = 205 FSB

**Difference**: 124 FSB (60% higher return)

**Risk**: If you need cash on day 15, you face liquidity shortfall (2× penalty).

**Break-Even**:
```
Shortfall penalty: 100,000 × 2 = 200,000 FSB
Extra yield from T-bill: 124 FSB

Penalty is 1,613× the extra yield! ❌
```

**Lesson**: Never lock cash in long-term instruments unless you're CERTAIN you won't need it. Liquidity shortfall penalties are catastrophic.

---

## Example 12: Optimal vs Suboptimal Treasury Management

### Suboptimal: Ignoring Treasury
```yaml
1:
  - buy: asset_1
  - buy: asset_6
  # Hold remaining 166,000 FSB as idle cash for 100 days

# Result:
# - Idle cash penalty: 166,000 × 0.001 × 100 = 16,600 FSB ❌
# - Lost treasury returns: ~1,500 FSB ❌
# - Total cost: 18,100 FSB
```

### Optimal: Active Treasury Management
```yaml
1:
  - buy: asset_1
  - buy: asset_6
  - invest_treasury: t_bill_30d, 100000
  - invest_treasury: repo_overnight, 66000

# Daily management: redeem, reinvest, ladder maturities
# Result:
# - Zero idle cash ✅
# - Treasury returns: ~1,500 FSB ✅
# - Savings vs suboptimal: 18,100 FSB
```

**Impact**: 18,100 FSB difference = ~1.8% of starting capital!

---

## Key Takeaways

1. **Zero idle cash is mandatory** - Even one day costs 0.1%
2. **Forecast 30 days ahead** - Know your obligations
3. **Match maturities to needs** - Avoid liquidity shortfalls
4. **Ladder for flexibility** - Regular maturity dates
5. **Maximize long-term when certain** - 30-day T-bills offer 60% higher yield
6. **Use overnight for uncertainty** - Flexibility is worth the yield sacrifice
7. **Coordinate with portfolio** - Time asset sales for liquidity
8. **Capture dividends immediately** - Redeploy into higher-yielding instruments
9. **Liquidity shortfalls are catastrophic** - 2× penalty destroys returns
10. **Treasury management matters** - Can add 15-25% to final score

This is how real sovereign wealth funds operate their treasury functions!

