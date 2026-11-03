from tools import check_price, search_products
from unittest.mock import patch
import pytest
from agent import run_agent


def test_search_existing_product():
    result = search_products("Laptop")
    assert "Laptop" in result
    assert "P001" in result
def test_check_p002_price():
    result = check_price("P002")
    assert "Wireless Mouse" in result
    assert "15,000 RWF" in result

def test_unknown_product_price():
    result = check_price("P999")
    assert "not found" in result.lower()
    assert "15,000" not in result
def test_simulated_tool_exception():
    with patch("agent.check_price", side_effect=Exception("Database connection timeout")):
        response = run_agent("What is the price of P002?")
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
