# Chapter 3 – Agent Identity and Ownership

**Pillar:** Govern
**What it proves:** Agents become governable directory identities. Every in-scope agent has a Microsoft Entra Agent ID linked to a blueprint, named owners and sponsors who are accountable for it, observable sign-in and audit activity, a risk-response path, and a sponsorship that survives when people move or leave.

**Success criteria**
- Every in-scope PoC agent appears in **Entra ID** > **Agents** > **Agent identities** with **Uses agent identity** = Yes and the expected **Blueprint App ID**.
- Every in-scope agent identity and blueprint has at least one named sponsor, and the technical owner is recorded.
- A sponsor can see their agents in the My Account portal and can disable (but not re-enable) one of them.
- (Optional) Filtering on `AgentGovernance/Project = Agent365PoC` returns every PoC agent identity.
- Agent sign-ins are visible in the sign-in logs with the **Agent type** and **Is Agent** filters, and agent identity events are visible in the audit logs.
- A test agent can be confirmed compromised (risk level **High**) and then confirmed safe (risk level **None**).
- A Lifecycle Workflows run transfers a test sponsor's agent identity sponsorships to that sponsor's manager.
- The PoC team can explain when to disable an agent identity, a blueprint, or apply a tenant-wide control.

## 3.1 Required permissions

Grant the read-only role first; assign setup roles only to the person who makes each change, and assign them as Active (not Eligible) for the PoC window.

| Task | Least-privilege role | Section |
|---|---|---|
| View agent identities and blueprints in the admin center | Any Microsoft Entra user (no admin role) | 3.4.1, 3.4.2 |
| List agent identities with Microsoft Graph | Agent ID Administrator (owners can read their own agent identities) | 3.4.3 |
| Migrate legacy Copilot Studio agents to Agent ID (preview) | Power Platform Administrator | 3.3.2 |
| Add or remove owners and sponsors | Agent ID Administrator (owners of the object can do this without a role) | 3.5 |
| Disable or re-enable agent identities and blueprints | Agent ID Administrator (owners can manage their own agents without a role) | 3.11 |
| Configure inheritable permissions on a blueprint | Agent ID Developer (blueprints you own) or Agent ID Administrator | 3.6 |
| Create attribute sets and attribute definitions | Attribute Definition Administrator | 3.7.1 |
| Assign custom security attribute values to agent identities | Attribute Assignment Administrator | 3.7.2 |
| Read custom security attribute assignments | Attribute Assignment Reader | 3.7.3 |
| Read sign-in and audit logs | Reports Reader | 3.8 |
| View the Risky agents report | Security Reader | 3.9.1 |
| Confirm compromised, confirm safe, dismiss risk (Microsoft Graph) | Security Administrator | 3.9.2 |
| Create, run, and delete Lifecycle Workflows | Lifecycle Workflows Administrator | 3.10 |
| Validation / read-only review | Any Microsoft Entra user; Reports Reader; Security Reader; Attribute Assignment Reader | 3.12 |

Notes:
- By default, Global Administrator and other administrator roles can't read, define, or assign custom security attributes. Assign the attribute roles explicitly.
- Users with Agent ID admin roles aren't made sponsor automatically when they create agents.

**Before you start:**
- Complete [Chapter 0 – Prerequisites and PoC preparation](../chapter-00-prerequisites/README.md) (test admin, standard test user, reviewer accounts, published PoC agents).
- Complete [Chapter 1 – Agent Discovery and Inventory](../chapter-01-agent-discovery/README.md) so you know which agents are in scope.
- If you use custom or SDK-built agents, complete [Chapter 2 – Third-Party and Custom Agents](../chapter-02-third-party-custom-agents/README.md) so their blueprint and agent identities exist in your tenant.
- Prepare two extra test users for the sponsor continuity test in 3.10: **PoC Sponsor** and **PoC Sponsor Manager**. Set PoC Sponsor's **Manager** attribute to PoC Sponsor Manager; the sponsorship transfer task requires a populated manager attribute, and the email tasks notify the manager and co-sponsors.
- Pick one non-production test agent that you can disable, mark as risky, and re-enable during the tests.
- Access packages for agents are covered in [Chapter 6 – Conditional Access and Least Privilege](../chapter-06-conditional-access/README.md). This chapter only links to it.

## 3.2 Understand the Agent ID object model
**Documentation:** [Fundamental concepts in Microsoft Entra Agent ID](https://learn.microsoft.com/entra/agent-id/key-concepts) · [Owners, sponsors, and managers](https://learn.microsoft.com/entra/agent-id/agent-owners-sponsors-managers) · [Agent's user account](https://learn.microsoft.com/entra/agent-id/agent-users) · [View and filter agent identities in your tenant](https://learn.microsoft.com/entra/agent-id/agent-lists) · [Disable agent identities in your tenant](https://learn.microsoft.com/entra/agent-id/disable-agent-identities)

### 3.2.1 Identity objects

| Object | What it is | PoC relevance |
|---|---|---|
| **Agent identity blueprint** | Template and authentication foundation for one or more agent identities. Holds the credentials and acquires tokens on behalf of all agent identities created from it. Policies applied to a blueprint, such as Conditional Access, take effect for all its agent identities. | For example the **Microsoft Copilot Studio agent identity blueprint**, or a blueprint you created in Chapter 2. |
| **Agent identity blueprint principal** | The object that records a blueprint's presence in a tenant, enables it to acquire tokens, and appears in audit logs. Listed under **Entra ID** > **Agents** > **Agent blueprints**. | Where you view linked agent identities, granted permissions, owners and sponsors, logs, and the **Disable** action for the blueprint. |
| **Agent identity** | The primary identity an agent uses to authenticate and access resources. It has no credentials of its own; it authenticates using tokens issued by its blueprint. | This is what you govern in this chapter. |
| **Agent's user account** (agent user) | Optional account paired 1:1 with an agent identity, used only when the agent must access systems that require a user object (mailbox, calendar, Teams, documents). It doesn't replace the agent identity; both must exist. | Shown in the sign-in logs **Agent type** filter as **Agent ID user**. |

The **Agent identities** list also includes agents that use a service principal instead of an agent identity object. For those, **Uses agent identity** = No and **Blueprint App ID** is blank. Agents created in earlier versions of Copilot Studio and Azure AI Foundry might have been created this way; they're subject to the same policies, governance, and processes as all other applications and service principals in your tenant.

### 3.2.2 Owners, sponsors, and managers

| | Owners | Sponsors | Managers |
|---|---|---|---|
| Purpose | Technical administration: setup, configuration, credential management | Business accountability: purpose, lifecycle decisions, access reviews, retention | User responsible for the agent in the organizational hierarchy |
| Required | Optional | At least one required on create for agent identities and agent identity blueprints (blueprint principals are exempt at creation) | Optional |
| Allowed types | Users (including guests) and service principals. Groups aren't supported. | Users (including guests); dynamic membership groups (security or Microsoft 365) and assigned membership Microsoft 365 groups. Role-assignable groups and assigned membership security groups aren't allowed. | Individual users |
| Limits | — | Up to 100 sponsors, no more than 5 groups | — |
| Can disable and delete agent identities | Yes | Yes (disable, soft-delete) | No |
| Can re-enable, restore, or hard-delete | Yes | No — contact an owner or admin | No |
| Can edit settings and credentials, add owners and sponsors | Yes | Can modify the identity's sponsors only | No |
| Can request access packages | Yes (for owned agents) | Yes (for sponsored agents) | Yes (for their agents' user accounts) |

When a group is a sponsor, all members of the group have sponsor rights. When you use a dynamic membership group as a sponsor, it can take up to 24 hours after a membership rule change or a user property change before the authorization check on sponsorship succeeds.

## 3.3 Bring Copilot Studio agents under Microsoft Entra Agent ID
**Documentation:** [Manage Entra Agent IDs (Copilot Studio)](https://learn.microsoft.com/microsoft-copilot-studio/admin-use-entra-agent-identities) · [Migrate Copilot Studio agents to Microsoft Entra Agent ID (preview)](https://learn.microsoft.com/microsoft-copilot-studio/govern-migrate-api-entra-agent-identity)

Copilot Studio automatically creates a Microsoft Entra Agent ID for each new agent, and you can no longer opt out of automatic agent identity creation. When the first agent identity is created, Copilot Studio adds the **Microsoft Copilot Studio agent identity blueprint** (Blueprint ID `25664c89-cea5-4ab6-b924-a54fd8a19ae0`) and a corresponding blueprint principal to your tenant. All Copilot Studio agent identities are children of this blueprint. Agents created before the Entra Agent ID rollout continue to use app registrations until they're migrated.

### 3.3.1 Confirm a Copilot Studio agent has an agent identity
Performed in Copilot Studio, then by **any Microsoft Entra user** in the Entra admin center.
1. Open <https://copilotstudio.microsoft.com> and go to the **Settings** page for the PoC agent.
2. Select **Advanced** and expand the **Metadata** section.
3. Copy the GUID shown under **Entra Agent ID**.
4. Open <https://entra.microsoft.com> > **Entra ID** > **Agents** > **Agent identities** and use the GUID to find the agent identity.

**Check result**
- The agent identity is listed with **Uses agent identity** = Yes, and its parent blueprint is the Microsoft Copilot Studio agent identity blueprint.
- Agents created before the Entra Agent ID rollout continue to use app registrations; see 3.3.2.

### 3.3.2 Migrate legacy Copilot Studio agents (optional, preview)
Performed by **Power Platform Administrator**. Power Platform inventory must be enabled for the tenant.

Existing agents that use an app-registration identity are being migrated automatically by Microsoft. Use this task only to migrate a PoC agent ahead of that. Migration converts the identity in place, the agent keeps its application (client) ID, and an agent can be reverted if it doesn't pass validation.

1. Open <https://admin.powerplatform.microsoft.com>.
2. In the left navigation pane, select **Actions** > **Recommendations**, then the **Active** tab.
3. Search for and select **Migrate Copilot Studio agents to Microsoft Entra Agent ID for enhanced agent governance**.
4. Expand **Why is this important?** and review the guidance.
5. Use **Suggested migration order** and **Migration notes** to select only the non-critical PoC agent(s).
6. Select **Migrate**, review the confirmation, and confirm.
7. Review the **Action**, **Action state**, and **Action date** columns (or the **Action history** tab).
8. With the agent's maker, confirm the agent responds in every channel where it's published and that its actions, connectors, and flows run, then repeat 3.3.1.

**Check result**
- The agent has gained a Microsoft Entra Agent ID that appears under **Entra ID** > **Agents** > **Agent identities**.
- If the agent doesn't pass validation, revert it with the Power Platform API rollback endpoint described in the migration article before you continue.

## 3.4 View and filter agent identities and blueprints
**Documentation:** [View and filter agent identities in your tenant](https://learn.microsoft.com/entra/agent-id/agent-lists) · [Manage agent identity blueprints in the Microsoft Entra admin center](https://learn.microsoft.com/entra/agent-id/manage-agent-blueprint) · [List agentIdentity objects (Microsoft Graph)](https://learn.microsoft.com/graph/api/agentidentity-list)

### 3.4.1 Review the agent identities list
Performed by **any Microsoft Entra user**.
1. Open <https://entra.microsoft.com> > **Entra ID** > **Agents** > **Agent identities**.
2. Search by **name** or **object ID**, or add the **Blueprint App ID** filter.
3. Select **Choose columns** and add: **Name**, **Created On**, **Status**, **Object ID**, **View Access**, **Blueprint App ID**, **Owners and Sponsors**, **Uses agent identity**.
4. Select a PoC agent identity and review its overview (name, description, status, link to the parent agent identity blueprint), its owners and sponsors, its access (granted permissions and Microsoft Entra roles), and its audit and sign-in logs.

| Column | Meaning |
|---|---|
| **Status** | Current operational state: **Active** or **Disabled** |
| **Blueprint App ID** | Identifier of the agent identity blueprint of this agent identity; blank for agents using service principals |
| **Owners and Sponsors** | Direct link to the owners and sponsors of the agent identity |
| **Uses agent identity** | **Yes** = agent identity object; **No** = service principal |
| **View Access** | Opens the agent's access pane on the **Permissions** tab |

**Check result**
- Every in-scope PoC agent is listed with **Status** = Active and **Uses agent identity** = Yes.

### 3.4.2 Review agent blueprints and linked agent identities
Performed by **any Microsoft Entra user**.
1. Go to **Entra ID** > **Agents** > **Agent blueprints**.
2. Search by name or object ID, or select **Add filters** > **Blueprint App ID**.
3. Note the **Agent identities** count for each PoC blueprint, then select the blueprint principal to open its management page.
4. Select **Linked agent identities** to list each child agent with **Name**, **Status**, **View Access**, and **Owners and Sponsors**.
5. Under **Access**, select **Granted permissions** and review the **Admin consent** and **User consent** tabs (**API name**, **Claim value**, **Permission**, **Type**, **Granted through**, **Granted by**).
6. Under **Access**, select **Owners and sponsors** and review the **Agent blueprint** and **Agent blueprint principal** tabs.

**Check result**
- Each PoC blueprint lists the expected child agent identities and has at least one sponsor.

### 3.4.3 List agent identities with Microsoft Graph (optional)
Performed by **Agent ID Administrator** in Graph Explorer, with delegated permission `AgentIdentity.Read.All`.

```http
GET https://graph.microsoft.com/v1.0/servicePrincipals/microsoft.graph.agentIdentity
```

**Check result**
- The response contains every PoC agent identity. For each, `agentIdentityBlueprintId` is the **appId** of its blueprint and `accountEnabled` is `true`.

## 3.5 Assign owners and sponsors
**Documentation:** [Add and manage owners and sponsors for agent identities and blueprints](https://learn.microsoft.com/entra/agent-id/manage-owners-sponsors-agents) · [Manage agents in end user experience](https://learn.microsoft.com/entra/agent-id/manage-agent-identities-end-user) · [Owners, sponsors, and managers](https://learn.microsoft.com/entra/agent-id/agent-owners-sponsors-managers)

PoC pattern: the technical builder is the **owner**; the business accountable person (or a supported group of accountable people) is the **sponsor**. For the sponsor continuity test, make **PoC Sponsor** a sponsor of the test agent.

### 3.5.1 Assign owners and sponsors to an agent identity
Performed by **Agent ID Administrator** or an existing **owner** of the agent identity.
1. Open <https://entra.microsoft.com> > **Entra ID** > **Agents** > **Agent identities**.
2. Select the agent identity.
3. Under **Access**, select **Owners and sponsors**.
4. Select **Add** > **Add owner** or **Add sponsor**.
5. Search for and select the users, and groups (for sponsors only), that you want to add.
6. Select **Add**.

To remove an entry, select the checkbox next to it and select **Remove**.

**Check result**
- The agent identity shows the expected owner and at least one sponsor.

### 3.5.2 Assign owners and sponsors to a blueprint
Performed by **Agent ID Administrator** or an existing **owner** of the agent identity blueprint.
1. Go to **Entra ID** > **Agents** > **Agent blueprints** and select the blueprint.
2. Under **Access**, select **Owners and sponsors**.
3. Select the **Agent blueprint** tab or the **Agent blueprint principal** tab.
4. Select **Add** > **Add owner** or **Add sponsor**, search for and select the users and groups (for sponsors only), and select **Add**.

**Check result**
- The selected tab lists the intended owners and sponsors.

### 3.5.3 Review owned and sponsored agents in My Account (self-service)
Performed by **PoC Sponsor** (any owner or sponsor of at least one agent identity).
1. Sign in to <https://myaccount.microsoft.com>.
2. If you haven't opted in to the new homepage yet, select **Use new version** in the banner.
3. In the left menu, select **Manage agents**. This menu item appears only for users who own or sponsor at least one agent identity.
4. Choose the **Agents you sponsor** or **Agents you own** tab and select an agent to view its details.

**Check result**
- PoC Sponsor sees the test agent under **Agents you sponsor**. The disable test is in 3.12.2.

## 3.6 Configure inheritable permissions on a blueprint (optional)
**Documentation:** [Inheritable permissions and required resource access](https://learn.microsoft.com/entra/agent-id/concept-inheritable-permissions) · [Configure inheritable permissions for agent identity blueprints](https://learn.microsoft.com/entra/agent-id/configure-inheritable-permissions-blueprints) · [Create inheritablePermission (Microsoft Graph)](https://learn.microsoft.com/graph/api/agentidentityblueprint-post-inheritablepermissions)

Inheritable permissions let agent identities created from a blueprint automatically inherit permissions from their parent blueprint, without interactive consent prompts. A permission is inherited only when **both** conditions are met:
- The resource scopes, roles, or both are listed in the inheritable permissions configuration on the agent identity blueprint.
- The permission is granted to the blueprint (static consent through required resource access, or dynamic consent with the permissions explicitly requested).

Inheritance patterns for delegated scopes (`inheritableScopes`):

| Pattern | `@odata.type` | Description |
|---|---|---|
| Enumerated scopes | `microsoft.graph.enumeratedScopes` | Inherit only the listed scopes. Provides fine-grained control and supports gradual permission expansion. |
| All allowed scopes | `microsoft.graph.allAllowedScopes` | Inherit all available delegated scopes for the resource app. Newly granted scopes on the blueprint principal are automatically included. |
| None | `microsoft.graph.noScopes` | Inherit no scopes for the resource app. |

Rules and limits:
- Maximum of 50 resource apps per agent identity blueprint.
- Enumerated `scopes` must be a non-empty list of unique scope identifiers and must not include globally blocked scopes.
- Inherited permissions aren't visible as permissions on agent identities in the Microsoft Entra admin center or through Microsoft Graph. They're only observable in the token: inherited scopes in the `scp` claim, inherited roles in the `roles` claim.
- Regularly review inherited scopes and roles, and remove unused permissions from both the blueprint principal and the inheritable permissions list.

Inheritable permissions are configured with Microsoft Graph through the `inheritablePermissions` navigation property on the `agentIdentityBlueprint` application resource. In the requests below, `{id}` is the `id` of the agent identity blueprint application.

### 3.6.1 Review current inheritable permissions
Performed by **Agent ID Developer** (blueprint owner) or **Agent ID Administrator**, with delegated permission `AgentIdentityBlueprint.Read.All`.

```http
GET https://graph.microsoft.com/v1.0/applications/{id}/microsoft.graph.agentIdentityBlueprint/inheritablePermissions
```

**Check result**
- You have a baseline list of `resourceAppId` entries and patterns to record as evidence before changing anything.

### 3.6.2 Add an enumerated-scopes entry for Microsoft Graph
Performed by **Agent ID Developer** (blueprint owner) or **Agent ID Administrator**, with delegated permission `AgentIdentityBlueprint.Create`.

```http
POST https://graph.microsoft.com/v1.0/applications/{id}/microsoft.graph.agentIdentityBlueprint/inheritablePermissions
Content-Type: application/json

{
  "resourceAppId": "00000003-0000-0000-c000-000000000000",
  "inheritableScopes": {
    "@odata.type": "microsoft.graph.enumeratedScopes",
    "scopes": [
      "User.Read",
      "Mail.Read"
    ]
  }
}
```

`00000003-0000-0000-c000-000000000000` is Microsoft Graph. Replace the scopes with the minimum your PoC agent needs. The inheritable permissions configuration doesn't grant access by itself; the permission must also be granted to the blueprint principal.

**Check result**
- The request returns `201 Created` with the new **inheritablePermission** object.

### 3.6.3 Update or remove an entry
Performed by **Agent ID Developer** (blueprint owner) or **Agent ID Administrator**, with delegated permission `AgentIdentityBlueprint.ReadWrite.All`.
- If an entry already exists for a `resourceAppId`, update it with `PATCH` on `.../inheritablePermissions/{resourceAppId}` instead of creating a duplicate, which results in `409 Conflict`.
- To remove inheritance for a resource app:

```http
DELETE https://graph.microsoft.com/v1.0/applications/{id}/microsoft.graph.agentIdentityBlueprint/inheritablePermissions/00000003-0000-0000-c000-000000000000
```

**Check result**
- `DELETE` returns `204 No Content`, and the entry no longer appears in 3.6.1.

## 3.7 Tag agents with custom security attributes (optional)
**Documentation:** [Custom security attributes overview](https://learn.microsoft.com/entra/fundamentals/custom-security-attributes-overview) · [Add or deactivate custom security attribute definitions](https://learn.microsoft.com/entra/fundamentals/custom-security-attributes-add) · [Update agentIdentity (Microsoft Graph)](https://learn.microsoft.com/graph/api/agentidentity-update) · [List agentIdentity objects (Microsoft Graph)](https://learn.microsoft.com/graph/api/agentidentity-list) · [Manage custom security attributes for an application](https://learn.microsoft.com/entra/identity/enterprise-apps/custom-security-attributes-apps)

Custom security attributes let you categorize agent identities with business-specific labels, and Conditional Access policies can target those attributes ([Chapter 6 – Conditional Access and Least Privilege](../chapter-06-conditional-access/README.md)).

Plan before you create: attribute set names and attribute names can't be renamed, attribute sets can't be deleted, and attribute definitions can only be deactivated, not deleted.

### 3.7.1 Create the AgentGovernance attribute set and attributes
Performed by **Attribute Definition Administrator**.
1. Open <https://entra.microsoft.com> > **Entra ID** > **Custom security attributes**.
2. Select **Add attribute set**, enter the name `AgentGovernance`, a description, and the maximum number of attributes, then select **Add**.
3. Open `AgentGovernance` and select **Add attribute** for each attribute below. Set **Data type** = String, **Allow multiple values to be assigned** = No, **Only allow predefined values to be assigned** = Yes, select **Add value** for each predefined value, and select **Save**.

| Attribute | Predefined values | Purpose |
|---|---|---|
| `Project` | `Agent365PoC` | One filter returns every PoC agent. |
| `Environment` | `Pilot`, `Prod` | Distinguishes PoC agents from production agents. |

**Check result**
- `AgentGovernance` lists `Project` and `Environment` with their predefined values.

### 3.7.2 Assign attribute values to PoC agent identities
Performed by **Attribute Assignment Administrator**, with delegated permissions `CustomSecAttributeAssignment.ReadWrite.All` and `AgentIdentity.ReadWrite.All`.

Repeat for each PoC agent identity (`{id}` = agent identity object ID):

```http
PATCH https://graph.microsoft.com/v1.0/servicePrincipals/{id}/microsoft.graph.agentIdentity
Content-Type: application/json

{
  "customSecurityAttributes": {
    "AgentGovernance": {
      "@odata.type": "#Microsoft.DirectoryServices.CustomSecurityAttributeValue",
      "Project": "Agent365PoC",
      "Environment": "Pilot"
    }
  }
}
```

**Check result**
- Each request returns `204 No Content`.

### 3.7.3 Filter agents by attribute
Performed by **Agent ID Administrator** together with **Attribute Assignment Reader**, with delegated permissions `AgentIdentity.Read.All` and `CustomSecAttributeAssignment.Read.All`.

```http
GET https://graph.microsoft.com/v1.0/servicePrincipals/microsoft.graph.agentIdentity?$count=true&$select=id,displayName,customSecurityAttributes&$filter=customSecurityAttributes/AgentGovernance/Project eq 'Agent365PoC'
ConsistencyLevel: eventual
```

The filter value is case sensitive. Include `ConsistencyLevel: eventual` and `$count=true`.

**Check result**
- The result contains every PoC agent identity.

## 3.8 Monitor agent sign-ins and audit events
**Documentation:** [Microsoft Entra Agent ID logs](https://learn.microsoft.com/entra/agent-id/sign-in-audit-logs-agents) · [List directoryAudits (Microsoft Graph)](https://learn.microsoft.com/graph/api/directoryaudit-list?view=graph-rest-beta)

### 3.8.1 Review agent sign-in logs
Performed by **Reports Reader**.
1. Have the standard test user exercise the PoC agent with a few prompts.
2. Open <https://entra.microsoft.com> > **Entra ID** > **Monitoring & health** > **Sign-in logs**.
3. Filter by **Agent type** (**Agent ID user**, **Agent Identity**, **Agent Identity Blueprint**, or **Not Agentic**) and **Is Agent** (**No** or **Yes**).
4. Because agents can sign in with either user-delegated or app-only permissions, check each of the sign-in log types.

**Check result**
- With **Is Agent** = Yes, sign-ins for the PoC agents are listed.

### 3.8.2 Review audit logs for agent changes
Performed by **Reports Reader**.

Agent activity is logged under the base identity type from which it originates:

| Agent action | Audit activity | `agentType` value |
|---|---|---|
| Create an agent identity blueprint | Add application | `agenticApp` |
| Update an agent identity blueprint | Update application | `agenticApp` |
| Delete an agent identity blueprint | Delete application | `agenticApp` |
| Create an agent identity | Add service principal | `agenticAppInstance` |
| Update an agent identity | Update service principal | `agenticAppInstance` |
| Delete an agent identity | Delete service principal | `agenticAppInstance` |
| Create an agent's user account | Add user | `agentIDuser` |

The blueprint principal uses `agentIdentityBlueprintPrincipal`, and `notAgentic` means the identity isn't an agent. The `agentType` property appears on the `initiatedBy`, `performedBy`, and `targetResources` fields; `blueprintId` correlates an agent identity back to its blueprint.

1. Open a PoC agent identity (3.4.1) and review its audit logs, or go to **Entra ID** > **Monitoring & health** > **Audit logs**.
2. Review the events for the PoC agent identities.

**Check result**
- Audit events for the PoC agent identities are listed.

### 3.8.3 Query agent logs with Microsoft Graph (optional)
Performed by **Reports Reader**, with delegated permission `AuditLog.Read.All`, on the beta endpoint.

Agent identity sign-ins:

```http
GET https://graph.microsoft.com/beta/auditLogs/signIns?$filter=signInEventTypes/any(t: t eq 'servicePrincipal') and agent/agentType eq 'agenticAppInstance'
```

Audit events (inspect `agentType` and `blueprintId` on `initiatedBy` and `targetResources`):

```http
GET https://graph.microsoft.com/beta/auditLogs/directoryAudits
Prefer: include-unknown-enum-members
```

The `Prefer: include-unknown-enum-members` header is required to receive the `agentIdentityBlueprintPrincipal` and `agentIDuser` values.

**Check result**
- The sign-in query returns records for the PoC agent identities, and the audit query returns events with an `agentType` other than `notAgentic`.

## 3.9 Detect and respond with ID Protection
**Documentation:** [ID Protection for agents](https://learn.microsoft.com/entra/id-protection/concept-risky-agents) · [riskyAgent resource type (Microsoft Graph beta)](https://learn.microsoft.com/graph/api/resources/riskyagent?view=graph-rest-beta) · [Manage agent identities in your organization](https://learn.microsoft.com/entra/agent-id/manage-agent-identities-admin)

ID Protection detects identity-based risks on agents that have agent identities. All risk detections for risky agents are offline. In on-behalf-of flows, risky activity is attributed to the **user** rather than the agent. **Learning Mode** suppresses behavioral alerts for agents that lack sufficient activity history; a separate detection runs in parallel to catch malicious early-life behavior.

| Agent risk detection | `riskEventType` |
|---|---|
| Confirmed compromised | `adminConfirmedAgentCompromised` |
| Early life malicious activity | `earlyLifeMaliciousActivity` |
| Entra Directory Reconnaissance | `entraDirectoryReconnaissance` |
| Failed access attempt | `failedAccessAttempt` |
| Microsoft Entra threat intelligence | `threatIntelligenceAccount` |
| Sign-in spike | `signInSpike` |
| Suspicious credential usage | `suspiciousCredentialUsage` |
| Unfamiliar resource access | `unfamiliarResourceAccess` |

Blocking risky agents with a Conditional Access policy on agent risk is configured in [Chapter 6 – Conditional Access and Least Privilege](../chapter-06-conditional-access/README.md).

### 3.9.1 Review the Risky agents report
Performed by **Security Reader**.
1. Open <https://entra.microsoft.com> > **ID Protection** > **Dashboard** and select **View risky agents** (or open the **Risky Agents** report from the ID Protection navigation menu).
2. Filter and sort by agent, risk state, or risk level. Select an entry to view the agent display name and ID, risk state and risk level, agent type and sponsors, and the corresponding risk detections.
3. Open the **Risk Detections** report and select the **Agent detections** tab to view detection events from up to the past 90 days.

**Check result**
- The reviewer can open the **Risky Agents** report and the **Agent detections** tab.

### 3.9.2 Respond to a risky agent
Performed by **Security Administrator** (Microsoft Graph, permission `IdentityRiskyAgent.ReadWrite.All`). The same actions are available directly from the **Risky Agents** report and the risky agent details view.

| Action | Effect | Graph (beta) |
|---|---|---|
| **Confirm compromise** | Sets the risk level to **High** and creates an event in the agent's risk detections. Triggers risk-based Conditional Access policies configured to block access on High agent risk. | `POST /identityProtection/riskyAgents/confirmCompromised` |
| **Confirm safe** | Clears active risk by setting the risk level to **None**; use for a false positive so the system avoids flagging similar activity. | `POST /identityProtection/riskyAgents/confirmSafe` |
| **Dismiss risk** | Marks the detected risk as no longer relevant, or a benign true positive where the system should continue to flag similar activity. | `POST /identityProtection/riskyAgents/dismiss` |
| **Disable** | Prevents all sign-ins for that agent across Microsoft Entra ID and connected apps. | — |

The `confirmCompromised` and `confirmSafe` requests take a body of `{"agentIds": ["<agent object ID>"]}`.

Incident sequence:
1. **Detect** – review the Risky Agents report (3.9.1).
2. **Respond** – **Confirm compromise** and/or **Disable** the agent.
3. **Investigate** – review the risk detection details together with the agent's sign-in and audit logs (3.8). The agent's sponsor can determine whether the agent behavior is expected.
4. **Recover** – false positive: dismiss the risk and re-enable the agent. True compromise: rotate credentials before re-enabling, or retire the agent identity (see [Chapter 5 – Agent Lifecycle and Audit](../chapter-05-lifecycle-audit/README.md)).

Risk data can also be exported through diagnostic settings in Microsoft Entra ID to a Log Analytics workspace, a storage account, an event hub, or a SIEM solution.

## 3.10 Keep sponsorship continuous with Lifecycle Workflows
**Documentation:** [Agent identity sponsor tasks in Lifecycle Workflows](https://learn.microsoft.com/entra/id-governance/agent-sponsor-tasks) · [Lifecycle Workflows templates](https://learn.microsoft.com/entra/id-governance/lifecycle-workflow-templates) · [Lifecycle Workflows tasks](https://learn.microsoft.com/entra/id-governance/lifecycle-workflow-tasks) · [Run a workflow on-demand](https://learn.microsoft.com/entra/id-governance/on-demand-workflow) · [Check status of a workflow](https://learn.microsoft.com/entra/id-governance/check-status-workflow)

If a sponsor leaves the organization, Microsoft Entra ID automatically reassigns sponsorship to the sponsor's manager. Lifecycle Workflows adds sponsor tasks that keep sponsorship continuous when a sponsor changes roles or leaves.

Built-in templates:

| Template | Category | Default tasks |
|---|---|---|
| **Agent sponsor job profile change** | Mover | Send email to manager about sponsorship changes · Transfer agent sponsorships to manager · Remove all access package assignments for user |
| **Offboard agent sponsors** | Leaver | Send email to manager about sponsorship changes · Send email to co-sponsors about sponsor changes · Transfer agent sponsorships to manager |

Sponsor tasks (mover and leaver tasks; available only under mover or leaver workflow templates):

| Task | What it does |
|---|---|
| **Send email to manager about sponsorship changes** | Notifies the manager of a user who moved or left that the user sponsored one or more agent IDs, so the manager can decide whether another employee should become sponsor. |
| **Send email to co-sponsors about sponsor changes** | Notifies co-sponsors of the agent ID about the sponsorship change. |
| **Transfer agent sponsorships to manager** | Retrieves the user's manager, adds the manager as sponsor of each agent identity the user sponsors, and removes the user as sponsor. Requires a populated manager attribute. |

### 3.10.1 Create the sponsor transition workflow
Performed by **Lifecycle Workflows Administrator**.
1. Open <https://entra.microsoft.com> > **ID Governance** > **Lifecycle workflows** > **Workflows**.
2. Create a new workflow based on the template **Agent sponsor job profile change**.
3. On the **Basics** tab, enter a unique display name (for example `PoC – Agent sponsor mover`) and description, select your trigger, and select **Next**.
4. On the **Configure scope** screen, select a scope that includes only the PoC test users, and select **Next**.
5. On the **Tasks** page, keep **Send email to manager about sponsorship changes** and **Transfer agent sponsorships to manager**. The template also includes **Remove all access package assignments for user**; disable it if the PoC sponsor must keep their access packages. Select **Next**.
6. Review the workflow and select **Create**.

To be run on demand, the workflow must be enabled.

**Check result**
- The workflow appears in the workflows list with the sponsor tasks enabled.

### 3.10.2 Run the workflow on demand
Performed by **Lifecycle Workflows Administrator**. Prerequisite: **PoC Sponsor** is a sponsor of the test agent (3.5.1) and has **PoC Sponsor Manager** as manager.
1. Select the workflow and select **Run on demand**.
2. On the **select users** tab, select **add users**, select **PoC Sponsor**, and select **Add**.
3. Confirm your choices and select **Run workflow**. An on-demand run doesn't take into account whether the user meets the workflow's execution conditions.
4. On the workflow overview screen, select **Workflow history** and review the user and task results.

**Check result**
- The tasks completed successfully for PoC Sponsor (see 3.12.4 for the full test).

## 3.11 Disable or restrict agents at the right scope
**Documentation:** [Disable agent identities in your tenant](https://learn.microsoft.com/entra/agent-id/disable-agent-identities) · [Manage agent identities in your organization](https://learn.microsoft.com/entra/agent-id/manage-agent-identities-admin) · [Manage agents in end user experience](https://learn.microsoft.com/entra/agent-id/manage-agent-identities-end-user)

| Scope | Effect | Where |
|---|---|---|
| **Individual agent identity** | Blocks its access and token issuance; the agent identity and its metadata stay in the tenant. | Admin center (administrators; the **All agent identities** page supports multi-select disable) or My Account portal (owners and sponsors) |
| **Blueprint** | Prevents new agent identities from being created from that blueprint and blocks existing ones. | Blueprint management page > **Disable** |
| **Tenant-wide** | Conditional Access policies block authentication of all agent identities, agents' user accounts, or users signing into agents; creation of agent identities can optionally be blocked through product-specific controls. | Conditional Access ([Chapter 6](../chapter-06-conditional-access/README.md)) |

Re-enabling a disabled agent identity at any scope restores access and token issuance.

Cautions:
- All Copilot Studio agent identities are children of the Microsoft Copilot Studio agent identity blueprint, so disabling that blueprint affects all of them.
- Globally disabling agent identities can cause existing agents to fail, degrade Microsoft product experiences, and push teams to use less transparent application or service principal identities. Evaluate the impact before enforcing. For a partial approach, use Conditional Access policies to block specific agents, and run policies in report-only mode first.

### 3.11.1 Disable and re-enable an individual agent identity
Performed by **Agent ID Administrator** (or the agent's owner).
1. Go to **Entra ID** > **Agents** > **Agent identities**.
2. Select the test agent identity, then select **Disable**.
3. After the test, enable the agent identity again from its overview.

**Check result**
- **Status** shows **Disabled**, then **Active** after re-enabling.

### 3.11.2 Disable a blueprint (only for a blueprint dedicated to the PoC)
Performed by **Agent ID Administrator**.
1. Go to **Entra ID** > **Agents** > **Agent blueprints** and select a blueprint used only by PoC test agents (for example one created in Chapter 2).
2. Select **Disable** in the command bar of the blueprint's overview page. The confirmation dialog warns that existing agent identities created from this blueprint will no longer be able to authenticate. Confirm the action.
3. Re-enable the blueprint after the test.

**Check result**
- The blueprint **Status** is **Disabled**, and returns to **Active** after re-enabling.

## 3.12 Test and validation

### 3.12.1 Test identity and ownership coverage
Performed by **reviewer** (any Microsoft Entra user).
1. Open **Entra ID** > **Agents** > **Agent identities** with the columns from 3.4.1.
2. For each in-scope PoC agent, open **Owners and Sponsors**.
3. (Optional) Run the custom security attribute filter in 3.7.3 (requires the roles listed there).

**Expected result**
- Every in-scope agent has an agent identity linked to the expected blueprint, **Status** = Active, at least one sponsor, and the intended owner.
- (Optional) The attribute filter returns every PoC agent identity.

### 3.12.2 Test sponsor self-service disable
Performed by **PoC Sponsor**, then **the agent owner** or **Agent ID Administrator**.
1. As PoC Sponsor, open <https://myaccount.microsoft.com> > **Manage agents** > **Agents you sponsor** and select the test agent.
2. Select **Disable agent**.
3. Confirm that PoC Sponsor can't re-enable the agent.
4. As the owner, select the agent in My Account and choose **Enable agent** (or, as Agent ID Administrator, re-enable it as in 3.11.1).

**Expected result**
- After step 2, the agent is disabled with the same effect as disabling it from the admin center: users can't access it and it isn't issued tokens. **Status** shows **Disabled** in the Entra admin center.
- The sponsor can't re-enable the agent; the owner or admin can, and **Status** returns to **Active**.

### 3.12.3 Test risk response
Performed by **Security Administrator** (Graph Explorer, beta, `IdentityRiskyAgent.ReadWrite.All`), then **Security Reader**.
1. Confirm the test agent as compromised:

```http
POST https://graph.microsoft.com/beta/identityProtection/riskyAgents/confirmCompromised
Content-Type: application/json

{
  "agentIds": ["<test agent identity object ID>"]
}
```

2. As Security Reader, open the **Risky Agents** report and the **Agent detections** tab (3.9.1).
3. If the Chapter 6 risk-based Conditional Access policy is enabled, run the Chapter 6 block test now.
4. As Security Administrator, confirm the agent as safe:

```http
POST https://graph.microsoft.com/beta/identityProtection/riskyAgents/confirmSafe
Content-Type: application/json

{
  "agentIds": ["<test agent identity object ID>"]
}
```

**Expected result**
- After step 1, the test agent is listed in the **Risky Agents** report with risk level **High**, and a **Confirmed compromised** detection exists for the agent.
- After step 4, the risk level is **None**.

### 3.12.4 Test sponsor continuity
Performed by **Lifecycle Workflows Administrator**, then **reviewer**.
1. Confirm PoC Sponsor is a sponsor of the test agent and PoC Sponsor Manager is not.
2. Run the workflow on demand for PoC Sponsor (3.10.2).
3. Open **Workflow history** and select the total tasks for PoC Sponsor.
4. Open the test agent > **Owners and sponsors**.
5. Check the PoC Sponsor Manager mailbox (and any co-sponsor mailboxes).

**Expected result**
- The workflow history shows the sponsor tasks completed for PoC Sponsor.
- PoC Sponsor Manager is now a sponsor of the test agent, and PoC Sponsor is no longer a sponsor.
- PoC Sponsor Manager received the sponsorship change email; co-sponsors (if any) received the co-sponsor email.

## 3.13 Evidence
- Export or screenshot of **Agent identities** with columns **Name**, **Status**, **Object ID**, **Blueprint App ID**, **Owners and Sponsors**, **Uses agent identity** for all PoC agents.
- Screenshot of one PoC blueprint showing **Linked agent identities**, **Granted permissions**, and **Owners and sponsors**.
- Copilot Studio **Settings** > **Advanced** > **Metadata** showing the **Entra Agent ID** of a PoC agent (and the Power Platform admin center **Action history** if you migrated an agent).
- Screenshot of PoC Sponsor's My Account **Manage agents** page and the test agent in **Disabled** status after step 2 of 3.12.2.
- (Optional) Graph responses for inheritable permissions before and after 3.6.2.
- (Optional) Graph response of the attribute filter in 3.7.3.
- Sign-in log export filtered by **Is Agent** = Yes, and audit log entries for the PoC agent identities.
- Screenshot of the **Risky Agents** report showing the test agent at **High**, then **None** after confirm safe.
- Lifecycle workflow **Workflow history** for PoC Sponsor, the agent's sponsors list after the run, and the manager notification email.

## 3.14 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| A Copilot Studio agent isn't listed in **Agent identities** as an agent identity, or shows **Uses agent identity** = No | Agent was created before the Entra Agent ID rollout and still uses an app registration | Migrate it (3.3.2) or wait for the automatic migration by Microsoft. |
| **Blueprint App ID** is blank | The agent uses a service principal, not an agent identity | Expected for agents without agent identities; see 3.3 or Chapter 2. |
| Can't add a group as owner | Groups aren't supported as owners | Add users or service principals as owners; use a supported group as sponsor. |
| Can't add a security group as sponsor | Role-assignable groups and assigned membership security groups aren't allowed | Use a dynamic membership group or an assigned membership Microsoft 365 group. |
| Members of a dynamic group sponsor can't act as sponsors | Up to 24 hours after a rule or user-property change before sponsorship authorization succeeds | Wait and retry. |
| **Manage agents** missing in My Account | User doesn't own or sponsor any agent identity, or hasn't opted in to the new homepage | Add the user as owner or sponsor (3.5.1); select **Use new version**. |
| Sponsor can't re-enable an agent | Sponsors can't re-enable agents | Ask an owner or admin to re-enable it. |
| Inheritable permission `POST` returns `409 Conflict` | An entry for that `resourceAppId` already exists | Use `PATCH` on `.../inheritablePermissions/{resourceAppId}`. |
| Inheritable permission request returns `400 Bad Request` | `resourceAppId` isn't a valid GUID | Correct the GUID. |
| Inherited scope isn't visible on the agent identity | Inherited permissions are only observable in the token | Check the token `scp`/`roles` claims; confirm the resource app is listed as inheritable and the permission is granted to the blueprint. |
| **Add attribute set** is disabled | Attribute Definition Administrator isn't assigned (Global Administrator doesn't include it) | Assign Attribute Definition Administrator. |
| Attribute filter returns no results | Missing `ConsistencyLevel: eventual` or `$count=true`, or the value case doesn't match | Fix the request. |
| No agent entries in sign-in logs | Agent sign-ins can appear across each of the four sign-in log types | Use the **Agent type** / **Is Agent** filters and check every sign-in log type. |
| **Risky Agents** is empty | No offline detections yet, Learning Mode, or risk attributed to the user in on-behalf-of flows | Use 3.12.3 for a controlled test. |
| `riskyAgents` actions fail in Graph Explorer | Signed-in user isn't Security Administrator, or `IdentityRiskyAgent.ReadWrite.All` isn't consented | Assign the role and consent the permission. |
| Sponsor tasks aren't selectable when building a workflow | Sponsor tasks are available only under mover or leaver templates | Use a mover or leaver template (3.10). |
| **Transfer agent sponsorships to manager** doesn't transfer sponsorship | User's manager attribute isn't populated | Set the manager and run the workflow on demand again. |
| Workflow can't be run on demand | Workflow isn't enabled | Enable the workflow. |

## 3.15 Cleanup
- Re-enable every agent identity and blueprint disabled during testing (owner or Agent ID Administrator).
- Make sure the test agent's risk is cleared (confirm safe or dismiss risk).
- Restore sponsors changed by the Lifecycle Workflows test: add PoC Sponsor back if needed and remove PoC Sponsor Manager if they shouldn't remain sponsor (3.5.1).
- Delete the PoC Lifecycle workflow: **ID Governance** > **Lifecycle workflows** > **Workflows** > select the workflow > **Delete**, then confirm with **Delete** (Lifecycle Workflows Administrator). Deleted workflows are permanently removed after 30 days.
- Remove inheritable permission entries added only for the PoC (`DELETE`, 3.6.3) and remove the related permission grants from the blueprint principal.
- Remove attribute values from PoC agent identities by setting them to `null` (keep them if Chapter 6 attribute-based policies still use them):

```http
PATCH https://graph.microsoft.com/v1.0/servicePrincipals/{id}/microsoft.graph.agentIdentity
Content-Type: application/json

{
  "customSecurityAttributes": {
    "AgentGovernance": {
      "@odata.type": "#Microsoft.DirectoryServices.CustomSecurityAttributeValue",
      "Project": null,
      "Environment": null
    }
  }
}
```

- Optionally deactivate the `Project` and `Environment` attribute definitions. Attribute definitions can't be deleted, only deactivated, and the `AgentGovernance` attribute set can't be deleted or renamed.
- If you migrated a Copilot Studio agent only for the PoC and it failed validation, revert it (3.3.2).
- Remove the setup role assignments made for this chapter.

---
Previous: [Chapter 2 – Third-Party and Custom Agents](../chapter-02-third-party-custom-agents/README.md) · Next: [Chapter 4 – Tools and MCP Server Governance](../chapter-04-tools-mcp-governance/README.md)
