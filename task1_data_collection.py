## Task 1: Fetch Data from HackerNews API 
#Fetches top stories, categorises them by keyword, and saves to a dated JSON file.


import requests
import json
import time
import os
from datetime import datetime

# Category definitions: maps category name → keywords to match (case-insensitive)
CATEGORIES = {
    "technology":    ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews":     ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":        ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science":       ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"],
}

MAX_PER_CATEGORY = 25   # collect up to 25 stories per category
TOP_STORIES_LIMIT = 500 # fetch the first 500 story IDs

#Header
HEADERS = {"User-Agent": "TrendPulse/1.0"}

BASE_URL = "https://hacker-news.firebaseio.com/v0"

#Step 1 — Get the list of top story IDs:

def fetch_top_story_ids():
    """Fetch the list of top story IDs from HackerNews and return the first 500."""
    url = f"{BASE_URL}/topstories.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        ids = response.json()
        # Slice to the first 500 IDs as required
        return ids[:TOP_STORIES_LIMIT]
    except requests.RequestException as e:
        print(f"Failed to fetch top story IDs: {e}")
        return []

#Step 2 — Get each story's details:
def fetch_story(story_id):
    """Fetch details for a single story by ID. Returns the JSON dict or None on failure."""
    url = f"{BASE_URL}/item/{story_id}.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Don't crash — just warn and continue to the next story
        print(f"  Warning: could not fetch story {story_id}: {e}")
        return None


def matches_category(title, keywords):
    """Return True if the title contains any of the given keywords (case-insensitive)."""
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in keywords)


def assign_category(title):
    """Return the first matching category for a title, or None if no match found."""
    for category, keywords in CATEGORIES.items():
        if matches_category(title, keywords):
            return category
    return None


def main():
    # ── Step 1: Fetch all top story IDs ──────────────────────────────────────────
    print(f"Fetching top {TOP_STORIES_LIMIT} story IDs from HackerNews...")
    story_ids = fetch_top_story_ids()
    if not story_ids:
        print("No story IDs retrieved. Exiting.")
        return

    print(f"Retrieved {len(story_ids)} story IDs. Fetching story details...")

    # ── Step 2: Fetch details for all stories upfront ────────────────────────────
    # Collecting them all first avoids redundant network calls when we loop by category
    all_stories = []
    for i, sid in enumerate(story_ids, start=1):
        story = fetch_story(sid)
        if story and story.get("type") == "story" and story.get("title"):
            all_stories.append(story)
        # Brief progress indicator every 100 stories
        if i % 100 == 0:
            print(f"  Fetched {i}/{len(story_ids)} stories so far...")

    print(f"Successfully fetched details for {len(all_stories)} stories.")

    # ── Step 3: Categorise — one category at a time, sleep between each ──────────
    collected_at = datetime.now().isoformat(timespec="seconds")  # single timestamp for all records
    results = []

    for category, keywords in CATEGORIES.items():
        # Sleep between category loops as required (not between individual story fetches)
        time.sleep(2)

        category_stories = []
        for story in all_stories:
            if len(category_stories) >= MAX_PER_CATEGORY:
                break  # stop once we have 25 for this category

            title = story.get("title", "")
            if matches_category(title, keywords):
                # Extract only the 7 required fields
                record = {
                    "post_id":      story.get("id"),
                    "title":        title,
                    "category":     category,
                    "score":        story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author":       story.get("by", ""),
                    "collected_at": collected_at,
                }
                category_stories.append(record)

        print(f"  {category}: {len(category_stories)} stories collected")
        results.extend(category_stories)

    # ── Step 4: Save to data/trends_YYYYMMDD.json ────────────────────────────────
    os.makedirs("data", exist_ok=True)  # create data/ folder if it doesn't exist
    date_suffix = datetime.now().strftime("%Y%m%d")
    output_path = f"data/trends_{date_suffix}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nCollected {len(results)} stories. Saved to {output_path}")


if __name__ == "__main__":
    main()
