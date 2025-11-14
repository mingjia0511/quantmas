# ⚖️ Year 3: North Pole Treasury Compliance  
## Difficulty: ⭐⭐⭐⭐☆ (Expert Elf Territory! 🧙‍♀️)

🎅 **Plot Twist Alert, Chief Investment Elf!** 🎅

The PRS coffers are overflowing, and Santa just bought himself a shiny new Lamborghini sleigh! 🏎️✨ But hold your reindeer—while the higher-ups are living large, our hardworking elves, faithful reindeer, and sweet gingerbread citizens are still struggling to make ends meet! 😢

Fear not! The North Pole Treasury has introduced a brilliant solution: **regional wealth redistribution**! 🗺️💝 New regional-based taxes and compliance requirements ensure prosperity flows to every corner of our magical realm.

Now you must navigate both regular asset taxes AND regional taxes, plus comply with strict regional investment limits. It's like juggling snowballs while riding a unicycle—challenging but totally doable for an elf of your caliber! 🤹‍♀️❄️

---

## 🌍 The Challenge

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

| region | tax_rate | base_rate_modifier |
|--------|-----------|----------------------|
| North  | 0.01      | 0.005                |
| South  | 0.015     | 0.007                |

### 📋 `compliance_requirements.csv`

| region | max_asset_number | max_asset_value |
|--------|-------------------|-----------------|
| North  | 5                 | 1000000         |
| South  | 3                 | 500000          |

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

## 🎁 You're Becoming a True Master!

Balancing multiple tax systems while staying compliant across regions—you're really showing your elf expertise now! Keep up the fantastic work, and remember: a well-diversified, compliant portfolio is a happy portfolio! 

🎄🏆 **Regional harmony through smart investing—you've got this!** 🏆🎄