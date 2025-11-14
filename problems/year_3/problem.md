# ⚖️ Year 3: Regional Reckoning 🗺️
## Difficulty: ⭐⭐⭐⭐☆ (Expert Elf Territory! 🧙‍♀️)

*"All real estate is local... especially when the local government is run by elves with agendas."* - Frosty Buffett

🎅 **Plot Twist Alert, Chief Investment Elf!** 🎅

The PRS coffers are overflowing, and Santa just bought himself a shiny new Lamborghini sleigh! 🏎️✨ But hold your reindeer—while the higher-ups are living large, our hardworking elves, faithful reindeer, and sweet gingerbread citizens are still struggling to make ends meet! 😢

Fear not! The North Pole Treasury has introduced a brilliant solution: **regional wealth redistribution**! 🗺️💝 New regional-based taxes and compliance requirements ensure prosperity flows to every corner of our magical realm.

Now you must navigate both regular asset taxes AND regional taxes, plus comply with strict regional investment limits. It's like juggling snowballs while riding a unicycle—challenging but totally doable for an elf of your caliber! 🤹‍♀️❄️

**The regional divide is real:**
- **Frostpeak**: Booming tech hub, aurora tourism, premium real estate
- **Tinseltown**: Struggling retail district, high taxes driving investors away
- **Evergreen Valley**: Steady industrial growth, moderate policies
- **Mistletoe Meadows**: Compliance-friendly, attracting new development

Your investment strategy must now account for regional performance, tax burdens, and portfolio limits. The days of concentrating all your wealth in one region are over.

---

## 🌍 The Challenge

## Regional Mechanics

### Regional Tax System

In addition to asset-type taxes (from Year 2), you now pay **regional taxes** based on where your properties are located.

**Regional Tax Formula:**
```
Regional Tax = Σ(All Assets in Region) × (Regional Tax Rate + Regional Rate Modifier × Days Since Last Payment)
```

**Key Differences from Asset Tax:**
- Calculated on **total regional holdings**, not individual assets
- Separate 30-day payment window per region
- Must be paid before selling any asset in that region

### Compliance Requirements

Each region has limits to prevent wealth concentration:

| Limit Type | Description |
|------------|-------------|
| `max_asset_number` | Maximum number of properties you can own in this region |
| `max_asset_value` | Maximum total value of all properties in this region |

**Compliance is checked:**
- When buying an asset (must not exceed limits after purchase)
- At day 100 (violations result in penalties)

**Example:**
```
Frostpeak limits: 5 assets max, 2,000,000 FSB total value max

Current holdings:
- asset_1: 250,000 FSB
- asset_5: 300,000 FSB
- asset_6: 450,000 FSB
- asset_13: 280,000 FSB
Total: 4 assets, 1,280,000 FSB ✓ Compliant

Can you buy another Frostpeak asset worth 800,000?
- Assets: 5 ✓ (at limit)
- Value: 2,080,000 ❌ (exceeds 2M cap)
Result: CANNOT BUY
```

---

## 📊 Challenge Files & Info

**📁 New Data Files:**
- 🗺️ `regional_tax_rates.csv` - Regional tax rates for Frostpeak, Tinseltown, Evergreen Valley, Mistletoe Meadows
- 📋 `compliance_requirements.csv` - Regional limits on asset number and total value

**🔄 Reused from Previous Years:**
- 🏠 `assets.csv` (Year 1)
- 📈 `valuations.csv` (Year 1)
- 💸 `tax_rates.csv` (Year 2)

**🆕 New Mechanics:**
- 🏛️ Regional taxes in addition to asset-type taxes
- ⚖️ Compliance limits: max number of assets and max total value per region

---

## 📥 Input Data Format

### 🗺️ `regional_tax_rates.csv`

| Column | Description |
|--------|-------------|
| `region` | Region name (Frostpeak, Tinseltown, Evergreen Valley, Mistletoe Meadows) |
| `tax_rate` | Base daily regional tax rate (as decimal) |
| `base_rate_modifier` | Additional rate per day of delay (as decimal) |

### 📋 `compliance_requirements.csv`

| Column | Description |
|--------|-------------|
| `region` | Region name |
| `max_asset_number` | Maximum number of assets allowed in this region |
| `max_asset_value` | Maximum total value (FSB) of assets in this region |

---

## 📤 Output Format

Another magical action joins your toolkit! 🎩✨ You can now pay regional taxes on top of your asset taxes, buying, and selling activities.

### 📋 `output.yml`

```yaml
1:
  - buy: id_1
2:
  - pay_tax: id_1
  - pay_region_tax: North
```

---

## ✅ Validation Rules

🚨 **All Year 1 & 2 rules still apply, PLUS:**
- 💰 You must have enough Frosty Bucks to pay regional taxes
- 🏠 You must own assets in a region to pay its regional tax
- ⏰ Regional tax must be paid within 30 days of the last payment
- ⚖️ You must comply with regional asset number and value limits at all times
- 🗓️ All regional tax must be paid by end of year
- 🤝 You must settle all taxes (asset AND regional) before selling an asset

---

## Scoring

Your performance is measured by **Total Wealth on Day 100**:

```
Score = Cash on Hand + Σ(Asset Valuations at day 100) - Tax Penalties - Compliance Penalties
```

**Penalties:**
- Unpaid taxes: 2× the tax owed
- Compliance violations: 10% of excess value

---

## Tips for Success

- 🗺️ **Diversify across regions** - don't hit compliance limits
- 📊 **Track regional exposure** - know your limits before buying
- 💰 **Regional tax timing** - coordinate with asset tax payments
- 🎯 **Focus on favorable regions** - Frostpeak and Mistletoe Meadows are booming
- ⚠️ **Avoid Tinseltown** - high taxes, stagnant growth
- 🔄 **Rebalance strategically** - sell in weak regions, buy in strong ones
- 🧮 **Calculate total tax burden** - asset tax + regional tax can be substantial

---

## Market Context for Year 3

Regional policies are creating dramatic divergence:

**🚀 Frostpeak** (Favorable policies)
- Residential: +35% from Year 1
- Commercial: +35% from Year 1
- Industrial: +35% from Year 1
- **Strategy**: Premium region, but watch compliance limits

**📉 Tinseltown** (High taxes, stagnation)
- All asset types: -1% to +8% from Year 1
- **Strategy**: Avoid or exit positions early

**📈 Evergreen Valley** (Moderate growth)
- All asset types: +12-21% from Year 1
- **Strategy**: Solid middle ground, good compliance limits

**🌱 Mistletoe Meadows** (Compliance-friendly)
- All asset types: +18-27% from Year 1
- **Strategy**: Attractive growth with reasonable limits

🎄🏆 **Regional harmony through smart investing—you've got this!** 🏆🎄