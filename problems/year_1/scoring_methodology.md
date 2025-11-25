# Year 1 Scoring Methodology

## Multi-Objective Evaluation

Your performance in Year 1 is measured across **THREE dimensions**, not just total wealth. This teaches a fundamental principle of investing: **returns aren't everything** — risk-adjusted returns matter!

---

## The Three Scoring Components

### 1. Terminal Wealth (60 points)

**What it measures:** Your total portfolio value on Day 100

**Formula:**
```
Terminal Wealth = Cash on Hand + Σ(Asset Valuations at Day 100)
Wealth Score = (Terminal Wealth / 1,500,000) × 60
```

**Target:** 1,500,000 FSB (50% gain from starting 1,000,000 FSB)

**Examples:**
- 1,500,000 FSB → 60 points (hit target)
- 1,600,000 FSB → 64 points (exceeded target)
- 1,200,000 FSB → 48 points (below target)

**Why 60%:** Absolute returns are still the primary goal, but not the only goal.

---

### 2. Sharpe Ratio (25 points)

**What it measures:** Risk-adjusted returns (reward per unit of risk taken)

**Formula:**
```
Daily Return = (Portfolio Value Today - Portfolio Value Yesterday) / Portfolio Value Yesterday
Mean Daily Return = Average of all daily returns (days 1-100)
StdDev Daily Return = Standard deviation of all daily returns
Sharpe Ratio = (Mean Daily Return / StdDev Daily Return) × √100
```

**Scoring:**
```
Sharpe Score = min(Sharpe Ratio × 10, 25)
```
*Capped at 25 points maximum*

**Interpretation:**
- **Sharpe < 1.0:** Poor risk-adjusted returns (< 10 points)
- **Sharpe 1.0-1.5:** Decent risk-adjusted returns (10-15 points)
- **Sharpe 1.5-2.0:** Good risk-adjusted returns (15-20 points)
- **Sharpe 2.0-2.5:** Excellent risk-adjusted returns (20-25 points)
- **Sharpe > 2.5:** Outstanding! (25 points - maximum)

**What improves Sharpe Ratio:**
- ✅ Consistent daily returns (low volatility)
- ✅ Diversification across assets
- ✅ Avoiding large drawdowns
- ✅ Smooth portfolio growth

**What hurts Sharpe Ratio:**
- ❌ High volatility (big swings up and down)
- ❌ Concentration in single assets
- ❌ Large losses followed by recoveries
- ❌ Erratic trading patterns

**Why 25%:** Risk management is a critical skill. A portfolio that grows steadily is often better than one that swings wildly.

---

### 3. Max Drawdown (15 points)

**What it measures:** The worst peak-to-trough decline your portfolio experienced during the year

**Formula:**
```
For each day:
  Peak Value = Maximum portfolio value from day 1 to current day
  Drawdown = (Peak Value - Current Value) / Peak Value

Max Drawdown = Maximum drawdown across all 100 days
Drawdown Score = 15 × (1 - Max Drawdown)
```

**Examples:**
- **5% max drawdown** → 15 × (1 - 0.05) = **14.25 points** (excellent resilience)
- **10% max drawdown** → 15 × (1 - 0.10) = **13.50 points** (good resilience)
- **20% max drawdown** → 15 × (1 - 0.20) = **12.00 points** (moderate resilience)
- **30% max drawdown** → 15 × (1 - 0.30) = **10.50 points** (concerning)
- **50% max drawdown** → 15 × (1 - 0.50) = **7.50 points** (very risky)

**What causes drawdowns:**
- Buying assets that subsequently crash
- Over-concentration in declining sectors
- Poor timing (buying at peaks)
- Lack of diversification

**What prevents drawdowns:**
- Diversification across asset types and regions
- Maintaining cash buffers
- Avoiding over-concentration
- Strategic timing of purchases

**Why 15%:** Resilience matters. Investors who avoid large losses often outperform those who take excessive risks.

---

## Total Score Calculation

```
Final Score = Wealth Score + Sharpe Score + Drawdown Score
Maximum Possible: 100 points
Typical Range: 60-90 points
```

---

## Strategy Examples

### Strategy A: Aggressive (All-In)

**Approach:** Invest everything in the single best-performing asset

**Typical Outcome:**
- Terminal Wealth: 1,600,000 FSB → **64 points**
- Sharpe Ratio: 0.8 (volatile) → **8 points**
- Max Drawdown: 45% (huge swings) → **8.25 points**
- **Total: 80.25 points**

**Pros:** Highest absolute returns
**Cons:** High volatility, large drawdowns, poor risk-adjusted returns

---

### Strategy B: Balanced (Diversified)

**Approach:** Diversify across 5-8 assets, maintain some cash buffer

**Typical Outcome:**
- Terminal Wealth: 1,450,000 FSB → **58 points**
- Sharpe Ratio: 1.5 (smooth growth) → **15 points**
- Max Drawdown: 20% (moderate) → **12 points**
- **Total: 85 points** ✅ **Often wins!**

**Pros:** Consistent returns, lower risk, better risk-adjusted performance
**Cons:** Lower absolute returns than aggressive strategy

---

### Strategy C: Conservative (Mostly Cash)

**Approach:** Hold mostly cash, invest in only 1-2 safe assets

**Typical Outcome:**
- Terminal Wealth: 1,100,000 FSB → **44 points**
- Sharpe Ratio: 0.3 (too safe) → **3 points**
- Max Drawdown: 5% (very stable) → **14.25 points**
- **Total: 61.25 points**

**Pros:** Very low risk, minimal drawdowns
**Cons:** Insufficient returns, opportunity cost of idle cash

---

## Key Insights

### 1. **There's No Single "Best" Strategy**

Different approaches can win depending on market conditions:
- Bull market → Aggressive strategies excel
- Volatile market → Balanced strategies excel
- Uncertain market → Conservative strategies hold up

### 2. **Risk-Adjusted Returns Often Beat Absolute Returns**

A portfolio that grows from 1M → 1.45M smoothly often scores higher than one that swings from 1M → 800k → 1.6M.

### 3. **Diversification is Your Friend**

Spreading investments across:
- Multiple assets (not just one)
- Different asset types (Residential, Commercial, Industrial)
- Different regions (Frostpeak, Tinseltown, Evergreen Valley, Mistletoe Meadows)

This improves both Sharpe Ratio and Max Drawdown scores.

### 4. **Timing Matters**

- Buying during dips → Better entry prices → Lower drawdowns
- Selling before crashes → Preserve capital → Better Sharpe Ratio
- Holding through volatility → May hurt risk metrics

### 5. **Cash is a Position**

Holding some cash:
- ✅ Reduces volatility (improves Sharpe)
- ✅ Provides buffer against drawdowns
- ✅ Allows buying opportunities
- ❌ But reduces absolute returns (opportunity cost)

---

## Tips for Maximizing Your Score

### For Terminal Wealth (60 points):
- Identify high-performing assets early
- Invest aggressively in winners
- Minimize transaction costs (avoid excessive trading)
- Hold winners through day 100

### For Sharpe Ratio (25 points):
- Diversify across 5-8 assets
- Avoid over-concentration in single assets
- Rebalance when one asset dominates portfolio
- Maintain consistent exposure (avoid all-in/all-out swings)

### For Max Drawdown (15 points):
- Never go all-in on a single asset
- Maintain 10-20% cash buffer
- Diversify across asset types and regions
- Avoid buying at obvious peaks
- Consider selling assets showing weakness

---

## Common Mistakes to Avoid

❌ **All-in on one asset:** Great for wealth, terrible for Sharpe and drawdown
❌ **Too conservative:** Low drawdown, but insufficient returns
❌ **Excessive trading:** Transaction costs (2% round-trip) erode returns
❌ **Ignoring risk metrics:** Focusing only on wealth leaves points on the table
❌ **No diversification:** One bad asset can destroy your score

---

## Calculating Your Score

You can track your score throughout the year:

**Daily Portfolio Value:**
```
Portfolio Value = Cash + Σ(Current Asset Valuations)
```

**Daily Return:**
```
Daily Return = (Today's Portfolio Value - Yesterday's Portfolio Value) / Yesterday's Portfolio Value
```

**Running Drawdown:**
```
Peak Value = Max(All Portfolio Values from Day 1 to Today)
Current Drawdown = (Peak Value - Today's Portfolio Value) / Peak Value
```

**At Day 100:**
```
Wealth Score = (Final Portfolio Value / 1,500,000) × 60
Sharpe Score = min((Mean Daily Return / StdDev Daily Return) × √100 × 10, 25)
Drawdown Score = 15 × (1 - Max Drawdown)
Final Score = Wealth Score + Sharpe Score + Drawdown Score
```

---

## Good Luck, Chief Investment Elf!

Remember: **The best investors don't just make money—they make money consistently with controlled risk.** 

Master the art of balancing returns, volatility, and resilience, and you'll be well on your way to saving Christmas! 🎄💰✨
