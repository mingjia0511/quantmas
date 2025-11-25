# Year 4 Scoring Methodology

## Multi-Objective Treasury Management

Year 4 introduces the reality of treasury management: **it's not just about returns—it's about balancing returns, liquidity, and efficiency.**

Your performance is evaluated across **THREE dimensions**:

---

## The Three Scoring Components

### 1. Terminal Wealth (40 points)

**What it measures:** Your total portfolio value on Day 100

**Formula:**
```
Terminal Wealth = Cash on Hand 
                + Σ(Asset Valuations at Day 100)
                + Treasury Instrument Values
                + All Treasury Returns Earned
                
Wealth Score = (Terminal Wealth / 1,600,000) × 40
```

**Target:** 1,600,000 FSB (60% gain from starting 1,000,000 FSB)

**Examples:**
- 1,600,000 FSB → 40 points (hit target)
- 1,700,000 FSB → 42.5 points (exceeded target)
- 1,400,000 FSB → 35 points (below target)

**Why 40%:** Absolute returns are still important, but treasury management requires balancing multiple objectives.

---

### 2. Liquidity Management (30 points)

**What it measures:** How well you maintain adequate cash buffers for upcoming obligations

**Daily Liquidity Ratio:**
```
Available Cash = Cash on Hand + Treasury Instruments Maturing Today
Next 7 Days Bills = Sum of all bills due in next 7 days (from cash_flows.csv)

Daily Liquidity Ratio = Available Cash / Next 7 Days Bills
```

**Target Ratio:** 1.2 (20% buffer above minimum needs)

**Daily Score Calculation:**
```
If Ratio ≥ 1.2:
    Daily Score = 1.0 (perfect liquidity management)
    
If 1.0 ≤ Ratio < 1.2:
    Daily Score = Ratio / 1.2 (adequate but tight)
    
If Ratio < 1.0:
    Daily Score = 0.5 × Ratio (danger zone - insufficient liquidity)
```

**Final Liquidity Score:**
```
Liquidity Score = 30 × Average(Daily Scores across all 100 days)
```

**Examples:**

**Day 45 Scenario A (Perfect):**
- Available Cash: 300,000 FSB
- Next 7 Days Bills: 250,000 FSB
- Ratio: 1.2 → Daily Score = 1.0 ✅

**Day 45 Scenario B (Tight):**
- Available Cash: 275,000 FSB
- Next 7 Days Bills: 250,000 FSB
- Ratio: 1.1 → Daily Score = 0.917 ⚠️

**Day 45 Scenario C (Danger):**
- Available Cash: 200,000 FSB
- Next 7 Days Bills: 250,000 FSB
- Ratio: 0.8 → Daily Score = 0.4 ❌

**What improves liquidity score:**
- ✅ Maintaining cash buffers (10-20% above needs)
- ✅ Using overnight instruments for near-term needs
- ✅ Planning ahead for large bills
- ✅ Selling assets before cash runs out
- ✅ Avoiding over-investment in long-term instruments

**What hurts liquidity score:**
- ❌ Running out of cash (ratio < 1.0)
- ❌ Locking all cash in 30-day instruments
- ❌ Not planning for upcoming bills
- ❌ Emergency asset sales at discounts
- ❌ Idle cash penalties forcing poor decisions

**Why 30%:** Liquidity management is critical in treasury operations. Running out of cash is catastrophic.

---

### 3. Yield Optimization (30 points)

**What it measures:** How efficiently you deploy cash to earn treasury returns

**Actual Treasury Yield:**
```
Total Treasury Returns = Sum of all returns from treasury investments
Average Cash Invested = Average daily balance in treasury instruments

Actual Yield = (Total Treasury Returns / Average Cash Invested) × (365 / 100)
```
*Annualized for comparison*

**Optimal Yield:** 4.0% (if all cash was in Monthly Blizzard Bills all year)

**Efficiency Calculation:**
```
Efficiency = Actual Yield / Optimal Yield (4.0%)
Yield Score = 30 × Efficiency
```

**Examples:**

**Strategy A: Aggressive (Mostly Monthly Blizzard Bills)**
- Actual Yield: 3.8% (95% efficient)
- Yield Score: 28.5 points ✅
- Risk: May run out of liquidity

**Strategy B: Balanced (Mix of instruments)**
- Actual Yield: 3.2% (80% efficient)
- Yield Score: 24 points ✅
- Benefit: Good liquidity + decent returns

**Strategy C: Conservative (Mostly Overnight Snowbank)**
- Actual Yield: 2.6% (65% efficient)
- Yield Score: 19.5 points ⚠️
- Benefit: Maximum flexibility

**What improves yield score:**
- ✅ Using longer-term instruments when possible
- ✅ Locking in Monthly Blizzard Bills (4.0%) when you don't need cash
- ✅ Minimizing idle cash (0% return)
- ✅ Planning cash needs to maximize long-term investments
- ✅ Taking advantage of yield spikes (liquidity events)

**What hurts yield score:**
- ❌ Keeping too much in Overnight Snowbank (2.5%)
- ❌ Idle cash penalties (negative return)
- ❌ Over-conservative cash management
- ❌ Not planning ahead (forced into short-term instruments)
- ❌ Emergency redemptions (opportunity cost)

**Why 30%:** Yield optimization is the other half of treasury management. Cash should always be working.

---

## Total Score Calculation

```
Final Score = Wealth Score + Liquidity Score + Yield Score
Maximum Possible: 100 points
Typical Range: 60-85 points
```

---

## Strategy Examples

### Strategy A: Aggressive Yield Maximizer

**Approach:** Maximize treasury returns, minimal cash buffers

**Typical Outcome:**
- Terminal Wealth: 1,650,000 FSB → **41.25 points**
- Liquidity Management: 0.75 average ratio → **22.5 points** ⚠️
- Yield Optimization: 3.8% actual → **28.5 points**
- **Total: 92.25 points**

**Pros:** Highest returns, excellent yield efficiency
**Cons:** Risky liquidity management, vulnerable to shocks

---

### Strategy B: Balanced Treasury Manager

**Approach:** Balance returns and liquidity, diversified instruments

**Typical Outcome:**
- Terminal Wealth: 1,580,000 FSB → **39.5 points**
- Liquidity Management: 1.15 average ratio → **28.75 points** ✅
- Yield Optimization: 3.2% actual → **24 points**
- **Total: 92.25 points** ✅ **Often wins!**

**Pros:** Consistent performance, handles shocks well, good balance
**Cons:** Lower absolute returns than aggressive strategy

---

### Strategy C: Conservative Liquidity Hoarder

**Approach:** Maximize liquidity, minimal risk

**Typical Outcome:**
- Terminal Wealth: 1,480,000 FSB → **37 points**
- Liquidity Management: 1.35 average ratio → **30 points** ✅
- Yield Optimization: 2.6% actual → **19.5 points** ⚠️
- **Total: 86.5 points**

**Pros:** Perfect liquidity, no stress, handles all shocks
**Cons:** Opportunity cost of idle cash, poor yield efficiency

---

## Key Insights

### 1. **The Liquidity-Yield Trade-off**

This is the fundamental challenge of treasury management:
- **More liquidity** (Overnight Snowbank) = Lower yields (2.5%)
- **Less liquidity** (Monthly Blizzard Bills) = Higher yields (4.0%)

The best treasury managers find the optimal balance.

### 2. **Planning is Everything**

Success requires looking ahead:
- What bills are due in the next 7-30 days?
- When do treasury instruments mature?
- When can I lock in long-term rates?
- What's my emergency buffer?

### 3. **Liquidity Crises Test Your Strategy**

Year 4 includes 4 liquidity shocks:
- Day 30: Credit freeze (can't redeem treasuries)
- Day 45: Emergency expense (250k bill)
- Day 65: Yield spike (opportunity to lock in higher rates)
- Day 85: Flash crash (opportunity to buy assets cheap)

**Good treasury managers survive these shocks. Great ones profit from them.**

### 4. **Idle Cash is the Enemy**

The 0.1% daily idle cash penalty (36.5% annualized!) means:
- Every Frosty Buck must be working
- Either in treasury instruments OR reserved for bills
- No lazy money allowed!

### 5. **Instrument Selection Matters**

| Instrument | Yield | Best For |
|------------|-------|----------|
| 🌙 Overnight Snowbank | 2.50% | Bills due tomorrow |
| 💎 Frosty Money Market | 2.80% | Daily flexibility |
| 📅 Weekly Icicle Bond | 3.20% | Bills due in 7-10 days |
| 🎄 Fortnight Frost Note | 3.50% | Bills due in 14-20 days |
| ❄️ Monthly Blizzard Bill | 4.00% | No bills for 30+ days |

**Ladder your investments** to match cash needs!

---

## Calculating Your Score

### Daily Tracking

**Portfolio Value:**
```
Portfolio Value = Cash + Σ(Asset Valuations) + Treasury Instrument Values
```

**Liquidity Ratio:**
```
Available Cash = Cash + Maturing Instruments Today
Next 7 Days Bills = Sum of bills due in next 7 days
Liquidity Ratio = Available Cash / Next 7 Days Bills
Daily Liquidity Score = (see formula above)
```

**Treasury Returns:**
```
Daily Return = Investment × (Annual Yield / 365) × Tenor Days
Cumulative Returns = Sum of all treasury returns to date
```

### Final Score (Day 100)

```
Wealth Score = (Final Portfolio Value / 1,600,000) × 40

Liquidity Score = 30 × Average(All 100 Daily Liquidity Scores)

Actual Yield = (Total Treasury Returns / Avg Cash Invested) × (365/100)
Yield Score = 30 × (Actual Yield / 4.0%)

Final Score = Wealth Score + Liquidity Score + Yield Score
```

---

## Tips for Maximizing Your Score

### For Terminal Wealth (40 points):
- Invest in high-performing assets
- Maximize treasury returns (every 0.5% matters!)
- Avoid idle cash penalties
- Minimize transaction costs

### For Liquidity Management (30 points):
- Maintain 20% buffer above minimum needs (ratio = 1.2)
- Use overnight instruments for near-term bills
- Plan ahead for large expenses
- Never let ratio drop below 1.0
- Sell assets BEFORE you desperately need cash

### For Yield Optimization (30 points):
- Use Monthly Blizzard Bills when you don't need cash for 30+ days
- Ladder investments to match cash needs
- Take advantage of yield spikes (day 65 event)
- Minimize time in Overnight Snowbank
- Zero idle cash at end of every day

---

## Common Mistakes to Avoid

❌ **All cash in Monthly Blizzard Bills:** Great yield, but you'll run out of liquidity
❌ **All cash in Overnight Snowbank:** Perfect liquidity, but terrible yield efficiency
❌ **Ignoring cash_flows.csv:** Surprises will destroy your liquidity score
❌ **No emergency buffer:** Liquidity crises will force bad decisions
❌ **Idle cash at day end:** 0.1% daily penalty adds up fast
❌ **Not planning ahead:** Reactive treasury management always loses

---

## Advanced Strategies

### Laddering

**What:** Spread investments across multiple tenors
**Why:** Balances liquidity and yield
**Example:**
- 20% in Overnight Snowbank (emergency buffer)
- 30% in Weekly Icicle Bonds (near-term bills)
- 30% in Fortnight Frost Notes (medium-term bills)
- 20% in Monthly Blizzard Bills (maximize yield)

### Cash Flow Forecasting

**What:** Project cash needs 30 days ahead
**Why:** Allows optimal instrument selection
**How:**
1. Sum all bills due in next 30 days
2. Add buffer (20%)
3. Reserve that amount in short-term instruments
4. Invest remainder in long-term instruments

### Shock Preparation

**What:** Maintain extra buffers before known shock dates
**Why:** Liquidity crises punish the unprepared
**When:**
- Day 30: Credit freeze coming (hold extra cash)
- Day 45: Emergency expense (250k ready)
- Day 65: Yield spike (have cash ready to invest)
- Day 85: Flash crash (have cash ready to buy assets)

---

## Good Luck, Chief Treasury Elf!

Remember: **The best treasury managers don't just make money—they make money efficiently while maintaining perfect liquidity.**

Master the art of balancing returns, liquidity, and efficiency, and you'll prove you're ready for the ultimate challenge! 🎄💰✨
