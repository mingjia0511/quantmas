# 🗳️ Year 4: Election Year Chaos!
## Difficulty: ⭐⭐⭐⭐☆ (Expert Elf Territory! 🧙‍♀️)

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
        - Can pay final taxes on day 20 (same day as sell initiation)

Day 50: Transaction completes (20 + 30 = 50)
        - Cash received: 450,000 FSB
        - You no longer own asset_6
        - Price locked at day 20 value (450,000)
        - All taxes must be paid by day 50 (can be paid on day 20 or any day before day 50)
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

---

## 📰 Campaign News & Sentiment Analysis

**⚠️ IMPORTANT:** Don't just look at the candidates' platforms—watch the news cycle! 📺

Throughout Year 4, various news events and scandals will emerge that could affect each candidate's chances. A candidate with strong policies might face reputation damage from unexpected controversies, while a weaker candidate might gain momentum from positive press coverage.

### What to Watch For:

**🗞️ News Sentiment Indicators:**
- **Positive Coverage:** Policy announcements, endorsements, successful rallies
- **Negative Coverage:** Scandals, gaffes, controversial statements, investigations
- **Neutral/Mixed:** Debates, routine campaign events

**📊 Reputation Risk Factors:**
- **Santa's Vulnerabilities:** 
  - Incumbent fatigue after years in office
  - Past policy failures (remember the trickle-down economics disaster?)
  - Potential scandals about gift distribution favoritism
  - Luxury spending (that Lamborghini sleigh didn't age well...)

- **Grinch's Vulnerabilities:**
  - Controversial past (literally tried to steal Christmas once)
  - Harsh industrial policies might alienate voters
  - Reputation for being "anti-Christmas spirit"
  - Business dealings under scrutiny

### Strategic Implications

**Don't assume the favorite will win!** 🎲

A candidate leading in early polls might:
- Face a scandal that tanks their support
- Make a gaffe that shifts momentum
- Get caught in a controversy that changes everything

**Example Scenario:**
```
Day 20: Santa leads polls 60-40
        → Market prices in Santa victory
        → Santa-favored assets surge +30%

Day 35: BREAKING: Santa caught in gift-giving scandal! 🚨
        → News sentiment turns negative
        → Polls shift to 45-55 (Grinch leading)
        → Santa-favored assets crash -20%
        → Grinch-favored assets rally +25%
```

**💡 Pro Tip:** A candidate with better policies isn't guaranteed to win if they face reputation damage. Monitor news sentiment throughout the year—it might matter more than the platforms themselves!

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
  - pay_tax: asset_6       # Pay final taxes
  - pay_region_tax: Frostpeak  # Pay regional taxes
  - sell: asset_6          # Sell on same day! Completes day 50, price locked at day 20
40:
  - pay_tax: asset_1  # Now own it, taxes start
70:
  - buy: asset_13  # Last chance! Completes day 100
```

**Critical Notes:**
- Plan 30 days ahead
- You can pay taxes and sell on the same day (order doesn't matter)
- Taxes must be paid before the sell transaction completes (day 50 in example above)
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
- 📰 **Monitor news sentiment** - scandals and reputation matter more than platforms!
- 📊 **Lock in peaks** - sell when prices spike (30 days before they drop)
- 💰 **Manage cash flow** - pending buys tie up future cash
- ⏰ **Day 70 deadline** - last chance to reposition
- 🗳️ **Hedge your bets** - or go all-in on one candidate (risky!)
- 🧮 **Track pending transactions** - don't lose track of what's coming
- 🚨 **Watch for October surprises** - late-breaking scandals can flip everything
- 📈 **Trade the volatility** - news-driven price swings create opportunities

---

## Market Context for Year 4

Election speculation AND news sentiment are driving extreme volatility:

**Santa-Favored Assets** (Residential/Commercial in Frostpeak/Mistletoe)
- Days 1-30: Surge on polling data (+30-40%)
- Days 31-50: Correction on uncertainty (-10-15%)
- Days 51-70: Rally on late momentum (+20-30%)
- Days 71-100: Consolidation
- **⚠️ Scandal Risk:** Watch for negative news that could crash prices

**Grinch-Favored Assets** (Industrial/Commercial in Tinseltown/Evergreen)
- Days 1-30: Speculation rally (+25-35%)
- Days 31-50: Volatility on debates (-5-10%)
- Days 51-70: Strong finish (+15-25%)
- Days 71-100: Consolidation
- **⚠️ Scandal Risk:** Past controversies could resurface

**Non-Favored Assets**
- Stagnant or declining (-5% to +5%)
- Safe havens during volatility
- Poor Year 5 prospects

**Strategy Considerations:**
- **All-in on Santa**: Max returns if he wins, disaster if he loses (or faces scandal)
- **All-in on Grinch**: Max returns if he wins, disaster if he loses (or faces scandal)
- **Hedged**: Moderate returns regardless of outcome, protected from scandal risk
- **Cash-heavy**: Safe but misses upside
- **News-driven trading**: Buy the dips after scandals, sell the peaks after good news

## 🎁 The Final Countdown!

This is it, Chief Investment Elf! 🚀 Year 4 is your ultimate test of adaptability and strategic thinking. Navigate the bureaucracy, predict the election outcome, and position yourself for whatever Year 5 brings!

🎄🗳️ **May your trades be swift and your predictions be true!** 🗳️🎄
