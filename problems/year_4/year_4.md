# Year 4 : Election year

At the end of year 4 an election will be held. This will drastically change the tax rates and asset valuations for year 5. You must adapt your strategy accordingly.

To quell controversy around reindeer trafficking, Santa Claus, the current president, has enacted the Reindeer Protection Act, hoping it will improve his chances of re-election. To verify whether a transaction is funding reindeer trafficking each buy and sell now takes 30 days to process. Sell/buy prices are based on the day the action is initiated. If you initiate a sale you still have to pay taxes during the processing time. To ensure proper tax calculation by the PRS you cannot buy/sell past day 70.

In addition, if elected for another term, Santa plans to significantly bolster the following asset types and regions through improved tax rates in year 5: …

Not to be outdone, the opposition candidate, the Grinch, is promising tax reductions for the following asset types and regions: …

In either case tax reductions promise greatly increased valuations for the favored asset types and regions.

### Info

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



**[EXPLAIN WHEN AND HOW THE USERS CAN VOTE]**

Prepare for the aftermath of the upcoming election and adapt your investment strategy.

---

## Validations (in addition to year 1,2 and 3)

- You cannot buy/sell an asset if there is already a pending transaction for that asset.  
- You cannot buy/sell past day 70.  
- Taxes are still owed during the sell processing time.  
