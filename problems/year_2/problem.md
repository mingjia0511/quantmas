# 🎄 Year 2: Polar Revenue ServiceThe tax is owed daily on the properties you own based on the **current valuation** of your asset (not what you paid for it! 📈). However, you can postpone payment for up to 30 days... but beware! 😱 

The longer you wait, the higher the tax rate becomes due to a base rate modifier that increases with each day you delay payment. This might be worth the risk if you expect the asset's valuation to drop significantly! 📉💭

**🧮 Tax Formula:**
```
tax = current_valuation × (tax_rate + (base_rate_modifier × days_since_last_payment))
```

**🎯 Example 1: Paying Daily**ficulty: ⭐⭐⭐☆☆ (Getting Spicy! 🌶️)

🎅 **Congratulations, Chief Investment Elf!** 🎅

Your Year 1 investments have been absolutely magical! 🌟 But as Uncle Ben Spider-man once said, "With great returns come great responsibilities..." It's time to give back to the North Pole community!

The newly founded **Polar Revenue Service (PRS)** has arrived with jingle bells and tax bills! 🔔💸 A shiny new tax system on asset holdings has been introduced. Now you must pay taxes on the assets you own based on their daily valuations.

But wait—there's a twist! 🎭 You can play the postponement game for up to 30 days, though it'll cost you more the longer you wait. Will you pay up front or gamble on market timing? The choice is yours, brave elf! ❄️💰

---

## 🏛️ The Challenge


## 📊 Challenge Files & Info

**📁 New Data Files:**
- 💸 `tax_rates.csv` - Tax rates by asset type/subtype that change throughout the year

**🔄 Reused from Year 1:**
- 🏠 `assets.csv`
- 📈 `valuations.csv`

**🆕 New Mechanics:**
- 📅 Daily tax owed on owned assets based on current valuation
- ⏰ Tax can be postponed up to 30 days with increasing penalties
- 📊 Tax formula: `tax = current_valuation × (tax_rate + (base_rate_modifier × days_since_last_payment))`

---

## 🧮 Tax Calculation Magic

The tax is owed daily on the properties you own based on the current valuation of your asset (not the valuation at the time it was bought). However, you can postpone the payment of the tax for up to 30 days. The longer you wait to pay, the higher the tax rate becomes due to a base rate modifier that increases with each day you delay payment. This might be worth it however if you expect the asset’s valuation to decrease significantly in the coming days.

**Tax Formula:**
tax = current_valuation * (tax_rate + (base_rate_modifier * days_since_last_payment))


**Example 1:**

- day 1: valuation = 100,000, tax rate 1%, base modifier 0.5%
  - tax owed = 100000 × (0.01 + (0.005 × 1)) = 1,500 FSB 💰
- day 2: valuation = 200,000  
  - tax owed = 200000 × (0.01 + (0.005 × 1)) = 3,000 FSB 💰
- day 3: valuation = 300,000  
  - tax owed = 300000 × (0.01 + (0.005 × 1)) = 4,500 FSB 💰
- day 4: valuation = 350,000  
  - tax owed = 350000 × (0.01 + (0.005 × 1)) = 5,250 FSB 💰

**(The pattern continues with more complex examples involving postponement...)**

---

## 📥 Input Data Format

### 💸 `tax_rates.csv`

| asset_type  | asset_sub_type | day | tax_rate | base_rate_modifier |
|-------------|----------------|-----|----------|---------------------|
| Real Estate | Residential    | 1   | 0.01     | 0.005               |
| Real Estate | Commercial     | 2   | 0.015    | 0.007               |

---

## 📤 Output Format

You now have a magical new action available! 🪄 You can pay taxes on any day in addition to your buying and selling activities.

### 📋 `output.yml`

```yaml
1:
  - buy: id_1
2:
  - pay_tax: id_1
  - buy: id_2
```

---

## ✅ Validation Rules

🚨 **All Year 1 rules still apply, PLUS:**
- 💰 You must have enough Frosty Bucks to pay the tax
- 🏠 You must own the asset to pay tax on it
- ⏰ Tax must be paid within 30 days of the last tax payment for the asset
- 🗓️ All tax must be paid by the end of the year
- 💯 You must pay the tax owed for an asset in full on the day you choose to pay it
- 🤝 You must settle all outstanding tax before selling an asset

---

## 🎁 Keep Up the Great Work!

The PRS might have their eye on you now, but smart tax planning is just another skill in your Chief Investment Elf toolkit! Master the art of timing and watch your portfolio grow even stronger! 

🎄💪 **May your taxes be low and your returns be high!** 💪🎄