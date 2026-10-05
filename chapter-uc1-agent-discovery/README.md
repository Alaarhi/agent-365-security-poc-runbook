# Chapter UC1 - Agent Discovery

**Pillar:** Observe
**What it proves:** you cannot govern what you cannot see. Every agent in the tenant surfaces in one registry, including the ones nobody registered, each with a named, accountable owner.

## Section 1 - Roles, scope, and prerequisites

| Task | Role | Notes |
|---|---|---|
| Setup / configuration | **AI Administrator** | Required to enable Agent 365, configure Registry sync for connected platforms, approve agents, and change registry settings. Assign Active for the PoC window. |
| Read-only / validation | **AI Reader** (or **Global Reader**) | Sufficient to view the Agent Registry, list agents, see owners, and export the registry. Use this role for reviewers, auditors, and anyone verifying results. |
| Optional (SDK agents) | **Agent ID Developer** | Required for developers onboarding custom-built agents via the Agent 365 SDK. Not required for viewing. |

Grant the read-only role first; only grant the setup role to whoever will make configuration changes.

### Task 1 - confirm agent types and discovery paths

The Agent Registry discovers three categories of agent. Each has a different discovery path and surfaces different metadata. Sample agents of each type are provided in [`agent-samples/`](agent-samples/).

| Category | Example platforms | Discovery path | Sample |
|---|---|---|---|
| Microsoft-native | Microsoft 365 Copilot / Agent Builder declarative agents, Copilot Studio, Azure AI Foundry, SharePoint agents | Automatic once Agent 365 is enabled. Agent appears in the Registry after publish (Copilot Studio / Agent Builder) or after agent creation (Foundry). Full propagation up to 24 hours. | [`agent-samples/copilot-studio/`](agent-samples/copilot-studio/), [`agent-samples/foundry/`](agent-samples/foundry/) |
| Connected platforms | Databricks Genie, Google Vertex AI, Snowflake Cortex, AWS Bedrock, Salesforce Agentforce | Registry sync configured per platform in `admin.cloud.microsoft` > **Agents** > **Connected platforms**. The source platform's agent inventory is pulled into the Agent Registry on a schedule. See the optional connected-platforms section at the end of this chapter. | - |
| Custom (Agent 365 SDK) | Customer-built agents in Node.js, Python, or .NET | Onboarded through [`microsoft/agent365-skills`](https://github.com/microsoft/agent365-skills) by running `a365 setup all`. Appears in the Registry once the Blueprint and Entra Agent Identity are provisioned. | [`agent-samples/sdk/`](agent-samples/sdk/) |

Each sample folder has a README that walks through the discovery path step by step.

### Task 2 - open the Agent 365 portal

Microsoft 365 admin center - <https://admin.cloud.microsoft> > **Agents**.

### Task 3 - review documentation

| Topic | Documentation |
|---|---|
| Agent 365 overview | [Overview of Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/overview) |
| Agent Registry | [Agent Registry in Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/administrator/agent-registry) |
| Connected platforms | [Connected platforms for Agent 365](https://learn.microsoft.com/microsoft-agent-365/administrator/connected-platforms) |

### Task 4 - confirm prerequisites

Complete [Chapter 0 - Prerequisites](../chapter-0-prerequisites/README.md). Agent 365 should be enabled and at least one Microsoft-native agent (Copilot Studio, Foundry, or Microsoft 365 Copilot Agent Builder) should exist so there is content to discover. If connected platforms are in scope (AWS Bedrock, Google Vertex AI, Databricks Genie, Snowflake Cortex, Salesforce Agentforce), their tenant-side integrations are configured in the optional connected-platforms section at the end of this chapter.

## Section 2 - Discovery setup and validation tasks

### Task 1 - setup Agent Registry discovery

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

### Task 2 - test registry inventory

Performed by anyone with **AI Reader**.

1. Open <https://admin.cloud.microsoft> > **Agents** > **All agents**.
2. Filter by platform and confirm every in-scope agent is listed.
3. Confirm the owner column is populated for every agent.
4. Export the registry (CSV or JSON) as evidence.

**Expected result**

- All in-scope agents are visible in the registry within the agreed discovery window (default: 24 hours after enablement).
- Every agent has a business owner.
- No unknown or orphaned agents remain.

### Task 3 - test Agent Map

Performed by anyone with **AI Reader**.

1. Open the **Agent Map** view in the Agents section.
2. Confirm the map renders agent-to-tool and agent-to-agent interactions.
3. Capture a screenshot as evidence.

**Expected result**

- Agent Map renders known interactions.
- Discovered agents that were not previously known are triaged with their owner.

## Section 3 - Evidence and common issues

### Task 1 - capture evidence

- Registry export (CSV/JSON) with owner column populated.
- Agent Map screenshot.
- List of any newly discovered / previously unknown agents, with owner assignment status.

### Task 2 - troubleshoot common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent missing from registry | Agent 365 not enabled for that platform, or agent never invoked | Enable the platform integration; run at least one turn on the agent. |
| Owner column blank | Sponsor / owner not assigned during agent creation | Assign an owner in the agent's platform (Copilot Studio, Foundry, or Entra Enterprise Applications). Covered in [UC2](../chapter-uc2-identity-ownership/README.md). |
| Connected platform not syncing | Registry sync not configured or credentials expired | Reconfigure Registry sync per platform documentation. |
| SDK agent missing | `a365 setup all` not completed for that project | Rerun `a365 setup all` and confirm Blueprint is registered. |

## Section 4 - Optional connected-platform discovery

Agent 365 can pull agents from non-Microsoft platforms into the same Registry so they are visible, assignable to owners, and in scope for the governance and audit workstreams. Setup is a one-time per-platform configuration in the Microsoft 365 admin center. All three paths below share the same pattern - prepare the source platform, register a connection, and let Registry sync populate the inventory on its schedule.

### Task 1 - open the connected-platforms entry point

Microsoft 365 admin center - <https://admin.cloud.microsoft> > **Agents** > **Connected platforms** > **+ Add platform**.

### Task 2 - connect AWS Bedrock

| Step | What to do |
|---|---|
| 1. AWS prerequisites | At least one Bedrock agent exists in an AWS account and region in scope. Create an IAM role or user with least-privilege read access to Bedrock agents (for example `bedrock:ListAgents`, `bedrock:GetAgent`). |
| 2. Credentials | Prepare the credentials or federation that Agent 365 will use to call Bedrock (IAM role ARN with trust policy, or access key for the IAM user). |
| 3. In Agent 365 | Open **Connected platforms** > **+ Add platform** > **AWS Bedrock**. Enter the AWS account ID, region(s), and credentials or federation details. Save. |
| 4. Validate | Confirm connector status is **Connected**. Wait for the first sync (typically within an hour). |
| 5. Verify in Registry | Bedrock agents appear under **Agents** > **All agents** with platform = AWS Bedrock, the AWS agent ID, and a configurable business owner. |

Documentation:
- [Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [IAM for Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html)
- [Agent 365 - Connected platforms](https://learn.microsoft.com/microsoft-agent-365/administrator/connected-platforms)

### Task 3 - connect Google Vertex AI

| Step | What to do |
|---|---|
| 1. Google Cloud prerequisites | At least one Vertex AI agent exists in a Google Cloud project in scope. Enable the Vertex AI API on the project. |
| 2. Service account | Create a Google Cloud service account with least-privilege read access to Vertex AI (for example `aiplatform.agents.list`, `aiplatform.agents.get`). Download the service-account key or configure Workload Identity Federation with Entra. |
| 3. In Agent 365 | Open **Connected platforms** > **+ Add platform** > **Google Vertex AI**. Enter the GCP project ID, region, and the service-account credentials or federation. Save. |
| 4. Validate | Confirm connector status is **Connected**. Wait for the first sync. |
| 5. Verify in Registry | Vertex agents appear with platform = Google Vertex AI, the Vertex agent/project ID, and an owner you can edit. |

Documentation:
- [Vertex AI Agents overview](https://cloud.google.com/vertex-ai/docs/agents)
- [Service accounts in Google Cloud](https://cloud.google.com/iam/docs/service-account-overview)
- [Workload Identity Federation with Microsoft Entra](https://cloud.google.com/iam/docs/workload-identity-federation)
- [Agent 365 - Connected platforms](https://learn.microsoft.com/microsoft-agent-365/administrator/connected-platforms)

### Task 4 - connect Databricks Genie

| Step | What to do |
|---|---|
| 1. Databricks prerequisites | At least one Genie space / agent exists in the Databricks workspace(s) in scope. Confirm the workspace URL and that the Genie product is enabled. |
| 2. Databricks credentials | Create a Databricks service principal (or personal access token for a bootstrap) with least-privilege read scope on Genie resources. |
| 3. In Agent 365 | Open **Connected platforms** > **+ Add platform** > **Databricks Genie**. Enter the Databricks workspace URL and credentials. Save. |
| 4. Validate | Confirm connector status is **Connected**. Wait for the first sync (typically within an hour). |
| 5. Verify in Registry | Genie agents appear with platform = Databricks Genie, the Databricks workspace, and owners you can assign. |

Documentation:
- [Databricks AI/BI Genie overview](https://learn.microsoft.com/azure/databricks/genie/)
- [Databricks service principals](https://learn.microsoft.com/azure/databricks/admin/users-groups/service-principals)
- [Agent 365 - Connected platforms](https://learn.microsoft.com/microsoft-agent-365/administrator/connected-platforms)

### Task 5 - test connected agents in the Registry

Performed by anyone with **AI Reader**.

1. Open <https://admin.cloud.microsoft> > **Agents** > **All agents**.
2. Filter by platform (AWS Bedrock, Google Vertex AI, Databricks Genie).
3. Confirm every expected connected agent is listed.
4. Confirm each has an assignable owner.
5. Export the filtered list as evidence.

### Task 6 - troubleshoot connected-platform issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Connector status = Error | Invalid credentials or missing permission on the source platform | Verify the IAM / service-account / service-principal permissions match the connector's requirements. |
| No agents sync | Connector connected but source platform has no agents, or Registry sync has not run yet | Confirm the source has agents; wait for the next sync cycle. |
| Partial sync | Permission scoped too narrowly on the source platform | Grant list + get permissions across the agent resources. |
| Agent appears without owner | Owner is set in Agent 365, not inherited from the source | Assign a business owner in the Agent 365 Registry UI. |

## Section 5 - Optional programmatic discovery with Microsoft Graph

The UI in the Microsoft 365 admin center is the fastest path for a visual review, but Microsoft Graph exposes the same inventory programmatically. Use this when you need scheduled exports, external reporting, CMDB sync, or automated reconciliation against a source of truth.

### Task 1 - confirm retrievable Graph signals

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

### Task 2 - confirm minimum Graph permissions

| Scope | Why |
|---|---|
| `Application.Read.All` (delegated or app) | Read agent applications and service principals. |
| `Directory.Read.All` (delegated) | Read owners, sponsors, and directory metadata. |
| `CustomSecAttributeAssignment.Read.All` (delegated) | Read custom security attribute values on agent identities (requires Attribute Assignment Reader). |
| `Policy.Read.All` (delegated) | Read Conditional Access policies that target agent identities. |
| `AuditLog.Read.All` (delegated or app) | Read directory audit and sign-in logs. |
| `AgentApplication.Read.All` / Copilot admin scopes (preview) | Read Copilot/agent inventory via the Copilot admin endpoints. Scope names and surface are preview; confirm against current docs before relying on them in production. |

Prefer delegated permissions scoped to a read-only account. Only grant application permissions for an unattended service that needs to run outside a user context.

### Task 3 - list agent service principals

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

### Task 4 - get sign-in activity for one agent

```http
GET https://graph.microsoft.com/v1.0/auditLogs/signIns?$filter=appId eq '<agent-app-id>'&$top=50
Authorization: Bearer <token>
```

Returns the service-principal sign-ins for the agent, including Conditional Access decisions. Used in [UC3](../chapter-uc3-least-privilege/README.md) and [UC6](../chapter-uc6-lifecycle-audit/README.md).

### Task 5 - read custom security attributes on an agent

```http
GET https://graph.microsoft.com/v1.0/servicePrincipals/{id}?$select=id,displayName,customSecurityAttributes
Authorization: Bearer <token>
```

### Task 6 - review Graph documentation

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

### Task 7 - choose Graph or portal

| Need | Use |
|---|---|
| One-off review during the PoC | Portal (<https://admin.cloud.microsoft>) |
| Scheduled export / CMDB reconciliation | Graph via PowerShell SDK or a lightweight job |
| Cross-tenant / multi-environment reporting | Graph with application permissions, scoped read-only |
| Evidence pack for an auditor | Portal export plus Graph `/auditLogs/*` extracts |

---

Previous: [Chapter 0 - Prerequisites](../chapter-0-prerequisites/README.md) · Next: [UC2 - Identity & Ownership](../chapter-uc2-identity-ownership/README.md)
