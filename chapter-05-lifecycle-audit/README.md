# Chapter 5 – Agent Lifecycle and Audit

**Pillar:** Govern
**What it proves:** IT can govern agents through their lifecycle from the Agent Registry in the Microsoft 365 admin center (install, activate, block, manage ownership, connect, delete, and restore) and can review the resulting records in Microsoft Purview Audit, Microsoft Entra logs, and Microsoft Defender Advanced Hunting.

**Success criteria**
- The test agent is installed for `A365-PoC-Users` and is ready to use for the standard test user without a manual install.
- After **Block**, the standard test user can't use the test agent. After **Unblock**, the standard test user can use it again.
- **Assign new owner** transfers the test agent to a new owner, and the previous owner loses all access.
- Each agent under **Agents without owners** has been reassigned, blocked, or deleted.
- The test agent is deleted, restored from the **Deleted** view with its previous configuration, and then permanently deleted.
- Microsoft Purview Audit returns the soft-delete, restore, and permanent-delete records for the test agent.
- `AgentsInfo` in Defender Advanced Hunting returns `LifecycleStatus` values `Blocked` and `Deleted` for the test agent after the corresponding steps.

## 5.1 Required permissions

Grant the read-only roles to reviewers first, grant the setup roles only to the person who performs each change, and assign all roles as Active for the PoC window. Chapter 0 assigns these roles to the test admin and the reviewer in [0.4.3 Assign the roles](../chapter-00-prerequisites/README.md#043-assign-the-roles).

| Task | Least-privilege role | Section |
|---|---|---|
| Install, uninstall, and activate agents; approve activation requests | **AI Administrator** | 5.2, 5.10 |
| Block and unblock agents | **AI Administrator** | 5.3, 5.10 |
| Start or stop a Microsoft Foundry agent | **AI Administrator** plus the **Azure AI Owner** role | 5.3 |
| Disable and enable an agent identity in Microsoft Entra (optional) | **Agent ID Administrator** | 5.3 |
| Assign a new owner, add or remove owners | **AI Administrator** | 5.4, 5.10 |
| Act on ownerless agents; create and run Agent management rules | **AI Administrator** | 5.5 |
| Connect or remove connected agents | **AI Administrator** | 5.6 |
| Block, unblock, and delete agent instances | **AI Administrator** | 5.7 |
| Delete, restore, and permanently delete agents | **AI Administrator** | 5.8, 5.10 |
| Search and export the Microsoft Purview audit log | **Audit Reader** role group in Microsoft Purview | 5.9, 5.10 |
| Review Microsoft Entra audit and sign-in logs | **Reports Reader** | 5.9, 5.10 |
| Run Advanced Hunting queries on `AgentsInfo` and `CloudAppEvents` | **Security Reader** | 5.9, 5.10 |
| Validation / read-only review of the Agent Registry, ownerless agents, connected agents, and instances | **AI Reader** or **Global Reader** | 5.5, 5.6, 5.7, 5.10 |

In the Microsoft 365 admin center, only **AI Administrator** and **Global Administrator** can install, modify, approve, and manage agent configurations. AI Reader and Global Reader have read-only access to tools and settings. Global Administrator is a highly privileged role; use AI Administrator for the changes in this chapter.

**Before you start:**
- Complete [Chapter 0 – Prerequisites and PoC preparation](../chapter-00-prerequisites/README.md): the test admin, the standard test user, the reviewer, and the group `A365-PoC-Users` exist ([0.4](../chapter-00-prerequisites/README.md#04-prepare-accounts-groups-and-role-assignments)), and Microsoft Purview Audit is turned on ([0.5](../chapter-00-prerequisites/README.md#05-turn-on-microsoft-purview-audit)).
- Complete [Chapter 1 – Agent Discovery and Inventory](../chapter-01-agent-discovery/README.md) so the test agents are visible in **Agents** > **All agents** > **Registry**.
- Review [Chapter 3 – Agent Identity and Ownership](../chapter-03-identity-ownership/README.md) for owners and sponsors in Microsoft Entra. This chapter covers ownership as managed in the Microsoft 365 admin center.
- Complete [8.2 Enable Security for AI](../chapter-08-threat-detection/README.md#82-enable-security-for-ai) and [8.3 Connect the Microsoft 365 connector](../chapter-08-threat-detection/README.md#83-connect-the-microsoft-365-connector) before you run the Advanced Hunting tasks in 5.9.4.
- As the maker, create the lifecycle test agent `PoC-Lifecycle-Agent`: a shared Agent Builder or Copilot Studio agent that you're allowed to delete permanently. **Assign new owner** is only available for shared Agent Builder and Copilot Studio agents. The maker is the agent's first owner; the standard test user becomes the new owner in 5.10.6.
- For 5.4.2 and 5.4.3, use an Agent Builder agent, because Agent Builder agents support multiple owners. If `PoC-Lifecycle-Agent` isn't an Agent Builder agent, create a separate one with [Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/agent-builder).
- For the optional 5.3.2, use the Microsoft Foundry test agent from [1.2.2 Create and publish a Foundry test agent](../chapter-01-agent-discovery/README.md#122-create-and-publish-a-foundry-test-agent).
- Note the PoC start time in UTC. The audit searches in 5.9 and 5.10 start from this time.

## 5.2 Install and activate agents

**Documentation:** [Governance and lifecycle actions for agents – Install agents and Activate agents](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions) · [Agent requests in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-requests) · [Policy templates](https://learn.microsoft.com/microsoft-agent-365/admin/policy-template)

Installing an agent makes it ready to use for the selected users without manual installation by end users. It affects the agent's availability and functionality in Copilot and in other host products, such as Outlook, Teams, or Microsoft 365. Activation is a governance step for new agents: when a user requests activation so they can create instances of an agent, the request requires AI admin approval before the requester can create instances.

### 5.2.1 Install an agent for users or groups

Performed by **AI Administrator**.

1. Sign in to the Microsoft 365 admin center at `https://admin.cloud.microsoft`.
2. Go to **Agents** > **All agents**, and make sure **Registry** is selected.
3. Select the **Status** filter, and then select **Available**.
4. Select an agent that isn't already installed, for example `PoC-Lifecycle-Agent`.
5. In the agent details pane, immediately under the agent's name, select **Install**.
6. In the **Deploy agent to selected users** pane, choose to install the agent for all users or for specific users or groups. For the PoC, select `A365-PoC-Users`. Select **Next**.
7. In the **Review permissions** pane, review the permissions requested for the agent. If they're acceptable, select **Grant admin consent**.
8. In the **Permissions requested** window, select **Accept**, and then select **Next**.
9. In the **Review & finish** pane, select **Finish deployment**.

**Check result**
- The agent is ready to use for the members of `A365-PoC-Users` without manual installation.

### 5.2.2 Uninstall an agent

Performed by **AI Administrator**.

Run this task only on an agent that you installed for the PoC.

1. Go to **Agents** > **All agents** > **Registry**, select the **Status** filter, and then select **Available**.
2. Select the installed agent.
3. In the agent details pane, immediately under the agent's name, select **Uninstall**. If you don't see **Uninstall**, the selected agent might not be installed.
4. In the **Remove agent** pane, select **Remove agent**, and then select **Uninstall Agent**.

**Check result**
- The agent is no longer installed for the users it was removed from.

### 5.2.3 Review and approve an activation request

Performed by **AI Administrator**.

Run this task only if an activation request is pending in **Requests**.

1. Go to **Agents** > **All agents** > **Requests**.
2. Filter **State** to **Pending activate**. New submissions appear with the status **Allow activation**, with the agent name, publisher name, status, and date requested.
3. Select the pending agent and review its description, capabilities, connected data sources, and tools.
4. Select the **Request** tab to open the request wizard.
5. Select the users and security groups that you approve for activating the agent. You can include the original requesters.
6. Apply a template:
   - **Default template** – Microsoft's template with essential security and compliance controls from Microsoft Entra, Microsoft Purview, and SharePoint.
   - **Custom template** – a template you create to apply extra policies, such as restricting external content sharing. See [Policy templates](https://learn.microsoft.com/microsoft-agent-365/admin/policy-template).
7. Review the permissions requested by the agent, and grant admin consent if appropriate.
8. Review all configurations, and then select **Finish**.

AI Administrators aren't authorized to configure Conditional Access policies or Microsoft Entra access package policies. These actions require a highly privileged administrator role with the appropriate Microsoft Graph permissions.

**Check result**
- The agent becomes available for creating instances in the Teams app store, Microsoft 365 Copilot, and Copilot Studio, and the requester is notified.
- For future user additions, you only approve or reject requests by using the existing template, without repeating the full activation steps.

### 5.2.4 Activate an agent without a request (admin-initiated)

Performed by **AI Administrator**.

Administrators can proactively activate an agent through the Agent Registry without waiting for an activation request. Run this task only if your registry contains an agent that users create instances from.

1. Go to **Agents** > **All agents** > **Registry** and select the agent.
2. Activate the agent, and make it available to all users, specific users, or specific security groups.

**Check result**
- The agent is activated for the selected audience without a pending request.

## 5.3 Control agent availability

**Documentation:** [Governance and lifecycle actions for agents – Block or unblock agents and Start or stop a Foundry agent](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions) · [Disable agent identities in your tenant](https://learn.microsoft.com/entra/agent-id/disable-agent-identities)

The agent actions in the Microsoft 365 admin center are **Install and uninstall**, **Activate**, **Block and unblock**, **Delete, restore, and permanently delete**, **Start and stop** (Microsoft Foundry agents only), **Assign a new owner**, **Add an owner**, **Remove an owner**, **Publish to store**, and **Reject submission**. To stop an agent identity from receiving tokens, use **Disable** in the Microsoft Entra admin center (5.3.3).

### 5.3.1 Block or unblock an agent

Performed by **AI Administrator**.

1. Go to **Agents** > **All agents** and select the agent.
2. In the agent details pane, immediately under the agent's name, select **Block** or **Unblock**.
3. In the **Block agent** or **Unblock agent** pane, select **Block agent** or **Unblock agent**, and then select **Save**.

The impact depends on how the agent was created:

| Agent platform | Effect of Block or Unblock |
|---|---|
| Agent Builder, Copilot Studio | Affects availability and functionality in Microsoft Copilot and in other host products, such as Outlook, Teams, or other Microsoft 365 applications. |
| SharePoint, Microsoft Foundry | Blocking only affects availability in Microsoft Copilot Chat. |
| Researcher, Analyst | The **Edit users** panel is disabled. Use **Block** to manage availability for the entire tenant. |

**Check result**
- No user in the organization can use the blocked agent, within the scope shown in the table.

### 5.3.2 Start or stop a Microsoft Foundry agent (optional)

Performed by **AI Administrator** with the **Azure AI Owner** role.

**Stop** and **Start** operate on individual deployments by deallocating or provisioning Azure compute resources. These actions affect your underlying Azure infrastructure, not just how the agent is used in your organization.

1. Go to **Agents** > **All agents**, and find and select the Microsoft Foundry test agent.
2. If required, in the agent details pane select **Add role** to add the **Azure AI Owner** role.
3. Select **Stop**.
4. After the check, select **Start**.

**Check result**
- **Stop** deallocates and **Start** provisions the Azure compute resources for the deployment.

### 5.3.3 Disable the agent identity in Microsoft Entra (optional)

Performed by **Agent ID Administrator**.

Disabling prevents an agent identity from receiving tokens and authenticating, while the agent identity and its metadata stay in your tenant. Run this task only on a test agent identity, as in [3.11.1 Disable and re-enable an individual agent identity](../chapter-03-identity-ownership/README.md#3111-disable-and-re-enable-an-individual-agent-identity).

1. Sign in to the Microsoft Entra admin center at `https://entra.microsoft.com`.
2. Go to **Entra ID** > **Agents** > **Agent identities**.
3. Select the test agent identity, and then select **Disable**.
4. After the check, enable the agent identity again from its overview.

**Check result**
- While disabled, the agent identity can't receive tokens or authenticate.
- After step 4, the agent identity is enabled again.

## 5.4 Manage agent ownership

**Documentation:** [Governance and lifecycle actions for agents – Assign new owner, Add an owner, Remove an owner](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions)

| Action | Applies to | Result |
|---|---|---|
| **Assign new owner** | Shared Agent Builder and Copilot Studio agents that are ownerless or active | The new owner gets full edit and delete permissions, plus access to any files the previous owner uploaded. The previous owner loses all access, including read rights. |
| **Add owner** | Agent Builder agents that already have an owner | All owners have the same rights to edit, share, manage, and maintain the agent; there are no primary or secondary owners. Only individual users, not groups. **Created by** doesn't change. |
| **Remove owner** | Agent Builder agents with multiple owners | The last remaining owner can't be removed. |

### 5.4.1 Assign a new owner

Performed by **AI Administrator**.

1. Go to **Agents** > **All agents**.
2. Use the **Platform** filter to show Agent Builder or Copilot Studio agents.
3. Select the agent that you want to reassign.
4. In the agent details pane, immediately under the agent's name, select **Assign new owner**.
5. In the **Assign a new owner** pane, enter a new owner from your organization, and then select **Assign**.

**Check result**
- The new owner has full edit and delete permissions and access to the files the previous owner uploaded.
- The previous owner has lost all access, including read rights.

### 5.4.2 Add an owner to an Agent Builder agent

Performed by **AI Administrator**.

1. Go to **Agents** > **All agents**, use the **Platform** filter to show Agent Builder agents, and select the Agent Builder test agent.
2. On the **Details** tab of the agent details pane, select the user link next to **Owner**.
3. In the **Owners** pane, select **Add owner**.
4. Search for and select the standard test user, and then select **Add**.

**Check result**
- The owner list change is reflected for the agent in Microsoft Agent 365 and in Agent Builder.
- The **Created by** value is unchanged.

### 5.4.3 Remove an owner from an Agent Builder agent

Performed by **AI Administrator**.

1. On the **Details** tab of the agent details pane of the Agent Builder test agent, select the user link next to **Owner**.
2. In the **Owners** pane, select the standard test user that you added in 5.4.2.
3. Select **Remove owner**, review the change, and then select **Remove**.

**Check result**
- The standard test user no longer appears in the owner list.
- The last remaining owner can't be removed. Add another owner before you remove the current owner. For an ownerless agent, use **Assign new owner** (5.4.1).

## 5.5 Govern ownerless agents

**Documentation:** [Agent registry – Agents without owners](https://learn.microsoft.com/microsoft-365/admin/manage/agent-registry) · [Agent settings – Agent management rules](https://learn.microsoft.com/microsoft-365/admin/manage/agent-settings) · [Governance and lifecycle actions for agents – Assign new owner](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions) · [Reassign ownership of orphaned agents with the Power Platform API](https://learn.microsoft.com/microsoft-copilot-studio/admin-api-reassign-ownership-orphaned-agent)

Shared agents can become ownerless when you delete the user who created them from the organization. The Agent Registry shows the number of ownerless shared agents, provides a one-click filter to isolate them, and updates the count when you hard delete a user. [1.3.3 Find agents without owners](../chapter-01-agent-discovery/README.md#133-find-agents-without-owners) shows the same view during discovery.

### 5.5.1 Identify and triage ownerless agents

Performed by **AI Administrator** (or **AI Reader** for review only).

1. Go to **Agents** > **All agents** > **Registry** and clear any previous filter.
2. Select the **Agents without owners** card. The agent list is filtered by **Publisher type** and **Owner** to show shared agents missing an owner.
3. Select **Export** to keep a copy of the list for the evidence pack.
4. Select each agent to open the agent details pane and review its details.

**Check result**
- The filtered list shows the shared agents without a valid owner, and the export is saved.

### 5.5.2 Decide: reassign, block, or delete

Performed by **AI Administrator**.

For each ownerless agent from 5.5.1, agree the action with the customer, and then take it:

| Action | Section |
|---|---|
| **Assign new owner** (shared Agent Builder and Copilot Studio agents) | 5.4.1 |
| **Block** | 5.3.1 |
| **Delete** | 5.8.1 |

**Check result**
- Every ownerless agent from 5.5.1 has been reassigned, blocked, or deleted, and the action is recorded next to the agent in the export.

### 5.5.3 Automate with Agent management rules

Performed by **AI Administrator**.

Agent management rules apply governance and lifecycle controls across agents by using bulk administrative actions. You identify agents that meet defined conditions, review the impacted agents before running the rule, and apply the action across the affected agents. Supported rule-based actions:

- **Install Microsoft agents** – install Microsoft-published agents for all users in one bulk action.
- **Reassign ownerless agents created with Agent Builder to manager** – transfer ownership in bulk to the manager of the previous owner, based on the Microsoft Entra ID hierarchy. This rule only supports agents created with Microsoft Copilot Agent Builder.
- **Block ownerless agents without usage** – a custom rule that blocks multiple ownerless agents that have no usage.
- **Apply a template** – apply security policies to existing agents. The rule evaluates agents in the registry that have an agent identity; it doesn't apply to agent blueprints or AI teammates. It's a one-time bulk operation, not a scheduled rule.
- **Reject agent publish requests older than a specified number of days**.

All rules are created from **Agents** > **Settings** > **Agent management rules** > **Add rule**. To apply a template to existing PoC agents:

1. In the Microsoft 365 admin center, go to **Agents** > **Settings** > **Agent management rules**, and then select **Add rule**.
2. Select **Apply template** as the rule action.
3. Define the criteria that determine which agent instances the rule applies to.
4. Choose a preexisting template, or select policies from the **Custom** section. Review the selected policies, and then save the rule.
5. In the rule details pane, select only the PoC test agents from the list. Run the rule to apply the template.

**Check result**
- You reviewed the impacted agents before running the rule, and the template was applied only to the selected PoC test agents.

If an agent resides in an environment configured with Power Platform IP firewall in active enforcement mode, admin actions initiated from the Microsoft 365 admin center fail. Run the action directly against the Power Platform API: [Reassign ownership of orphaned agents](https://learn.microsoft.com/microsoft-copilot-studio/admin-api-reassign-ownership-orphaned-agent) or [Quarantine noncompliant agents](https://learn.microsoft.com/microsoft-copilot-studio/admin-api-quarantine).

## 5.6 Manage connected agents

**Documentation:** [Manage connected agents in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/manage-connected-agents)

Connected agents are other Copilot-enabled agents that a primary agent can invoke during a conversation. When a user's request falls within a connected agent's domain, the primary agent can delegate the request to that agent.

- You can add connected agents to **Researcher** and **Sales**. For other primary agents, you can only view the connections configured by the agent developer.
- Primary agents can connect to declarative agents and to agents that are available over the Agent2Agent (A2A) protocol. An agent can connect to up to 10 other agents.
- You can't remove connected agents configured by the agent developer.
- Both the primary agent and each connected agent must be acquired for the user.
- If a connected agent is external to your organization, the primary agent can include information from its context in the prompt it sends to the connected agent. Review the connected agent and your organization's data policies before making it available to users.

Tasks 5.6.2 to 5.6.4 are optional.

### 5.6.1 Review the connected agents of an agent

Performed by **AI Administrator** (or **AI Reader** for review only).

1. Go to **Agents** > **All agents** and select an agent.
2. Select the **Connected Agents** tab.

**Check result**
- The tab lists the agents that provide information and answers when users interact with the primary agent.

### 5.6.2 Connect agents to Researcher or Sales

Performed by **AI Administrator**.

1. Go to **Agents** > **All agents**.
2. Select **Researcher** or **Sales**, and then select the **Connected Agents** tab.
3. Select **+ Connect agents**.
4. In the **Select agent to connect** pane, use the search bar to find a PoC test agent, and select the check box next to it.
5. Select **Save**.

**Check result**
- The connected PoC test agent appears on the **Connected Agents** tab.

### 5.6.3 Make connected agents available to users

Performed by **AI Administrator**.

1. On the **Connected Agents** tab, select the connected agent. The agent's details page opens.
2. Install the agent for `A365-PoC-Users` (5.2.1).
3. Install the primary agent for the same users if it isn't installed.

**Check result**
- The primary agent and the connected agent are acquired for the members of `A365-PoC-Users`, so the primary agent can invoke the connected agent.

### 5.6.4 Remove or reset connected agents

Performed by **AI Administrator**.

1. To remove one connection, on the **Connected Agents** list select an agent that an admin added, and then select **Remove**.
2. To remove all admin-added connections, select **Reset to default**. This restores the connections configured by the agent developer and also removes admin-added connections that existed before the PoC.

**Check result**
- The connection that you added in 5.6.2 no longer appears on the **Connected Agents** tab.

## 5.7 Manage agent instances

**Documentation:** [Manage agent instances in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/manage-agent-instances)

After an admin or AI admin activates an agent (5.2.3 or 5.2.4), the requesters can create instances of it. The Microsoft 365 admin center provides a centralized view for managing these instances. Run this section only if your registry contains agents with the **AI teammate** tag.

### 5.7.1 View instances

Performed by **AI Administrator** (or **AI Reader** for review only).

1. Go to **Agents** > **All agents** > **Registry**.
2. Find agents with the **AI teammate** tag and note the number of instances created for each.
3. Select the agent to open the agent details flyout, and then select **See details** to list all instances created under that agent.

**Check result**
- From the instance list you can manage individual instances and review the security and compliance status of each instance.

### 5.7.2 Block or unblock an instance

Performed by **AI Administrator**.

1. Go to **Agents** > **All agents** and select an agent from the list.
2. Select the **Instances** tab to see all instances created by that agent.
3. Select a test instance and choose **Block**.
4. To restore functionality, select **Unblock** for the instance.

**Check result**
- Blocking an instance stops it and any actions it's performing.

### 5.7.3 Delete an instance and clean up

Performed by **AI Administrator**.

1. Go to **Agents** > **All agents**, filter the list by setting **Agent template** to **Yes**, and select the agent.
2. Select the **Instances** tab.
3. Select the test instance you want to delete, select **Delete**, and confirm the deletion when prompted.
4. Notify the owner of the deletion.

**Check result**
- Once deleted, the instance no longer appears in the list.
- After 30 days, all instance accounts and data are permanently deleted. Audit logs are kept.

## 5.8 Delete, restore, and permanently delete agents

**Documentation:** [Governance and lifecycle actions for agents – Delete agents](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions)

When you delete an agent in the Microsoft 365 admin center, the agent is soft deleted. A soft-deleted agent is unavailable to its maker and end users, but its properties and associated resources are retained for 30 days, including the agent ID, metadata, channels, ownership, and connections. During the 30-day retention period you can restore the agent or permanently delete it. If you do neither, Microsoft 365 permanently deletes it automatically when the retention period ends. Soft-delete, restore, and permanent-delete events are recorded in the audit log with information about the system that initiated the action.

### 5.8.1 Delete an agent (soft delete)

Performed by **AI Administrator**.

1. Go to **Agents** > **All agents** and select the agent.
2. In the agent details pane, select **Delete agent**.
3. In the confirmation pane, select **Delete**.

**Check result**
- The agent is unavailable to its maker and end users.
- The agent can be selected under **Agents** > **All agents** > **Deleted** during the 30-day retention period.

### 5.8.2 Restore a deleted agent

Performed by **AI Administrator**.

1. Go to **Agents** > **All agents**, and then select **Deleted**.
2. Select the agent.
3. In the agent details pane, select **Restore agent**, and then in the confirmation dialog select **Restore**.

**Check result**
- The agent returns to an active state and is available to its maker and end users with its previous configuration.
- Restore is only possible while the agent is soft deleted and within its 30-day retention period.

### 5.8.3 Permanently delete an agent

Performed by **AI Administrator**.

Permanently deleting an agent removes the agent and its associated resources and can't be undone. You can permanently delete only an agent that's already soft deleted.

1. Go to **Agents** > **All agents**, and then select **Deleted**.
2. Select the agent.
3. In the agent details pane, select **Permanently delete**, and then in the confirmation dialog select **Delete**.

**Check result**
- The agent and its associated resources are removed, and the action can't be undone.

## 5.9 Audit the agent lifecycle

**Documentation:** [Search the audit log](https://learn.microsoft.com/purview/audit-search) · [Audit logs for Copilot and AI applications](https://learn.microsoft.com/purview/audit-copilot) · [Audit log activities – Agent 365 activities](https://learn.microsoft.com/purview/audit-log-activities) · [Agent sign-in and audit logs in Microsoft Entra](https://learn.microsoft.com/entra/agent-id/sign-in-audit-logs-agents) · [Access activity logs in Microsoft Entra](https://learn.microsoft.com/entra/identity/monitoring-health/howto-access-activity-logs) · [Discover AI agents in Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-inventory) · [AgentsInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-agentsinfo-table)

Microsoft Purview Audit is turned on in [0.5 Turn on Microsoft Purview Audit](../chapter-00-prerequisites/README.md#05-turn-on-microsoft-purview-audit). If auditing was turned on within the last 180 days, the search date range can't start before the date auditing was turned on.

### 5.9.1 Search admin actions on agents in Purview Audit

Performed by **Audit Reader**.

1. Sign in to the Microsoft Purview portal at `https://purview.microsoft.com` and select the **Audit** solution card.
2. On the **Search** page, set **Date and time range (UTC)** to cover the lifecycle actions, starting at the PoC start time.
3. In **Users**, select the test admin account that performed the actions.
4. Optionally, enter `PoC-Lifecycle-Agent` in **Keyword Search**.
5. Enter a **Search name**, for example `PoC-Ch5-Admin-Actions`, and run the search.
6. When the search job completes, open it. Select an activity to see its details in the fly-out window.
7. Select **Export** on the command bar to export the search job items to a .csv file.

**Check result**
- The soft-delete, restore, and permanent-delete events for the test agent are in the results, with information about the system that initiated the action.

### 5.9.2 Search agent interactions in Purview Audit

Performed by **Audit Reader**.

Run two searches: one for the Copilot interaction record types and one for the Agent 365 activity operation names.

1. On the Microsoft Purview **Audit** > **Search** page, set the date range to cover the test interactions, and in **Users** select the standard test user.
2. Search 1: in **Record types**, select `CopilotInteraction`. For custom-built or third-party AI applications deployed and registered in your organization, also select `ConnectedAIAppInteraction`. Enter a search name, run the search, and export the results.
3. Search 2: clear **Record types**, and in **Activities - operations names** enter the Agent 365 activities that are logged when an agent is invoked or performs actions or tool calls: `AIExecuteTool,AIInvokeAgent,AIInferenceCall,AIGuardrail`. Enter a search name, run the search, and export the results.
4. In the exports, filter the `AgentId` or `AgentName` property for the test agent. To filter on `AppIdentity`, export the results first and filter offline.

**Check result**
- The exports contain the standard test user's interactions with the test agent, with properties such as `AgentId`, `AgentName`, `AppHost`, and `AccessedResources` (including `SensitivityLabelId`, `PolicyDetails`, and `Status` where applicable).

### 5.9.3 Review Entra audit and sign-in logs for the agent identity

Performed by **Reports Reader**.

Run this task only if the test agent has an agent identity.

1. Sign in to the Microsoft Entra admin center at `https://entra.microsoft.com`.
2. Go to **Entra ID** > **Agents** > **Agent identities** and find the test agent's identity.
3. Go to **Entra ID** > **Monitoring & health** > **Audit logs** and adjust the filter for the PoC date range. Agent identity activities appear as service principal events, such as **Add service principal**, **Update service principal**, and **Delete service principal**, with the `agentType` value `agenticAppInstance`.
4. Go to **Entra ID** > **Monitoring & health** > **Sign-in logs**, and use the filters **Is Agent** = **Yes** and **Agent type** = **Agent Identity**. Because agents can sign in with either user-delegated or app-only permissions, check each of the sign-in log types.

To retrieve agent identity sign-in events by using Microsoft Graph:

```http
GET https://graph.microsoft.com/beta/auditLogs/signIns?$filter=signInEventTypes/any(t: t eq 'servicePrincipal') and agent/agentType eq 'agenticAppInstance'
```

**Check result**
- Audit events for the agent identity show `agentType` = `agenticAppInstance` on the `initiatedBy`, `performedBy`, or `targetResources` fields.
- Sign-in events for the agent identity are returned by the sign-in log filters or the Graph request.

### 5.9.4 Track lifecycle state in Defender Advanced Hunting

Performed by **Security Reader**.

The `AgentsInfo` table stores multiple snapshots of each agent over time; use `arg_max(Timestamp, *)` to return the latest state of each agent. `LifecycleStatus` is the agent's current operational state in the tenant, with the possible values `Active`, `Blocked`, `Uninstalled`, and `Deleted`.

1. Sign in to the Microsoft Defender portal at `https://security.microsoft.com`.
2. Select **Investigation & response** > **Hunting** > **Advanced hunting**.
3. Run the queries below.

Latest record for each agent:

```kql
AgentsInfo
| summarize arg_max(Timestamp, *) by AgentId
| where LifecycleStatus != "Deleted"
```

All recorded snapshots of the test agent:

```kql
AgentsInfo
| where Name has "PoC-Lifecycle-Agent"
| project Timestamp, AgentId, Name, Platform, LifecycleStatus, PublishedStatus, Availability, Owners, EntraAgentID
| sort by Timestamp asc
```

`LifecycleStatus` changes between snapshots:

```kql
AgentsInfo
| where Timestamp > ago(30d)
| project Timestamp, AgentId, Name, LifecycleStatus
| sort by AgentId asc, Timestamp asc
| extend PrevAgentId = prev(AgentId), PrevStatus = prev(LifecycleStatus)
| where AgentId == PrevAgentId and LifecycleStatus != PrevStatus
| project Timestamp, Name, PrevStatus, LifecycleStatus
| sort by Timestamp desc
```

`CloudAppEvents` contains Agent 365 observability data for AI agent activity, including agent actions, tool invocations, and data access events:

```kql
CloudAppEvents
| where Timestamp between (datetime(<START>) .. datetime(<END>))
| where RawEventData has "<test agent name or AgentId>"
| project Timestamp, Application, ActionType, AccountDisplayName, AccountObjectId, RawEventData
| sort by Timestamp desc
```

**Check result**
- The snapshots of the test agent show the `LifecycleStatus` values recorded during the test walk.

## 5.10 Test and validation

Sections 5.2 to 5.8 describe each action. This section runs them in order on `PoC-Lifecycle-Agent`. After each step, record the UTC time and a screenshot of the agent details pane. Collect the Microsoft Purview Audit records (5.9.1, 5.9.2) and the `AgentsInfo` snapshots (5.9.4) for all steps in 5.10.10.

| Step | Action | Documented outcome |
|---|---|---|
| 5.10.2 | Install | Agent ready to use for `A365-PoC-Users` |
| 5.10.3 | Block | No user can use the agent |
| 5.10.4 | User tries to use the agent | Agent not available |
| 5.10.5 | Unblock | Agent available again |
| 5.10.6 | Assign new owner | New owner has full access; previous owner loses all access |
| 5.10.7 | Delete | Soft deleted, unavailable to maker and end users, audit record |
| 5.10.8 | Restore | Active state with previous configuration, audit record |
| 5.10.9 | Permanently delete | Agent and resources removed, can't be undone, audit record |

### 5.10.1 Prepare the test agent and record a baseline

Performed by **AI Reader**, **Security Reader**, and the **standard test user**.

1. As AI Reader, in **Agents** > **All agents** > **Registry**, search for `PoC-Lifecycle-Agent` and capture the agent details pane, including the owner.
2. As the standard test user, check whether the agent is already available to you.
3. As Security Reader, run the "All recorded snapshots of the test agent" query from 5.9.4 and save the result.

**Expected result**
- You have a baseline of the agent's details, its owner (the maker), and its `AgentsInfo` snapshots before the walk.

### 5.10.2 Install the agent for the test group

Performed by **AI Administrator**, then the **standard test user**.

1. Install the agent for `A365-PoC-Users` (5.2.1).
2. As the standard test user, open Microsoft 365 Copilot and start a conversation with the agent.

**Expected result**
- The agent is ready to use for the standard test user without manual installation.
- Audit evidence: a `CopilotInteraction` record for the standard test user's conversation (5.9.2).

### 5.10.3 Block the agent

Performed by **AI Administrator**.

1. Block the agent (5.3.1).

**Expected result**
- The agent is blocked for the organization.
- Audit evidence: an `AgentsInfo` snapshot of the test agent with `LifecycleStatus` = `Blocked` (5.9.4).

### 5.10.4 Confirm that the user can't use the blocked agent

Performed by the **standard test user**.

1. Try to open or invoke the agent in Microsoft 365 Copilot.
2. Try to open the agent in Outlook and Teams.

**Expected result**
- The agent isn't available to the standard test user in Microsoft Copilot or in other host products such as Outlook and Teams (Agent Builder and Copilot Studio agents).

### 5.10.5 Unblock the agent

Performed by **AI Administrator**, then the **standard test user**.

1. Unblock the agent (5.3.1).
2. As the standard test user, start a new conversation with the agent.

**Expected result**
- The agent is unblocked, and the standard test user can use it again.
- Audit evidence: a new `CopilotInteraction` record for the standard test user's conversation (5.9.2).

### 5.10.6 Reassign the owner

Performed by **AI Administrator**, then the maker and the **standard test user**.

1. Assign the standard test user as the new owner of the agent (5.4.1).
2. As the maker (the previous owner), try to open the agent.
3. As the standard test user (the new owner), open the agent for editing.

**Expected result**
- The standard test user has full edit and delete permissions and access to any files the maker uploaded.
- The maker has lost all access, including read rights.

### 5.10.7 Delete the agent

Performed by **AI Administrator**, then the **standard test user**.

1. Delete the agent (5.8.1).
2. As the standard test user, try to use the agent.

**Expected result**
- The agent is unavailable to its owner and end users and can be selected under **Deleted**.
- Audit evidence: the soft-delete event in Microsoft Purview Audit (5.9.1), and an `AgentsInfo` snapshot with `LifecycleStatus` = `Deleted` (5.9.4).

### 5.10.8 Restore the agent

Performed by **AI Administrator**, then the **standard test user**.

1. Restore the agent (5.8.2).
2. Compare the agent details pane with the screenshot from 5.10.6.
3. As the standard test user, start a conversation with the agent.

**Expected result**
- The agent is back in an active state and available to its owner and end users with its previous configuration, including ownership, channels, and connections.
- Audit evidence: the restore event in Microsoft Purview Audit (5.9.1), and an `AgentsInfo` snapshot with `LifecycleStatus` = `Active` (5.9.4).

### 5.10.9 Permanently delete the agent

Performed by **AI Administrator**.

1. Delete the agent again (5.8.1).
2. Permanently delete it from the **Deleted** view (5.8.3).

**Expected result**
- The agent and its associated resources are removed, and the action can't be undone.
- Audit evidence: the second soft-delete event and the permanent-delete event in Microsoft Purview Audit (5.9.1).

### 5.10.10 Reconcile the audit trail

Performed by **Audit Reader**, **Security Reader**, and **Reports Reader**.

1. As Audit Reader, run 5.9.1 and 5.9.2 for the full walk window and export the results.
2. As Security Reader, run the "All recorded snapshots of the test agent" and "`LifecycleStatus` changes between snapshots" queries from 5.9.4 and export the results.
3. As Reports Reader, if the test agent has an agent identity, run 5.9.3 and download the Microsoft Entra audit and sign-in records.
4. Build one timeline: step, UTC time, admin action, Microsoft Purview record, `LifecycleStatus`.

**Expected result**
- The soft-delete, restore, and permanent-delete events of the test agent each have a Microsoft Purview audit record.
- The timeline shows `LifecycleStatus` = `Blocked` after 5.10.3 and `Deleted` after 5.10.7.

## 5.11 Evidence

- Export of **Agents** > **All agents** > **Registry** before and after the PoC, and the export of **Agents without owners** with the action taken for each agent (5.5.1, 5.5.2).
- Screenshots of the agent details pane after each step of the test walk (5.10.1 to 5.10.9), with UTC time.
- Screenshot of the **Deleted** view showing the test agent (5.10.7).
- Screenshot of the activation wizard with the selected template, if you ran 5.2.3 or 5.2.4.
- Screenshots of the Foundry agent after **Stop** and **Start** (5.3.2) and of the disabled agent identity (5.3.3), if you ran these tasks.
- Screenshots of the **Owners** pane (5.4.2, 5.4.3) and of the **Assign a new owner** pane (5.4.1).
- Screenshot of the Agent management rule and its impacted agents, if you ran 5.5.3.
- Screenshots of the **Connected Agents** tab before and after changes, if you ran 5.6.
- Screenshot of the **Instances** tab, if you ran 5.7.
- Microsoft Purview Audit exports: admin actions (5.9.1) and agent interactions (5.9.2) for the full walk window.
- Microsoft Entra audit log and sign-in log downloads for the agent identity (5.9.3), if the test agent has one.
- Advanced Hunting result exports for the `AgentsInfo` queries (5.9.4).
- The reconciled timeline from 5.10.10.

## 5.12 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| You can view agents but can't install, modify, approve, or manage them | Signed in with a read-only role (AI Reader, Global Reader, Security Reader, Reports Reader) | Use an account with **AI Administrator**. |
| An admin action fails and isn't applied to the agent | The agent's environment uses Power Platform IP firewall in active enforcement mode | In the Power Platform admin center, go to **Security** > **Identity and access** > **IP firewall**, select the environment, and check the **Advanced** tab. Run the action against the Power Platform API instead. |
| **Uninstall** isn't shown | The selected agent might not be installed | Install it first (5.2.1). |
| You can't reassign ownership | Ownership reassignment is only available for shared Agent Builder and Copilot Studio agents | Use a shared Agent Builder or Copilot Studio agent. |
| You can't remove an owner | The owner is the last remaining owner | Add another owner first (5.4.2). |
| **Edit users** is disabled for Researcher or Analyst | The **Edit users** panel is disabled for these agents | Use **Block** to manage availability for the entire tenant. |
| A blocked SharePoint or Microsoft Foundry agent is still available outside Copilot Chat | Blocking these agents only affects availability in Microsoft Copilot Chat | No fix needed; this is the documented scope of **Block** for these agents. |
| **Stop** or **Start** isn't possible for a Foundry agent | The **Azure AI Owner** role is missing | Select **Add role** in the agent details pane to add the **Azure AI Owner** role. |
| **Restore agent** isn't possible | The agent was permanently deleted, or the 30-day retention period has ended | The action can't be undone. |
| Microsoft Purview Audit search returns no results for older activity | The date range starts before auditing was turned on | Set the start date on or after the date auditing was turned on. |
| Microsoft Purview Audit search job takes a long time | Broad search scope in a large tenant | Narrow the date range and users. Broadly scoped search jobs in large tenants may take up to 48 hours. |
| No `CopilotInteraction` records for a custom or third-party AI app | Interactions with custom-built or third-party apps registered in the organization use a different record type | Also search `ConnectedAIAppInteraction`. |
| A query on `AIAgentsInfo` fails | `AIAgentsInfo` is transitioning to `AgentsInfo` | Use the `AgentsInfo` table. |
| **Agents without owners** count doesn't change after deleting a user | The count updates when a user is hard deleted | Check again after the user is hard deleted. |

## 5.13 Cleanup

- Make sure `PoC-Lifecycle-Agent` is permanently deleted (5.10.9).
- Delete the separate Agent Builder test agent if you created one only for 5.4.2 and 5.4.3 (5.8.1, 5.8.3), or confirm that the standard test user was removed as owner (5.4.3).
- Uninstall any other agent you installed only for this chapter (5.2.2).
- Unblock any other agent you blocked during testing (5.3.1).
- Confirm that the Foundry test agent was started again (5.3.2, step 4) and that any agent identity you disabled was enabled again (5.3.3, step 4).
- Remove the connection you added to Researcher or Sales (5.6.4, step 1).
- Unblock or delete the test instances you used (5.7.2, 5.7.3) and notify their owners.
- Record the Agent management rules you created in 5.5.3 and the PoC agents they were applied to in the PoC handover.
- Remove the AI Administrator and Agent ID Administrator role assignments at the end of the PoC window. Keep the read-only roles only for reviewers who still need them.
- Keep the Microsoft Purview Audit exports, Advanced Hunting exports, and the reconciled timeline with the PoC evidence pack.

---
Previous: [Chapter 4 – Tools and MCP Server Governance](../chapter-04-tools-mcp-governance/README.md) · Next: [Chapter 6 – Conditional Access and Least Privilege](../chapter-06-conditional-access/README.md)
