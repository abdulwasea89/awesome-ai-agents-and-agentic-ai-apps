# Metrics
# Understanding the metrics of the Agent or detailing about hte tokens, runs, permessage or ..., We use metrics

# Metrics are available at multiple levels:
# Per-message: Each message (assistant, tool, etc.) has its own metrics.
# Per-tool call: Each tool execution has its own metrics.
# Aggregated: The RunResponse aggregates metrics across all messages in the run.
# Where Metrics Live
# RunResponse.metrics: Aggregated metrics for the whole run, as a dictionary.
# ToolExecution.metrics: Metrics for each tool call.
# Message.metrics: Metrics for each message (assistant, tool, etc.)

import os
from typing import Iterator
from agno.agent import Agent, RunResponse, RunResponseEvent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from rich.pretty import pprint
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

agent = Agent(
    model = Gemini(api_key=GEMINI_API_KEY, id="gemini-2.0-flash-001"),
    tools=[YFinanceTools(stock_price=True)],
    markdown=True,
    show_tool_calls=True
)

agent.print_response(
    "What is the stock price of NVDIA"
)

if agent.run_response.messages:
    for message in agent.run_response.messages:
        if message.role == "assistant":
            if message
