# Glacial Investment Corporation (GIC)

*"Ho ho... oh no!"* - Santa Claus, upon reviewing Q4 toy sales

The world is changing rapidly. Children are glued to their phones, TikTok dances have replaced toy trains, and the North Pole's traditional toy business is melting faster than a snowman in July. To ensure the prosperity of the North Pole and save Christmas for generations to come, the **Glacial Investment Corporation (GIC)** has been established.

**YOU** have been appointed as the **Chief Investment Elf (CIE)** - congratulations! 🎄 

But there's a catch: you're on a **5-year probation period**. Fail to grow the North Pole's wealth, and you'll be reassigned to coal sorting duty in the basement. No pressure!

Each year consists of **100 trading days** (represented as integers 1-100). Your performance will be evaluated at the end of Year 5 based on your total portfolio value.

---

## Year 1: Sleigh the Market 🛷

### The Challenge

Santa has entrusted you with **1,000,000 Frosty Bucks (FSB)** from the Pole Retirement Treasury. Your mission: invest wisely in North Pole real estate to maximize returns.

The market is volatile - asset valuations change daily based on factors like:
- 🎅 Holiday shopping trends
- 🦌 Reindeer migration patterns  
- ❄️ Blizzard insurance premiums
- 🎁 Gift production forecasts

**Warning:** The North Pole real estate market can be unpredictable! Some assets may soar to new heights, while others might crash harder than Rudolph on an icy rooftop. Not every investment is a winner - choose wisely!

Some premium properties don't come to market immediately - they have an `available_on_day` and can only be purchased on or after that day. Early birds might miss the best worms, but patient elves can catch the biggest fish!

### Your Goal

**Maximize your total wealth by day 100.** Your final score is:
```
Total Wealth = Cash on Hand + Sum of All Owned Asset Valuations (at day 100 prices)
```

Buy low, sell high, and don't get caught holding the bag when the market crashes!

---

## Input Files

You'll find these files in `data/year_1/`:

### `assets.csv`

Contains information about all available properties in the North Pole real estate market.

| Column | Description |
|--------|-------------|
| `id` | Unique asset identifier (e.g., `asset_1`) |
| `name` | Property name (e.g., "Snowflake Manor") |
| `type` | Asset type (all are "Real Estate" in Year 1) |
| `sub_type` | Property category: Residential, Commercial, or Industrial |
| `available_on_day` | First day this asset can be purchased (1-100) |
| `region` | Location: Frostpeak, Tinseltown, Evergreen Valley, or Mistletoe Meadows |

**Example rows:**
```csv
id,name,type,sub_type,available_on_day,region
asset_1,Snowflake Manor,Real Estate,Residential,1,Frostpeak
asset_2,Candy Cane Plaza,Real Estate,Commercial,1,Tinseltown
asset_3,Toy Factory Complex,Real Estate,Industrial,10,Evergreen Valley
```

**Total assets available:** 15

---

### `valuations.csv`

Contains daily market valuations for every asset across all 100 days.

| Column | Description |
|--------|-------------|
| `asset_id` | Asset identifier matching `assets.csv` |
| `day` | Trading day (1-100) |
| `valuation` | Market price in Frosty Bucks (FSB) |

**Example rows:**
```csv
asset_id,day,valuation
asset_1,1,151869
asset_1,2,155995
asset_1,3,151282
asset_2,1,303281
asset_2,2,309824
```

**Total rows:** 1,500 (15 assets × 100 days)

---

## Output Format

Submit your trading strategy as `output.yml` - a YAML file mapping days to actions.

### Structure

```yaml
<day>:
  - <action>: <asset_id>
  - <action>: <asset_id>
  ...
```

- **`<day>`**: Trading day (1-100)
- **`<action>`**: Either `buy` or `sell`
- **`<asset_id>`**: Asset identifier from `assets.csv`

### Example

```yaml
1:
  - buy: asset_1
5:
  - buy: asset_3
  - buy: asset_6
12:
  - sell: asset_1
  - buy: asset_2
50:
  - sell: asset_3
  - sell: asset_6
```

**Notes:**
- You can perform multiple actions on the same day
- Actions on the same day are executed in the order listed
- Days without actions can be omitted
- All transactions execute at that day's market price (from `valuations.csv`)

---

## Trading Rules & Validations

### ✅ Valid Transactions

1. **Sufficient Funds**: You must have enough FSB to buy an asset
   - Purchase price = asset's valuation on the purchase day
   
2. **Asset Availability**: Can only buy assets on or after their `available_on_day`
   - Example: If `available_on_day = 10`, you can buy on day 10, 11, 12... but not day 9

3. **Ownership Rules**:
   - Can only sell assets you currently own
   - Cannot buy an asset you already own (must sell first, then can re-buy)
   - Can buy and sell the same asset multiple times (just not simultaneously)

4. **Transaction Timing**: All transactions execute immediately at the current day's price

### ❌ Invalid Transactions

- Buying without sufficient cash
- Buying an asset you already own
- Selling an asset you don't own
- Buying an asset before its `available_on_day`

### 💰 Cash Flow

- **Starting cash**: 1,000,000 FSB
- **After buying**: Cash decreases by purchase price
- **After selling**: Cash increases by sale price
- **Year-end**: Remaining cash + owned assets (at day 100 prices) = Total Wealth

---

## Scoring

Your performance is measured by **Total Wealth on Day 100**:

```
Score = Cash on Hand + Σ(Valuation of Each Owned Asset on Day 100)
```

**Example:**
- Cash remaining: 200,000 FSB
- Own asset_5 (day 100 value: 325,983 FSB)
- Own asset_12 (day 100 value: 564,589 FSB)
- **Total Score: 1,090,572 FSB**

The elf with the highest score wins! 🏆

---

## Tips for Success

- 📊 **Study the trends carefully** - some assets are more volatile than others
- 📉 **Not all assets go up** - some may look good early but crash later
- ⏰ **Timing matters** - the market has ups and downs throughout the year
- 💰 **Keep cash reserves** - opportunities may arise when prices dip
- 🎯 **Remember the goal** - you're scored on day 100, not day 50
- 🧮 **Track your liquidity** - running out of cash means missing opportunities
- 🎲 **Diversification helps** - but choose wisely, not all assets are winners
- 🔄 **Active trading can pay off** - buy low, sell high isn't just a saying!