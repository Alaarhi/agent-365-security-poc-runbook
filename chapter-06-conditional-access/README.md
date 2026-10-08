# Chapter 6 – Conditional Access and Least Privilege

**Pillar:** Secure
**What it proves:** Agents get only the access you approve. Conditional Access refuses a token to agent identities you haven't approved or that ID Protection flags as high risk, and the denial is visible in the sign-in log. Access packages grant resource access to agents with approval, and the access is removed automatically when it expires.

**Success criteria**
- A default-deny policy for agent identities exists. In report-only mode, the sign-in log shows **Report-only: Failure** for an unapproved test agent and **Report-only: Not applied** for an approved test agent.
- The policy **Block high-risk agent identities** is **On**. It targets **All agent identities** with **Agent risk (Preview)** = **High** and the grant control **Block**.
- Optional (6.9): after a test agent is marked as compromised, its token request as the agent identity fails with `AADSTS53003`, and the sign-in log lists the risk policy with result **Failure**. A control agent that isn't risky still gets a token.
- If agent user accounts are in scope, the agent-user policies exist in report-only mode, and the device and network policies are limited to sessions from endpoints with the **Agent execution environments (Preview)** condition.
- Optional (6.9): the **Risky agents** report shows the test agent as high risk during the test, and as no longer at risk after the reset.
- An access package for agent identities exists, with a request policy for **All agents**, an approval stage, and an expiration. A test agent receives the access, and loses it automatically when the assignment expires.
- A custom policy template with a Conditional Access policy and a custom security attribute is applied when a requested agent is published. The published agent's identity carries the attribute value, and its sign-in details show the template's Conditional Access policy.

## 6.1 Required permissions
Grant the read-only roles first. Grant setup roles only to the people who make the changes, and assign them as Active (not Eligible) for the PoC window.

| Task | Least-privilege role | Section |
|---|---|---|
| Create the three lab agent identities from the lab blueprint | Agent ID Administrator | Before you start |
| Review agent sign-ins and Conditional Access results in the sign-in logs | Reports Reader | 6.2.1, 6.2.4, 6.8.1, 6.8.3, 6.9.4 |
| Create, edit, and enable Conditional Access policies for agent identities and agent users | Conditional Access Administrator | 6.2, 6.3, 6.4, 6.12 |
| Select custom security attributes in a Conditional Access policy | Conditional Access Administrator and Attribute Definition Reader | 6.2.3 |
| Create attribute definitions / assign or remove attribute values on agent identities | Attribute Definition Administrator / Attribute Assignment Administrator | 6.2.3, 6.12 |
| Delete the PoC group after the tests | Groups Administrator | 6.12 |
| View the Risky agents report and agent risk detections | Security Reader | 6.5.1 |
| Confirm compromise, confirm safe, or dismiss risk (Microsoft Entra admin center or Microsoft Graph) | Security Administrator | 6.5.2, 6.9.2, 6.9.5 |
| Configure diagnostic settings to export risk and sign-in data (optional) | Security Administrator | 6.5.3, 6.12 |
| Query the exported data in the Log Analytics workspace (optional) | Permission to access data in the Log Analytics workspace | 6.5.3 |
| Create catalogs, access packages, and policies, and assign or remove access | Identity Governance Administrator | 6.6, 6.8.2, 6.12 |
| Add API permissions or directory roles as resource roles (optional) | Global Administrator | 6.6.2 |
| Request an access package for an agent in My Access | Owner or sponsor of the agent identity (no admin role) | 6.6.3 |
| Approve access package requests | Approver named in the policy (no admin role) | 6.6.3 |
| Create a Conditional Access policy that a template can select | Conditional Access Administrator | 6.7.1 |
| Create a custom policy template with Conditional Access and custom security attribute policies, and apply it when publishing an agent | Global Administrator with Attribute Assignment Administrator | 6.7.2, 6.7.3, 6.12 |
| Verify custom security attribute values on the published agent | Agent ID Administrator together with Attribute Assignment Reader | 6.8.3 |
| Run the community reference script (optional) and remove the lab client secret | Owner of the lab agent identity blueprint | 6.9.1, 6.9.3, 6.12 |
| Delete the lab agent identity blueprint and its agent identities | Cloud Application Administrator (or the owner of the blueprint) | 6.12 |
| Validation / read-only review | Global Reader (policies, access packages, group members), Reports Reader (sign-in logs), Security Reader (risky agents) | 6.6.4, 6.8, 6.9, 6.10 |

Notes:
- By default, Global Administrator and other administrator roles can't read, define, or assign custom security attributes. Assign the attribute roles explicitly.
- To keep the PoC least-privileged, the core path in 6.6 uses only a security group, because adding OAuth API permissions or directory roles to an access package marks the catalog as privileged and requires a Global Administrator.
- The role requirements for policy templates are described in 6.7.

**Before you start:**
- Complete [Chapter 0 – Prerequisites and PoC preparation](../chapter-00-prerequisites/README.md). You need the test admin, the standard test user, the reviewer, and the PoC approver accounts (0.4.1).
- Complete [Chapter 1 – Agent Discovery and Inventory](../chapter-01-agent-discovery/README.md) so you know which agents exist and which ones must keep working.
- Complete [Chapter 3 – Agent Identity and Ownership](../chapter-03-identity-ownership/README.md). Sponsors must be assigned (3.5), and you need the sign-in log filters (3.8) and the Risky agents report (3.9). Sponsor transitions with Lifecycle Workflows are covered in [3.10 Keep sponsorship continuous with Lifecycle Workflows](../chapter-03-identity-ownership/README.md#310-keep-sponsorship-continuous-with-lifecycle-workflows).
- Prepare a lab agent identity blueprint with a client secret you control, for example with [2.8 Create the agent blueprint with a365 setup](../chapter-02-third-party-custom-agents/README.md#28-create-the-agent-blueprint-with-a365-setup). Then, as an **Agent ID Administrator**, create the three agent identities below from that blueprint: open <https://entra.microsoft.com> > **Entra ID** > **Agents** > **Agent identities** > **New agent identity (Preview)**, select the lab blueprint under **Agent blueprint**, enter the name in **Agent identity name**, and complete the wizard with **Create**. Record each agent identity's ID. For agent identities, the object ID and app ID are always the same value.

| Test object | Purpose | Approved (excluded from default deny) |
|---|---|---|
| `PoC-Agent-Approved` | Control agent for all tests; receives the access package | Yes |
| `PoC-Agent-Risk` | Marked as compromised in the optional risk test (6.9) | Yes |
| `PoC-Agent-Unapproved` | Not on the allow list | No |
| `PoC-Agent-Resource-Access` (security group from Chapter 0, 0.4.2) | Resource granted through the access package | – |
| PoC approver (test user from Chapter 0, 0.4.1) | Approves access package requests | – |

- Set the standard test user as a sponsor of `PoC-Agent-Approved`, as in [3.5.1 Assign owners and sponsors to an agent identity](../chapter-03-identity-ownership/README.md#351-assign-owners-and-sponsors-to-an-agent-identity). The standard test user is the sponsor in 6.6.3 and uses the published agent in 6.8.3.
- For 6.7, have a member of your organization submit a test agent for admin approval, so that it appears in **Agents** > **All agents** > **Requests** in the Microsoft 365 admin center.
- Security defaults must be off in the tenant. Conditional Access policies don't apply while security defaults are enabled.

## 6.2 Allow only approved agent identities (default deny)
**Documentation:** [Conditional Access for agents](https://learn.microsoft.com/entra/identity/conditional-access/agent-id) · [Target agents in Conditional Access policies](https://learn.microsoft.com/entra/identity/conditional-access/howto-target-agent-identities) · [Secure autonomous agents with Conditional Access](https://learn.microsoft.com/entra/identity/conditional-access/policy-autonomous-agents) · [Conditional Access report-only mode](https://learn.microsoft.com/entra/identity/conditional-access/concept-conditional-access-report-only)

Conditional Access evaluates the **token subject**. It applies when Microsoft Entra ID issues or refreshes an access token. Agents can use three access patterns, and each one needs its own policy:

| If the agent | Access pattern | Token subject / policy target | Covered in |
|---|---|---|---|
| Accesses resources for a signed-in user | On-behalf-of (delegated) | The **user**. Target users and groups with your existing user policies. | Out of scope for agent policies |
| Accesses resources with its own identity and no signed-in user | App-only (autonomous) | **Agent identity** or **agent identity blueprint** | 6.2, 6.3 |
| Accesses resources through its own user account (mailbox, chat, team member) | Agent user | **Agent's user account** | 6.4 |

A policy that targets agent identities doesn't apply to the agent's user account, and the reverse is also true. A policy that targets a blueprint covers every agent identity created from it, including agent identities created later. The blueprint target doesn't cover the agents' user accounts.

Conditions and grant controls depend on the token subject:

| | Agent identities | Agent user accounts (Preview) |
|---|---|---|
| Include options | **All agent identities**, **Select agent identities** (individual agents or blueprints, or custom security attributes) | **All agent users (Preview)**, **Select agent users (Preview)** (individual accounts or custom security attributes). Group-based include and exclude isn't supported. |
| Conditions | **Agent risk (Preview)** only | **Agent risk (Preview)**, **Agent execution environments (Preview)**, **Device platforms**, **Filter for devices**, **Network**. Device and network signals are available only for agents that run on endpoints. |
| Grant controls | **Block access** only. Interactive remediation isn't possible. | **Block access**, or **Grant access** with **Require device to be marked as compliant** or **Require compliant network** |

Conditional Access doesn't apply in these cases:
- A blueprint acquires a Microsoft Graph token to create an agent identity or an agent's user account.
- A blueprint or agent identity performs the intermediate token exchange at **AAD Token Exchange Endpoint: Public** (resource ID `fb60f99c-7a34-4190-8149-302f77469936`). In the autonomous agent flow, this is the blueprint's token request (T1, see 6.9). Conditional Access protects the token request that follows, made by the agent identity (T2).
- Security defaults are enabled.
- The agent authenticates to a resource without Microsoft Entra ID, for example with an API key.

Also keep in mind:
- Policies that target **All users** don't include agents' user accounts.
- Target resources must have an enterprise application (service principal) in your tenant. To protect a custom MCP server or tool, register it in Microsoft Entra ID and expose its permissions.

### 6.2.1 Map each PoC agent to its token subject
Performed by **Reports Reader**.
1. Have the owner of each PoC agent exercise it once. For the three lab agent identities, use the community reference script in 6.9.1.
2. Open <https://entra.microsoft.com> > **Entra ID** > **Monitoring & health** > **Sign-in logs**.
3. Add the filter **Is Agent** = **Yes**, and add the filter **Agent type**.
4. Check the **Service principal sign-ins** tab and the user sign-in tabs. Note for each agent where it appears:
   - **Agent type** = **Agent Identity** on **Service principal sign-ins**: app-only. Use 6.2 and 6.3.
   - **Agent type** = **Agent ID user**: agent user account. Use 6.4.

**Check result**
- Every PoC agent is mapped to one or more token subjects. The three lab agent identities appear on **Service principal sign-ins** with **Agent type** = **Agent Identity**.

### 6.2.2 Create the default-deny policy with the enhanced object picker
Performed by **Conditional Access Administrator**.
1. Open <https://entra.microsoft.com> > **Entra ID** > **Conditional Access** > **Policies** > **New policy**.
2. Name: `PoC – Agents – Default deny except approved`.
3. Under **Assignments**, select **Users, agents or workload identities**.
4. Under **What does this policy apply to?**, select **Agents**.
5. Under **Include**, select **All agent identities**.
6. Under **Exclude**, select **Select individual agent identities**. In the enhanced object picker, use the **All**, **Agent blueprint principals**, and **Agent identities** tabs to select `PoC-Agent-Approved`, `PoC-Agent-Risk`, and every other agent identity or blueprint that must keep working. Then select **Select**.
7. Under **Target resources** > **Include**, select **All resources (formerly 'All cloud apps')**.
8. Under **Access controls** > **Grant**, select **Block**, and then select **Select**.
9. Set **Enable policy** to **Report-only**, and then select **Create**.

> **All agent identities** applies the policy to every agent identity in your tenant. Report-only mode evaluates and logs the policy but doesn't block anything. Before you switch to **On** (6.2.4), make sure every agent from your Chapter 1 inventory that must keep working is excluded. To exclude a whole fleet, exclude its blueprint.

**Check result**
- The policy is listed with state **Report-only**. Its exclusions contain both approved test agents.

### 6.2.3 (Optional) Exclude approved agents with custom security attributes
Use this variant when you have many agents. Every agent that carries the approval attribute is excluded automatically, including agents added later.

Performed by **Attribute Definition Administrator** (steps 1–2), **Attribute Assignment Administrator** (step 3), and **Conditional Access Administrator** with **Attribute Definition Reader** (steps 4–8).
1. Open <https://entra.microsoft.com> > **Entra ID** > **Custom security attributes**, and add an attribute set named `AgentAttributes`.
2. In `AgentAttributes`, add the attribute `AgentApprovalStatus` with data type **String**. Select **Allow multiple values to be assigned** and **Only allow predefined values to be assigned**, and add the predefined values `New`, `In_Review`, `HR_Approved`, `Finance_Approved`, and `IT_Approved`. Conditional Access supports only attributes of type string.
3. Assign `IT_Approved` to `PoC-Agent-Approved` and `PoC-Agent-Risk`. Use the Graph method from [3.7.2 Assign attribute values to PoC agent identities](../chapter-03-identity-ownership/README.md#372-assign-attribute-values-to-poc-agent-identities) (`PATCH https://graph.microsoft.com/v1.0/servicePrincipals/{id}/microsoft.graph.agentIdentity`, delegated permissions `CustomSecAttributeAssignment.ReadWrite.All` and `AgentIdentity.ReadWrite.All`), with this body for a multi-valued attribute:

   ```json
   {
     "customSecurityAttributes": {
       "AgentAttributes": {
         "@odata.type": "#Microsoft.DirectoryServices.CustomSecurityAttributeValue",
         "AgentApprovalStatus@odata.type": "#Collection(String)",
         "AgentApprovalStatus": ["IT_Approved"]
       }
     }
   }
   ```

4. Create a new policy as in 6.2.2, steps 1–5. Name it `PoC – Agents – Default deny except approved (attributes)`.
5. Under **Exclude**, select **Select agent identities based on attributes**, and set **Configure** to **Yes**.
6. Select the attribute **AgentApprovalStatus**, set **Operator** to **Contains** and **Value** to `IT_Approved`, and then select **Done**.
7. Complete 6.2.2, steps 7–8.
8. Set **Enable policy** to **Report-only**, and select **Create**.

Use only one of the two default-deny variants for the tests in 6.8.

**Check result**
- Each `PATCH` request returns `204 No Content`. Both approved agents carry `AgentApprovalStatus` = `IT_Approved`, and the policy is in **Report-only**.

### 6.2.4 Review the report-only results, then switch to On
Performed by **Reports Reader** (review) and **Conditional Access Administrator** (switch).
1. Run the allow-list test in 6.8.1.
2. In the sign-in log, open recent agent sign-ins and select the **Report-only** tab. Confirm that only agents you intend to block show **Report-only: Failure**.
3. Add any agent that must keep working to the exclusions.
4. When the results match your intent, open the policy and move **Enable policy** from **Report-only** to **On**. In a shared or production tenant, you can keep the policy in report-only for the PoC and record the results as evidence.

> The **Policy impact** view shows the impact of policies on interactive sign-ins. Report-only results for each sign-in are logged on the **Conditional Access** and **Report-only** tabs of the sign-in log details.

**Check result**
- No agent that must keep working shows **Report-only: Failure**. The final state of the policy (**On** or **Report-only**) is recorded in the evidence.

## 6.3 Block high-risk agent identities
**Documentation:** [Secure autonomous agents with Conditional Access – Block high-risk agent identities](https://learn.microsoft.com/entra/identity/conditional-access/policy-autonomous-agents#block-high-risk-agent-identities) · [ID Protection for agents](https://learn.microsoft.com/entra/id-protection/concept-risky-agents)

This policy blocks agent identities dynamically when ID Protection raises their risk. It works alongside the static allow list in 6.2. Microsoft recommends **High** as the starting level.

### 6.3.1 Create the risk-based policy
Performed by **Conditional Access Administrator**.
1. Open <https://entra.microsoft.com> > **Entra ID** > **Conditional Access** > **Policies** > **New policy**.
2. Name: `PoC – Agents – Block high-risk agent identities`.
3. Under **Assignments**, select **Users, agents or workload identities**, and under **What does this policy apply to?**, select **Agents**.
4. Under **Include**, select **All agent identities**.
5. Under **Target resources** > **Include**, select **All resources (formerly 'All cloud apps')**.
6. Under **Conditions** > **Agent risk (Preview)**, set **Configure** to **Yes**. Under **Configure agent risk levels needed for policy to be enforced**, select **High**.
7. Under **Access controls** > **Grant**, select **Block**, and then select **Select**.
8. Set **Enable policy** to **Report-only**, and then select **Create**.
9. After you confirm the settings with report-only mode (the **Report-only** tab of agent sign-ins), move **Enable policy** from **Report-only** to **On**.

The optional risk test in 6.9 requires this policy to be **On**. Report-only mode evaluates the policy but doesn't enforce it.

> Microsoft Learn also provides a ready-made Conditional Access template for this policy: <https://aka.ms/CreateAgentRiskPolicy>.

**Check result**
- The policy is **On**. It includes **All agent identities** with **Agent risk (Preview)** = **High** and the grant control **Block**.

## 6.4 Protect agents that act as users (agent user accounts)
**Documentation:** [Secure agent users with Conditional Access](https://learn.microsoft.com/entra/identity/conditional-access/policy-agent-user) · [Target agents in Conditional Access policies](https://learn.microsoft.com/entra/identity/conditional-access/howto-target-agent-identities) · [Agents' user accounts](https://learn.microsoft.com/entra/agent-id/agent-users) · [What is Windows 365 for Agents?](https://learn.microsoft.com/windows-365/agents/introduction-windows-365-for-agents) · [What is Global Secure Access?](https://learn.microsoft.com/entra/global-secure-access/overview-what-is-global-secure-access)

Complete this section only if a PoC agent uses its own agent user account. Agent user targeting is in preview. Agents that run directly in cloud infrastructure, such as Copilot Studio hosted agents, have no device. A device or network requirement without the **Agent execution environments (Preview)** condition blocks those agents with no path to remediation.

Prerequisites:
- An agent user account linked to an agent identity.
- For 6.4.2: an agent that runs on an Intune-managed Windows 365 Cloud PC for Agents. Device compliance requires Intune enrollment, which today is supported only on Windows 365 Cloud PCs for Agents.
- For 6.4.3: the same Cloud PC with the Global Secure Access client installed.

### 6.4.1 Block risky agent user accounts
Performed by **Conditional Access Administrator**.
1. Open <https://entra.microsoft.com> > **Entra ID** > **Conditional Access** > **Policies** > **New policy**.
2. Name: `PoC – Agent users – Block medium and high risk`.
3. Under **Assignments**, select **Users, agents or workload identities**. Under **What does this policy apply to?**, select **Agents**, and under **Include**, select **All agent users (Preview)**.
4. Under **Target resources** > **Include**, select **All resources (formerly 'All cloud apps')**.
5. Under **Conditions** > **Agent risk (Preview)**, set **Configure** to **Yes**, and select **Medium** and **High**.
6. Under **Access controls** > **Grant**, select **Block**, and then select **Select**.
7. Set **Enable policy** to **Report-only**, and then select **Create**. Move it to **On** after you review the report-only results.

**Check result**
- The policy targets **All agent users (Preview)** with **Agent risk (Preview)** = **Medium**, **High**, and **Block**.

### 6.4.2 Require a compliant device (endpoint agents only)
Performed by **Conditional Access Administrator**.
1. Create a new policy named `PoC – Agent users – Require compliant device (endpoints)`.
2. Under **Assignments**, select **Users, agents or workload identities** > **Agents**, and under **Include**, select **All agent users (Preview)**.
3. Under **Target resources** > **Include**, select **All resources (formerly 'All cloud apps')**.
4. Under **Conditions** > **Agent execution environments (Preview)**, set **Configure** to **Yes**. Under **Include**, select **Agent user sessions initiated from endpoints**.
5. Under **Access controls** > **Grant**, select **Grant access** and **Require device to be marked as compliant**, and then select **Select**.
6. Set **Enable policy** to **Report-only**, and then select **Create**.

**Check result**
- The policy includes the condition **Agent user sessions initiated from endpoints**. Agents that don't run on a device are excluded from evaluation.

### 6.4.3 Require a compliant network (endpoint agents only)
Performed by **Conditional Access Administrator**.
1. Create a new policy named `PoC – Agent users – Require compliant network (endpoints)`.
2. Configure the assignments, target resources, and **Agent execution environments (Preview)** as in 6.4.2, steps 2–4.
3. Under **Access controls** > **Grant**, select **Grant access** and **Require compliant network**, and then select **Select**.
4. Set **Enable policy** to **Report-only**, and then select **Create**.

**Check result**
- The policy includes the condition **Agent user sessions initiated from endpoints** and the grant control **Require compliant network**.

## 6.5 Use ID Protection signals for agents
**Documentation:** [ID Protection for agents](https://learn.microsoft.com/entra/id-protection/concept-risky-agents) · [riskyAgent resource type (Microsoft Graph beta)](https://learn.microsoft.com/graph/api/resources/riskyagent?view=graph-rest-beta) · [riskyAgent: confirmCompromised](https://learn.microsoft.com/graph/api/riskyagent-confirmcompromised?view=graph-rest-beta) · [List agentRiskDetections](https://learn.microsoft.com/graph/api/identityprotectionroot-list-agentriskdetections?view=graph-rest-beta) · [Export risk data](https://learn.microsoft.com/entra/id-protection/howto-export-risk-data)

ID Protection supplies the **Agent risk (Preview)** signal used in 6.3 and 6.4.1. All agent risk detections are offline. In on-behalf-of flows, risk is attributed to the user, not the agent. The detection list and incident sequence are in [3.9 Detect and respond with ID Protection](../chapter-03-identity-ownership/README.md#39-detect-and-respond-with-id-protection). This section focuses on how risk feeds Conditional Access.

### 6.5.1 Review risky agents and agent detections
Performed by **Security Reader**.
1. Open <https://entra.microsoft.com> > **ID Protection** > **Dashboard**, and select **View risky agents**. You can also open the **Risky agents** report from the ID Protection menu.
2. Filter by risk level and risk state. Open an agent to see its risk state, risk level, agent type, sponsors, and detections.
3. Open the **Risk detections** report, and select the **Agent detections** tab. Detections are kept for up to 90 days.
4. Optional, with Graph Explorer and the delegated permissions `IdentityRiskyAgent.Read.All` and `IdentityRiskEvent.Read.All` (beta):

   ```http
   GET https://graph.microsoft.com/beta/identityProtection/riskyAgents?$filter=riskLevel eq 'high'
   GET https://graph.microsoft.com/beta/identityProtection/agentRiskDetections
   ```

**Check result**
- The reviewer can open the **Risky agents** report and the **Agent detections** tab.

### 6.5.2 Respond to a risky agent
Performed by **Security Administrator**.

| Action (Risky agents report) | Effect | Graph (beta) |
|---|---|---|
| **Confirm compromise** | Sets risk level to **High** and adds a detection. Triggers policies that block on high agent risk (6.3). | `POST /identityProtection/riskyAgents/confirmCompromised` |
| **Confirm safe** | Sets risk level to **None**. Use it for a false positive. Similar activity isn't flagged again. | `POST /identityProtection/riskyAgents/confirmSafe` |
| **Dismiss risk** | Sets risk level to **None**. Similar activity is still flagged in future. | `POST /identityProtection/riskyAgents/dismiss` |
| **Disable** | Prevents all sign-ins for the agent across Microsoft Entra ID and connected apps. | – |

All three Graph actions take the body `{"agentIds": ["<object ID>"]}` and return `204 No Content`. They require the permission `IdentityRiskyAgent.ReadWrite.All`, and **Security Administrator** is the least-privileged supported role. The IDs can be agent identities, blueprint principals, or agent users.

**Check result**
- The responder can see the actions on a risky agent. The optional test in 6.9 uses them.

### 6.5.3 Export agent risk and sign-in data
Performed by **Security Administrator** (steps 1–2) and a user with permission to access data in the Log Analytics workspace (step 3).

This task is optional. It requires an Azure subscription with a Log Analytics workspace.

1. Open <https://entra.microsoft.com> > **Entra ID** > **Monitoring & health** > **Diagnostic settings**, and select **+ Add diagnostic setting**.
2. Enter a **Diagnostic setting name**, and select the log categories **RiskyAgents**, **AgentRiskEvents**, and **ServicePrincipalSignInLogs**. Under **Destination Details**, select **Send to Log Analytics workspace**, select the **Subscription** and **Log Analytics workspace**, and then select **Save**. Data can take about 15 minutes to appear, and only events from after you enable the setting are exported.
3. In the workspace, run:

   ```kusto
   AADRiskyAgents
   | where TimeGenerated > ago(7d)
   | project TimeGenerated, AgentDisplayName, Id, IdentityType, RiskLevel, RiskState, RiskDetail
   | order by TimeGenerated desc
   ```

   ```kusto
   AADServicePrincipalSignInLogs
   | where TimeGenerated > ago(1d)
   | where ServicePrincipalId in ("<PoC-Agent-Risk ID>", "<PoC-Agent-Approved ID>", "<PoC-Agent-Unapproved ID>")
   | project TimeGenerated, ServicePrincipalName, ServicePrincipalId, ResourceDisplayName, ResultType, ConditionalAccessStatus, ConditionalAccessPolicies
   | order by TimeGenerated desc
   ```

**Check result**
- After the tests in 6.8 and 6.9, `AADServicePrincipalSignInLogs` contains the agent identity sign-ins, and `AADRiskyAgents` contains `PoC-Agent-Risk` if you ran 6.9.

## 6.6 Grant time-bound access with access packages
**Documentation:** [Access packages for agent identities](https://learn.microsoft.com/entra/agent-id/agent-access-packages) · [Create and manage a catalog](https://learn.microsoft.com/entra/id-governance/entitlement-management-catalog-create) · [Change resource roles for an access package](https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-resources) · [Change lifecycle settings for an access package](https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-lifecycle-policy) · [Request access packages on behalf of other identities](https://learn.microsoft.com/entra/id-governance/entitlement-management-request-behalf) · [View, add, and remove assignments](https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-assignments)

Conditional Access decides whether an agent gets a token. Access packages decide what the agent can reach. Access packages for agents support these resource roles:
- Security group membership.
- OAuth API permissions, application or delegated. Certain high-risk Microsoft Graph permissions are blocked for agents.
- Directory roles allowed for agents.

You can't add agent identities and service principals to application roles, SAP roles, or SharePoint Online site roles through access packages. For this reason, you can't reuse an existing access package that contains those roles. Create a new one.

### 6.6.1 Prepare the catalog and the resource
Performed by **Identity Governance Administrator**.

This task uses the security group `PoC-Agent-Resource-Access` from [0.4.2 Create the PoC groups](../chapter-00-prerequisites/README.md#042-create-the-poc-groups). It has assigned (not dynamic) membership and no members at the start.

1. Open <https://entra.microsoft.com> > **ID Governance** > **Catalogs** > **New catalog**. Enter the name `PoC – Agent access` and a description, set **Enabled** to **Yes**, and then select **Create**.
2. Open the catalog, select **Resources** > **Add resources** > **Groups and Teams**, select `PoC-Agent-Resource-Access`, and then select **Add**.

**Check result**
- The catalog lists the group as a resource.

### 6.6.2 Create the access package and the request policy for agents
Performed by **Identity Governance Administrator**.
1. Open <https://entra.microsoft.com> > **ID Governance** > **Entitlement management** > **Access packages** > **New access package**.
2. On **Basics**, enter the name `PoC – Agent resource access` and a description. Under **Catalog**, select `PoC – Agent access`.
3. Select **Next: Resource roles**. Select **Groups and Teams**, select `PoC-Agent-Resource-Access`, and set **Role** to **Member**. Don't add application roles, SAP roles, or SharePoint Online site roles.
   - Optional: to grant API permissions, select **API Permissions**. Choose the source application, select **delegated** or **application**, select the permissions, and then select **Update permissions**. This step requires a **Global Administrator** and marks the catalog as privileged. Users can't receive API permissions, so the policy must be scoped to agents or service principals. Adding directory roles has the same requirements.
4. Select **Next: Requests**. Under **Who can get access**, select **For users, service principals, and agent identities in your directory**. Under **Select specific scope**, select **All agents**.
   - If some agents use plain service principals instead of agent identities, create a second policy later with **All Service principals**.
5. Configure approval: set **How many stages** to **1**. For the first approver, select **Choose specific approvers** > **Add approvers**, and select the PoC approver. Set **Decision must be made in how many days?** to `2`, and set **Require approver justification** to **Yes**.
6. Select **Next: Requestor Information**, and then select **Next: Lifecycle**.
7. Under **Expiration**, set **Access package assignments expire** to **Number of hours** and enter `2`. Select **Show advanced expiration settings**. Set **Allow users to extend access** to **Yes**, and **Require approval to grant extension** to **Yes**.
8. Select **Next: Rules**, then **Next: Review + create**. Fix any validation errors, and then select **Create**.

**Check result**
- The access package shows one policy with the scope **All agents**, one approval stage, and a 2-hour expiration with extension allowed.

### 6.6.3 Assign the access package to an agent (three pathways)
Agents receive access packages in three ways. After a request is submitted, it goes to the approvers configured in the policy.

| Pathway | Who | How |
|---|---|---|
| Agent self-request | The agent identity | Programmatically, by creating an [accessPackageAssignmentRequest](https://learn.microsoft.com/graph/api/entitlementmanagement-post-assignmentrequests) (developer scenario, optional in the PoC) |
| Sponsor or owner request | Sponsor or owner of the agent identity | My Access portal (**Sponsor request** below) |
| Admin direct assignment | Identity Governance Administrator | Microsoft Entra admin center (**Admin direct assignment** below). No approval is needed. |

**Sponsor request**, performed by the **standard test user** (sponsor of `PoC-Agent-Approved`) and the **PoC approver**:
1. Sign in to <https://myaccess.microsoft.com>, and select **Access packages**.
2. Locate `PoC – Agent resource access`, and select **Request**.
3. Under **Request details**, select **Requesting for Sponsored agent** (or **Requesting for Owned agent**).
4. Select `PoC-Agent-Approved`, select **Continue**, enter a justification, and submit the request.
5. As the **PoC approver**, sign in to <https://myaccess.microsoft.com>, and select **Approvals** > **Pending**.
6. Open the request, enter a justification, and approve it.

**Admin direct assignment** (use it for another agent identity, or if the sponsor pathway isn't available), performed by **Identity Governance Administrator**:
1. Open <https://entra.microsoft.com> > **ID Governance** > **Entitlement management** > **Access packages**, and open `PoC – Agent resource access`.
2. Select **Assignments** > **New assignment**.
3. In **Select policy**, select the policy from 6.6.2, and add the agent identity.
4. Optionally set the start and end of the assignment. If you set no end date, the policy's lifecycle settings apply.
5. Enter a justification, select **Add**, and after a few moments select **Refresh**.

**Check result**
- The assignment for `PoC-Agent-Approved` shows the status **Delivered**, and the agent identity is a member of `PoC-Agent-Resource-Access`.

### 6.6.4 Track expiry and sponsor extension
Performed by **Global Reader** (review).

When an assignment belongs to an agent identity with a sponsor, the sponsor is notified as the expiry date approaches. The sponsor can request an extension, if the policy allows it, which starts a new approval cycle. If the sponsor takes no action, the assignment expires automatically on its end date, and the agent identity loses access to the target resources. For a group resource role, the identity is removed from the group when its assignment expires, unless another access package assignment includes the same group.

1. Open <https://entra.microsoft.com> > **ID Governance** > **Entitlement management** > **Access packages**, and open `PoC – Agent resource access`.
2. Select **Assignments**, and review the assignment of `PoC-Agent-Approved`.
3. Select **Policies**, open the policy from 6.6.2, and review its lifecycle (expiration and extension) settings.

**Check result**
- The assignment has an end date. The policy expires assignments after 2 hours and allows extension with approval.

## 6.7 Apply Conditional Access and custom security attributes at publish time (policy templates)
**Documentation:** [Policy templates](https://learn.microsoft.com/microsoft-agent-365/admin/policy-template) · [Agent requests in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-requests) · [Agent actions – Activate agents](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions) · [Agent settings – Apply a template](https://learn.microsoft.com/microsoft-365/admin/manage/agent-settings) · [Conditional Access for agents – Attribute-driven Conditional Access](https://learn.microsoft.com/entra/identity/conditional-access/agent-id?tabs=custom-security-attributes)

An Agent 365 policy template is a collection of predefined governance and security policies that you apply to agents to enforce organizational standards. You select a template when you publish a requested agent or activate an agent. Its policies are applied to that agent.

| Template type | Content |
|---|---|
| Default templates | Predefined policies from Microsoft Entra, Microsoft Purview, SharePoint Online, and Microsoft Defender. There are two default templates: one for all agents except AI teammates, and one for AI teammates in Frontier. Microsoft's built-in default policies appear locked and can't be edited. |
| Custom templates | Extend the default policies with Microsoft Entra policies that you apply case by case. The supported custom policies are **Conditional access**, **Access packages**, and **Custom security attribute**. |

When templates apply:
- Policy templates support only new agent activation. You can't apply a template to agents that are already approved.
- An edited template applies to all new activations. The changes don't affect agents that are already approved.
- To apply policies to existing agents, use an agent management rule with the **Apply template** action. It's a one-time bulk operation that evaluates agents in the registry that have an agent identity. It doesn't apply to agent blueprints or AI teammates.
- A Microsoft Entra policy requires the agent to authenticate with its Microsoft Entra identity when it accesses resources. If the agent doesn't use Entra-based authentication, you can assign the policy, but it might not be enforced at runtime. Work with the agent developer to verify that Entra-based authentication is enabled.

Prerequisites:
- Create every policy in Microsoft Entra first. If a policy doesn't exist yet, you can't select it when you create a template.
- **Conditional access:** only Conditional Access policies that include at least one individual agent identity are visible in the Microsoft 365 admin center when you create a template. A policy scoped to all agent identities is selected automatically in the Microsoft 365 admin center experience and can't be overridden. This applies to the policies from 6.2 and 6.3. Create the selectable policy in 6.7.1.
- **Custom security attribute:** the attribute set `AgentAttributes` and the attribute `AgentApprovalStatus` from 6.2.3 (steps 1–2) must exist. You can also use the `AgentGovernance` attributes from [3.7 Tag agents with custom security attributes](../chapter-03-identity-ownership/README.md#37-tag-agents-with-custom-security-attributes-optional).
- **Access packages (optional):** the access package from 6.6.
- A test agent that a member of your organization submitted for admin approval (for example from Copilot Studio, Microsoft Foundry, or Microsoft 365 Agents Toolkit), as prepared in Chapter 0 (0.6.1). It must be listed in **Agents** > **All agents** > **Requests** in the Microsoft 365 admin center with the state **Pending review**.
- Roles: the Global Administrator and the AI Administrator both need the **Attribute Assignment Administrator** role for custom security attribute policies. The AI Administrator can create and apply access packages, but doesn't have enough privileges for Conditional Access and custom security attributes. Because this section uses both, perform 6.7.2 and 6.7.3 as a **Global Administrator** with **Attribute Assignment Administrator**.

### 6.7.1 Create a Conditional Access policy that the template can select
Performed by **Conditional Access Administrator**.
1. Open <https://entra.microsoft.com> > **Entra ID** > **Conditional Access** > **Policies** > **New policy**.
2. Name: `PoC – Agents – Template – Block high-risk agent identities`.
3. Under **Assignments**, select **Users, agents or workload identities**, and under **What does this policy apply to?**, select **Agents**.
4. Under **Include**, select **Select agent identities**, and select at least one individual agent identity, for example `PoC-Agent-Approved`.
5. Under **Target resources** > **Include**, select **All resources (formerly 'All cloud apps')**.
6. Under **Conditions** > **Agent risk (Preview)**, set **Configure** to **Yes**, and select **High**.
7. Under **Access controls** > **Grant**, select **Block**, and then select **Select**.
8. Set **Enable policy** to **Report-only**, and then select **Create**.

**Check result**
- The policy includes at least one individual agent identity. It doesn't use **All agent identities**.

### 6.7.2 Create the custom policy template
Performed by **Global Administrator** with **Attribute Assignment Administrator**.
1. Open the Microsoft 365 admin center at <https://admin.cloud.microsoft>.
2. In the navigation pane, expand **Agents**.
3. Select **Settings** > **Templates** > **Add a New Template**.
4. Enter the template details:
   1. Template name: `PoC – Agent CA and attributes`.
   2. A description.
   3. Indicate whether this template applies to agents with their own access.
5. Select **Next**, and choose the custom policies to add:
   - **Conditional access**: the policy `PoC – Agents – Template – Block high-risk agent identities` from 6.7.1.
   - **Custom security attribute**: `AgentApprovalStatus` in the attribute set `AgentAttributes`, with the value `IT_Approved`.
   - **Access packages** (optional): `PoC – Agent resource access` from 6.6.
6. Review, and finish adding the template.
7. Select **Save template**.

**Check result**
- The template appears under **Agents** > **Settings** > **Templates** with the selected custom policies. The default policies appear locked.

### 6.7.3 Apply the template when you publish a requested agent
Performed by **Global Administrator** with **Attribute Assignment Administrator**.
1. Sign in to the Microsoft 365 admin center at <https://admin.cloud.microsoft>.
2. Select **Agents** > **All agents** > **Requests**.
3. Select the requested test agent and view its details. Confirm the capabilities, data sources, security and permissions, and custom actions that the agent can invoke.
4. Select **Publish to store** in the agent details pane to open the agent publishing wizard.
5. Select the users or groups that can install the agent. Publishing makes the agent available for installation to the selected audience.
6. (Optional) Select the users or groups who will have the agent preinstalled.
7. Select **Next** to view the template options.
8. Choose the policy template `PoC – Agent CA and attributes`.
9. Select **Next** to review permissions.
10. In the **Review permissions** step, view the permissions requested by the agent, and grant admin consent if appropriate.
11. Select **Next** to complete the process.
12. After you review the agent details, select **Publish**.

For an agent request with the state **Pending activate**, the activation wizard contains the same **Apply a template** step. Choose the custom template there, review the permissions, and select **Finish**.

**Check result**
- The publishing wizard completes with the template `PoC – Agent CA and attributes` selected. Verify the applied policies in 6.8.3.

## 6.8 Test and validation
**Documentation:** [Microsoft Entra Agent ID logs](https://learn.microsoft.com/entra/agent-id/sign-in-audit-logs-agents) · [Conditional Access report-only mode](https://learn.microsoft.com/entra/identity/conditional-access/concept-conditional-access-report-only) · [View, add, and remove assignments](https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-assignments) · [Change resource roles for an access package](https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-resources) · [Policy templates](https://learn.microsoft.com/microsoft-agent-365/admin/policy-template) · [Manage custom security attributes for an application](https://learn.microsoft.com/entra/identity/enterprise-apps/custom-security-attributes-apps)

### 6.8.1 Test the allow list (default deny)
Performed by **Reports Reader**. The agents are exercised by their owners or developers.

Precondition: the default-deny policy from 6.2.2 (or 6.2.3) is in **Report-only**.

1. Exercise `PoC-Agent-Unapproved` and `PoC-Agent-Approved` so that each one requests a token with its own agent identity. For lab agent identities, you can use the community reference script from 6.9.1.
2. Open <https://entra.microsoft.com> > **Entra ID** > **Monitoring & health** > **Sign-in logs**, and select the **Service principal sign-ins** tab.
3. Add the filters **Is Agent** = **Yes** and **Agent type** = **Agent Identity**, open the entry for each agent, and select the **Report-only** tab.
4. Optional, enforced run: do this only in a dedicated PoC tenant, or where every agent that must keep working is excluded (6.2.4). Switch the default-deny policy to **On**, exercise both agents again, and open their entries on the **Conditional Access** tab. Switch the policy back to **Report-only** if required.

**Expected result**
- Report-only run: the policy isn't enforced, so both sign-ins succeed. `PoC-Agent-Unapproved` shows **Report-only: Failure** for `PoC – Agents – Default deny except approved`, and `PoC-Agent-Approved` shows **Report-only: Not applied**.
- Enforced run: the sign-in for `PoC-Agent-Unapproved` fails with `AADSTS53003` (`BlockedByConditionalAccess`), and the **Conditional Access** tab shows the policy with result **Failure**. The sign-in for `PoC-Agent-Approved` succeeds.

### 6.8.2 Test access package expiry
Performed by **Identity Governance Administrator** or **Global Reader**.
1. Right after the assignment in 6.6.3, open the access package and select **Assignments**. Confirm that `PoC-Agent-Approved` is **Delivered**, and record the expiry time.
2. Open <https://entra.microsoft.com> > **Entra ID** > **Groups** > **All groups** > `PoC-Agent-Resource-Access` > **Members**. Confirm that the agent identity is a member.
3. After the expiry time, open **Assignments** again, set the status filter to **Expired**, and confirm the assignment. Select **Download** to export the list.
4. Check the group members again.

**Expected result**
- Before expiry, the assignment is **Delivered** and the agent identity is a member of the group.
- After expiry, the assignment appears in the **Expired** list, and the agent identity is no longer a member of the group. The agent identity loses access to the target resources of the access package.

### 6.8.3 Test the policy template applied at publish time
Performed by **Agent ID Administrator** together with **Attribute Assignment Reader** (steps 1–2), the **standard test user** (step 3), and **Reports Reader** (steps 4–5).
1. Find the agent identity of the agent published in 6.7.3 in **Entra ID** > **Agents** > **Agent identities**, as in [3.4.1 Review the agent identities list](../chapter-03-identity-ownership/README.md#341-review-the-agent-identities-list), and record its object ID.
2. With the delegated permissions `AgentIdentity.Read.All` and `CustomSecAttributeAssignment.Read.All`, run the attribute filter from [3.7.3 Filter agents by attribute](../chapter-03-identity-ownership/README.md#373-filter-agents-by-attribute) with the attribute from the template:

   ```http
   GET https://graph.microsoft.com/v1.0/servicePrincipals/microsoft.graph.agentIdentity?$count=true&$select=id,displayName,customSecurityAttributes&$filter=customSecurityAttributes/AgentAttributes/AgentApprovalStatus eq 'IT_Approved'
   ConsistencyLevel: eventual
   ```

3. Use the published agent.
4. Open <https://entra.microsoft.com> > **Entra ID** > **Monitoring & health** > **Sign-in logs**, and add the filters **Is Agent** = **Yes** and **Agent type** = **Agent Identity**. Check the **Service principal sign-ins** tab and the user sign-in tabs.
5. Open a sign-in entry of the published agent's agent identity, and select the **Conditional Access** and **Report-only** tabs.

**Expected result**
- The query in step 2 returns the object ID recorded in step 1, with `AgentApprovalStatus` = `IT_Approved`.
- The sign-in details of the published agent's agent identity show the evaluation result for `PoC – Agents – Template – Block high-risk agent identities`.
- If you use the attribute-based default-deny policy (6.2.3), the published agent is excluded from it by its `IT_Approved` value, and its sign-in shows **Report-only: Not applied** for that policy.
- Microsoft Entra policies in a template require the agent to authenticate with its Microsoft Entra identity. If the agent doesn't use Entra-based authentication, the policies might not be enforced at runtime. Work with the agent developer to verify that Entra-based authentication is enabled (6.7).

## 6.9 Test the risk-based block with the agent token flow (optional)
**Documentation:** [Agent autonomous app OAuth flow](https://learn.microsoft.com/entra/agent-id/agent-autonomous-app-oauth-flow) · [Authenticate and acquire tokens for autonomous agents](https://learn.microsoft.com/entra/agent-id/identity-platform/autonomous-agent-request-tokens) · [riskyAgent: confirmCompromised](https://learn.microsoft.com/graph/api/riskyagent-confirmcompromised?view=graph-rest-beta) · [Microsoft Entra Agent ID logs](https://learn.microsoft.com/entra/agent-id/sign-in-audit-logs-agents) · [Microsoft Entra authentication and authorization error codes](https://learn.microsoft.com/entra/identity-platform/reference-error-codes)

**Community reference (not Microsoft documentation):** [Conditional Access for Agents: Blocking Agent Identities with Risk and Custom Security Attributes](https://derkvanderwoude.medium.com/conditional-access-for-agents-blocking-agent-identities-with-risk-and-custom-security-attributes-2ec3d6bf995b) · sample script [AgentID-AuthenticationFlow.ps1](https://github.com/Blue161616/Agent-Identity/blob/main/AgentID-AuthenticationFlow.ps1)

This optional test proves the policy from 6.3 end to end. It follows the community lab article above. You mark a lab agent identity as compromised, run the autonomous agent token flow with the community sample script, and confirm the block in the sign-in log.

The autonomous agent flow, as documented on Microsoft Learn, has two token requests:
1. **T1 – blueprint token request.** The agent identity blueprint presents its credential in a `client_credentials` request with `scope=api://AzureADTokenExchange/.default` and `fmi_path=<agent identity client ID>`. Conditional Access doesn't apply to this intermediate token exchange.
2. **T2 – agent identity token request.** The agent identity sends a `client_credentials` request with `client_id=<agent identity client ID>` and the resource scope, and presents T1 as `client_assertion` with `client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer`. Conditional Access protects this token acquisition by the agent identity.

Microsoft Learn states that client secrets shouldn't be used as client credentials for agent identity blueprints in production. The community script uses a blueprint client secret, so run it only against a lab blueprint.

Precondition: the policy from 6.3 is **On**. `PoC-Agent-Risk` and `PoC-Agent-Approved` are excluded from the default-deny policy (6.2).

### 6.9.1 Prepare the community reference script
Performed by the **owner of the lab agent identity blueprint**.
1. Open the community sample script [AgentID-AuthenticationFlow.ps1](https://github.com/Blue161616/Agent-Identity/blob/main/AgentID-AuthenticationFlow.ps1) and review it before you use it.
2. In its configuration block, set `$tenantId`, `$blueprintAppId`, and `$blueprintClientSecret` for the lab blueprint. The script doesn't run while placeholders are still in place.
3. Note how the script works. It takes `-AgentIdentityClientId <agent identity ID>`, requests T1 with `fmi_path`, and then requests T2 for `https://graph.microsoft.com/.default`. It reports one of these results for T2:
   - `[BLOCKED]`: Conditional Access denied the token (`AADSTS53003`).
   - `[FAIL]`: T2 failed for a reason other than Conditional Access.
   - `[WARN]`: the agent obtained a token, so Conditional Access didn't block it.

**Check result**
- Running the script for `PoC-Agent-Approved` prints `[OK] Blueprint authenticated - T1 obtained` and a T2 result.

### 6.9.2 Mark the test agent as compromised
Performed by **Security Administrator**.
1. In Graph Explorer, sign in, consent to `IdentityRiskyAgent.ReadWrite.All`, and send:

   ```http
   POST https://graph.microsoft.com/beta/identityProtection/riskyAgents/confirmCompromised
   Content-Type: application/json

   { "agentIds": [ "<PoC-Agent-Risk ID>" ] }
   ```

   The response is `204 No Content`. Alternatively, open **ID Protection** > **Risky agents**, select the agent, and select **Confirm compromise**.
2. Read the risk state:

   ```http
   GET https://graph.microsoft.com/beta/identityProtection/riskyAgents/<PoC-Agent-Risk ID>
   ```

3. Record the time (UTC).

**Check result**
- `riskLevel` is `high` and `riskState` is `confirmedCompromised`. Confirm compromise triggers risk-based Conditional Access policies that are configured to block on high agent risk.

### 6.9.3 Run the token flow for the risky agent and the control agent
Performed by the **owner of the lab agent identity blueprint**.
1. Run the script for the risky agent:

   ```powershell
   .\AgentID-AuthenticationFlow.ps1 -AgentIdentityClientId <PoC-Agent-Risk ID>
   ```

2. Run the script for the control agent:

   ```powershell
   .\AgentID-AuthenticationFlow.ps1 -AgentIdentityClientId <PoC-Agent-Approved ID>
   ```

3. Save the console output of both runs.

**Expected result**
- `PoC-Agent-Risk`: T1 is obtained, and T2 returns `[BLOCKED]` with `AADSTS53003`.
- `PoC-Agent-Approved`: T1 is obtained, and the T2 result isn't `[BLOCKED]`.

### 6.9.4 Confirm the block in the sign-in log
Performed by **Reports Reader**.
1. Open <https://entra.microsoft.com> > **Entra ID** > **Monitoring & health** > **Sign-in logs**, and select the **Service principal sign-ins** tab.
2. Set the date range to include the test, and add the filters **Is Agent** = **Yes** and **Agent type** = **Agent Identity**.
3. Open the entry for `PoC-Agent-Risk` at the recorded time, and select the **Conditional Access** tab.
4. Open the entry for `PoC-Agent-Approved`, and select the **Conditional Access** tab.
5. Optional, with Graph Explorer and `AuditLog.Read.All` (beta):

   ```http
   GET https://graph.microsoft.com/beta/auditLogs/signIns?$filter=signInEventTypes/any(t: t eq 'servicePrincipal') and agent/agentType eq 'agenticAppInstance'
   ```

**Expected result**
- `PoC-Agent-Risk`: the sign-in failed, and `PoC – Agents – Block high-risk agent identities` shows the result **Failure**.
- `PoC-Agent-Approved`: the risk policy doesn't block the sign-in. This proves that the policy acts on risk, not on identity.
- If the risk policy is in **Report-only**, it isn't enforced. The entry for `PoC-Agent-Risk` then shows **Report-only: Failure** on the **Report-only** tab.

### 6.9.5 Reset the test agent's risk
Performed by **Security Administrator**.
1. Reset the risk with **Dismiss risk** or **Confirm safe**. You can use **ID Protection** > **Risky agents** > select the agent, or Graph:

   ```http
   POST https://graph.microsoft.com/beta/identityProtection/riskyAgents/dismiss
   Content-Type: application/json

   { "agentIds": [ "<PoC-Agent-Risk ID>" ] }
   ```

   **Confirm safe** (`/confirmSafe`, same body) tells the system to avoid flagging similar activity. **Dismiss risk** keeps flagging similar activity. Both set the risk level to none.
2. Read `riskyAgents/<PoC-Agent-Risk ID>` again.

**Check result**
- `riskLevel` is `none`.

## 6.10 Evidence
- **Policies (6.2–6.4, 6.7.1):** screenshots of each Conditional Access policy, or its JSON from Microsoft Graph (`GET https://graph.microsoft.com/beta/identity/conditionalAccess/policies/{id}`, permission `Policy.Read.All`), showing the name, assignments, conditions, grant control, and state. Include the default-deny policy with its final state (6.2.4), the high-risk policy (**On**), the template policy, and the agent-user policies if in scope.
- **Allow list (6.8.1):** sign-in log details (the **Conditional Access** and **Report-only** tabs) for `PoC-Agent-Unapproved` and `PoC-Agent-Approved`.
- **Access package (6.6, 6.8.2):** the policy summary (scope **All agents**, one approval stage, 2-hour expiration, extension with approval), the approval record from My Access, the assignment list exported as **Delivered** and then **Expired**, and the group members of `PoC-Agent-Resource-Access` before and after expiry.
- **Policy template (6.7, 6.8.3):** a screenshot of the template under **Agents** > **Settings** > **Templates** with its custom policies, a screenshot of the template step in the publishing wizard, the output of the attribute query, and the sign-in log details of the published agent showing the template's Conditional Access policy.
- **Optional risk test (6.9):**
  - the `confirmCompromised` request with its `204` response, and the `riskyAgents/<id>` response showing `riskLevel` = `high`;
  - the console output of the community script for `PoC-Agent-Risk` and `PoC-Agent-Approved`;
  - the sign-in log details showing the risk policy with result **Failure**;
  - the **Risky agents** report before and after the reset.
- **Optional export (6.5.3):** the results of the KQL queries.
## 6.11 Troubleshooting
| Symptom | Likely cause | Fix |
|---|---|---|
| A policy has no blocking effect | Policy is in **Report-only**, which evaluates but doesn't enforce | Check the **Report-only** tab for the result. Switch to **On** to enforce. |
| Policy doesn't apply to an agent's user account | Policy targets agent identities (or a blueprint), which don't cover agent users | Create a separate agent-user policy (6.4). |
| Existing **All users** policies don't affect agent users | **All users** doesn't include agents' user accounts | Target **All agent users (Preview)** or select agent users. Group-based targeting isn't supported. |
| Delegated (on-behalf-of) agent isn't affected by agent policies | In delegated access, the token subject is the user | Use user-targeted policies for that access pattern. |
| Unapproved agent shows **Report-only: Not applied** | Agent is excluded directly, through its blueprint, or through a custom security attribute | Review the exclusions and the agent's attribute values. |
| No agent entries in the sign-in log | Wrong tab or missing filters | Use **Service principal sign-ins** with **Is Agent** = **Yes** and **Agent type** = **Agent Identity**. |
| Community script: T1 fails | Wrong blueprint app ID or secret, or `fmi_path` isn't a child agent identity of this blueprint (a blueprint can only impersonate its own child agent identities) | Check the IDs in **Entra ID** > **Agents** > **Agent identities** ([3.4.1](../chapter-03-identity-ownership/README.md#341-review-the-agent-identities-list)) and the blueprint credential. |
| Community script: `[WARN]` for `PoC-Agent-Risk` after confirm compromise | Risk policy in **Report-only**; agent excluded from the risk policy; or the policy targets agent users instead of agent identities | Check the policy state and assignments, and check that `riskyAgents/<id>` shows `riskLevel` = `high`. |
| A blueprint token-exchange sign-in succeeds while the agent identity is blocked | Conditional Access doesn't apply to the intermediate token exchange | Evaluate the agent identity's sign-in entry. |
| Attribute isn't selectable in the policy | Missing **Attribute Definition Reader** role, or the attribute isn't of type string | Assign the role, and use a string attribute. |
| Device or network policy blocks cloud-hosted agents | **Agent execution environments (Preview)** isn't configured | Include only **Agent user sessions initiated from endpoints**. |
| Can't add API permissions or directory roles to the access package | You aren't a Global Administrator; the policy isn't scoped to agents or service principals; or the permission is blocked for agents | Use a Global Administrator, scope the policy to **All agents**, or choose another permission. |
| Existing access package can't be used for agents | It contains application, SAP, or SharePoint Online site roles | Create a new access package (6.6.2). |
| Sponsor doesn't see **Requesting for Sponsored agent** | The user isn't a sponsor or owner of the agent identity | Assign the sponsor (Chapter 3.5.1). |
| Agent identity can't be assigned in **New assignment** | The identity isn't eligible under the selected policy | Select the policy with **For users, service principals, and agent identities in your directory** > **All agents**. |
| Conditional Access policy isn't listed when you create the template | The policy doesn't include at least one individual agent identity, or it wasn't created in Microsoft Entra first | Create the policy with **Select agent identities** and at least one agent identity (6.7.1). |
| Policies from 6.2 and 6.3 are selected in the template and can't be removed | Policies scoped to all agent identities are selected automatically and can't be overridden | No action needed. Use **Select agent identities** for policies that you want to choose per template. |
| Conditional access or custom security attribute policies can't be added to the template | The admin is an AI Administrator, or lacks **Attribute Assignment Administrator** | Use a Global Administrator who also has **Attribute Assignment Administrator**. |
| An edited template doesn't change an agent that's already published | Templates apply only to new activations | Use an agent management rule with the **Apply template** action (agents with an agent identity). |
| Template's Entra policies have no effect on the published agent | The agent doesn't authenticate with its Entra identity | Work with the agent developer to enable Entra-based authentication. |

## 6.12 Cleanup
Perform the cleanup in this order, because the policy template references the Conditional Access policy, the attribute, and the access package.

1. If you ran 6.9, confirm that 6.9.5 is complete and `PoC-Agent-Risk` no longer shows as at risk (**Security Administrator**).
2. Delete the policy template (**Global Administrator**). In the Microsoft 365 admin center, expand **Agents**, go to **Settings** > **Templates**, select the template, select a policy to delete, and select **Delete**.
3. If the agent from 6.7.3 was published only for the PoC, block it as in [5.3.1 Block or unblock an agent](../chapter-05-lifecycle-audit/README.md#531-block-or-unblock-an-agent) or delete it as in [5.8.1 Delete an agent (soft delete)](../chapter-05-lifecycle-audit/README.md#581-delete-an-agent-soft-delete).
4. Remove the `AgentApprovalStatus` value from the published agent and from the lab agent identities (**Attribute Assignment Administrator**). Use the `PATCH` method from 6.2.3 with an empty value list:

   ```json
   {
     "customSecurityAttributes": {
       "AgentAttributes": {
         "@odata.type": "#Microsoft.DirectoryServices.CustomSecurityAttributeValue",
         "AgentApprovalStatus": []
       }
     }
   }
   ```

5. Deactivate the attribute `AgentApprovalStatus` if you created it (**Attribute Definition Administrator**). Attribute sets and attribute definitions can't be deleted.
6. Set the PoC Conditional Access policies to **Off**, or delete them (**Conditional Access Administrator**). This includes the default-deny policies, the high-risk policy, the agent-user policies, and `PoC – Agents – Template – Block high-risk agent identities`. Save the JSON of any policy the customer wants to reuse first (6.10). Keep the default-deny policy in **Report-only** only if the customer adopts it.
7. Remove the access package assignments: open the access package, select **Assignments**, select the agent identity, and select **Remove**. Then delete the access package and the catalog `PoC – Agent access` (**Identity Governance Administrator**). Delete the group `PoC-Agent-Resource-Access` (**Groups Administrator**) if no other test uses it.
8. Delete the diagnostic setting from 6.5.3 if you created it only for the PoC (**Security Administrator**).
9. Remove the lab client secret from the blueprint, delete your local copy of the community script (it contains the secret), and revoke the Graph Explorer consent if it isn't needed (**owner of the lab agent identity blueprint**).
10. Delete the lab agent identity blueprint, or keep it for later chapters (**Cloud Application Administrator** or the owner of the blueprint). Deleting the agent identities isn't supported in the Microsoft Entra admin center. Use Microsoft Graph with `Application.ReadWrite.All`:

    ```http
    DELETE https://graph.microsoft.com/v1.0/applications/{blueprint-app-object-id}
    ```

    Deleting the blueprint soft-deletes its child agent identities automatically. Soft-deleted objects are permanently deleted after 30 days.

**Check result**
- No PoC Conditional Access policy is **On** unless the customer adopted it. The template, the access package, and the catalog no longer exist, and no PoC agent identity carries `AgentApprovalStatus`.
---
Previous: [Chapter 5 – Agent Lifecycle and Audit](../chapter-05-lifecycle-audit/README.md) · Next: [Chapter 7 – Sensitive Data Protection (Purview)](../chapter-07-sensitive-data-protection/README.md)
