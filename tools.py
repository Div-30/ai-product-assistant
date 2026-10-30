import json 
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "products.json")

with open(DATA_PATH, "r") as f:
    PRODUCTS = json.load(f)

def search_products(query: str) -> str:
    query_lower = query.lower()
    results = [
        p for p in PRODUCTS
        if query_lower in p["name"].lower()
        or query_lower in p["description"].lower()
    ]
    if not results:
        return f"No products found matching '{query}'."
    return json.dumps(results, indent=2)
