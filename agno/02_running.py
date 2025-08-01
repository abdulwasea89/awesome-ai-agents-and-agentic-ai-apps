# Running Your Agent 
# The Agent.run() func(x) runs the agent and generate the response, either as a RunResponse object or a stream of RunResponse
# You see in the exmaple of Agno agent there agent.print_response() which is a helper utility to print res in the shell/terminal. it uses agent.run() under the hood

import os
from agno.agent import Agent, RunResponse
from agno.models.google import Gemini
from agno.utils.pprint import pprint_run_response
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

agent = Agent(
    model=Gemini(api_key=GEMINI_API_KEY,id="gemini-2.0-flash"),
)

response: RunResponse = agent.run("Top AI agent fromwrok and very latest")

pprint_run_response(response, markdown=True,)



# Streaming Response

import os
from typing import Iterator
from agno.agent import Agent, RunResponse
from agno.models.google import Gemini
from agno.utils.pprint import pprint_run_response