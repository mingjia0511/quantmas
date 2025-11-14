# 🗳️ Year 4: Election Year Chaos!
## Difficulty: ⭐⭐⭐⭐⭐ (Legendary Elf Challenge! 🦄)

*"In politics, nothing is certain except uncertainty, volatility, and elves hedging their bets."* - Winston Frost-chill

🎅 **BREAKING NEWS: ELECTION YEAR MADNESS!** 🎅

Hold onto your pointed hats, Chief Investment Elf! 🧝‍♀️ The North Pole is in full election mode, and things are about to get WILD! 🌪️ At the end of Year 4, a historic election will reshape the entire North Pole economy, dramatically affecting tax rates and asset valuations for Year 5.

But wait—there's more chaos! 📢 To address the scandal around illegal reindeer trafficking, President Santa Claus has enacted the **Reindeer Protection Act**! 🦌⚖️ This well-intentioned but bureaucratic nightmare means ALL transactions now take 30 days to process!

Talk about adding excitement to your trading strategy! Will you adapt and thrive, or will the red tape tangle your portfolio? Time to show your legendary elf skills! 🎯✨

---

## 🗳️ The Challenge

To prevent any shady reindeer business, the **Reindeer Protection Act** requires thorough verification of every transaction! 🔍 Each buy and sell now takes **30 full days** to process (talk about North Pole bureaucracy! 📋).

🎯 **Key Trading Changes:**
- 📅 30-day processing time for ALL transactions
- 💰 Buy/sell prices locked in on the day you initiate the action
- 💸 You still owe taxes during the processing period if selling
- 🚫 No trading allowed after day 70 (to ensure everything clears by year-end)

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

## 🗳️ Meet the Candidates

Two very different visions for the North Pole's future! 🎭

### 🎅 **Santa Claus** (Incumbent)
*"Traditional Values, Cozy Comfort!"*
- 🏠 **Favors:** Residential & Commercial assets
- 🗺️ **Preferred Regions:** Frostpeak & Mistletoe Meadows
- 📉 **Year 5 Promises:** 25% tax reduction + 30% valuation boost for favored assets

### 😈 **The Grinch** (Challenger)
*"Industrial Revolution, Business First!"*
- 🏭 **Favors:** Industrial & Commercial assets
- 🗺️ **Preferred Regions:** Tinseltown & Evergreen Valley
- 📉 **Year 5 Promises:** 30% tax reduction + 35% valuation boost for favored assets

## 📊 Challenge Files & Info

**📁 New Data Files:**
- 🗳️ `election_info.csv` - Detailed candidate policies and their Year 5 impact predictions

**🔄 Reused from Previous Years:**
- 🏠 `assets.csv` (Year 1)
- 📈 `valuations.csv` (Year 1)
- 💸 `tax_rates.csv` (Year 2)
- 🗺️ `regional_tax_rates.csv` (Year 3)
- 📋 `compliance_requirements.csv` (Year 3)

**🆕 New Mechanics:**
- ⏰ 30-day processing time for ALL buy/sell transactions (Reindeer Protection Act)
- 🚫 No trading allowed after day 70
- 💸 Taxes still owed during sell processing periods
- 🗳️ Election outcome determines Year 5 market conditions

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

## 🗳️ Voting & Election Details

**🚨 IMPORTANT:** The election outcome will be determined, and you'll need to prepare your Year 5 strategy accordingly! The winning candidate's policies will dramatically reshape the investment landscape.

Position your portfolio wisely—will you bet on Santa's cozy residential focus or the Grinch's industrial ambitions? 🤔💭

---

## ✅ Validation Rules

🚨 **All Years 1, 2 & 3 rules still apply, PLUS:**
- ⏰ You cannot buy/sell an asset if there's already a pending transaction for it
- 🚫 No buy/sell transactions allowed after day 70
- 💸 Taxes are still owed during sell processing periods
- 📋 All transactions must clear before year-end

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

## 🎁 The Final Countdown!

This is it, Chief Investment Elf! 🚀 Year 4 is your ultimate test of adaptability and strategic thinking. Navigate the bureaucracy, predict the election outcome, and position yourself for whatever Year 5 brings!

🎄🗳️ **May your trades be swift and your predictions be true!** 🗳️🎄
