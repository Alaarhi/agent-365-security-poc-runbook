# Chapter UC1 - Agent Discovery

**Pillar:** Observe
**What it proves:** you cannot govern what you cannot see. Every agent in the tenant surfaces in one registry, including the ones nobody registered, each with a named, accountable owner.

## Roles - least privilege

| Task | Role | Notes |
|---|---|---|
| Setup / configuration | **AI Administrator** | Required to enable Agent 365, configure Registry sync for connected platforms, approve agents, and change registry settings. Assign Active for the PoC window. |
| Read-only / validation | **AI Reader** (or **Global Reader**) | Sufficient to view the Agent Registry, list agents, see owners, and export the registry. Use this role for reviewers, auditors, and anyone verifying results. |
| Optional (SDK agents) | **Agent ID Developer** | Required for developers onboarding custom-built agents via the Agent 365 SDK. Not required for viewing. |

Grant the read-only role first; only grant the setup role to whoever will make configuration changes.

## Scope - which agent types get discovered

| Category | Example platforms | Onboarding path |
|---|---|---|
| Microsoft-native (auto-discovered) | Microsoft 365 Copilot / Agent Builder declarative agents, Copilot Studio, Microsoft Foundry, SharePoint agents | Automatic once Agent 365 is enabled |
| Connected platforms (Registry sync) | Databricks Genie, Google Vertex AI, Snowflake Cortex, AWS Bedrock, Salesforce Agentforce | Registry sync configured per platform |
| Custom (Agent 365 SDK) | Customer-built agents in Node.js, Python, or .NET | Onboarded via [`microsoft/agent365-skills`](https://github.com/microsoft/agent365-skills) |

## Portal

Microsoft 365 admin center - <https://admin.cloud.microsoft> > **Agents**.

## Documentation

| Topic | Documentation |
|---|---|
| Agent 365 overview | [Overview of Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/overview) |
| Agent Registry | [Agent Registry in Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/administrator/agent-registry) |
| Connected platforms | [Connected platforms for Agent 365](https://learn.microsoft.com/microsoft-agent-365/administrator/connected-platforms) |

## Prerequisites

Complete [Chapter 0 - Prerequisites](../chapter-0-prerequisites/README.md). In addition:

1. Agent 365 is enabled for the tenant.
2. Frontier features are opted in if the customer wants Frontier-only capabilities.
3. At least one Microsoft-native agent exists (Copilot Studio, Foundry, or Microsoft 365 Copilot Agent Builder) so there is content to discover.
4. If connected platforms are in scope (Databricks, Vertex, Snowflake, Bedrock, Agentforce), those tenant-side integrations are ready.

## Setup steps

Performed by the AI Administrator.

1. Open <https://admin.cloud.microsoft> and go to **Agents**.
2. Confirm **Agent Registry** is enabled.
3. For each connected platform in scope, configure Registry sync per that platform's onboarding page.
4. For custom SDK agents, confirm they have been onboarded via `a365 setup all` from the `microsoft/agent365-skills` toolchain so they appear in the registry.
5. Exercise each agent at least once (send a prompt or invoke a tool) so it registers activity and appears with the expected metadata.

**Check result (Setup role)**

- Registry contains every in-scope agent.
- Each agent shows a named business owner.
- Connected platform syncs report healthy.

## Test - registry inventory

Performed by anyone with **AI Reader**.

1. Open <https://admin.cloud.microsoft> > **Agents** > **All agents**.
2. Filter by platform and confirm every in-scope agent is listed.
3. Confirm the owner column is populated for every agent.
4. Export the registry (CSV or JSON) as evidence.

**Expected result**

- All in-scope agents are visible in the registry within the agreed discovery window (default: 24 hours after enablement).
- Every agent has a business owner.
- No unknown or orphaned agents remain.

## Test - Agent Map

Performed by anyone with **AI Reader**.

1. Open the **Agent Map** view in the Agents section.
2. Confirm the map renders agent-to-tool and agent-to-agent interactions.
3. Capture a screenshot as evidence.

**Expected result**

- Agent Map renders known interactions.
- Discovered agents that were not previously known are triaged with their owner.

## Evidence to capture

- Registry export (CSV/JSON) with owner column populated.
- Agent Map screenshot.
- List of any newly discovered / previously unknown agents, with owner assignment status.

## Common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent missing from registry | Agent 365 not enabled for that platform, or agent never invoked | Enable the platform integration; run at least one turn on the agent. |
| Owner column blank | Sponsor / owner not assigned during agent creation | Assign an owner in the agent's platform (Copilot Studio, Foundry, or Entra Enterprise Applications). Covered in [UC2](../chapter-uc2-identity-ownership/README.md). |
| Connected platform not syncing | Registry sync not configured or credentials expired | Reconfigure Registry sync per platform documentation. |
| SDK agent missing | `a365 setup all` not completed for that project | Rerun `a365 setup all` and confirm Blueprint is registered. |

---

Previous: [Chapter 0 - Prerequisites](../chapter-0-prerequisites/README.md) · Next: [UC2 - Identity & Ownership](../chapter-uc2-identity-ownership/README.md)
