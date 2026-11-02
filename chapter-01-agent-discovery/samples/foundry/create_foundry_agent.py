"""Create a Microsoft Foundry prompt agent for the Agent 365 PoC.

Based on "Quickstart: Create a prompt agent" (Microsoft Learn):
https://learn.microsoft.com/azure/foundry/agents/quickstarts/prompt-agent

Install and sign in:
    pip install "azure-ai-projects>=2.3.0" azure-identity
    az login

Before you run the script, replace the placeholder values below.
"""

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

# Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
FOUNDRY_PROJECT_ENDPOINT = "your_project_endpoint"
FOUNDRY_AGENT_NAME = "poc-foundry-trail-guide"

# Create project client to call Foundry API
project = AIProjectClient(
    endpoint=FOUNDRY_PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

# Create an agent with a model and instructions
agent = project.agents.create_version(
    agent_name=FOUNDRY_AGENT_NAME,
    definition=PromptAgentDefinition(
        model="gpt-5-mini",  # supports all Foundry direct models
        instructions="You are a helpful trail guide that answers questions about hiking trails.",
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
