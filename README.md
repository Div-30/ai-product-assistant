# AI Product Assistant
    An intelligent product assistant built with **Claude Haiku**, equipped with tool-use capabilities,
    evaluated with **DeepEval**, tested using **pytest**, and monitored via Python's native logging
    framework

## Architecture & Tools

    The agent operates in a conversational loop and has access to two deterministic tools:
    - `search_products(query)`: Searches catalogue by product name and description.
    - `check_price(product_id)`: Fetches validated price in Rwandan Francs (RWF).
    - **Catalogue**: Loaded from local `products.json`.

    ---

## Getting Started

### 1. Clone & Set Up Virtual Environment

    ```bash
    git clone <your-repo-url>
    cd product-assistant
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
### 2. Configure Environment Variables

  Create a .env file in the project root:

    ANTHROPIC_API_KEY=your_anthropic_api_key_here
  ──────
## Running Evaluations & Tests

### 1. Automated Functional Tests (pytest)

  Runs 4 unit tests covering catalogue search, price verification, unknown IDs, and tool failure simulation:
    pytest -v
### 2. DeepEval Quality Evaluation

  Evaluates agent interactions on Answer Relevancy and Faithfulness using a custom Claude LLM judge:

    python evaluate_agent.py

### 3. Monitoring & Latency Run

  Executes 5 live queries to generate latency and tool execution logs in logs/app.log:
    python run_requests.py
### 4. Security / Prompt Injection Test
  Tests agent resistance against instructions to hallucinate prices:
    python security_test.py
  ──────
## Summary of Results

  • DeepEval Faithfulness: 100% (zero hallucination detected)
  • DeepEval Relevancy: 83% average score
  • Unit Tests: 4/4 passing (100%)
  • Security Audit: Successfully prevented prompt injection override

  For detailed metric breakdowns, latency distributions, and root-cause analysis, see REPORT.md.
