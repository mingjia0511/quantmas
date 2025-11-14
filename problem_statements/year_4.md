## Year 4: Election Chaos 🗳️

*"In politics, nothing is certain except uncertainty, volatility, and elves hedging their bets."* - Winston Frost-chill

### The Challenge

It's election year at the North Pole, and the political climate is more volatile than a commercial property in Tinseltown.

The current administration (Santa Claus) is facing a serious challenge from the opposition (The Grinch). Both candidates have radically different visions for Year 5, and the market is in full speculation mode.

**But there's a twist:** To combat reindeer trafficking concerns, Santa has enacted the **Reindeer Protection Act**, which requires all buy/sell transactions to undergo a **30-day verification period**. This means:
- You initiate a trade on day X
- The trade completes 30 days later (day X+30)
- Prices are locked at day X values
- You still pay taxes during the waiting period
- **No trading after day 70** (or transactions won't complete by day 100)

The election outcome will dramatically reshape Year 5. Choose your investments wisely - the wrong bet could cost you everything.

### Election Candidates & Policies

**🎅 Santa Claus** (Incumbent)
- **Platform**: "Housing First, Families Forever"
- **Favored Assets**: Residential & Commercial in Frostpeak & Mistletoe Meadows
- **Year 5 Impact**: 
  - Tax cuts: -25% on favored asset types
  - Valuation boost: +30% on favored assets
  - Other assets: Stagnate or decline

**👹 The Grinch** (Challenger)
- **Platform**: "Industry & Commerce, Growth Through Production"
- **Favored Assets**: Industrial & Commercial in Tinseltown & Evergreen Valley
- **Year 5 Impact**:
  - Tax cuts: -30% on favored asset types
  - Valuation boost: +35% on favored assets
  - Other assets: Stagnate or decline

### Your Goal

**Maximize your total wealth by day 100** while navigating election uncertainty and transaction delays.

```
Total Wealth = Cash on Hand + Σ(Asset Valuations at day 100) - Tax Penalties
```

**Critical constraints:**
- 30-day transaction processing time
- No trading after day 70
- Election speculation creates extreme volatility
- Must position portfolio for Year 5 outcome

---

## Transaction Processing Mechanics

### How the 30-Day Delay Works

**Buying an Asset:**
```
Day 10: Initiate buy of asset_1 at 200,000 FSB
        - Cash is NOT deducted yet
        - You do NOT own the asset yet
        - Transaction is "pending"

Day 40: Transaction completes (10 + 30 = 40)
        - Cash deducted: 200,000 FSB
        - You now own asset_1
        - Price locked at day 10 value (200,000)
        - Taxes start accruing from day 41
```

**Selling an Asset:**
```
Day 20: Initiate sell of asset_6 at 450,000 FSB
        - You still own the asset
        - Must continue paying taxes
        - Transaction is "pending"

Day 50: Transaction completes (20 + 30 = 50)
        - Cash received: 450,000 FSB
        - You no longer own asset_6
        - Price locked at day 20 value (450,000)
        - Must have paid all taxes before day 50
```

### Strategic Implications

**Opportunities:**
- Lock in prices before they change
- Sell at peaks, buy at dips (30 days ahead)
- Arbitrage price movements

**Risks:**
- Can't react to sudden market changes
- Taxes accrue during sell processing
- Cash tied up in pending transactions
- Must plan 30 days ahead

### Trading Deadline

**Day 70 is the last day to trade!**

Why? Transactions initiated on day 70 complete on day 100. Any later and they won't complete in time.

```
Day 70: Last chance to buy/sell
Day 71-100: No new transactions allowed
Day 100: All pending transactions complete, final scoring
```

---

## Input Files

You'll find these files in `data/year_4/`:

### `election_info.csv`

Contains candidate platforms and their Year 5 impact.

| Column | Description |
|--------|-------------|
| `candidate` | Candidate name |
| `favored_asset_types` | Asset types they favor (pipe-separated) |
| `favored_regions` | Regions they favor (pipe-separated) |
| `tax_reduction_percent` | Tax reduction for favored assets in Year 5 (as decimal) |
| `valuation_boost_percent` | Valuation increase for favored assets in Year 5 (as decimal) |

**Example rows:**
```csv
candidate,favored_asset_types,favored_regions,tax_reduction_percent,valuation_boost_percent
Santa Claus,Residential|Commercial,Frostpeak|Mistletoe Meadows,0.25,0.30
The Grinch,Industrial|Commercial,Tinseltown|Evergreen Valley,0.30,0.35
```

### Reused Files from Previous Years

- `assets.csv` - Same properties (Year 1)
- `valuations.csv` - Updated market prices (Year 4 speculation)
- `tax_rates.csv` - Asset-type taxes (Year 2)
- `regional_tax_rates.csv` - Regional taxes (Year 3)
- `compliance_requirements.csv` - Regional limits (Year 3)

---

## Output Format

Your `output.yml` works the same, but remember the 30-day delay!

### Example

```yaml
10:
  - buy: asset_1  # Completes day 40, price locked at day 10
20:
  - sell: asset_6  # Completes day 50, price locked at day 20
30:
  - pay_tax: asset_6  # Still own it until day 50!
40:
  - pay_tax: asset_1  # Now own it, taxes start
50:
  - pay_region_tax: Frostpeak
70:
  - buy: asset_13  # Last chance! Completes day 100
```

**Critical Notes:**
- Plan 30 days ahead
- Pay taxes on assets you're selling (until transaction completes)
- No transactions after day 70
- Pending transactions show in your portfolio

---

## Trading Rules & Validations

### ✅ Valid Transactions (from Years 1-3)

All previous rules still apply, with modifications:
- Sufficient funds (checked when transaction completes, not initiates)
- Ownership rules (can't initiate buy if you own it, can't initiate sell if you don't)
- Tax payments (must pay before sell transaction completes)

### ✅ New Processing Rules

1. **Transaction Timing**
   - Initiated on day X, completes on day X+30
   - Prices locked at initiation day
   - Cash/ownership changes on completion day

2. **Pending Transactions**
   - Cannot initiate buy if you own the asset (even if sell is pending)
   - Cannot initiate sell if you don't own the asset (even if buy is pending)
   - Can have multiple pending transactions

3. **Trading Deadline**
   - Last day to trade: Day 70
   - Days 71-100: No new transactions allowed
   - Pending transactions complete automatically

4. **Tax During Processing**
   - Selling: Must pay taxes until transaction completes
   - Buying: Taxes start accruing after transaction completes

### ❌ Invalid Transactions

- Trading after day 70
- Initiating buy when you own the asset (or have pending buy)
- Initiating sell when you don't own the asset (or have pending sell)
- Not paying taxes on assets being sold (before completion)

---

## Scoring

Your performance is measured by **Total Wealth on Day 100**:

```
Score = Cash on Hand + Σ(Asset Valuations at day 100) - Tax Penalties - Compliance Penalties
```

**Note:** All pending transactions complete on their scheduled day. Plan accordingly!

---

## Tips for Success

- 📅 **Plan 30 days ahead** - market will change while you wait
- 🎯 **Position for Year 5** - bet on an election outcome
- 📊 **Lock in peaks** - sell when prices spike (30 days before they drop)
- 💰 **Manage cash flow** - pending buys tie up future cash
- ⏰ **Day 70 deadline** - last chance to reposition
- 🗳️ **Hedge your bets** - or go all-in on one candidate
- 🧮 **Track pending transactions** - don't lose track of what's coming

---

## Market Context for Year 4

Election speculation is driving extreme volatility:

**Santa-Favored Assets** (Residential/Commercial in Frostpeak/Mistletoe)
- Days 1-30: Surge on polling data (+30-40%)
- Days 31-50: Correction on uncertainty (-10-15%)
- Days 51-70: Rally on late momentum (+20-30%)
- Days 71-100: Consolidation

**Grinch-Favored Assets** (Industrial/Commercial in Tinseltown/Evergreen)
- Days 1-30: Speculation rally (+25-35%)
- Days 31-50: Volatility on debates (-5-10%)
- Days 51-70: Strong finish (+15-25%)
- Days 71-100: Consolidation

**Non-Favored Assets**
- Stagnant or declining (-5% to +5%)
- Safe havens during volatility
- Poor Year 5 prospects

**Strategy Considerations:**
- **All-in on Santa**: Max returns if he wins, disaster if he loses
- **All-in on Grinch**: Max returns if he wins, disaster if he loses
- **Hedged**: Moderate returns regardless of outcome
- **Cash-heavy**: Safe but misses upside

The election will determine Year 5. Choose wisely! 🎄

**Note:** The actual election outcome will be revealed at the start of Year 5. Your Year 4 strategy should position you for success regardless of who wins... or bet everything on your prediction!
