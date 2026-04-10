import pandas as pd
import json

# Step 1: Load JSON file
file_path = "data/trends_20260410.json"  # change date if needed

with open(file_path, "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)

print(f"Loaded {len(df)} stories from {file_path}")

# Step 2: Remove duplicates (based on post_id)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Step 3: Remove missing values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Step 4: Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Step 5: Remove low quality (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Step 6: Clean whitespace (title)
df["title"] = df["title"].str.strip()

# Step 7: Save as CSV
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# Step 8: Category summary
print("\nStories per category:")
print(df["category"].value_counts())