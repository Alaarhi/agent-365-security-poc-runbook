# Microsoft Foundry sample agent (prompt agent)

A minimal example that creates a Microsoft Foundry prompt agent. After you publish it, it appears in the Agent 365 agent registry.

## Files

- `create_foundry_agent.py`: creates the prompt agent `poc-foundry-trail-guide`. The code follows [Quickstart: Create a prompt agent](https://learn.microsoft.com/azure/foundry/agents/quickstarts/prompt-agent) and uses the Foundry projects (new) API.

## Prerequisites

- A model deployed in Microsoft Foundry.
- The **Foundry Project Manager** role on the Foundry resource scope to publish the agent.

## Run

1. Install the packages and sign in:

```powershell
pip install "azure-ai-projects>=2.3.0" azure-identity
az login
```

2. Copy your project endpoint from the welcome screen in the Foundry portal. In `create_foundry_agent.py`, replace `your_project_endpoint` with it, and replace `gpt-5-mini` with your model deployment if needed.
3. Run `python create_foundry_agent.py`.

## Discovery path in the Agent Registry

| Step | What happens |
|---|---|
| 1. Create | The script creates an agent version. An unpublished agent uses the project's shared agent identity. |
| 2. Publish | Publish the agent as an Agent Application. The published agent receives its own Entra agent identity and Entra agent blueprint. Permissions don't transfer automatically, so reassign the RBAC permissions that the agent's tools need to the new agent identity. |
| 3. Registry sync | Every Foundry agent that you publish appears in the Agent 365 registry automatically. Registry sync is supported for prompt agents and hosted agents. |
| 4. Activity | Activity data collection is supported for prompt agents. For hosted agents, it's supported by using the Agent 365 SDK. Logging is controlled per Foundry resource through the `agent365Config` configuration. |

Verify the result in the Microsoft 365 admin center under **Agents** > **All agents** > **Registry**, and in the Microsoft Entra admin center under **Entra ID** > **Agents** > **Agent identities**.

Microsoft Foundry data residency follows the Azure region of the Foundry resource. Agent 365 data residency follows the storage location of the Microsoft Entra tenant. You can opt out individual Foundry resources from Agent 365 data collection.

## Documentation

- [Microsoft Agent 365 integration with Foundry](https://learn.microsoft.com/azure/foundry/agents/concepts/agent-365-integration)
- [Quickstart: Create a prompt agent](https://learn.microsoft.com/azure/foundry/agents/quickstarts/prompt-agent)
- [Publish your agent as an Agent Application](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-agent)
- [Configure Agent 365 data collection for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/agents/how-to/configure-agent-365-data-collection)
