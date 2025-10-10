import sys
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from pymongo import MongoClient

# ----------------------------
# 1. Connect to MongoDB Atlas
# ----------------------------
client = MongoClient("mongodb+srv://kanitimaanas_db_user:fEgO1ZOnUtRyBUKR@cluster0.wa6xl5p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")   # <-- replace with process.env.MONGO_URI
db = client["test"]              # e.g., "animeDB"
collection = db["animes"]                # same collection as your Node app

# ----------------------------
# 2. Load data into pandas
# ----------------------------
data = pd.DataFrame(list(collection.find({}, {
    "_id": 0,
    "title": 1,
    "genres": 1,
    "description": 1
})))

# Combine genres + description for better recommendations
data["content"] = data["genres"].apply(lambda g: " ".join(g) if isinstance(g, list) else "") + " " + data["description"].fillna("")

# ----------------------------
# 3. Build TF-IDF matrix
# ----------------------------
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(data["content"])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# ----------------------------
# 4. Recommendation function
# ----------------------------
indices = pd.Series(data.index, index=data["title"]).drop_duplicates()

def recommend(title, num_recs=5):
    if title not in indices:
        return []
    idx = indices[title]
    # Compute similarity only for the selected anime
    sim_scores = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    # Get indices of top matches (excluding itself)
    top_indices = sim_scores.argsort()[::-1][1:num_recs+1]
    return [
        {
            "_id": str(data.iloc[i].get("_id", "")),
            "title": data.iloc[i]["title"]
        }
        for i in top_indices
    ]

# ----------------------------
# 5. CLI entrypoint (for Node)
# ----------------------------
if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else ""
    results = recommend("Naruto")
    print(json.dumps(results))
