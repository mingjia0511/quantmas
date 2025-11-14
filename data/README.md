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





## Year 4: Election Year


## Year 5: Election Aftermath


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
