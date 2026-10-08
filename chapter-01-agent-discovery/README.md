# Chapter 1 – Agent Discovery and Inventory

**Pillar:** Observe
**What it proves:** You can't govern what you can't see. Every agent available to the organization appears in one inventory, the Agent Registry in the Microsoft 365 admin center, with its type, platform, owner, status and risk signals. You can also read the same inventory programmatically with Microsoft Graph.

**Success criteria**
- Each in-scope Microsoft-native test agent (Copilot Studio and Microsoft Foundry, where in scope) is listed in **Agents** > **All agents** > **Registry**.
- Every in-scope agent has a named owner, or is listed under **Agents without owners** and has a recorded remediation decision.
- The **Agents at risk** tile and **Risks** column were reviewed, and every agent with a high-severity risk signal has a named follow-up owner.
- Agent Map shows the test agents in their platform clusters.
- At least one agent request was reviewed in the **Requests** tab and either published or rejected.
- A registry export and the Microsoft Graph list of catalog packages were captured and compared, and any difference in counts is recorded.

## 1.1 Required permissions

Grant the read-only role first. Grant setup roles only to the people who make changes, and assign them as **Active** for the length of the PoC.

| Task | Least-privilege role | Section |
|---|---|---|
| Publish a Foundry agent as an Agent Application | **Foundry Project Manager** on the Foundry resource scope | 1.2.2 |
| View the Agent Registry, Overview, filters, risk counts and export | **AI Reader** or **Global Reader** | 1.3 |
| Open risk source deep links into Microsoft Entra and Microsoft Defender | **Global Reader**, **Security Reader**, **Security Administrator**, **AI Administrator** or **Global Administrator** | 1.3.4 |
| Open risk source deep links for Microsoft Purview Insider Risk Management alerts | **IRM Analyst** or **IRM Investigator** | 1.3.4 |
| Open Agent Map | **AI Administrator** | 1.4 |
| Approve, publish or reject agent requests | **AI Administrator** | 1.5 |
| View **Data & tools**, tag an agent and take actions from the details pane | **AI Administrator** | 1.6 |
| Read the Agent 365 catalog through Graph (`/copilot/admin/catalog/packages`) | **AI Administrator** | 1.7 |
| Read agent identities, blueprints and blueprint principals through Graph (delegated) | **Agent ID Administrator** | 1.7 |
| Read risky agents and agent risk detections through Graph (delegated) | **Security Reader** | 1.7 |
| Read agent sign-in logs through Graph (delegated) | **Reports Reader** | 1.7 |
| Run Advanced Hunting queries (`AgentsInfo`) | **Security Reader** | 1.7.5 |
| Register the app for app-only access | **Application Developer** | 1.7.4 |
| Grant admin consent to Microsoft Graph application permissions | **Privileged Role Administrator** | 1.7.4 |
| View agents in governed tenants (optional, preview) | **Global Reader** (delegated, in each governed tenant). **AI Administrator** to act. | 1.8 |
| Validation and read-only review | **AI Reader** | 1.3, 1.5, 1.6 |

Notes on roles:
- Only **AI Administrator** and **Global Administrator** can perform governance actions such as approving agent requests or assigning ownership. Other roles can monitor governance gaps but can't take administrative action.
- Agent Map requires the **Global Administrator** or **AI Administrator** role.
- Global Administrator is a highly privileged role. Limit its use to scenarios where you can't use an existing role.

**Before you start:**
- Complete [Chapter 0 – Prerequisites and PoC preparation](../chapter-00-prerequisites/README.md). Agent 365 must be enabled in the Microsoft 365 admin center, and the PoC accounts and role assignments must be in place.
- Prepare at least one Microsoft-native test agent per platform in scope, as described in [1.2](#12-discover-microsoft-native-agents). Use the samples in [`samples/`](samples/README.md).
- Prepare a test SharePoint site to use as a knowledge source for the Copilot Studio sample.
- Non-Microsoft platforms (Amazon Bedrock, Google Vertex AI and others) and custom agents built with the Agent 365 SDK are covered in [Chapter 2 – Third-Party and Custom Agents](../chapter-02-third-party-custom-agents/README.md). Local agents and Shadow AI are covered in [Chapter 9 – Shadow AI and Local Agents](../chapter-09-shadow-ai-local-agents/README.md).
- If you plan to use Microsoft Graph PowerShell (1.7.3), install PowerShell 7, which is the recommended version for the Microsoft Graph PowerShell SDK.

## 1.2 Discover Microsoft-native agents

**Documentation:** [Connect existing agents to Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/connect-existing-agents) · [Agent registry integration for Copilot Studio](https://learn.microsoft.com/microsoft-agent-365/builder/agent-registry) · [Agent identity integration for Copilot Studio](https://learn.microsoft.com/microsoft-agent-365/builder/identity) · [Microsoft Agent 365 integration with Foundry](https://learn.microsoft.com/azure/foundry/agents/concepts/agent-365-integration) · [Publish your agent as an Agent Application](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-agent) · [Agent overview in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview) · [Get started with agents in SharePoint](https://learn.microsoft.com/sharepoint/get-started-sharepoint-agents)

Agents built with Microsoft Foundry, Microsoft Copilot Studio and Agent Builder in Microsoft Copilot integrate with Agent 365 automatically.

| Platform | How the agent reaches the Registry | Identity behavior | Sample |
|---|---|---|---|
| Copilot Studio | Appears in the Registry immediately when the agent is created. Metadata updates are synchronized automatically, and the entry is removed automatically when the agent is deleted. Draft agents are visible only for Copilot Studio. | The agent ID is created at agent creation time, not during publishing. All Copilot Studio app-based agents share a single blueprint, and an agent ID is created for each agent. | [`samples/copilot-studio/`](samples/copilot-studio/README.md) |
| Agent Builder in Microsoft Copilot | Integrated automatically. Draft Agent Builder agents aren't currently visible. | — | — |
| Microsoft Foundry | Every Foundry agent that you publish appears in the Agent 365 registry automatically. Registry sync is supported for prompt agents and hosted agents. Overview analytics currently support only Microsoft Foundry V2 agents. | An unpublished agent uses the project's shared agent identity. A published agent receives its own Entra agent identity and Entra agent blueprint. | [`samples/foundry/`](samples/foundry/README.md) |
| SharePoint | Listed as a supported platform. Draft SharePoint agents aren't currently visible. | — | — |
| Microsoft 365 Agents Toolkit | Agents submitted for admin approval appear in the **Requests** tab (1.5). | — | — |

### 1.2.1 Create a Copilot Studio test agent

Performed by a **test maker account**.

1. Open [`samples/copilot-studio/declarative-agent.json`](samples/copilot-studio/declarative-agent.json) and copy the name, description and instructions.
2. Sign in to Copilot Studio (`https://copilotstudio.microsoft.com`) and create a new agent named `poc-cs-trail-guide`. Use the description and instructions from the sample.
3. Add your PoC SharePoint site as a knowledge source.
4. Publish the agent.
5. Open the configuration panel for the **Teams and Microsoft Copilot** channels, select **Availability options**, and share the agent with the organization by submitting it for admin approval. You use this request in 1.5.

**Check result**
- The agent appears in the Registry (1.3) immediately after it was created.
- The submitted agent appears in **Agents** > **All agents** > **Requests**.

### 1.2.2 Create and publish a Foundry test agent

Performed by **Foundry Project Manager** (publishing).

1. Follow [`samples/foundry/README.md`](samples/foundry/README.md) to create the prompt agent `poc-foundry-trail-guide`.
2. Publish the agent as an Agent Application, as described in [Publish your agent as an Agent Application](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-agent).
3. Reassign any RBAC permissions that the agent's tools need to the new agent identity. Permissions don't transfer automatically when you publish.

**Check result**
- The published agent appears in the Registry.
- In the Microsoft Entra admin center (`https://entra.microsoft.com`), **Entra ID** > **Agents** > **Agent identities** lists the agent identity of the published agent.

## 1.3 Review the Agent Registry

**Documentation:** [Agent Registry in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-registry) · [Agent management roles and permissions](https://learn.microsoft.com/microsoft-365/admin/manage/agent-roles-perms) · [Agent overview in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview)

The Agent Registry provides a centralized view of all agents available for your organization.

### 1.3.1 Open the Registry and read the summary

Performed by **AI Reader**.

1. Sign in to the Microsoft 365 admin center (`https://admin.cloud.microsoft`).
2. Select **Agents** > **Overview**. Note the **Agent registry** count and the cards **Pending requests**, **Agents without owners**, **Agents at risk** and **Agents with exceptions**. The Overview shows only the top five most used platforms. To see all platforms, go to the **Registry** tab.
3. Select **Agents** > **All agents** > **Registry**.
4. Review the summary tiles:

| Tile | Meaning |
|---|---|
| **Total agents** | The number of agents available in your organization's tenant. Applying filters doesn't change this count. |
| **Agents without owners** | The number of agents that no longer have owners at your organization. |
| **Unmanaged agents** | The number of agents created or managed outside of Agent 365, without its risk protection and observability. |
| **Agents at risk** | The total number of agents in the tenant that have one or more risk signals (see 1.3.4). |

5. Review the agent types:

| Agent type | Description |
|---|---|
| **Microsoft agents** | Agents built and maintained by Microsoft. |
| **External partner-built agents** | Agents built by trusted non-Microsoft developers and published for broader or public availability. |
| **Published by your org** | Custom agents approved and published by your organization for broader use (line-of-business agents). |
| **Shared by creator** | Agents created and shared by individual users or developers at your organization (shared agents). |

**Check result**
- The test agents from 1.2 are listed.
- You recorded the **Total agents**, **Agents without owners**, **Unmanaged agents** and **Agents at risk** values as a baseline.

### 1.3.2 Filter, sort and search

Performed by **AI Reader**.

1. On the **Registry** tab, filter the list by:
   - **Status**
   - **Publisher Type**: distinguishes Microsoft agents, external partner-built agents and agents published by your organization
   - **Channel**: **Copilot**, **Teams**, **Outlook**, **Microsoft 365 apps** or **SharePoint**
   - **Platform**: the platform or product used to create the agent
   - **Data source**: **Embedded knowledge** or **Fine-tuned models**
2. To sort the list, select a column title. Only certain columns support sorting.
3. Use **Search** to find a test agent by name.
4. Select the list icon next to the **Search** box to switch between **Normal list** and **Compact list**.

**Check result**
- Filtering by **Platform** isolates each test agent.
- If you don't see the agents that you expect, check that no filter is still applied.

### 1.3.3 Find agents without owners

Performed by **AI Reader** (review) and **AI Administrator** (remediation).

Shared agents can become ownerless when you delete the user who created them from the organization. The ownerless agent count updates automatically when you hard delete a user.

1. On **Agents** > **All agents** > **Registry**, select the **Agents without owners** card. The list is filtered by **Publisher type** and **Owner**.
2. For each agent, decide on an action, such as blocking or deleting the agent, and record the decision.
3. Lifecycle actions (assign a new owner, block, delete) are covered in [Chapter 5 – Agent Lifecycle and Audit](../chapter-05-lifecycle-audit/README.md). Owners and sponsors of agent identities are covered in [Chapter 3 – Agent Identity and Ownership](../chapter-03-identity-ownership/README.md).

**Check result**
- The ownerless list was captured, and each entry has a recorded decision.

### 1.3.4 Review risk signals

Performed by **AI Reader** (Registry view) and **Security Reader** (source deep links).

Risk signals in the Agent Registry are a consolidated set of agent-related security detections from Microsoft security platforms, such as Microsoft Purview, Microsoft Entra and Microsoft Defender.

1. On the **All agents** page, review the **Risks** column. It shows the aggregated count of risk signals for each agent.
2. Select the count for an agent. The **Risk details** pane opens and shows:
   - Risk signals grouped into expandable high, medium and low severity sections, with a description of each signal.
   - An **Occurrences** count for each signal.
   - **Risk signals are sourced from**: the Microsoft security platforms that contribute signals for the agent. Each platform name is a deep link to that portal.
   - For an agent with multiple instances, risk signals grouped by instance.
3. Select the **Agents at risk** tile. It opens a prefiltered view of agents with detected risk signals.
4. Open a source deep link. Access depends on your role in the target portal:

| Security portal | Required role (any one) |
|---|---|
| Microsoft Entra | Global Administrator, Global Reader, Security Reader, Security Administrator or AI Administrator |
| Microsoft Defender | Global Administrator, Global Reader, Security Reader, Security Administrator or AI Administrator |
| Microsoft Purview, Insider Risk Management alerts | IRM Analyst or IRM Investigator. Global Administrator alone is insufficient. |

The risk signal counts in the Microsoft 365 admin center might be up to an hour behind the security portals. A count of zero indicates that no active signals are currently detected for that agent across the connected platforms.

**Check result**
- Every agent with a high-severity signal has a named follow-up owner. Investigation and response are covered in [Chapter 8 – Threat Detection and Runtime Protection (Defender)](../chapter-08-threat-detection/README.md).

### 1.3.5 Customize the view and export

Performed by **AI Reader**.

1. On the **Registry** toolbar, select **Customize view** and choose which columns to display.
2. Select **Export** and set the export scope to **All agents** or **Filtered agents**. The export can include over 30 items for each agent, such as name, status, channel, date created, last modified, publisher, publisher type, version, owner, description, platform and instructions. The export can take some time, depending on the number of agents in the tenant.
3. Optionally, export the list of active users for the last 30 days. It includes user principal name, total agents used, total sessions and last activity date.

**Check result**
- An export file exists that contains the test agents with their owner and platform values.

## 1.4 Visualize agents with Agent Map

**Documentation:** [Use Agent Map in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-map)

Agent Map groups agents by the platform they were created on. It complements the Registry with a visual view for environments with large numbers of agents.

### 1.4.1 Open Agent Map and review clusters

Performed by **AI Administrator**.

1. In the Microsoft 365 admin center, select **Agents** > **All agents** > **Map**.
2. Identify the clusters: **Microsoft Copilot Agent Builder**, **Copilot Studio**, **Copilot Studio Legacy**, **Microsoft 365 Agents Toolkit**, **SharePoint**, **Azure AI Foundry**, **Amazon Bedrock**, **Google Vertex AI**, **Microsoft**, **External Partners** and **Others**.
3. Use **Zoom In/Out**, **Keyboard shortcuts** and **Settings** (**Max agents per platform**) to navigate the map.

**Check result**
- Each test agent from 1.2 appears in its platform cluster.

### 1.4.2 Use summary cards, filters and export

Performed by **AI Administrator**.

1. Review the summary cards: **Total agents**, **Agents at risk** (agents with at least one high security risk), **Agents without owners** and **Unmanaged agents**.
2. Filter the map by:
   - **Status**: **Available**, **Blocked**, **Draft**, **Not activated**
   - **Publisher type**: **Your org**, **Your users**, **Microsoft**, **Third party**
   - **Platform**
   - **Channel**
   - **Usage**: **Active users**, **Total sessions**, **Exception rate**, **Assisted hours**, **Security alerts**
3. Use the search bar to find an agent by name.
4. Select **Export** to download the agents displayed in the Agent Map to an Excel file.

Usage and observability filters are currently available only for tenants with fewer than 4,000 users. Usage is based on agents that report activity through Agent 365.

**Check result**
- The four summary cards are displayed, and the map can be filtered by platform.

## 1.5 Review agent requests

**Documentation:** [Manage agent requests in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-requests) · [Governance and lifecycle actions for agents](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions)

When a member of your organization publishes an agent to your tenant, the agent requires administrator approval before it becomes available tenant-wide. Agents created with Copilot Studio, Microsoft Foundry or Microsoft 365 Agents Toolkit can be submitted for admin approval.

### 1.5.1 Review pending requests

Performed by **AI Administrator**.

1. In the Microsoft 365 admin center, select **Agents** > **All agents** > **Requests**.
2. Filter by **State**:
   - **Pending review**
   - **Pending update**: a new version of an existing agent. Until you approve it, users can access the previous version.
   - **Pending activate**: a member of your organization asks to activate an agent so that they can create agent instances
   - **Allow user to install**: a user requests a Microsoft-built agent that admin policy makes unavailable
3. Filter by **Channel** if needed: **Microsoft Teams**, **Copilot**, **Office**, **Outlook**, **Word**, **Excel** or **PowerPoint**.
4. Select the Copilot Studio test agent submitted in 1.2.1. Confirm the capabilities, data sources, security and permissions, and custom actions that the agent can invoke.

**Check result**
- The test agent is listed in the **Requests** tab.

### 1.5.2 Approve and publish a request

Performed by **AI Administrator**.

1. In the agent details pane, select **Publish to store** to open the publishing wizard.
2. Select the users or groups that can install the agent. For the PoC, use a test group.
3. Optionally, select the users or groups who will have the agent preinstalled.
4. Select **Next** to view template options. Apply an existing template, the default template or a custom template. See [Policy templates](https://learn.microsoft.com/microsoft-agent-365/admin/policy-template).
5. Select **Next** to review permissions. In the **Review permissions** step, view the permissions that the agent requests and grant admin consent if appropriate.
6. Select **Next**, then select **Publish**.

For a request in the **Pending update** state, select the agent and then select **Update in store**.

**Check result**
- The agent is available for installation to the selected audience.

### 1.5.3 Reject a submission

Performed by **AI Administrator**.

1. In the **Requests** list, select the ellipses to the right of the agent name.
2. Select **Reject submission**.

**Check result**
- The agent isn't made available to your organization.

## 1.6 Inspect agent details and tag agents

**Documentation:** [Understand agent details in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-details) · [Agent settings in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-settings)

### 1.6.1 Review the agent details pane

Performed by **AI Administrator**.

1. Go to **Agents** > **All agents**. The **Registry** tab is selected.
2. Select a test agent. The details pane shows the common actions (**Install**, **Uninstall**, **Block**, **Update in store**, **Pin for users**) and a set of tabs. The tabs shown depend on the agent's capabilities.

| Tab | What to check during the PoC |
|---|---|
| **Details** | Description, instructions, publish status, availability, publisher, deployment, agent type, channel, platform, last updated, sensitivity and version. |
| **Users** | **Available to** (which users can install and use the agent) and **Installed for** (which users automatically have the agent preinstalled). Availability and installation are independent actions. |
| **Data & tools** | Read-only. Capabilities, knowledge sources and tools available to the agent, plus Microsoft Entra details such as Agent ID and Agent User ID. |
| **Security** | Monitoring agent activity, protecting sensitive data and evaluating compliance gaps. |
| **Permissions** | Permissions to data that the agent can access and perform actions on. |
| **Certification** | Trust and attestation signals available for the agent. |
| **Activity** | How the agent is used and how it performs across the tenant. |
| **Agent instances** | Shown for agents tagged as **AI teammate**. |
| **Connected Agents** | Agents connected to the selected agent. |
| **Computer use** | Shown for agents that support computer-use capabilities, such as Researcher. |

**Check result**
- For each test agent, you recorded the platform, owner, knowledge sources, tools and Agent ID, where shown.

### 1.6.2 Tag an agent

Performed by **AI Administrator**.

Tags are labels that admins and users apply to agents to organize and find them, such as by team, function or project. Tags don't change what an agent can do or access.

1. If the tag you need doesn't exist yet, select **Agents** > **Settings** > **Tags**, select **Add** and enter a name such as `Agent365-PoC`. An organization can have up to 50 tags.
2. Go to **Agents** > **All agents** and select a test agent from the **Registry** list.
3. In the agent details pane, select **Add tag**.
4. Select up to five tags from the tags available in your organization.
5. In the Registry, filter the list by the tag.

**Check result**
- The tag appears on the agent's page and in the **Tags** column of the agents list, and filtering by the tag returns the PoC test agents.

## 1.7 Programmatic discovery with Microsoft Graph

**Documentation:** [Graph API for agent registry and agent details](https://learn.microsoft.com/microsoft-agent-365/admin/graph-api) · [Package Management API overview](https://learn.microsoft.com/microsoft-365/copilot/extensibility/api/admin-settings/package/overview) · [List Copilot packages](https://learn.microsoft.com/microsoft-365/copilot/extensibility/api/admin-settings/package/copilotpackages-list) · [List agentIdentity objects](https://learn.microsoft.com/graph/api/agentidentity-list?view=graph-rest-1.0) · [List riskyAgents](https://learn.microsoft.com/graph/api/riskyagent-list?view=graph-rest-beta) · [Microsoft Entra Agent ID logs](https://learn.microsoft.com/entra/agent-id/sign-in-audit-logs-agents) · [agentSignIn resource type (agentType values)](https://learn.microsoft.com/graph/api/resources/agentic-agentsignin?view=graph-rest-beta) · [security: runHuntingQuery](https://learn.microsoft.com/graph/api/security-security-runhuntingquery?view=graph-rest-1.0)

Two data sources answer different questions:

- **The Agent 365 catalog** (Package Management API, `/copilot/admin/catalog/packages`). A package represents an agent in the organization catalog. Use the List packages API to get all agents in your inventory, and the Get package details API to get detailed metadata for one agent. These APIs require the AI Administrator or Global Administrator role.
- **Microsoft Entra Agent ID objects** (agent identities, blueprints and blueprint principals). The Microsoft Entra admin center shows agents that have a Microsoft Entra Agent ID. The comprehensive agent inventory, including agents without a Microsoft Entra agent identity, is available in Agent 365.

### 1.7.1 Choose the right API

All APIs in this table are read operations. **Permission** is the least-privileged Microsoft Graph permission documented on the API page.

| Question you want to answer | API | Version | Permission | Role (delegated) |
|---|---|---|---|---|
| Which agents are in the Agent 365 registry? | `GET /copilot/admin/catalog/packages` | v1.0 and beta (preview) | `CopilotPackages.Read.All` | AI Administrator or Global Administrator |
| What are the detailed metadata of one agent? | `GET /copilot/admin/catalog/packages/{id}` | v1.0 and beta (preview) | `CopilotPackages.Read.All` | AI Administrator or Global Administrator |
| Which agent requests are open? | `GET /copilot/admin/catalog/packages?$filter=requestStatus eq 'pending'` | v1.0 and beta (preview) | `CopilotPackages.Read.All` | AI Administrator or Global Administrator |
| Which agent identities exist in Microsoft Entra? | `GET /servicePrincipals/microsoft.graph.agentIdentity` | v1.0 | `AgentIdentity.Read.All` | Agent ID Administrator |
| Which agent identity blueprints exist? | `GET /applications/microsoft.graph.agentIdentityBlueprint` | v1.0 | `AgentIdentityBlueprint.Read.All` | Agent ID Administrator |
| Which blueprint principals exist in my tenant? | `GET /servicePrincipals/microsoft.graph.agentIdentityBlueprintPrincipal` | v1.0 | `AgentIdentityBlueprintPrincipal.Read.All` | Agent ID Administrator |
| Who owns an agent identity? | `GET /servicePrincipals/{id}/microsoft.graph.agentIdentity/owners` | v1.0 | `AgentIdentity.Read.All` | Directory Readers or Global Reader |
| Who sponsors an agent identity? | `GET /servicePrincipals/{id}/microsoft.graph.agentIdentity/sponsors` | v1.0 | `AgentIdentity.Read.All` (delegated, validated in a lab tenant). The API page lists the application permission `AgentIdentity.ReadWrite.All`. | Validated with Global Administrator |
| Which agents does ID Protection consider risky? | `GET /identityProtection/riskyAgents` | **beta** | `IdentityRiskyAgent.Read.All` | Security Reader, Security Operator, Global Reader or Security Administrator |
| Which risk detections were raised for agents? | `GET /identityProtection/agentRiskDetections` | **beta** | `IdentityRiskEvent.Read.All` | Security Reader, Security Operator, Global Reader or Security Administrator |
| Which agent identities signed in? | `GET /auditLogs/signIns` with the filter `agent/agentType eq 'agenticAppInstance'` | **beta** | `AuditLog.Read.All` | Reports Reader |
| What configuration does Defender record for each agent? | `POST /security/runHuntingQuery` with the `AgentsInfo` table (preview) | v1.0 | `ThreatHunting.Read.All` | Security Reader |

Notes:
- APIs under `/beta` are subject to change. Use of these APIs in production applications isn't supported.
- Sponsors: you can also view the owners and sponsors of each agent identity in the Microsoft Entra admin center under **Entra ID** > **Agents** > **Agent identities** (**Owners and Sponsors** column). Sponsors are covered in [Chapter 3 – Agent Identity and Ownership](../chapter-03-identity-ownership/README.md).
- `riskyAgents` supports the `$select`, `$count` and `$filter` query parameters.
- To receive the `agentIdentityBlueprintPrincipal` and `agentIDuser` enum values in responses, include the request header `Prefer: include-unknown-enum-members`.
- Paging: treat `@odata.nextLink` as an opaque URL. Request it exactly as returned, and continue until it's absent.

The queries used in this chapter:

```http
GET https://graph.microsoft.com/v1.0/copilot/admin/catalog/packages
GET https://graph.microsoft.com/v1.0/copilot/admin/catalog/packages/{id}
GET https://graph.microsoft.com/v1.0/copilot/admin/catalog/packages?$filter=requestStatus eq 'pending'
GET https://graph.microsoft.com/v1.0/servicePrincipals/microsoft.graph.agentIdentity
GET https://graph.microsoft.com/v1.0/servicePrincipals/{id}/microsoft.graph.agentIdentity/owners
GET https://graph.microsoft.com/v1.0/applications/microsoft.graph.agentIdentityBlueprint
GET https://graph.microsoft.com/v1.0/servicePrincipals/microsoft.graph.agentIdentityBlueprintPrincipal
GET https://graph.microsoft.com/beta/identityProtection/riskyAgents
GET https://graph.microsoft.com/beta/identityProtection/agentRiskDetections
GET https://graph.microsoft.com/beta/auditLogs/signIns?$filter=signInEventTypes/any(t: t eq 'servicePrincipal') and agent/agentType eq 'agenticAppInstance'
```

### 1.7.2 Run queries in Graph Explorer

Performed by **AI Administrator** (catalog queries), **Agent ID Administrator** (agent identity queries) and **Security Reader** (risk and hunting queries).

1. Open [Graph Explorer](https://developer.microsoft.com/graph/graph-explorer).
2. Select the profile avatar and sign in with your PoC account. Check the tenant that is shown in the top navigation.
3. Select **GET** as the HTTP method and **v1.0** as the API version.
4. Enter `https://graph.microsoft.com/v1.0/copilot/admin/catalog/packages` in the query box.
5. Select the **Modify permissions** tab, then select **Consent** next to `CopilotPackages.Read.All`. You can also use **Consent to permissions** under the profile avatar. Tenant-wide admin consent for delegated permissions can be granted by a Cloud Application Administrator, AI Administrator or Application Administrator.
6. Select **Run query**.
7. Review the **Response preview**:
   - `value` contains the packages. The documented properties include `id`, `displayName`, `type` (`microsoft`, `external`, `shared`, `custom`), `publisher`, `isBlocked`, `availableTo`, `deployedTo`, `supportedHosts`, `elementTypes` and `lastModifiedDateTime`.
   - If the response contains `@odata.nextLink`, request that URL exactly as returned, and continue until no `@odata.nextLink` is returned.
8. Repeat for the agent identity query, and consent to `AgentIdentity.Read.All`.
9. For the beta queries, select **beta** as the API version. For `riskyAgents`, add the request header `Prefer` with the value `include-unknown-enum-members` under **Request headers**, and consent to `IdentityRiskyAgent.Read.All`.
10. For Advanced Hunting, select **POST**, enter `https://graph.microsoft.com/v1.0/security/runHuntingQuery`, consent to `ThreatHunting.Read.All`, and use this request body:

```json
{
  "Query": "AgentsInfo | summarize arg_max(Timestamp, *) by AgentId | project AgentId, Name, Platform, PublishedStatus, LifecycleStatus, Owners, EntraAgentID, EntraBlueprintID"
}
```

The response contains a `schema` array and a `results` array. The optional `Timespan` parameter defaults to 30 days.

**Check result**
- The catalog query returns the PoC test agents, and you recorded the number of items after following every `@odata.nextLink`.

### 1.7.3 Export the inventory with Microsoft Graph PowerShell

Performed by **AI Administrator**.

1. Install the Microsoft Graph PowerShell SDK:

```powershell
Install-Module Microsoft.Graph -Scope CurrentUser -Repository PSGallery -Force
```

2. Run the example from the Agent Registry article. It lists all agents in your tenant and follows `@odata.nextLink` until all pages are read:

```powershell
Connect-MgGraph -Scopes 'CopilotPackages.Read.All'

$uri = "https://graph.microsoft.com/v1.0/copilot/admin/catalog/packages"
$agentCount = 0

do {
    $response = Invoke-MgGraphRequest -Method GET -Uri $uri
    $agentCount += @($response.value).Count
    $response.value | ForEach-Object { Write-Host $_.displayName }
    $uri = $response.'@odata.nextLink'
} while ($uri)

Write-Host "Total agents: $agentCount"
```

**Check result**
- The script lists the display name of every agent in the catalog and prints the total count.

### 1.7.4 Run the export unattended with an app registration

Performed by **Application Developer** (app registration) and **Privileged Role Administrator** (admin consent).

Use application permissions when the call runs as a background service without a signed-in user. Microsoft Graph application permissions always require administrator consent.

1. Sign in to the Microsoft Entra admin center (`https://entra.microsoft.com`). Browse to **Entra ID** > **App registrations** and select **New registration**. Enter a name, for example `agent365-poc-inventory`. Under **Supported account types**, select **Single tenant only**.
2. In the app registration, select **Certificates & secrets** > **Certificates** > **Upload certificate**, and upload the public key of your certificate.
3. On the **API permissions** page, select **Add a permission** > **Microsoft Graph** > **Application permissions**. Add only the permissions you need, for example:
   - `CopilotPackages.Read.All`
   - `AgentIdentity.Read.All`
   - `IdentityRiskyAgent.Read.All`
   - `ThreatHunting.Read.All`
4. A **Privileged Role Administrator** grants tenant-wide admin consent: on **API permissions**, select **Grant admin consent**. Cloud Application Administrator, AI Administrator and Application Administrator can't grant consent to Microsoft Graph application permissions.
5. Make sure the certificate is present in `Cert:\CurrentUser\My\` or `Cert:\LocalMachine\My\` on the machine that runs the script. Then connect with app-only access and run the loop from 1.7.3 without the `Connect-MgGraph -Scopes` line:

```powershell
Connect-MgGraph -ClientId "YOUR_APP_ID" -TenantId "YOUR_TENANT_ID" -CertificateThumbprint "YOUR_CERT_THUMBPRINT"
```

**Check result**
- The app-only connection succeeds, and the catalog list from 1.7.3 returns the same agents as the delegated run.

### 1.7.5 Query the Defender agent inventory with Advanced Hunting

Performed by **Security Reader**.

The `AgentsInfo` table (preview) contains information about AI agents and their properties from various platforms. The `AIAgentsInfo` table is transitioning to `AgentsInfo`. Migrate queries from `AIAgentsInfo` to `AgentsInfo`.

1. In the Microsoft Defender portal (`https://security.microsoft.com`), select **Hunting** > **Advanced hunting**.
2. Run this query:

```kql
AgentsInfo
| summarize arg_max(Timestamp, *) by AgentId
| project AgentId, Name, Platform, PublishedStatus, LifecycleStatus, Availability,
          Owners, EntraAgentID, EntraBlueprintID, InstanceCount, LastUpdatedDateTime
| order by Platform asc, Name asc
```

3. To run the same query from automation, call `POST https://graph.microsoft.com/v1.0/security/runHuntingQuery` with the request body shown in 1.7.2.

**Check result**
- The query returns the agents in the `AgentsInfo` table, with their platform, status and owners.

## 1.8 Review agents across multiple tenants (optional, preview)

**Documentation:** [Manage agents across multiple tenants in the Microsoft 365 admin center (preview)](https://learn.microsoft.com/microsoft-365/admin/manage/agent-multi-tenant)

Multi-tenant agent management is in public preview. It's intended for Microsoft partners who manage customer tenants by using Partner Center (GDAP), and for enterprises whose tenants are connected through Microsoft Entra Tenant Governance. Microsoft Entra Tenant Governance isn't the same as Multitenant Collaboration (MTO) in Microsoft 365.

| Delegated role in the governed tenant | View agent inventory | Add, install, block or change availability |
|---|---|---|
| AI Administrator | Yes | Yes |
| Global Administrator | Yes | Yes |
| Global Reader | Yes | No |

### 1.8.1 Open the consolidated inventory

Performed by **Global Reader** (delegated, in each governed tenant).

1. Sign in to the Microsoft 365 admin center with an account in the governing tenant.
2. Select **All tenants** > **Agents**. The **All tenants** scope is available only when the governing tenant has at least one supported tenant relationship and the signed-in administrator has a supported delegated role.
3. Review **Total agents**, **Risky agents** and **Assigned tenants**.
4. Select an agent and a governed tenant to review that tenant's details. Agent status is tenant-specific.

### 1.8.2 Switch into a governed tenant

Performed by **Global Reader**.

1. In the Microsoft 365 admin center command bar, select the tenant switcher next to the current tenant name.
2. Search for or select the governed tenant. The admin center opens in the selected governed tenant by using your delegated access.
3. Use the tenant switcher again to return to the governing tenant.

**Check result**
- The consolidated inventory lists agents from the governed tenants in scope. The PoC doesn't run cross-tenant **Install** or **Block** unless the customer explicitly asks for it.

## 1.9 Evidence

- Agent overview screenshot showing the **Agent registry** count and the **Pending requests**, **Agents without owners** and **Agents at risk** cards.
- Registry export of all agents, and a filtered export of the PoC test agents with the owner column populated.
- Screenshots of the **Agents without owners** list and the **Agents at risk** list, with the triage decisions.
- Screenshot of one **Risk details** pane, if any agent has risk signals.
- Agent Map screenshot showing the platform clusters.
- Screenshots of the **Requests** tab before and after the approval or rejection in 1.5.
- Screenshot of a test agent's details pane (**Details** and **Data & tools** tabs) showing the applied tag.
- Microsoft Graph results: the Graph Explorer response of the catalog query and the agent identity query, and the output of the PowerShell example (1.7.3). Mark results from beta APIs (`riskyAgents`, `agentRiskDetections`, `signIns`) as beta.
- `AgentsInfo` query results from Advanced Hunting.
- A note that records any difference between the Registry export and the Graph results.

## 1.10 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Expected agent missing from the Registry list | A filter is set | Clear the filters. Applying filters doesn't change the **Total agents** count. |
| Foundry agent missing from the Registry | The agent isn't published | Publish the agent as an Agent Application (1.2.2). Every Foundry agent that you publish appears in the registry. |
| Agent Builder, Foundry or SharePoint draft agent missing | Draft agents are visible only for Copilot Studio | Publish the agent. |
| Non-Microsoft or Agent 365 SDK agent missing | Connected platform or SDK onboarding isn't done | See [Chapter 2 – Third-Party and Custom Agents](../chapter-02-third-party-custom-agents/README.md). |
| **Map** isn't available | Agent Map requires the Global Administrator or AI Administrator role | Use an AI Administrator account. |
| **Usage** filters missing on the map | Usage and observability filters are available only for tenants with fewer than 4,000 users, and usage is based on agents that report activity through Agent 365 | Use the other map filters. |
| Risk source deep link doesn't open the source data | Deep links are subject to the user's roles and permissions in the target portal | Use a role listed in 1.3.4. |
| Risk count differs from the security portal | Counts in the admin center might be up to an hour behind the security portals | Refresh the Registry later. |
| `400 Bad Request` from `/copilot/admin/catalog/packages` with a filter | Unsupported filter, such as a request property combined with `supportedHosts`, `elementTypes` or `platform`; `eq`, `gt` or `lt` on `lastModifiedDateTime`; `or`, `ne` or `contains`; or `$count` with a request filter | Use one of the supported filter expressions listed in [List Copilot packages](https://learn.microsoft.com/microsoft-365/copilot/extensibility/api/admin-settings/package/copilotpackages-list). |
| `agentIdentityBlueprintPrincipal` or `agentIDuser` values aren't returned | The `Prefer` header is missing | Add `Prefer: include-unknown-enum-members`. |
| An admin action on an agent fails in the Microsoft 365 admin center | The agent is in a Power Platform environment with IP firewall in active enforcement mode | In the Power Platform admin center, go to **Security** > **Identity and access** > **IP firewall**, select the environment, and check the **Advanced** tab. See [Governance and lifecycle actions](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions). |

## 1.11 Cleanup

- Delete the test agents (`poc-cs-trail-guide`, `poc-foundry-trail-guide`) after evidence is collected, unless later chapters still use them.
- Remove the `Agent365-PoC` tag from any agent that isn't part of the PoC.
- Delete the `agent365-poc-inventory` app registration, if you created it.
- Remove time-bound role assignments (AI Administrator, Agent ID Administrator, Security Reader, Reports Reader, Application Developer, Privileged Role Administrator) at the end of the PoC window.
- Store the exports in the restricted evidence location, and delete local copies.

---
Previous: [Chapter 0 – Prerequisites and PoC preparation](../chapter-00-prerequisites/README.md) · Next: [Chapter 2 – Third-Party and Custom Agents](../chapter-02-third-party-custom-agents/README.md)
