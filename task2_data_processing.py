"""
Task 2 — Clean the Data & Save as CSV
TrendPulse: What's Actually Trending Right Now
"""

import glob
import pandas as pd

# ── 1. Load the JSON file ────────────────────────────────────────────────────

# Use glob so the script works for any date-stamped filename
json_files = glob.glob("data/trends_*.json")
if not json_files:
    raise FileNotFoundError("No trends JSON file found in data/ folder.")

json_path = json_files[0]  # take the first match
df = pd.read_json(json_path)

print(f"Loaded {len(df)} stories from {json_path}")

# ── 2. Clean the data ────────────────────────────────────────────────────────

# Step 2a: Remove duplicate rows based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"\nAfter removing duplicates: {len(df)}")

# Step 2b: Drop rows where post_id, title, or score is missing
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Step 2c: Ensure score and num_comments are integers (JSON may load them as float)
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# Step 2d: Remove low-quality stories — score below 5 is noise
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Step 2e: Strip leading/trailing whitespace from title
df["title"] = df["title"].str.strip()

# ── 3. Save as CSV ───────────────────────────────────────────────────────────

output_path = "data/trends_clean.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")

# Print a quick summary: how many stories fall in each category
print("\nStories per category:")
category_counts = df["category"].value_counts()
for category, count in category_counts.items():
    print(f"  {category:<20} {count}")
