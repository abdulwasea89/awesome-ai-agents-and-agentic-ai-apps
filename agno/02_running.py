# Running Your Agent 
# The Agent.run() func(x) runs the agent and generate the response, either as a RunResponse object or a stream of RunResponse
# You see in the exmaple of Agno agent there agent.print_response() which is a helper utility to print res in the shell/terminal. it uses agent.run() under the hood

import os
from agno.agent import Agent, RunResponse, RunResponseEvent
from agno.models.google import Gemini
from agno.utils.pprint import pprint_run_response
from dotenv import load_dotenv
from agno.tools.yfinance import YFinanceTools

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

agent = Agent(
    model=Gemini(api_key=GEMINI_API_KEY,id="gemini-2.0-flash"),
    tools=[YFinanceTools(stock_price=True)]
)

response: RunResponse = agent.run("Top AI agent fromwrok and very latest")

pprint_run_response(response, markdown=True,)



# Streaming Response

import os
from typing import Iterator
from agno.agent import Agent, RunResponse
from agno.models.google import Gemini
from agno.utils.pprint import pprint_run_response

response_stream: Iterator[RunResponse] = agent.run(
    "Tell me a story on a donald duck",
    stream = True
)

pprint_run_response(response_stream, markdown=True)


# Streaming Responseses with detailed. You will use  stream_intermediate_steps=True in the agent run

response_with_detailed : Iterator[RunResponseEvent] = agent.run(
    "Tell me a 5 second short story about a lion",
    stream=True,
    stream_intermediate_steps=True
)

# Handling Events in the App

# Run with streaming and intermediate steps
response_stream: Iterator[RunResponseEvent] = agent.run(
    "What is the stock price of NVDA", 
    stream=True, 
    stream_intermediate_steps=True
)

# Process events as they arrive
for event in response_stream:
    if event.event == "RunResponseContent":
        print(f"Content: {event.content}")
    elif event.event == "ToolCallStarted":
        print(f"Tool call started: {event.tool}")
    elif event.event == "ReasoningStep":
        print(f"Reasoning step: {event.content}")
    elif event.event == "ToolCallCompleted":
        print(f"Tool call completed: {event.tool}")
    elif event.event == "RunStarted":
        print("Run started")
    elif event.event == "RunCompleted":
        print("Run completed")
    print("---" * 20)

    