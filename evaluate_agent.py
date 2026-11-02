import os
import json
import anthropic
from deepeval import evaluate
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from dotenv import load_dotenv


from agent import run_agent

load_dotenv()

class ClaudeEvaluator(DeepEvalBaseLLM):
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    def load_model(self):
        return self.client
    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)
    def get_model_name(self):
        return "Claude Haiku"

TEST_CASES = [
    {
        "input": "What is the price of P002?",
        "retrieval_context": [
            "The price of Wireless Mouse (ID: P002) is 15,000 RWF."
        ]
    },
    {
        "input": "Find the laptop",
        "retrieval_context": [
            json.dumps({
                "id": "P001",
                "name": "Laptop",
                "description": "8GB RAM, 256GB SSD",
                "price": 750000
            })
        ]
    },
    {
        "input": "What is the price of P999?",
        "retrieval_context": [
            "Product with ID 'P999' not found."
        ]
    }
]

def main():
    model = ClaudeEvaluator()
    test_cases = []
    print("=" * 50)
    print("Running agent on each test case...")
    print("=" * 50)

    for case in TEST_CASES:
        print(f"\nInput: {case['input']}")
        actual_output = run_agent(case["input"])
        print(f"Output: {actual_output}")

        test_case = LLMTestCase(
            input=case["input"],
            actual_output=actual_output,
            retrieval_context=case["retrieval_context"]
        )
        test_cases.append(test_case)
    metrics = [
        AnswerRelevancyMetric(threshold=0.7, model=model),
        FaithfulnessMetric(threshold=0.7, model=model)
    ]
    print("\n" + "=" * 50)
    print("Running DeepEval metrics...")
    print("=" * 50 + "\n")
    evaluate(test_cases, metrics)

    print("\n" + "=" * 50)
    print("EVALUATION RESULTS SUMMARY")
    print("=" * 50)
    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i + 1}: {test_case.input}")
        for metric in metrics:
            metric.measure(test_case)
            status = "PASS" if metric.is_successful() else "FAIL"
            print(f"  {metric.__class__.__name__}:")
            print(f"    Score  : {metric.score:.2f}")
            print(f"    Result : {status}")
            print(f"    Reason : {metric.reason}")

if __name__ == "__main__":
    main()