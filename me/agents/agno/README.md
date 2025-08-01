# AGNO - AI AGENT FRAMEWORK

## What are agents?

Agents are AI Program that operate autonomously. Traditional Systems or software follow a pre-trained steps to do or accomplish the work

The core of an Agent is the **Model, Tools and instructions, memory, knowledge, reason, goal:**

* Model: Control the flow of execution
* Tools: enable an agent to use the external systems and softwares
* Instructions: are how we program the agent, teach the agent how to behave
* Goal: The goal of the task
* Reasoning: enable the ability to think
* Knowledge: Knowledge is specific domain information to better the response and accurate
* Storage: is used by Agent to store the conversation between the user and agent to make agent stateful, long-term conversations
* Memory: Give agent the ability to store and recall information from previous interactions

## Research agent

Lets Build a research agent using Exa to showcase how to guide the Agent to produce the report in a specific format. In advanced cases, we should use [Structured Outputs](https://docs.agno.com/agents/structured-output) instead.

### Explain the Agent: 


This code creates a research agent using Agno that generates academic-style reports. Here's what it does:

**Core Components:**

* **Agent** : Uses OpenAI's GPT-4o model with ExaTools for web searching
* **ExaTools** : Configured to search for content published today using keyword search
* **Persona** : "Professor X-1000" - an AI research scientist with academic writing expertise

**Key Features:**

* **Structured Output** : Defines expected report format with sections like Executive Summary, Key Findings, etc.
* **Research Process** : Instructions to run 3 distinct searches and cross-reference sources
* **Academic Style** : Clear, authoritative writing with proper citations
* **Markdown Output** : Formatted reports with show_tool_calls enabled

**Configuration Options:**

* `markdown=True`: Enables markdown formatting
* `show_tool_calls=True`: Displays tool usage in responses
* `add_datetime_to_instructions=True`: Adds timestamp context
* `stream=True`: Enables streaming responses
