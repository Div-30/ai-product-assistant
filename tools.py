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

def check_price(product_id: str) -> str:
    product_id_upper = product_id.strip().upper()
    for product in PRODUCTS:
        if product_id["id"] == product_id_upper:
            return (
                f"The price of {product['name']}"
                f"(ID: {product['id']}) is"
                f"{product['price']:,} RWF."
            )
    return f"Product with ID '{product_id}' not found."