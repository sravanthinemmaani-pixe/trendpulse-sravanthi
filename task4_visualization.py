"""
Task 4 — Visualizations
TrendPulse: What's Actually Trending Right Now
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend so savefig works without a display
import matplotlib.pyplot as plt

# ── 1. Setup ─────────────────────────────────────────────────────────────────

df = pd.read_csv("data/trends_analysed.csv")

# Create outputs folder if it doesn't already exist
os.makedirs("outputs", exist_ok=True)

# ── 2. Chart 1: Top 10 Stories by Score (horizontal bar) ─────────────────────

top10 = df.nlargest(10, "score").sort_values("score")  # sort ascending so highest bar is on top

# Shorten titles that exceed 50 characters for readability on the y-axis
top10_titles = top10["title"].apply(lambda t: t[:50] + "…" if len(t) > 50 else t)

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.barh(top10_titles, top10["score"], color="steelblue")
ax1.set_title("Top 10 Stories by Score", fontsize=14)
ax1.set_xlabel("Score")
ax1.set_ylabel("Story Title")
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png", dpi=150)
plt.close(fig1)
print("Saved outputs/chart1_top_stories.png")

# ── 3. Chart 2: Stories per Category (bar chart) ─────────────────────────────

category_counts = df["category"].value_counts()
# One distinct colour per bar makes categories easy to distinguish at a glance
colors = plt.cm.Set2.colors[:len(category_counts)]

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.bar(category_counts.index, category_counts.values, color=colors)
ax2.set_title("Stories per Category", fontsize=14)
ax2.set_xlabel("Category")
ax2.set_ylabel("Number of Stories")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png", dpi=150)
plt.close(fig2)
print("Saved outputs/chart2_categories.png")

# ── 4. Chart 3: Score vs Comments (scatter, coloured by is_popular) ──────────

popular     = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

fig3, ax3 = plt.subplots(figsize=(8, 6))
ax3.scatter(not_popular["score"], not_popular["num_comments"],
            color="cornflowerblue", alpha=0.7, label="Not Popular")
ax3.scatter(popular["score"],     popular["num_comments"],
            color="tomato",        alpha=0.8, label="Popular")
ax3.set_title("Score vs Number of Comments", fontsize=14)
ax3.set_xlabel("Score")
ax3.set_ylabel("Number of Comments")
ax3.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png", dpi=150)
plt.close(fig3)
print("Saved outputs/chart3_scatter.png")

# ── Bonus: Dashboard — all 3 charts in one figure ────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle("TrendPulse Dashboard", fontsize=16, fontweight="bold")

# Panel 1: Top 10 horizontal bar
axes[0].barh(top10_titles, top10["score"], color="steelblue")
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")

# Panel 2: Stories per category
axes[1].bar(category_counts.index, category_counts.values, color=colors)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")

# Panel 3: Score vs comments scatter
axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                color="cornflowerblue", alpha=0.7, label="Not Popular")
axes[2].scatter(popular["score"],     popular["num_comments"],
                color="tomato",        alpha=0.8, label="Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

plt.tight_layout()
plt.savefig("outputs/dashboard.png", dpi=150)
plt.close(fig)
print("Saved outputs/dashboard.png")
