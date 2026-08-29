"""
Task 3 — Analysis with Pandas & NumPy
TrendPulse: What's Actually Trending Right Now
"""

import pandas as pd
import numpy as np

# ── 1. Load and Explore ──────────────────────────────────────────────────────

df = pd.read_csv("data/trends_clean.csv")

print(f"Loaded data: {df.shape}")

print("\nFirst 5 rows:")
print(df.head())

# Pandas mean gives a quick overall view before we dive into NumPy stats
avg_score    = df["score"].mean()
avg_comments = df["num_comments"].mean()
print(f"\nAverage score   : {avg_score:,.2f}")
print(f"Average comments: {avg_comments:,.2f}")

# ── 2. Basic Analysis with NumPy ─────────────────────────────────────────────

scores = df["score"].to_numpy()

print("\n--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores):,.2f}")
print(f"Median score : {np.median(scores):,.2f}")
print(f"Std deviation: {np.std(scores):,.2f}")
print(f"Max score    : {np.max(scores):,}")
print(f"Min score    : {np.min(scores):,}")

# Category with the most stories
top_category = df["category"].value_counts().idxmax()
top_count    = df["category"].value_counts().max()
print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Story with the highest comment count
most_commented_idx   = df["num_comments"].idxmax()
most_commented_title = df.loc[most_commented_idx, "title"]
most_commented_count = df.loc[most_commented_idx, "num_comments"]
print(f'\nMost commented story: "{most_commented_title}" — {most_commented_count:,} comments')

# ── 3. Add New Columns ───────────────────────────────────────────────────────

# engagement: how much discussion a story generates per upvote (avoids div-by-zero with +1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular: True if this story's score beats the overall average
df["is_popular"] = df["score"] > avg_score

# ── 4. Save the Result ───────────────────────────────────────────────────────

output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)
print(f"\nSaved to {output_path}")
