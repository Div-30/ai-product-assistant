from agent import run_agent


requests = [
    "What is the price of P002?",
    "Find the laptop",
    "What is the price of P001?",
    "Do you have any headphones?",
    "What is the price of P999?",
]

for i, request in enumerate(requests, 1):
    print(f"\n--- Request {i} ---")
    print(f"User: {request}")
    response = run_agent(request)
    print(f"Agent: {response}")