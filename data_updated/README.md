# Quantmas Challenge Data Files

This directory contains all the CSV data files needed for the 5-year Glacial Investment Corporation (GIC) challenge.

## Directory Structure

```
data/
├── year_1/          # Basic Asset Trading
│   ├── assets.csv
│   └── valuations.csv
├── year_2/          # Polar Revenue Service (Tax System)
│   └── tax_rates.csv          # New file (reuse year_1 assets & valuations)
├── year_3/          # North Pole Treasury Compliance (Regional Taxes)
│   ├── regional_tax_rates.csv # New file
│   └── compliance_requirements.csv # New file
├── year_4/          # Election Year (Transaction Processing Delays)
│   └── election_info.csv      # New file
└── year_5/          # Election Aftermath
    ├── santa_wins/  # Data if Santa Claus wins election
    │   ├── valuations.csv     # Modified valuations
    │   ├── tax_rates.csv      # Modified tax rates
    │   └── regional_tax_rates.csv # Modified regional rates
    └── grinch_wins/ # Data if The Grinch wins election
        ├── valuations.csv     # Modified valuations
        ├── tax_rates.csv      # Modified tax rates
        └── regional_tax_rates.csv # Modified regional rates
```

**Note:** Files not present in a year directory should be reused from the previous year(s):
- Years 2-4 reuse `assets.csv` and `valuations.csv` from Year 1
- Years 3-4 reuse `tax_rates.csv` from Year 2
- Year 4 reuses `regional_tax_rates.csv` and `compliance_requirements.csv` from Year 3
- Year 5 reuses `assets.csv` and `compliance_requirements.csv` from Year 1/3

## Year 1: Basic Asset Trading

**Files:**
- `assets.csv` - 15 assets with properties (id, name, type, sub_type, available_on_day, region)
- `valuations.csv` - Daily valuations for all assets across 100 days (1,500 rows)

**Starting Capital:** 1,000,000 Frosty Bucks (FSB)

## Year 2: Polar Revenue Service

**New Files:**
- `tax_rates.csv` - Tax rates by asset type/subtype that change throughout the year

**Reused from Year 1:**
- `assets.csv`
- `valuations.csv`

**New Mechanics:**
- Daily tax on owned assets based on current valuation
- Tax can be postponed up to 30 days with increasing base rate modifier
- Tax formula: `tax = current_valuation * (tax_rate + (base_rate_modifier * days_since_last_payment))`

## Year 3: North Pole Treasury Compliance

**New Files:**
- `regional_tax_rates.csv` - Regional tax rates for Frostpeak, Tinseltown, Evergreen Valley, Mistletoe Meadows
- `compliance_requirements.csv` - Regional limits on asset number and total value

**Reused from Previous Years:**
- `assets.csv` (Year 1)
- `valuations.csv` (Year 1)
- `tax_rates.csv` (Year 2)

**New Mechanics:**
- Regional taxes in addition to asset-type taxes
- Compliance limits: max number of assets and max total value per region

## Year 4: Election Year

**New Files:**
- `election_info.csv` - Candidate policies and their impact on Year 5

**Reused from Previous Years:**
- `assets.csv` (Year 1)
- `valuations.csv` (Year 1)
- `tax_rates.csv` (Year 2)
- `regional_tax_rates.csv` (Year 3)
- `compliance_requirements.csv` (Year 3)

**New Mechanics:**
- 30-day processing time for all buy/sell transactions (Reindeer Protection Act)
- Cannot buy/sell after day 70
- Taxes still owed during sell processing time
- Election determines Year 5 conditions

**Election Candidates:**
- **Santa Claus**: Favors Residential/Commercial assets in Frostpeak/Mistletoe Meadows regions
  - 25% tax reduction, 30% valuation boost for favored assets in Year 5
- **The Grinch**: Favors Industrial/Commercial assets in Tinseltown/Evergreen Valley regions
  - 30% tax reduction, 35% valuation boost for favored assets in Year 5

## Year 5: Election Aftermath

**Files (two scenarios):**

### If Santa Wins (`santa_wins/`)
**New/Modified Files:**
- `valuations.csv` - Boosted valuations (+30%) for Residential/Commercial in Frostpeak/Mistletoe Meadows
- `tax_rates.csv` - Reduced tax rates (-25%) for Residential/Commercial
- `regional_tax_rates.csv` - Reduced rates (-25%) for Frostpeak/Mistletoe Meadows regions

**Reused from Previous Years:**
- `assets.csv` (Year 1)
- `compliance_requirements.csv` (Year 3)

**Boosted Assets:** asset_1, asset_4, asset_5, asset_9, asset_13

### If Grinch Wins (`grinch_wins/`)
**New/Modified Files:**
- `valuations.csv` - Boosted valuations (+35%) for Industrial/Commercial in Tinseltown/Evergreen Valley
- `tax_rates.csv` - Reduced tax rates (-30%) for Industrial/Commercial
- `regional_tax_rates.csv` - Reduced rates (-30%) for Tinseltown/Evergreen Valley regions

**Reused from Previous Years:**
- `assets.csv` (Year 1)
- `compliance_requirements.csv` (Year 3)

**Boosted Assets:** asset_2, asset_3, asset_8, asset_11, asset_14, asset_15

## Asset Details

| ID | Name | Type | Sub-Type | Available Day | Region |
|----|------|------|----------|---------------|--------|
| asset_1 | Snowflake Manor | Real Estate | Residential | 1 | Frostpeak |
| asset_2 | Candy Cane Plaza | Real Estate | Commercial | 1 | Tinseltown |
| asset_3 | Toy Factory Complex | Real Estate | Industrial | 10 | Evergreen Valley |
| asset_4 | Gingerbread Village | Real Estate | Residential | 1 | Mistletoe Meadows |
| asset_5 | Ice Rink Center | Real Estate | Commercial | 15 | Frostpeak |
| asset_6 | Reindeer Stables | Real Estate | Industrial | 1 | Frostpeak |
| asset_7 | Elf Quarters | Real Estate | Residential | 20 | Tinseltown |
| asset_8 | Workshop Warehouse | Real Estate | Industrial | 5 | Evergreen Valley |
| asset_9 | Sleigh Showroom | Real Estate | Commercial | 25 | Mistletoe Meadows |
| asset_10 | Frozen Lake Resort | Real Estate | Residential | 30 | Evergreen Valley |
| asset_11 | North Star Mall | Real Estate | Commercial | 1 | Tinseltown |
| asset_12 | Gift Wrapping Plant | Real Estate | Industrial | 35 | Mistletoe Meadows |
| asset_13 | Aurora Apartments | Real Estate | Residential | 40 | Frostpeak |
| asset_14 | Mistletoe Market | Real Estate | Commercial | 45 | Evergreen Valley |
| asset_15 | Cookie Factory | Real Estate | Industrial | 50 | Tinseltown |

## Data Characteristics

- **100 days per year** (represented as integers 1-100)
- **15 assets** with varying availability dates
- **4 regions**: Frostpeak, Tinseltown, Evergreen Valley, Mistletoe Meadows
- **3 asset sub-types**: Residential, Commercial, Industrial
- **Valuations**: Range from ~75,000 to ~1,500,000 FSB with daily volatility
- **Tax rates**: Range from 0.75% to 1.8% with modifiers from 0.375% to 0.85%

## Christmas-Themed Regions

- **Frostpeak**: The icy northern highlands where the aurora dances
- **Tinseltown**: The glittering southern district of holiday cheer
- **Evergreen Valley**: The eastern forest region filled with Christmas trees
- **Mistletoe Meadows**: The western countryside of festive traditions

## Notes

- All monetary values are in Frosty Bucks (FSB)
- Valuations include realistic market volatility and trends
- Tax rates increase throughout each year to simulate policy changes
- Regional compliance limits ensure portfolio diversification
- Election outcomes significantly impact Year 5 strategy
