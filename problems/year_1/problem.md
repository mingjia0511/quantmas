# 🎅 Year 1: Basic Asset Trading
## Difficulty: ⭐⭐☆☆☆ (Elf-level Easy!)

🎄 **Ho ho ho, new Chief Investment Elf!** 🎄

Welcome to your first year at the Glacial Investment Corporation (GIC)! The world is changing rapidly—children are increasingly glued to their magical glowing rectangles, and traditional toys are becoming less popular. But fear not! To ensure the prosperity of the North Pole for generations to come, the GIC has been established to manage and grow our festive investments.

YOU have been chosen as our Chief Investment Elf (CIE) to save Christmas for many years ahead! Consider this your probationary period—you have 5 magical years to prove your worth. Each year consists of 100 merry days (represented with integer values from 1-100).

Time to jingle those investment bells and make some Frosty Bucks! 💰❄️

---

## 🏠 The Challenge

You start with 1 million Frosty Bucks (FSB) straight from Santa's Pole Retirement Treasury! 🏦 Your mission is to invest wisely in various North Pole real estate assets. The valuations change daily like the Northern Lights, and you must make strategic decisions to buy and sell throughout the year to maximize returns. 

🎁 **Special Note:** Some premium properties come to market after a certain day and can only be purchased on or after their availability date. Think of them as exclusive Christmas listings! 🏡✨

## 📊 Challenge Files & Info 

**📁 Data Files:**
- 🏠 `assets.csv` - 15 magical properties with details (id, name, type, sub_type, available_on_day, region)
- 📈 `valuations.csv` - Daily market values for all assets across 100 festive days (1,500 rows of data)

**💰 Starting Capital:** 1,000,000 Frosty Bucks (FSB)

---

## 📥 Input Data Format

### 🏠 `assets.csv`

| id   | name    | type        | sub_type     | available_on_day | region |
|------|----------|-------------|--------------|------------------|--------|
| id_1 | Asset 1  | Real Estate | Residential  | 1                | North  |
| id_2 | Asset 2  | Real Estate | Commercial   | 1                | South  |
| id_3 | Asset 3  | Real Estate | Industrial   | 10               | East   |

### 📈 `valuations.csv`

| asset_id | day | valuation |
|----------|------|-----------|
| id_1     | 1    | 100000    |
| id_1     | 2    | 200000    |
| id_1     | 200  | 150000    |
| id_2     | 1    | 300000    |
| id_2     | 2    | 250000    |

---

## 📤 Output Format

Your festive trading decisions should be recorded as a list of daily actions! 🎯 On each day you can buy or sell any number of assets, but remember—you must have enough Frosty Bucks to complete the transactions!

### 📋 `output.yml`

```yaml
1:
  - buy: id_1
2:
  - buy: id_2
3:
  - sell: id_1
```

---

## ✅ Validation Rules

🚨 **Important Trading Rules to Follow:**
- 💰 You must have enough Frosty Bucks to buy an asset
- 🏠 You cannot buy an asset you already own (but can sell and re-buy later!)
- 📅 Asset must be available on the day of purchase (current day ≥ available_on_day)
- 🤝 You must own the asset to sell it

---

## 🎁 Good Luck, Chief Investment Elf!

May your portfolio be merry and bright! Remember, this is just the beginning of your 5-year journey to save Christmas through smart investments. Show Santa what you're made of! 

🎅✨ **Ho ho ho, now get out there and make some magical returns!** ✨🎄



