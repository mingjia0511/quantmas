# 🎄 Year 2: The Tax Collector Cometh 💰

*"Nothing is certain except death, taxes, and elves complaining about both."* - Benjamin Frost-lin

🎅 **Congratulations, Chief Investment Elf!** 🎅

Your Year 1 investments have been absolutely magical! 🌟 But as Uncle Ben Spider-man once said, "With great returns come great responsibilities..." It's time to give back to the North Pole community!

The newly founded **Polar Revenue Service (PRS)** has arrived with jingle bells and tax bills! 🔔💸 A shiny new tax system on asset holdings has been introduced. Now you must pay taxes on the assets you own based on their daily valuations.

But wait—there's a twist! 🎭 You can play the postponement game for up to 30 days, though it'll cost you more the longer you wait. Will you pay up front or gamble on market timing? The choice is yours, brave elf! ❄️💰

The market has also matured since Year 1. The wild housing boom has cooled, retail remains volatile, and industrial properties continue their steady performance. Tax pressure is dampening speculation - investors are fleeing to quality. 📉💭

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

## Difficulty: ⭐⭐⭐☆☆ (Getting Spicy! 🌶️)

## 🏛️ The Challenge

**Maximize your total wealth by day 100** while managing tax obligations strategically.

```
Total Wealth = Cash on Hand + Sum of All Owned Asset Valuations (at day 100 prices)
```

**New constraint:** All taxes must be paid by day 100, or you face penalties (automatic deduction from final score).


## 📊 Challenge Files & Info

**📁 New Data Files:**
- 💸 `tax_rates.csv` - Tax rates by asset type/subtype that change throughout the year

**🔄 Reused from Year 1:**
- 🏠 `assets.csv`
- 📈 `valuations.csv`

**🆕 New Mechanics:**
- 📅 Daily tax owed on owned assets based on current valuation
- ⏰ Tax can be postponed up to 30 days with increasing penalties
- 📊 Tax formula: `tax = current_valuation × (tax_rate + (base_rate_modifier × days_since_last_payment))`

---

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

## 📥 Input Data Format

### 💸 `tax_rates.csv`

| Column | Description |
|--------|-------------|
| `asset_type` | Type of asset (e.g., "Real Estate") |
| `asset_sub_type` | Sub-category: Residential, Commercial, or Industrial |
| `day` | Day when this tax rate becomes effective |
| `tax_rate` | Base daily tax rate (as decimal, e.g., 0.01 = 1%) |
| `base_rate_modifier` | Additional rate per day of delay (as decimal) |

---

## 📤 Output Format

You now have a magical new action available! 🪄 You can pay taxes on any day in addition to your buying and selling activities.

### 📋 `output.yml`

```yaml
1:
  - buy: asset_1
2:
  - pay_tax: asset_1
  - buy: asset_2
```

---

## ✅ Validation Rules

🚨 **All Year 1 rules still apply, PLUS:**
- 💰 You must have enough Frosty Bucks to pay the tax
- 🏠 You must own the asset to pay tax on it
- ⏰ Tax must be paid within 30 days of the last tax payment for the asset
- 🗓️ All tax must be paid by the end of the year
- 💯 You must pay the tax owed for an asset in full on the day you choose to pay it
- 🤝 You must settle all outstanding tax before selling an asset

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

## 🎁 Keep Up the Great Work!

The PRS might have their eye on you now, but smart tax planning is just another skill in your Chief Investment Elf toolkit! Master the art of timing and watch your portfolio grow even stronger!

🎄💪 **May your taxes be low and your returns be high!** 💪🎄