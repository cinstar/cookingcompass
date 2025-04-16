# recommend.py

import numpy as np
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
from app.services.llm_substituter import suggest_diet_substitutes  # Optional
import os

# Load model + FAISS index once
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("models/recipe_index.faiss")

# Load recipe data (must match index order!)
RECIPES_CSV_PATH = "data/recipes.csv"
recipes_df = pd.read_csv(RECIPES_CSV_PATH)


def get_recipe_embedding(text: str) -> np.ndarray:
    embedding = model.encode([text])
    return np.array(embedding).astype("float32")


def get_similar_recipe_indices(query_embedding: np.ndarray, k: int = 5) -> list[int]:
    distances, indices = index.search(query_embedding.reshape(1, -1), k)
    return indices[0].tolist()


def hybrid_recommendation(query: str, diet: str = None, use_llm: bool = False) -> list[dict]:
    """
    query: a string like "chickpea curry with garlic"
    diet: "vegan", "vegetarian", etc. (optional)
    use_llm: whether to rewrite ingredients with LLM (optional)
    """
    embedding = get_recipe_embedding(query)
    similar_idxs = get_similar_recipe_indices(embedding)

    results = []
    for idx in similar_idxs:
        row = recipes_df.iloc[idx]
        
        if diet and row["diet_label"].lower() != diet.lower():
            continue

        recipe = {
            "id": row["id"],
            "title": row["title"],
            "ingredients": row["ingredients"].split(", "),
            "diet_label": row["diet_label"],
            "url": row.get("url", "")
        }

        if use_llm and diet:
            recipe["ingredients_substituted"] = suggest_diet_substitutes(recipe["ingredients"], diet)

        results.append(recipe)

    return results
