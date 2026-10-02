# Foundry sample agent (hosted / prompt agent)

A minimal example of creating a hosted agent in Azure AI Foundry so it becomes discoverable through Agent 365.

## Files

- `create_foundry_agent.py` - Python example that creates a Foundry hosted agent via the Foundry SDK.

## Characteristics

- Microsoft-native, auto-discovered.
- Hosted and executed on Foundry; no custom hosting required.
- Uses Entra ID / managed identity for Foundry access.
- Tool definitions (code interpreter, file search, custom tools) are added inline.

## Discovery path in Agent Registry

| Step | What happens |
|---|---|
| 1. Create the Foundry project | A Foundry project is provisioned in Azure AI Foundry. |
| 2. Create the agent | Developer runs the sample script (or uses the Foundry portal) to create a hosted agent with its instructions, model, and tools. |
| 3. Associate with Agent 365 | The agent is linked to the Agent 365 tenant (automatic for projects in the Agent 365-connected subscription, or via Registry sync for other projects). |
| 4. Registry entry | The Foundry agent appears in the Agent Registry with its name, project, model, and owner. |
| 5. Entra Agent ID | Enabled per Foundry project policy; when on, the agent receives an Entra Agent ID service principal. |
| 6. Observability | Interactions are recorded in Advanced Hunting (`AgentsInfo`, `CloudAppEvents`) if the agent is instrumented per Agent 365 guidance. |

Latency: within minutes of agent creation; up to 24 hours for full registry propagation after enablement.

## Documentation

- [Azure AI Foundry overview](https://learn.microsoft.com/azure/ai-foundry/)
- [Create and manage agents in Foundry](https://learn.microsoft.com/azure/ai-foundry/agents/overview)
- [Enable threat protection for Microsoft Foundry AI workloads](https://learn.microsoft.com/azure/defender-for-cloud/ai-onboarding)
