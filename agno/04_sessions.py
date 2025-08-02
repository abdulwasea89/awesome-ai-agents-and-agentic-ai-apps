# Sessions
# When we call Agent.run(), it creates a stateless, singular Agent run.
# But what if we want to continue this run i.e. have a multi-turn conversation? That’s where sessions come in. A session is collection of consecutive runs.
# In practice, a session is a multi-turn conversation between a user and an Agent. Using a session_id, we can connect the conversation history and state across multiple runs.
# Let’s outline some key concepts:
# User: A user represents an individual that interacts with the Agent. Each user has associated memories, sessions, and conversation history separate from other users.
# Session: A session is collection of consecutive runs like a multi-turn conversation between a user and an Agent. Sessions are identified by a session_id and each turn is a run.
# Run: Every interaction (i.e. chat or turn) with an Agent is called a run. Runs are identified by a run_id and Agent.run() creates a new run_id when called.
# Messages: are the individual messages sent between the model and the Agent. Messages are the communication protocol between the Agent and model.


# Multi-user, multi-session Agents
# Each user that is interacting with an Agent gets a unique set of sessions and you can have multiple users interacting with the same Agent at the same time.
# Set a user_id to connect a user to their sessions with the Agent.
# In the example below, we set a session_id to demo how to have multi-turn conversations with multiple users at the same time. In production, the session_id is auto generated.


import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.memory.v2 import memory as Memory
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

agent = Agent(
    model = Gemini(api_key=GEMINI_API_KEY, id="gemini-2.0-flash"),
    memory = Memory(),
    add_history_to_messages=True,
    num_history_runs=3
)

user_1_id = "user_1"
user_2_id = "user_2"

user_1_session_id = "session_101"
user_2_session_id = "session_202"

agent.print_response(
    "Now tell me a joke",
    user_id=user_1_id,
    session_id=user_1_session_id,
)

agent.print_response(
    "Tell me about quantum physics",
    user_id=user_2_id,
    session_id=user_2_session_id,
)

agent.print_response(
    "What is the speed of light",
    user_id=user_2_id,
    session_id=user_2_session_id,
)

agent.print_response(
    "Give me a summary of our conversation.",
    user_id=user_1_id,
    session_id=user_1_session_id,
)

agent.print_response(
    "Give me a summary of our conversation.",
    user_id=user_2_id,
    session_id=user_2_session_id,
)
