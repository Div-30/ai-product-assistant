import os
import anthropic
from dotenv import load_dotenv
from tools import search_products, check_price

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
TOOLS = [
    {
        "name": "search_product",
        "description": "Search the product catalogue by name or description.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search term to look up in the catalogue"
                }
            }
        },
        "required": ["query"]
    },
    {
        "name": "check_price",
        "description": "Get the price of a product using its product ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "The product ID"
                }
            },
            "required": ["product_id"]
        }
    }
]
