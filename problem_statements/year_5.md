## Year 5: The Final Reckoning 🏆

*"This is it. Five years of trading, taxing, and political maneuvering come down to this final year. Don't blow it."* - Your inner voice

### The Challenge

The election is over. The results are in. The North Pole has chosen its path forward, and the market is reacting accordingly.

**[ELECTION OUTCOME WILL BE REVEALED HERE]**

This is your **final year** as Chief Investment Elf. Your 5-year probation period ends on day 100, and your performance will be evaluated based on your total portfolio value. Succeed, and you'll be promoted to permanent CIE with a corner office and unlimited hot cocoa. Fail, and it's back to the coal mines.

The winning candidate's policies are now in full effect:
- **Tax cuts** for favored asset types
- **Valuation boosts** for favored assets
- **Stagnation or decline** for non-favored assets

The market has stabilized after Year 4's volatility. Clear winners and losers have emerged. Your job: maximize returns in this new reality.

### Your Goal

**Maximize your total wealth by day 100** - this is your final score for the entire 5-year challenge.

```
Final Score = Cash on Hand + Σ(Asset Valuations at day 100) - Tax Penalties - Compliance Penalties
```

This score determines your fate. Make it count.

---

## Year 5 Scenarios

The data files you use depend on the election outcome:

### 🎅 Scenario A: Santa Wins

**Data Location:** `data/year_5/santa_wins/`

**Policy Impact:**
- **Favored Assets**: Residential & Commercial in Frostpeak & Mistletoe Meadows
  - Tax rates: -25% reduction
  - Valuations: +30% boost from Year 4
  
- **Non-Favored Assets**: Everything else
  - Tax rates: Unchanged
  - Valuations: Stagnant or declining

**Market Narrative:**
Santa's "Housing First" agenda is driving a residential boom. Frostpeak and Mistletoe Meadows are experiencing unprecedented growth. Commercial properties in these regions are thriving on increased consumer spending.

Industrial properties and Tinseltown/Evergreen assets are being left behind as policy focus shifts to housing and family-friendly development.

**Winning Strategy:**
- Heavy exposure to Residential in Frostpeak/Mistletoe
- Commercial properties in favored regions
- Exit or minimize Industrial and non-favored regions

---

### 👹 Scenario B: Grinch Wins

**Data Location:** `data/year_5/grinch_wins/`

**Policy Impact:**
- **Favored Assets**: Industrial & Commercial in Tinseltown & Evergreen Valley
  - Tax rates: -30% reduction
  - Valuations: +35% boost from Year 4
  
- **Non-Favored Assets**: Everything else
  - Tax rates: Unchanged
  - Valuations: Stagnant or declining

**Market Narrative:**
The Grinch's "Industry & Commerce" platform is supercharging production and trade. Tinseltown is experiencing a renaissance as industrial policy drives investment. Evergreen Valley's factories are running at full capacity.

Residential properties are being neglected as policy focus shifts to economic growth and industrial development.

**Winning Strategy:**
- Heavy exposure to Industrial properties
- Commercial properties in Tinseltown/Evergreen
- Exit or minimize Residential and Frostpeak/Mistletoe

---

## Input Files

You'll find these files in `data/year_5/santa_wins/` or `data/year_5/grinch_wins/`:

### Scenario-Specific Files

- `valuations.csv` - Updated market prices reflecting policy impact
- `tax_rates.csv` - Modified tax rates with cuts for favored assets
- `regional_tax_rates.csv` - Modified regional rates

### Reused Files from Previous Years

- `assets.csv` - Same properties (Year 1)
- `compliance_requirements.csv` - Regional limits (Year 3)

---

## Output Format

Same as previous years - no new mechanics in Year 5.

### Example

```yaml
1:
  - buy: asset_1
  - buy: asset_4
10:
  - pay_tax: asset_1
  - pay_tax: asset_4
  - pay_region_tax: Frostpeak
50:
  - sell: asset_6
  - buy: asset_13
100:
  - pay_tax: asset_13
  - pay_region_tax: Frostpeak
```

---

## Trading Rules & Validations

### ✅ All Previous Rules Apply

- Year 1: Basic trading, ownership, availability
- Year 2: Asset-type taxes
- Year 3: Regional taxes, compliance limits
- Year 4: **NO 30-day delay** (Reindeer Protection Act expired)

**Important:** Year 5 returns to **immediate transaction execution** like Year 1. The 30-day processing delay from Year 4 is gone.

### 💰 Cash Flow

- Transactions execute immediately
- Taxes calculated on current valuations
- Regional compliance still enforced
- All taxes must be paid by day 100

---

## Scoring

Your **FINAL SCORE** for the entire 5-year challenge:

```
Final Score = Cash on Hand + Σ(Asset Valuations at day 100) - Tax Penalties - Compliance Penalties
```

This is it. This number determines everything:
- Your promotion (or demotion)
- Your ranking against other elves
- Your legacy at GIC

**Penalties:**
- Unpaid taxes: 2× the tax owed
- Compliance violations: 10% of excess value
- Don't let penalties ruin 5 years of work!

---

## Tips for Success

- 🎯 **Adapt to the winner** - your Year 4 bets pay off (or don't)
- 📊 **Maximize favored assets** - they have the best returns
- 💰 **Exit non-favored assets** - they're dead weight
- 🗺️ **Regional focus** - concentrate in winning regions
- ⏰ **No delays** - immediate execution is back
- 🧮 **Final tax settlement** - don't leave money on the table
- 🏆 **This is your legacy** - make every trade count

---

## Market Context for Year 5

### If Santa Wins:

**🚀 Booming:**
- Residential properties: +30% boost, -25% taxes
- Commercial in Frostpeak/Mistletoe: +30% boost, -25% taxes
- **Best performers**: asset_1, asset_4, asset_5, asset_9, asset_13

**📉 Declining:**
- Industrial properties: Stagnant
- Tinseltown/Evergreen commercial: Weak
- **Underperformers**: asset_6, asset_8, asset_12

### If Grinch Wins:

**🚀 Booming:**
- Industrial properties: +35% boost, -30% taxes
- Commercial in Tinseltown/Evergreen: +35% boost, -30% taxes
- **Best performers**: asset_2, asset_6, asset_8, asset_11, asset_12, asset_15

**📉 Declining:**
- Residential properties: Stagnant
- Frostpeak/Mistletoe residential: Weak
- **Underperformers**: asset_1, asset_4, asset_7, asset_13

---

## The Final Word

Five years ago, you started with 1,000,000 FSB and a dream. You've navigated:
- Year 1: A volatile housing boom
- Year 2: The introduction of taxes
- Year 3: Regional divergence and compliance
- Year 4: Election chaos and transaction delays
- Year 5: The final reckoning

Your decisions over these five years have led to this moment. The market has spoken. The election has decided. Now it's time to prove you deserve to be the Chief Investment Elf.

**Good luck. The North Pole is counting on you.** 🎄

---

## Post-Challenge

After day 100, your final score will be calculated and you'll see:
- Your total wealth
- Your ranking among all participants
- A breakdown of your best and worst decisions
- Whether you kept your job (or got promoted!)

The elf with the highest final score wins eternal glory and a lifetime supply of candy canes. 🏆
