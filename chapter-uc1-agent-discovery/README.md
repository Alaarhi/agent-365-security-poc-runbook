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

## Optional - programmatic discovery with Microsoft Graph

The UI in the Microsoft 365 admin center is the fastest path for a visual review, but Microsoft Graph exposes the same inventory programmatically. Use this when the customer needs scheduled exports, external reporting, CMDB sync, or automated reconciliation against a source of truth.

### What you can retrieve

| Signal | Where to get it in Graph |
|---|---|
| List of agents in the tenant (Copilot Studio / M365 Copilot declarative, Foundry, SharePoint, SDK) with display name, owner, publishing state | `/copilot/admin/agents` and related Copilot admin endpoints (beta) |
| Agent identity in the directory (Entra Agent ID service principal) | `/servicePrincipals` filtered to the agent subtype |
| Owners and sponsors of an agent | `/servicePrincipals/{id}/owners`, `/applications/{id}/owners` |
| Custom security attributes on an agent identity | `/servicePrincipals/{id}?$select=customSecurityAttributes` |
| Conditional Access policies that target agent identities | `/identity/conditionalAccess/policies` |
| Sign-in activity for an agent (allow/deny, including CA decisions) | `/auditLogs/signIns` filtered by `appId`, service-principal filters |
| Audit of lifecycle actions on an agent (create, update, block, delete) | `/auditLogs/directoryAudits` and Microsoft Purview Audit APIs |
| Copilot interaction records (for UC4/UC6 cross-check) | Microsoft Purview Audit via Microsoft 365 Management Activity API, or Graph audit APIs where available |

### Minimum required Graph permissions (least-privilege)

| Scope | Why |
|---|---|
| `Application.Read.All` (delegated or app) | Read agent applications and service principals. |
| `Directory.Read.All` (delegated) | Read owners, sponsors, and directory metadata. |
| `CustomSecAttributeAssignment.Read.All` (delegated) | Read custom security attribute values on agent identities (requires Attribute Assignment Reader). |
| `Policy.Read.All` (delegated) | Read Conditional Access policies that target agent identities. |
| `AuditLog.Read.All` (delegated or app) | Read directory audit and sign-in logs. |
| `AgentApplication.Read.All` / Copilot admin scopes (preview) | Read Copilot/agent inventory via the Copilot admin endpoints. Scope names and surface are preview; confirm against current docs before relying on them in production. |

Prefer delegated permissions scoped to a read-only account. Only grant application permissions for an unattended service that needs to run outside a user context.

### Example - list agent service principals

```http
GET https://graph.microsoft.com/v1.0/servicePrincipals?$filter=servicePrincipalType eq 'Application'&$select=id,displayName,appId,servicePrincipalType,tags
Authorization: Bearer <token>
```

To focus on agent identities only, filter further by display name convention (for example names ending in `-AgentIdentity`) or by a known custom security attribute set:

```http
GET https://graph.microsoft.com/beta/servicePrincipals?$count=true&$filter=customSecurityAttributes/AgentGovernance/Project eq 'Agent365PoC'&$select=id,displayName,appId,owners
ConsistencyLevel: eventual
Authorization: Bearer <token>
```

### Example - get sign-in activity for one agent

```http
GET https://graph.microsoft.com/v1.0/auditLogs/signIns?$filter=appId eq '<agent-app-id>'&$top=50
Authorization: Bearer <token>
```

Returns the service-principal sign-ins for the agent, including Conditional Access decisions. Used in [UC3](../chapter-uc3-least-privilege/README.md) and [UC6](../chapter-uc6-lifecycle-audit/README.md).

### Example - read custom security attributes on an agent

```http
GET https://graph.microsoft.com/v1.0/servicePrincipals/{id}?$select=id,displayName,customSecurityAttributes
Authorization: Bearer <token>
```

### Documentation

| Topic | Documentation |
|---|---|
| Microsoft Graph overview | [Microsoft Graph REST API overview](https://learn.microsoft.com/graph/overview) |
| Service principals in Graph | [servicePrincipal resource type](https://learn.microsoft.com/graph/api/resources/serviceprincipal) |
| List service principals | [List servicePrincipals](https://learn.microsoft.com/graph/api/serviceprincipal-list) |
| Custom security attributes via Graph | [Manage custom security attributes using Microsoft Graph](https://learn.microsoft.com/graph/api/resources/custom-security-attributes-overview) |
| Audit logs | [auditLogRoot: directoryAudits](https://learn.microsoft.com/graph/api/directoryaudit-list) |
| Sign-in logs | [auditLogRoot: signIns](https://learn.microsoft.com/graph/api/signin-list) |
| Conditional Access policies | [conditionalAccessPolicy resource type](https://learn.microsoft.com/graph/api/resources/conditionalaccesspolicy) |
| Microsoft 365 Copilot admin APIs | [Microsoft 365 Copilot developer documentation](https://learn.microsoft.com/microsoft-365-copilot/extensibility/) and [Copilot API reference (preview)](https://learn.microsoft.com/graph/api/resources/copilot-admin-overview) |
| Entra Agent ID (reference) | [Microsoft Entra Agent ID](https://learn.microsoft.com/entra/agent-id/overview) |
| PowerShell with Graph | [Microsoft Graph PowerShell SDK](https://learn.microsoft.com/powershell/microsoftgraph/overview) |

### When to use Graph vs the portal

| Need | Use |
|---|---|
| One-off review during the PoC | Portal (<https://admin.cloud.microsoft>) |
| Scheduled export / CMDB reconciliation | Graph via PowerShell SDK or a lightweight job |
| Cross-tenant / multi-environment reporting | Graph with application permissions, scoped read-only |
| Evidence pack for an auditor | Portal export plus Graph `/auditLogs/*` extracts |

---

Previous: [Chapter 0 - Prerequisites](../chapter-0-prerequisites/README.md) · Next: [UC2 - Identity & Ownership](../chapter-uc2-identity-ownership/README.md)
