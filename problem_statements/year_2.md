## Year 2: The Tax Collector Cometh 💰

*"Nothing is certain except death, taxes, and elves complaining about both."* - Benjamin Frost-lin

### The Challenge

Congratulations on surviving Year 1! Your portfolio grew, Santa is pleased, and the North Pole economy is booming. But success breeds bureaucracy...

The **Polar Revenue Service (PRS)** has been established, and they want their cut. A new property tax system has been introduced, and every asset you own now incurs **daily taxes** based on its current market valuation.

**The twist?** You can delay paying taxes for up to 30 days, but the longer you wait, the higher the penalty rate climbs. This creates a strategic dilemma: pay now and preserve cash flow, or gamble that asset values will drop and reduce your tax burden?

The market has also matured since Year 1. The wild housing boom has cooled, retail remains volatile, and industrial properties continue their steady performance. Tax pressure is dampening speculation - investors are fleeing to quality.

### Your Goal

**Maximize your total wealth by day 100** while managing tax obligations strategically.

```
Total Wealth = Cash on Hand + Sum of All Owned Asset Valuations (at day 100 prices)
```

**New constraint:** All taxes must be paid by day 100, or you face penalties (automatic deduction from final score).

---

## Tax Mechanics

### How Taxes Work

Taxes accrue **daily** on every asset you own, based on the asset's **current market valuation** (not purchase price).

**Tax Formula:**
```
Daily Tax Owed = Current Valuation × (Base Tax Rate + (Rate Modifier × Days Since Last Payment))
```

**Key Points:**
- Tax starts accruing the day after you buy an asset
- You can delay payment for up to **30 days**
- Each day you delay, the rate modifier increases your effective tax rate
- You must pay the **full accumulated tax** when you choose to pay
- You must settle all taxes before selling an asset

### Tax Payment Strategy

**Pay Early (Days 1-10):**
- Lower effective tax rate
- Preserves predictability
- Costs more cash upfront

**Pay Late (Days 20-30):**
- Higher effective tax rate
- Gamble on asset value dropping
- Risk of cash flow problems

### Example Calculation

You own an asset worth 100,000 FSB with base tax rate 1% and rate modifier 0.5%.

**Scenario A: Pay on Day 1**
```
Tax = 100,000 × (0.01 + 0.005 × 1) = 1,500 FSB
```

**Scenario B: Wait 5 days, asset value stays 100,000**
```
Day 1: 100,000 × (0.01 + 0.005 × 1) = 1,500
Day 2: 100,000 × (0.01 + 0.005 × 2) = 2,000
Day 3: 100,000 × (0.01 + 0.005 × 3) = 2,500
Day 4: 100,000 × (0.01 + 0.005 × 4) = 3,000
Day 5: 100,000 × (0.01 + 0.005 × 5) = 3,500
Total: 12,500 FSB
```

**Scenario C: Wait 5 days, asset value drops to 80,000**
```
Day 1: 100,000 × 0.015 = 1,500
Day 2: 95,000 × 0.020 = 1,900
Day 3: 90,000 × 0.025 = 2,250
Day 4: 85,000 × 0.030 = 2,550
Day 5: 80,000 × 0.035 = 2,800
Total: 11,000 FSB (saved 1,500 by waiting!)
```

---

## Input Files

You'll find these files in `data/year_2/`:

### `tax_rates.csv`

Contains tax rates by asset type and sub-type. Rates may change throughout the year as policy evolves.

| Column | Description |
|--------|-------------|
| `asset_type` | Type of asset (e.g., "Real Estate") |
| `asset_sub_type` | Sub-category: Residential, Commercial, or Industrial |
| `day` | Day when this tax rate becomes effective |
| `tax_rate` | Base daily tax rate (as decimal, e.g., 0.01 = 1%) |
| `base_rate_modifier` | Additional rate per day of delay (as decimal) |

**Example rows:**
```csv
asset_type,asset_sub_type,day,tax_rate,base_rate_modifier
Real Estate,Residential,1,0.01,0.005
Real Estate,Commercial,1,0.015,0.007
Real Estate,Industrial,1,0.012,0.006
Real Estate,Residential,25,0.011,0.0055
```

**Note:** When a new rate takes effect, it applies to all future tax calculations for that asset type.

### Reused Files from Year 1

- `assets.csv` - Same properties available
- `valuations.csv` - Updated market prices (Year 2 conditions)

---

## Output Format

Your `output.yml` now supports a new action: `pay_tax`

### Structure

```yaml
<day>:
  - <action>: <asset_id>
  - pay_tax: <asset_id>
  ...
```

### Example

```yaml
1:
  - buy: asset_6
5:
  - buy: asset_8
10:
  - pay_tax: asset_6  # Pay accumulated tax on asset_6
15:
  - sell: asset_6     # Must pay tax before selling
  - buy: asset_1
50:
  - pay_tax: asset_8
  - pay_tax: asset_1
```

**Notes:**
- You can pay tax on multiple assets on the same day
- Tax payments and trades can be mixed on the same day
- Actions execute in order listed

---

## Trading Rules & Validations

### ✅ Valid Transactions (from Year 1)

All Year 1 rules still apply:
- Sufficient funds for purchases
- Asset availability timing
- Ownership rules (can't buy what you own, can't sell what you don't own)
- Transaction timing (immediate execution)

### ✅ New Tax Rules

1. **Tax Payment Timing**
   - Can pay tax any time after owning an asset
   - Must pay within 30 days of last payment (or purchase)
   - Must pay all accumulated tax in full

2. **Tax Before Selling**
   - Must settle all outstanding taxes before selling an asset
   - Can pay tax and sell on the same day

3. **Year-End Settlement**
   - All taxes must be paid by day 100
   - Unpaid taxes are deducted from final score (with penalty)

### ❌ Invalid Transactions

- Paying tax on an asset you don't own
- Paying partial tax (must pay full amount owed)
- Selling an asset with unpaid taxes
- Letting tax go unpaid for more than 30 days
- Not paying all taxes by day 100

### 💰 Cash Flow

- **Tax payments**: Deducted from cash immediately
- **Tax accumulation**: Calculated daily based on current valuations
- **Strategic timing**: Balance tax costs vs. cash preservation

---

## Scoring

Your performance is measured by **Total Wealth on Day 100**:

```
Score = Cash on Hand + Σ(Valuation of Each Owned Asset on Day 100) - Unpaid Tax Penalties
```

**Penalty for unpaid taxes:** 2× the tax owed (don't let this happen!)

---

## Tips for Success

- 📊 **Monitor valuations closely** - falling prices reduce tax burden
- ⏰ **Time your tax payments** - pay before assets spike in value
- 💰 **Maintain cash reserves** - tax bills can be substantial
- 🎯 **Consider tax efficiency** - industrial assets have lower tax rates
- 🔄 **Active trading helps** - sell before tax accumulates too much
- 📉 **Use market dips** - wait to pay tax if you expect prices to fall
- 🧮 **Calculate total tax burden** - don't get caught without cash on day 100

---

## Market Context for Year 2

Based on the new tax environment, expect:

- **Residential properties**: Modest growth (+8% from Year 1), tax pressure dampens speculation
- **Commercial properties**: Continued volatility, higher tax rates hurt performance
- **Industrial properties**: Defensive plays, lower tax rates make them attractive
- **Overall market**: More conservative, "flight to quality" behavior
- **Tax-driven sell-offs**: Watch for dips around days 25, 50, 75 (common payment periods)

The elves who master tax timing will have a significant advantage! 🎄
