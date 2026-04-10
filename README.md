# api-ethics-assignment
import requests
import time
import json
import os
from datetime import datetime

# Step 1: Create data folder if not exists
if not os.path.exists("data"):
    os.makedirs("data")

# Step 2: API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

# Step 3: Fetch top story IDs (first 50)
top_ids = requests.get(TOP_STORIES_URL, headers=headers).json()[:50]

# Step 4: Category keywords
categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

# Step 5: Function to assign category
def assign_category(title):
    title_lower = title.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return "others"

# Step 6: Store data category-wise (max 25 each)
collected_data = []
category_count = {cat: 0 for cat in categories}

# Step 7: Fetch each story
for story_id in top_ids:
    url = ITEM_URL.format(story_id)
    response = requests.get(url, headers=headers)
    story = response.json()

    if not story or "title" not in story:
        continue

    category = assign_category(story["title"])

    # Limit 25 per category
    if category in category_count and category_count[category] >= 25:
        continue

    data = {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    collected_data.append(data)

    if category in category_count:
        category_count[category] += 1

    # Stop when total reaches 125 (25 × 5 categories)
    if sum(category_count.values()) >= 125:
        break

    time.sleep(2)  # wait 2 seconds between request

# Step 8: Save to JSON file
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w") as f:
    json.dump(collected_data, f, indent=4)

# Step 9: Output
print(f"Collected {len(collected_data)} stories.")
print(f"Saved to {filename}")








import json
import pandas as pd
import os

# Step 1: File path (use your generated JSON file)
file_path = "data/trends_20260410.json"  # change date if needed

# Step 2: Load JSON data
with open(file_path, "r") as f:
    data = json.load(f)

# Step 3: Convert to DataFrame
df = pd.DataFrame(data)

# Step 4: Basic Cleaning

# Remove duplicates (based on post_id)
df.drop_duplicates(subset="post_id", inplace=True)

# Remove rows with missing important values
df.dropna(subset=["title", "author"], inplace=True)

# Fill missing numeric values
df["score"] = df["score"].fillna(0)
df["num_comments"] = df["num_comments"].fillna(0)

# Convert collected_at to datetime
df["collected_at"] = pd.to_datetime(df["collected_at"])

# Step 5: Optional Filtering (high-quality data)
df = df[df["score"] > 10]  # keep only useful stories

# Step 6: Sort data (important for analysis)
df = df.sort_values(by="score", ascending=False)

# Step 7: Save cleaned CSV
output_file = "data/cleaned_trends.csv"
df.to_csv(output_file, index=False)

# Step 8: Output
print("Cleaned data saved successfully!")
print(f"Total rows after cleaning: {len(df)}")
print(f"Saved file: {output_file}")






import pandas as pd
import numpy as np

# Step 1: Load cleaned CSV
file_path = "data/cleaned_trends.csv"
df = pd.read_csv(file_path)

# Step 2: Basic Info
print("Total Stories:", len(df))
print("\nColumns:\n", df.columns)

# Step 3: Category-wise Count
category_count = df["category"].value_counts()
print("\nStories per Category:\n", category_count)

# Step 4: Average Score per Category
avg_score = df.groupby("category")["score"].mean()
print("\nAverage Score per Category:\n", avg_score)

# Step 5: Top 5 Stories (Highest Score)
top_stories = df.sort_values(by="score", ascending=False).head(5)
print("\nTop 5 Stories:\n", top_stories[["title", "score", "category"]])

# Step 6: NumPy Analysis

# Convert columns to NumPy arrays
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

print("\nNumPy Analysis:")

# Mean, Median, Max
print("Mean Score:", np.mean(scores))
print("Median Score:", np.median(scores))
print("Max Score:", np.max(scores))

print("Mean Comments:", np.mean(comments))
print("Max Comments:", np.max(comments))

# Step 7: Correlation (Score vs Comments)
correlation = np.corrcoef(scores, comments)[0, 1]
print("\nCorrelation (Score vs Comments):", correlation)

# Step 8: Save Analysis Summary (optional bonus)
summary = {
    "total_stories": len(df),
    "category_count": category_count.to_dict(),
    "avg_score": avg_score.to_dict(),
    "mean_score": float(np.mean(scores)),
    "max_score": int(np.max(scores)),
    "correlation_score_comments": float(correlation)
}

import json
with open("data/analysis_summary.json", "w") as f:
    json.dump(summary, f, indent=4)

print("\nAnalysis summary saved to data/analysis_summary.json")




import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load data
file_path = "data/cleaned_trends.csv"
df = pd.read_csv(file_path)

# Step 2: Category-wise Count (Bar Chart)
category_count = df["category"].value_counts()

plt.figure()
category_count.plot(kind="bar")
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Step 3: Average Score per Category (Bar Chart)
avg_score = df.groupby("category")["score"].mean()

plt.figure()
avg_score.plot(kind="bar")
plt.title("Average Score per Category")
plt.xlabel("Category")
plt.ylabel("Average Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Step 4: Score Distribution (Histogram)
plt.figure()
plt.hist(df["score"], bins=10)
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Step 5: Score vs Comments (Scatter Plot)
plt.figure()
plt.scatter(df["score"], df["num_comments"])
plt.title("Score vs Number of Comments")
plt.xlabel("Score")
plt.ylabel("Comments")
plt.tight_layout()
plt.show()

print("Visualization Completed Successfully!")