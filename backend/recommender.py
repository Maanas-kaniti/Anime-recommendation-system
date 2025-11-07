import sys
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import traceback

# ----------------------------
# Utility: Always print JSON errors
# ----------------------------
def error_response(msg):
    """Prints an error message in JSON so Node.js can parse it."""
    print(json.dumps({"error": msg}))
    sys.exit(1)

# ----------------------------
# 1. Connect to MongoDB Atlas
# ----------------------------
try:
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")

    if not MONGO_URI:
        error_response("MONGO_URI not found in environment variables. Please set it in your .env file.")

    client = MongoClient(MONGO_URI)
    db = client["test"]             # your database name
    collection = db["animes"]       # your collection name

    # Fetch data
    data = pd.DataFrame(list(collection.find({})))

    if data.empty:
        error_response("No data found in MongoDB. Please check your collection.")
    print("Connected to MongoDB successfully!")
    print("Columns found:", list(data.columns))

except Exception as e:
    error_response(f" Database connection failed: {str(e)}")

# ----------------------------
# 2. Clean and verify data
# ----------------------------
try:
    # Detect correct column names dynamically
    title_col = "title" if "title" in data.columns else None
    genre_col = "genres" if "genres" in data.columns else "genre"
    desc_col = "description" if "description" in data.columns else "desc"

    if not title_col:
        error_response(f"Missing 'title' column. Found: {list(data.columns)}")

    # Fill missing values safely
    data[genre_col] = data.get(genre_col, [[]])
    data[desc_col] = data.get(desc_col, "").fillna("")

except Exception as e:
    error_response(f"Data cleaning failed: {str(e)}")

# ----------------------------
# 3. Build TF-IDF similarity
# ----------------------------
try:
    tfidf = TfidfVectorizer(stop_words="english")
    desc_matrix = tfidf.fit_transform(data[desc_col])
    desc_similarity = cosine_similarity(desc_matrix)
    print("TF-IDF matrix created successfully!")

except Exception as e:
    traceback.print_exc()
    error_response(f"TF-IDF creation failed: {str(e)}")

# ----------------------------
# 4. Recommendation Function
# ----------------------------
def recommend_anime_by_description(title, df, desc_similarity, top_n=5):
    try:
        idx = df[df["title"].str.lower() == title.lower()].index
        if len(idx) == 0:
            return {"error": f"Anime '{title}' not found in database."}

        idx = idx[0]
        sim_scores = list(enumerate(desc_similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        recommended = [
            {
                "_id": str(df.iloc[i[0]]["_id"]),
                "title": df.iloc[i[0]]["title"],
                "similarity_score": float(i[1])
            }
            for i in sim_scores[1:top_n + 1]
        ]
        return recommended
    except Exception as e:
        return {"error": f"Recommendation failed: {str(e)}"}

# ----------------------------
# 5. CLI entrypoint (for Node)
# ----------------------------
if __name__ == "__main__":
    try:
        title = sys.argv[1] if len(sys.argv) > 1 else ""
        if not title:
            error_response(" Please provide an anime title as an argument.")

        results = recommend_anime_by_description(title, data, desc_similarity)
        print(json.dumps(results, ensure_ascii=False))

    except Exception as e:
        traceback.print_exc()
        error_response(f" Unexpected error: {str(e)}")
