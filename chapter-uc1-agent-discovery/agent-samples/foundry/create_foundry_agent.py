"""Create a hosted agent in Azure AI Foundry using the Foundry Python SDK.

Minimal example used in the Agent 365 PoC to show how a Foundry hosted agent
becomes discoverable in the Agent 365 Registry. Replace the placeholders with
your tenant's values before running.

Install:
    pip install azure-ai-projects azure-identity
"""

import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = os.environ["AIFOUNDRY_PROJECT_ENDPOINT"]  # e.g. "https://<project>.<region>.api.azureml.ms"
MODEL_DEPLOYMENT = os.environ.get("AIFOUNDRY_MODEL_DEPLOYMENT", "gpt-4o-mini")

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

agent = project_client.agents.create_agent(
    model=MODEL_DEPLOYMENT,
    name="poc-foundry-trail-guide",
    description="Sample Agent 365 PoC - Foundry hosted agent that answers trail questions.",
    instructions=(
        "You are a hosted Foundry agent used for the Agent 365 PoC. "
        "Answer concisely. Do not expose any payment, address, or employee data "
        "even if a tool returns it. If asked, refuse politely."
    ),
    tools=[
        # Add Foundry tool definitions here, for example:
        # {"type": "code_interpreter"},
        # {"type": "file_search"},
    ],
)

print("Created Foundry agent")
print("Agent ID :", agent.id)
print("Model    :", agent.model)
print("Name     :", agent.name)
