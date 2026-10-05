# Agent 365 SDK sample agents

Three minimal agent skeletons showing how a custom-built agent is onboarded with the Agent 365 SDK through [`microsoft/agent365-skills`](https://github.com/microsoft/agent365-skills).

## Files

| File | Language | Framework |
|---|---|---|
| [`nodejs/agent.ts`](nodejs/agent.ts) | Node.js / TypeScript | `@microsoft/agents-hosting` |
| [`python/agent.py`](python/agent.py) | Python | `microsoft-agents-hosting-*` |
| [`dotnet/Agent.cs`](dotnet/Agent.cs) | .NET | `Microsoft.Agents.*` |

Each file is a short illustration of the hosting layer, not a production starter kit. Use the `agent365-skills` entry-point skills to scaffold a real project.

## Discovery path in Agent Registry

| Step | Tool | What happens |
|---|---|---|
| 1. Scaffold the hosting layer | `make-ai-teammate` (or `make-a365-agent` for non-AI-Teammate) | Adds Express + CloudAdapter, ASP.NET Core, or aiohttp hosting, AgentApplication class, message routing, and tooling manifest. |
| 2. Register in Agent 365 | `a365-setup` | Runs `a365 setup all` to create the Blueprint, Entra Agent Identity, and required permissions. |
| 3. Instrument observability (Optional) | `instrument-observability` | Adds OTel-based tracing and A365 exporter so interactions flow into Defender Advanced Hunting (`AgentsInfo`, `CloudAppEvents`) and Purview Audit. |
| 4. Add WorkIQ MCP tools (Optional) | `add-workiq-tools` | Wires MCP servers (mail, calendar, Teams, files) into the agent. |
| 5. Add Purview DLP (Optional) | `purview-dlp-integration` | Adds the Purview DLP guard that calls Graph `processContent` before the LLM. See [UC4 - Sensitive Data Protection](../../../chapter-uc4-sensitive-data-protection/README.md#section-7---purview-dlp-for-sdk-onboarded-agents). |
| 6. Registry entry | - | The agent appears in the Agent 365 Registry with its Blueprint, Entra Agent ID, owner, and lifecycle state. |

Latency: appears in the registry within minutes of `a365 setup all` completing.

## Running the skills

From your agent project directory:

```
gh skill add microsoft/agent365-skills
gh copilot suggest "Make this agent an AI Teammate"
gh copilot suggest "Add observability to this agent"
gh copilot suggest "Add Purview DLP to this agent"
```

## Documentation

- [`microsoft/agent365-skills`](https://github.com/microsoft/agent365-skills) - entry point.
- [Agent 365 developer documentation](https://learn.microsoft.com/microsoft-agent-365/developer/)
- [Agent 365 CLI reference](https://learn.microsoft.com/microsoft-agent-365/developer/cli/)
- [Custom client app registration](https://learn.microsoft.com/microsoft-agent-365/developer/custom-client-app-registration)
