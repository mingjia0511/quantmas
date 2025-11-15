"""Quick data analysis script."""
import pandas as pd

# Load data
assets = pd.read_csv("../problems/year_1/data/assets.csv")
valuations = pd.read_csv("../problems/year_1/data/valuations.csv")

print("=== ASSETS ===")
print(f"Total assets: {len(assets)}")
print(f"\nAssets by availability:")
print(assets.groupby("available_on_day")["id"].count().sort_index())

print("\n=== VALUATION ANALYSIS ===")
results = []

for asset_id in assets["id"]:
    asset_vals = valuations[valuations["asset_id"] == asset_id]
    
    # Get day 1 and day 100 prices
    day1_price = asset_vals[asset_vals["day"] == 1]["valuation"].values
    day100_price = asset_vals[asset_vals["day"] == 100]["valuation"].values
    
    if len(day1_price) > 0 and len(day100_price) > 0:
        day1 = float(day1_price[0])
        day100 = float(day100_price[0])
        return_pct = ((day100 - day1) / day1) * 100
        profit = day100 - day1
        
        # Get availability
        avail_day = int(assets[assets["id"] == asset_id]["available_on_day"].values[0])
        
        results.append({
            "asset_id": asset_id,
            "available_day": avail_day,
            "day1_price": day1,
            "day100_price": day100,
            "profit": profit,
            "return_pct": return_pct
        })

# Sort by return percentage
results_df = pd.DataFrame(results)
results_df = results_df.sort_values("return_pct", ascending=False)

print("\n=== TOP PERFORMERS (by return %) ===")
print(results_df.to_string(index=False))

print("\n=== STRATEGY INSIGHTS ===")
print(f"Best performer: {results_df.iloc[0]['asset_id']} with {results_df.iloc[0]['return_pct']:.2f}% return")
print(f"Worst performer: {results_df.iloc[-1]['asset_id']} with {results_df.iloc[-1]['return_pct']:.2f}% return")

# Check if we can afford top assets
print(f"\nWith 1,000,000 FSB starting capital:")
affordable = results_df[results_df["day1_price"] <= 1000000]
print(f"Can afford {len(affordable)} assets on day 1")

# Simple strategy: buy best affordable asset
best_affordable = affordable.iloc[0]
print(f"\nSimple strategy: Buy {best_affordable['asset_id']} on day {best_affordable['available_day']}")
print(f"  Cost: {best_affordable['day1_price']:,.0f} FSB")
print(f"  Day 100 value: {best_affordable['day100_price']:,.0f} FSB")
print(f"  Profit: {best_affordable['profit']:,.0f} FSB")
print(f"  Final wealth: {best_affordable['day100_price']:,.0f} FSB")
