# 🎅 Year 1: Basic Asset Trading
## Difficulty: ⭐⭐☆☆☆ (Elf-level Easy!)

🎄 **Ho ho ho, new Chief Investment Elf!** 🎄

Welcome to your first year at the Glacial Investment Corporation (GIC)! The world is changing rapidly—children are increasingly glued to their magical glowing rectangles, and traditional toys are becoming less popular. But fear not! To ensure the prosperity of the North Pole for generations to come, the GIC has been established to manage and grow our festive investments.

YOU have been chosen as our Chief Investment Elf (CIE) to save Christmas for many years ahead! Consider this your probationary period—you have 5 magical years to prove your worth. Each year consists of 100 merry days (represented with integer values from 1-100). Your performance will be evaluated at the end of Year 5 based on your total portfolio value.

Time to jingle those investment bells and make some Frosty Bucks! 💰❄️

---

## 🏠 Year 1: Sleigh the Market

You start with 1 million Frosty Bucks (FSB) straight from Santa's Pole Retirement Treasury! 🏦 Your mission is to invest wisely in various North Pole real estate assets. The valuations change daily like the Northern Lights, and you must make strategic decisions to buy and sell throughout the year to maximize returns. Your final score is:
```
Total Wealth = Cash on Hand + Sum of All Owned Asset Valuations (at day 100 prices)
```

The market is volatile - asset valuations change daily based on factors like:
- 🎅 Holiday shopping trends
- 🦌 Reindeer migration patterns
- ❄️ Blizzard insurance premiums
- 🎁 Gift production forecasts

**Warning:** The North Pole real estate market can be unpredictable! Some assets may soar to new heights, while others might crash harder than Rudolph on an icy rooftop. Not every investment is a winner - choose wisely!

**Special Note:** Some premium properties come to market after a certain day and can only be purchased on or after their availability date. Think of them as exclusive Christmas listings! 🏡✨

## 📊 Challenge Files & Info

**📁 Data Files:**
- 🏠 `assets.csv` - 15 magical properties with details (id, name, type, sub_type, available_on_day, region)
- 📈 `valuations.csv` - Daily market values for all assets across 100 festive days (1,500 rows of data)

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
| `valuation` | Market price in Frosty Bucks (FSB) |

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
- 💰 You must have enough Frosty Bucks to buy an asset
- 🏠 You cannot buy an asset you already own (but can sell and re-buy later!)
- 📅 Asset must be available on the day of purchase (current day ≥ available_on_day)
- 🤝 You must own the asset to sell it

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

## Tips for Success

- 📊 **Study the trends carefully** - some assets are more volatile than others
- 📉 **Not all assets go up** - some may look good early but crash later
- ⏰ **Timing matters** - the market has ups and downs throughout the year
- 💰 **Keep cash reserves** - opportunities may arise when prices dip
- 🎯 **Remember the goal** - you're scored on day 100, not day 50
- 🧮 **Track your liquidity** - running out of cash means missing opportunities
- 🎲 **Diversification helps** - but choose wisely, not all assets are winners
- 🔄 **Active trading can pay off** - buy low, sell high isn't just a saying!

## 🎁 Good Luck, Chief Investment Elf!

May your portfolio be merry and bright! Remember, this is just the beginning of your 5-year journey to save Christmas through smart investments. Show Santa what you're made of!

🎅✨ **Ho ho ho, now get out there and make some magical returns!** ✨🎄



