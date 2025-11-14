## Year 3: Regional Reckoning 🗺️

*"All real estate is local... especially when the local government is run by elves with agendas."* - Frosty Buffett

### The Challenge

Year 2's tax system worked... too well. The PRS coffers are overflowing, but the wealth distribution across the North Pole is wildly uneven. Santa's got a new Lamborghini sleigh, but the elves, reindeer, and gingerbread citizens are struggling.

Enter the **North Pole Treasury Compliance Act** - a sweeping reform that introduces **regional taxes** and **compliance limits** to ensure wealth is distributed more evenly across all four regions.

**The regional divide is real:**
- **Frostpeak**: Booming tech hub, aurora tourism, premium real estate
- **Tinseltown**: Struggling retail district, high taxes driving investors away
- **Evergreen Valley**: Steady industrial growth, moderate policies
- **Mistletoe Meadows**: Compliance-friendly, attracting new development

Your investment strategy must now account for regional performance, tax burdens, and portfolio limits. The days of concentrating all your wealth in one region are over.

### Your Goal

**Maximize your total wealth by day 100** while navigating regional taxes and compliance requirements.

```
Total Wealth = Cash on Hand + Σ(Asset Valuations at day 100) - Tax Penalties
```

**New constraints:**
- Regional asset limits (can't own too many properties in one region)
- Regional value caps (total holdings per region capped)
- Regional taxes (in addition to asset-type taxes)

---

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

## Input Files

You'll find these files in `data/year_3/`:

### `regional_tax_rates.csv`

Contains tax rates by region.

| Column | Description |
|--------|-------------|
| `region` | Region name (Frostpeak, Tinseltown, Evergreen Valley, Mistletoe Meadows) |
| `tax_rate` | Base daily regional tax rate (as decimal) |
| `base_rate_modifier` | Additional rate per day of delay (as decimal) |

**Example rows:**
```csv
region,tax_rate,base_rate_modifier
Frostpeak,0.01,0.005
Tinseltown,0.015,0.007
Evergreen Valley,0.012,0.006
Mistletoe Meadows,0.011,0.0055
```

### `compliance_requirements.csv`

Contains regional portfolio limits.

| Column | Description |
|--------|-------------|
| `region` | Region name |
| `max_asset_number` | Maximum number of assets allowed in this region |
| `max_asset_value` | Maximum total value (FSB) of assets in this region |

**Example rows:**
```csv
region,max_asset_number,max_asset_value
Frostpeak,5,2000000
Tinseltown,4,1800000
Evergreen Valley,6,2200000
Mistletoe Meadows,5,1900000
```

### Reused Files from Previous Years

- `assets.csv` - Same properties (Year 1)
- `valuations.csv` - Updated market prices (Year 3 conditions)
- `tax_rates.csv` - Asset-type taxes still apply (Year 2)

---

## Output Format

Your `output.yml` now supports a new action: `pay_region_tax`

### Structure

```yaml
<day>:
  - <action>: <asset_id>
  - pay_tax: <asset_id>
  - pay_region_tax: <region_name>
  ...
```

### Example

```yaml
1:
  - buy: asset_1  # Frostpeak
  - buy: asset_6  # Frostpeak
10:
  - pay_tax: asset_1
  - pay_tax: asset_6
  - pay_region_tax: Frostpeak  # Pay regional tax for all Frostpeak assets
25:
  - buy: asset_2  # Tinseltown
50:
  - pay_region_tax: Frostpeak
  - pay_tax: asset_2
  - pay_region_tax: Tinseltown
```

**Notes:**
- Regional tax covers ALL assets in that region
- You still pay individual asset taxes separately
- Both must be settled before selling any asset in the region

---

## Trading Rules & Validations

### ✅ Valid Transactions (from Years 1-2)

All previous rules still apply:
- Sufficient funds, ownership rules, asset availability
- Asset-type tax payment (within 30 days, before selling)

### ✅ New Regional Rules

1. **Regional Tax Payment**
   - Pay regional tax for all assets in a region together
   - Must pay within 30 days of last payment
   - Must pay before selling any asset in that region

2. **Compliance Checks**
   - Cannot buy if it would exceed `max_asset_number` for that region
   - Cannot buy if total value would exceed `max_asset_value` for that region
   - Compliance checked at purchase time and day 100

3. **Year-End Settlement**
   - All regional taxes must be paid by day 100
   - Compliance violations result in penalties

### ❌ Invalid Transactions

- Buying an asset that would violate regional limits
- Selling an asset without paying regional tax for that region
- Letting regional tax go unpaid for more than 30 days
- Not paying all regional taxes by day 100

### 💰 Cash Flow

- **Regional tax**: Calculated on total regional holdings
- **Dual tax burden**: Asset tax + regional tax
- **Strategic diversification**: Spread across regions to manage limits

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

The regional divide is the story of Year 3. Choose your regions wisely! 🎄
