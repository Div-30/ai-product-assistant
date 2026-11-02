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

SYSTEM_PROMPT = """You are a helpful product assistant for an online shop.
You help customers find products and check prices. Always use the provided tools to look up real product information.
Never invent or guess prices or product details."""

def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    while True:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input

                    if tool_name == "search_product":
                        result = search_products(tool_input["query"])
                    elif tool_name == "check_price":
                        result = check_price(tool_input["product_id"])
                    else: 
                        result = "Unknown tool."
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            messages.append({"role": "user", "content": tool_results})
