from langgraph.graph import StateGraph
from stock_tool import fetch_stock_data
import re

# List of known stock tickers (expand as needed)
KNOWN_TICKERS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NVDA", "NFLX"]

def extract_tickers(user_input):
    """Extracts valid stock tickers from user input."""
    words = user_input.upper().split()
    return [word for word in words if word in KNOWN_TICKERS]

def stock_agent(state):
    user_input = state["user_input"].lower()
    print(f"User input received: {user_input}")  

    tickers = extract_tickers(user_input)
    if tickers:
        print(f"Extracted tickers: {tickers}")  
        result = fetch_stock_data(tickers)
        print(f"Stock data fetched: {result}")  
        return {"user_input": user_input, "tool_output": result}

    return {"user_input": user_input, "tool_output": "I couldn't identify a valid stock ticker. Try something like 'Get stock data for AAPL, MSFT'."}

# Create LangGraph workflow
workflow = StateGraph(dict)
workflow.add_node("agent", stock_agent)
workflow.set_entry_point("agent")

# Compile graph
graph = workflow.compile()
