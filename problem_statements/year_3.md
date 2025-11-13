# Year 3: North pole treasury compliance

The federal pockets of the PRS are quite full and Santa has a brand new Lamborghini sleigh. However the elves, reindeer and gingerbread men are still struggling to make ends meet. To ensure that the wealth is now more evenly distributed across the North Pole regions, new regional-based taxes and compliance requirements have been introduced. You must now pay regional taxes based on the region of the asset you own and also comply with regional limits on the number and value of assets you can hold in each region.

---

## Input

### `regional_tax_rates.csv`

| region | tax_rate | base_rate_modifier |
|--------|-----------|----------------------|
| North  | 0.01      | 0.005                |
| South  | 0.015     | 0.007                |

### `compliance_requirements.csv`

| region | max_asset_number | max_asset_value |
|--------|-------------------|-----------------|
| North  | 5                 | 1000000         |
| South  | 3                 | 500000          |

---

## Output

You may now do an additional action on each day to pay the full regional tax owed on an asset you own.

### `output.yml`

```yaml
1:
  - buy: id_1
2:
  - pay_tax: id_1
  - pay_region_tax: North

## Validations (in addition to year 1 and 2)
- You must have enough Frosty Bucks to pay the regional tax.
- You must own the asset to pay regional tax.
- Regional tax must be paid within 30 days of the last payment.
- You must comply with regional asset number and value limits.
- All regional tax must be paid by end of year.
- You must settle tax before selling an asset.