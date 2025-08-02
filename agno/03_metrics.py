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
            if message.content:
                print(f"Message: {message.content}")
            elif message.tool_calls:
                print(f"Tool Calls: {message.tool_calls}")
            print("---" * 5, "Metrics", "---" * 5)
            pprint(message.metrics)
            print("---" * 20)

print("---" * 5, "Collected Metrics", "---" * 5)
pprint(agent.run_response.metrics)
# Print the aggregated metrics for the whole session
print("---" * 5, "Session Metrics", "---" * 5)
pprint(agent.session_metrics)


# You’d see the outputs with following information:
# ​
# Tool Execution Metrics
# This section provides metrics for each tool execution. It includes details about the resource usage and performance of individual tool calls.
# Tool Calls: [{'id': 'db09d128-a697-4007-8b0a-86d5c0bf01c3', 'type': 'function', 'function': {'name': 'get_current_stock_price', 'arguments': '{"symbol": "NVDA"}'}}]
# --------------- Metrics ---------------
# MessageMetrics(
# │   input_tokens=61,
# │   output_tokens=10,
# │   total_tokens=71,
# │   audio_tokens=0,
# │   input_audio_tokens=0,
# │   output_audio_tokens=0,
# │   cached_tokens=0,
# │   cache_write_tokens=0,
# │   reasoning_tokens=0,
# │   prompt_tokens=0,
# │   completion_tokens=0,
# │   prompt_tokens_details=None,
# │   completion_tokens_details=None,
# │   additional_metrics=None,
# │   time=2.8088704769998003,
# │   time_to_first_token=None,
# │   timer=<agno.utils.timer.Timer object at 0x724e45111c90>
# )

# Message Metrics
# Here, you can see the metrics for each message response from the agent. All “assistant” responses will have metrics like this, helping you understand the performance and resource usage at the message level.
# Message: The stock price of NVIDIA is $173.72.

# --------------- Metrics ---------------
# MessageMetrics(
# │   input_tokens=87,
# │   output_tokens=15,
# │   total_tokens=102,
# │   audio_tokens=0,
# │   input_audio_tokens=0,
# │   output_audio_tokens=0,
# │   cached_tokens=0,
# │   cache_write_tokens=0,
# │   reasoning_tokens=0,
# │   prompt_tokens=0,
# │   completion_tokens=0,
# │   prompt_tokens_details=None,
# │   completion_tokens_details=None,
# │   additional_metrics=None,
# │   time=1.3146591199997602,
# │   time_to_first_token=None,
# │   timer=<agno.utils.timer.Timer object at 0x724e44672b60>
# )


# Aggregated Run Metrics
# The aggregated metrics provide a comprehensive view of the entire run. This includes a summary of all messages and tool calls, giving you an overall picture of the agent’s performance and resource usage.
# -------------- Collected Metrics ---------------
# {
# │   'input_tokens': [61, 87],
# │   'output_tokens': [10, 15],
# │   'total_tokens': [71, 102],
# │   'audio_tokens': [0, 0],
# │   'input_audio_tokens': [0, 0],
# │   'output_audio_tokens': [0, 0],
# │   'cached_tokens': [0, 0],
# │   'cache_write_tokens': [0, 0],
# │   'reasoning_tokens': [0, 0],
# │   'prompt_tokens': [0, 0],
# │   'completion_tokens': [0, 0],
# │   'time': [2.8088704769998003, 1.3146591199997602]
# }
# --------------- Session Metrics ---------------