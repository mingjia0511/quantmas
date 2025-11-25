# 🎅 Year 1: Basic Asset Trading
## Difficulty: ⭐⭐☆☆☆ (Elf-level Easy!)

🎄 **Ho ho ho, new Chief Investment Elf!** 🎄

Welcome to your first year at the Glacial ELF Investment Corporation (GEIC)! The world is changing rapidly—children are increasingly glued to their magical glowing rectangles, and traditional toys are becoming less popular. But fear not! To ensure the prosperity of the North Pole for generations to come, the GEIC has been established to manage and grow our festive investments.

YOU have been chosen as our Chief Investment Elf (CIE) to save Christmas for many years ahead! Consider this your probationary period—you have 5 magical years to prove your worth. Each year consists of 100 merry days (represented with integer values from 1-100). Your performance will be evaluated at the end of Year 5 based on your total portfolio value.

Time to jingle those investment bells and make some Frosty Bucks! 💰❄️

---

## 🏠 Year 1: Sleigh the Market

You start with 1 million Frosty Bucks (FSB) straight from Santa's Pole Retirement Treasury! 🏦 Your mission is to invest wisely in various North Pole real estate assets. The valuations change daily like the Northern Lights, and you must make strategic decisions to buy and sell throughout the year to maximize returns. Your final score is:
```
Total Wealth = Cash on Hand + Sum of All Owned Asset Valuations (at day 100 prices)
```

### 🌍 The Macro Environment

The North Pole economy doesn't exist in a vacuum! Real estate values are influenced by broader economic forces. Two key macro indicators drive the market:

**📈 Inflation Index**
- Measures the general price level in the North Pole economy
- Rising inflation typically **benefits Residential assets** (housing as inflation hedge)
- Tracked daily from a base of 100

**💰 Interest Rate Index**
- The cost of borrowing Frosty Bucks (expressed as %)
- Rising interest rates typically **pressure Commercial assets** (higher cap rates, lower valuations)
- Affects financing costs for property acquisitions

**🏭 Industrial Assets**
- Respond to **both** inflation and interest rate dynamics
- More complex behavior patterns

💡 **Smart elves study these macro trends when making investment decisions!** The data is provided in `macro_indicators.csv` for your analysis.

### 💸 Transaction Costs

Real estate transactions aren't free! Each trade incurs realistic market costs:

- **Buying**: You pay **1% above** the market valuation
- **Selling**: You receive **1% below** the market valuation

**Example:**
If `asset_1` has a market valuation of 100,000 FSB on day 50:
- **Buy price**: 101,000 FSB (100,000 × 1.01)
- **Sell proceeds**: 99,000 FSB (100,000 × 0.99)
- **Round-trip cost**: 2,000 FSB (2% total)

🎯 **Trade wisely—frequent trading eats into your returns!** Transaction costs reflect broker fees, legal costs, and market friction in real estate deals.

### ⏳ Illiquidity & Holding Periods

Real estate is not like stocks—you can't flip properties overnight! The North Pole real estate market has realistic settlement and due diligence periods.

**Rule**: You must hold any purchased asset for **at least 10 days** before selling it.

**Example:**
- Buy `asset_1` on day 5
- ❌ Cannot sell on days 5-14
- ✅ Earliest sale date: day 15

🏠 **This reflects the reality of property transactions**: inspections, legal reviews, closing periods, and settlement times. Plan your strategy accordingly!

### 📊 Market Dynamics

The market is volatile - asset valuations change daily based on factors like:
- 🎅 Holiday shopping trends
- 🦌 Reindeer migration patterns
- ❄️ Blizzard insurance premiums
- 🎁 Gift production forecasts
- 📈 Inflation and interest rate movements

**Warning:** The North Pole real estate market can be unpredictable! Some assets may soar to new heights, while others might crash harder than Rudolph on an icy rooftop. Not every investment is a winner - choose wisely!

**Special Note:** Some premium properties come to market after a certain day and can only be purchased on or after their availability date. Think of them as exclusive Christmas listings! 🏡✨

## 📊 Challenge Files & Info

**📁 Data Files:**
- 🏠 `assets.csv` - 15 magical properties with details (id, name, type, sub_type, available_on_day, region)
- 📈 `valuations.csv` - Daily market values for all assets across 100 festive days (1,500 rows of data)
- 🌍 `macro_indicators.csv` - Daily inflation and interest rate indices (100 rows)
- 📊 `scoring_methodology.md` - **NEW!** Detailed explanation of multi-objective scoring

**💰 Starting Capital:** 1,000,000 Frosty Bucks (FSB)

---

## 📥 Input Data Format

### 🏠 `assets.csv`

| Column | Description |
|--------|-------------|
| `id` | Unique asset identifier (e.g., `asset_1`) |
| `name` | Property name (e.g., "Snowflake Manor") |
| `type` | Asset type (all are "Real Estate" in Year 1) |
| `sub_type` | Property category: Residential, Commercial, or Industrial |
| `available_on_day` | First day this asset can be purchased (1-100) |
| `region` | Location: Frostpeak, Tinseltown, Evergreen Valley, or Mistletoe Meadows |

### 📈 `valuations.csv`

| Column | Description |
|--------|-------------|
| `asset_id` | Asset identifier matching `assets.csv` |
| `day` | Trading day (1-100) |
| `valuation` | Market price in Frosty Bucks (FSB) - **before transaction costs** |

### 🌍 `macro_indicators.csv`

| Column | Description |
|--------|-------------|
| `day` | Trading day (1-100) |
| `inflation_index` | Inflation index (base = 100 on day 1) |
| `interest_rate_index` | Interest rate level (expressed as %) |

---

## 📤 Output Format

Your festive trading decisions should be recorded as a list of daily actions! 🎯 On each day you can buy or sell any number of assets, but remember—you must have enough Frosty Bucks to complete the transactions!

### 📋 `output.yml`

```yaml
1:
  - buy: asset_1
2:
  - buy: asset_2
3:
  - sell: asset_1
```

---

## ✅ Validation Rules

🚨 **Important Trading Rules to Follow:**

### Basic Rules
- 💰 You must have enough Frosty Bucks to buy an asset (including the 1% transaction cost)
- 🏠 You cannot buy an asset you already own (but can sell and re-buy later!)
- 📅 Asset must be available on the day of purchase (current day ≥ available_on_day)
- 🤝 You must own the asset to sell it

### Transaction Cost Rules
- 📈 **Buy Price** = `valuation × 1.01` (you pay 1% above market)
- 📉 **Sell Proceeds** = `valuation × 0.99` (you receive 1% below market)
- 💸 Your cash must cover the full buy price (including the 1% premium)

### Holding Period Rules
- ⏳ You must hold any asset for **at least 10 days** after purchase
- 🚫 Attempting to sell before the holding period expires is invalid
- ✅ Track purchase dates: if bought on day X, earliest sale is day X+10

**Example Scenario:**
```
Day 5: Buy asset_1 at valuation 100,000 FSB
       → Cost: 101,000 FSB (100,000 × 1.01)
       → Cash reduced by 101,000 FSB
       
Day 10: Try to sell asset_1 ❌ INVALID (only held 5 days)

Day 15: Sell asset_1 at valuation 105,000 FSB ✅ VALID
        → Proceeds: 103,950 FSB (105,000 × 0.99)
        → Net gain: 2,950 FSB (despite 5% valuation increase)
```

---

## 🎯 Multi-Objective Scoring (NEW!)

**Year 1 introduces a critical investing concept:** Returns aren't everything—**risk-adjusted returns** matter!

Your performance is evaluated across **THREE dimensions**:

### 1. Terminal Wealth (60 points)
```
Terminal Wealth = Cash on Hand + Σ(Valuation of Each Owned Asset on Day 100)
Wealth Score = (Terminal Wealth / 1,500,000) × 60
```

**Target:** 1,500,000 FSB (50% gain from starting capital)

### 2. Sharpe Ratio (25 points)
```
Sharpe Ratio = (Mean Daily Return / StdDev Daily Return) × √100
Sharpe Score = min(Sharpe Ratio × 10, 25)
```

**What it measures:** Risk-adjusted returns (reward per unit of risk)
- Higher Sharpe = More consistent returns with less volatility
- Improved by diversification and avoiding large drawdowns

### 3. Max Drawdown (15 points)
```
Max Drawdown = Worst peak-to-trough decline during the year
Drawdown Score = 15 × (1 - Max Drawdown)
```

**What it measures:** Portfolio resilience
- Lower drawdown = Better risk management
- Improved by diversification and maintaining cash buffers

### Final Score
```
Total Score = Wealth Score + Sharpe Score + Drawdown Score
Maximum: 100 points
```

### 📊 Strategy Comparison

**Aggressive (All-in on one asset):**
- Wealth: 1,600,000 → 64 pts | Sharpe: 0.8 → 8 pts | Drawdown: 45% → 8.25 pts
- **Total: 80.25 points**

**Balanced (Diversified portfolio):**
- Wealth: 1,450,000 → 58 pts | Sharpe: 1.5 → 15 pts | Drawdown: 20% → 12 pts
- **Total: 85 points** ✅ **Often wins despite lower wealth!**

**Conservative (Mostly cash):**
- Wealth: 1,100,000 → 44 pts | Sharpe: 0.3 → 3 pts | Drawdown: 5% → 14.25 pts
- **Total: 61.25 points**

📖 **For detailed scoring methodology, see `scoring_methodology.md`**

---

## Tips for Success

### For Terminal Wealth (60 points):
- 📊 **Study the trends carefully** - some assets are more volatile than others
- 🌍 **Watch the macro indicators** - inflation and interest rates drive asset class performance
- 📉 **Not all assets go up** - some may look good early but crash later
- ⏰ **Timing matters** - the market has ups and downs throughout the year
- 🎯 **Remember the goal** - you're scored on day 100, not day 50

### For Sharpe Ratio (25 points):
- 🎲 **Diversify across 5-8 assets** - reduces volatility and improves risk-adjusted returns
- 🔄 **Avoid over-concentration** - don't put all eggs in one basket
- 📈 **Seek consistent growth** - smooth returns beat erratic swings
- 🏠 **Mix asset types** - Residential, Commercial, and Industrial respond differently to macro conditions
- 💰 **Maintain some cash** - reduces portfolio volatility

### For Max Drawdown (15 points):
- 🛡️ **Never go all-in** - concentration risk leads to large drawdowns
- 💵 **Keep 10-20% cash buffer** - provides cushion against market drops
- 🌍 **Diversify across regions** - Frostpeak, Tinseltown, Evergreen Valley, Mistletoe Meadows
- 📉 **Avoid buying at peaks** - wait for better entry points
- ⚖️ **Balance your portfolio** - don't let one asset dominate

### General Strategy:
- 💸 **Transaction costs add up** - frequent trading (2% round-trip cost) can erode gains
- ⏳ **Plan for illiquidity** - 10-day holding periods mean you can't react instantly
- 🔄 **Strategic trading beats day-trading** - real estate rewards patience and planning
- 🧮 **Track your liquidity** - running out of cash means missing opportunities
- 📊 **Monitor all three metrics** - optimize for total score, not just wealth

## 🎁 Good Luck, Chief Investment Elf!

May your portfolio be merry and bright! Remember, this is just the beginning of your 5-year journey to save Christmas through smart investments. Show Santa what you're made of!

🎅✨ **Ho ho ho, now get out there and make some magical returns!** ✨🎄



