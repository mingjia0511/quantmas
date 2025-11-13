# Year 2: Polar revenue service

Your investments have been successful and it's time to start giving back. The Polar Revenue Service (PRS) has been founded and a new tax system on asset holdings has been introduced. You must now pay taxes on the assets you own based on their daily valuations.

---

## Tax calculation

The tax is owed daily on the properties you own based on the current valuation of your asset (not the valuation at the time it was bought). However, you can postpone the payment of the tax for up to 30 days. The longer you wait to pay, the higher the tax rate becomes due to a base rate modifier that increases with each day you delay payment. This might be worth it however if you expect the asset’s valuation to decrease significantly in the coming days.

**Tax Formula:**
tax = current_valuation * (tax_rate + (base_rate_modifier * days_since_last_payment))


**Example 1:**

- day 1: valuation = 100,000, tax rate 1%, base modifier 0.5%
  - tax owed = 100000 * (0.01 + (0.005 * 1)) = 1,500  
- day 2: valuation = 200,000  
  - tax owed = 200000 * (0.01 + (0.005 * 1)) = 3,000  
- day 3: valuation = 300,000  
  - tax owed = 300000 * (0.01 + (0.005 * 1)) = 4,500  
- day 4: valuation = 350,000  
  - tax owed = 350000 * (0.01 + (0.005 * 1)) = 5,250  

**Example 2:**  
(Same structure but with multiple days skipped — omitted here for brevity.)

---

## Input

### `tax_rates.csv`

| asset_type  | asset_sub_type | day | tax_rate | base_rate_modifier |
|-------------|----------------|-----|----------|---------------------|
| Real Estate | Residential    | 1   | 0.01     | 0.005               |
| Real Estate | Commercial     | 2   | 0.015    | 0.007               |

---

## Output

You may now do an addition action on each day to pay the full tax owed on an asset you own.

### `output.yml`

```yaml
1:
  - buy: id_1
2:
  - pay_tax: id_1
  - buy: id_2

## Validations (in addition to year 1)
- You must have enough Frosty Bucks to pay the tax.
- You must own the asset to pay tax.
- Tax must be paid within 30 days of the last tax payment for the asset.
- All tax must be paid by the end of the year.
- You must pay the tax owed for an asset in full on the day you choose to pay it.
- You must settle tax before selling an asset.