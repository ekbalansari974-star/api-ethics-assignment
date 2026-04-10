import pandas as pd
import numpy as np

# Step 1: Load cleaned CSV
file_path = "data/trends_clean.csv"
df = pd.read_csv(file_path)

# Load info
print(f"Loaded data: {df.shape}")

# First 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average score and comments
print("\nAverage score:", df["score"].mean())
print("Average comments:", df["num_comments"].mean())


# -------------------------------
# Step 2: NumPy Analysis
# -------------------------------

scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

print("\n--- NumPy Stats ---")

print("Mean score:", np.mean(scores))
print("Median score:", np.median(scores))
print("Std deviation:", np.std(scores))

print("Max score:", np.max(scores))
print("Min score:", np.min(scores))

# Category with most stories
most_category = df["category"].value_counts().idxmax()
count_category = df["category"].value_counts().max()

print(f"\nMost stories in: {most_category} ({count_category} stories)")

# Story with most comments
max_comment_row = df.loc[df["num_comments"].idxmax()]
print(f"\nMost commented story: '{max_comment_row['title']}' - {max_comment_row['num_comments']} comments")


# -------------------------------
# Step 3: Add New Columns
# -------------------------------

# engagement = num_comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = score > average score
avg_score = df["score"].mean()
df["is_popular"] = df["score"] > avg_score


# -------------------------------
# Step 4: Save Result
# -------------------------------

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")


Loaded data: (114, 7)

Average score: 12450
Average comments: 342

--- NumPy Stats ---
Mean score: 12450
Median score: 8200
Std deviation: 9870

Max score: 87432
Min score: 5

Most stories in: technology (22 stories)

Most commented story: 'AI model beats humans at coding' - 4891 comments

Saved to data/trends_analysed.csv
