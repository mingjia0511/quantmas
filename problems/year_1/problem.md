# Glacial Investment Corporation (GIC)

The world is changing rapidly, children are increasingly on their phones and toys are becoming less popular. To ensure the prosperity of the North Pole, the Glacial Investment Corporation (GIC) has been established to manage and grow investments in the region. YOU are in charge of all investments made by the GIC and are in charge of saving Christmas for many years to come. You are on a probation period of 5 years to prove your worth as the chief investment elf (CIE). Each year consists of 100 days (represented with integer values).

## Year 1: Basic Asset Trading

You start with 1 million Frosty Bucks (FSB) from the Pole Retirement Treasury to invest in various assets. The asset valuations change daily and you must make strategic decisions to buy and sell throughout the year to maximize returns. Some properties come to market after a certain day and can only be purchased on or after that day.

### Info 

**Files:**
- `assets.csv` - 15 assets with properties (id, name, type, sub_type, available_on_day, region)
- `valuations.csv` - Daily valuations for all assets across 100 days (1,500 rows)

**Starting Capital:** 1,000,000 Frosty Bucks (FSB)


---

## Input

### `assets.csv`

| id   | name    | type        | sub_type     | available_on_day | region |
|------|----------|-------------|--------------|------------------|--------|
| id_1 | Asset 1  | Real Estate | Residential  | 1                | North  |
| id_2 | Asset 2  | Real Estate | Commercial   | 1                | South  |
| id_3 | Asset 3  | Real Estate | Industrial   | 10               | East   |

---

### `valuations.csv`

| asset_id | day | valuation |
|----------|------|-----------|
| id_1     | 1    | 100000    |
| id_1     | 2    | 200000    |
| id_1     | 200  | 150000    |
| id_2     | 1    | 300000    |
| id_2     | 2    | 250000    |

---

## Output

The output is a list of days with actions taken on those days. On each day you can buy or sell any number of assets. You must have the required Frosty Bucks to complete the transactions.

### `output.yml`

```yaml
1:
  - buy: id_1
2:
  - buy: id_2
3:
  - sell: id_1


## Validations
- You must have enough Frosty Bucks to buy an asset.
- You cannot buy an asset you already own (but can sell and re-buy).
- Asset must be available on the day of purchase (current day ≥ available_on_day).
- You must own the asset to sell it.



