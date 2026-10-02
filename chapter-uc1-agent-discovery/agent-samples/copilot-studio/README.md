# Copilot Studio sample agent

A minimal declarative agent definition for Microsoft 365 Copilot / Copilot Studio Agent Builder.

## Files

- `declarative-agent.json` - the agent manifest using the v1.2 declarative-agent schema.

## Characteristics

- Microsoft-native, auto-discovered.
- Grounded on a SharePoint knowledge source.
- Includes conversation starters and web search capability.
- No credentials or secrets - safe to version-control.

## Discovery path in Agent Registry

| Step | What happens |
|---|---|
| 1. Build in Copilot Studio or Agent Builder | Creator uploads or edits `declarative-agent.json` in the Agent Builder UI, or builds the agent through Copilot Studio. |
| 2. Publish | Publisher releases the agent to the Microsoft 365 Copilot catalog or an org catalog. |
| 3. Approve (if required) | AI Administrator approves in `admin.cloud.microsoft` > **Agents** > **Requested**. |
| 4. Registry entry | The agent appears automatically in the Agent Registry with its display name, owner, publishing state, and Entra Agent ID (if Agent Identity is enabled at the environment level). |
| 5. Agent Map | After the first interactions, the Agent Map renders the agent's connections to tools and knowledge sources. |

Latency: typically within minutes of publishing; up to 24 hours for full registry propagation after enablement.

## Documentation

- [Declarative agent schema](https://learn.microsoft.com/microsoft-365-copilot/extensibility/declarative-agent-manifest)
- [Microsoft 365 Copilot Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/overview-declarative-agent)
- [Microsoft Copilot Studio overview](https://learn.microsoft.com/microsoft-copilot-studio/)
