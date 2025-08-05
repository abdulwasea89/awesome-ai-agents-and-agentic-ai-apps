# agno/agui.py

from agno.agent.agent import Agent
from agno.app.agui import AGUIApp
from agno.models.google import Gemini
import os
from dotenv import load_dotenv

# 1) Load env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2) Define your Agent
chat_agent = Agent(
    name="Assistant",
    model=Gemini(api_key=GEMINI_API_KEY, id="gemini-2.0-flash"),
    instructions="You are a helpful AI assistant.",
    add_datetime_to_instructions=True,
    markdown=True,
)

# 3) Build the AGUIApp
agui_app = AGUIApp(
    agent=chat_agent,
    name="Basic AG-UI Agent",
    app_id="basic_agui_agent",
    description="A basic agent that demonstrates AG-UI protocol integration.",
)

# 4) **Expose** the ASGI app at module level:
app = agui_app.get_app()


if __name__ == "__main__":
    # When running directly via `python agno/agui.py`,
    # serve it programmatically:
    agui_app.serve(app=app, port=8000, reload=False)
