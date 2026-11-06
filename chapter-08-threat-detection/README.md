# Chapter 8 - Threat detection and runtime protection (Defender)

**Pillar:** Secure
**What it proves:** The SOC can investigate AI agent activity in Microsoft Defender, correlate a detected threat with its agent and incident, review the registry risk signal, and contain the agent. Optional blocking tests verify enforcement separately from detection.

**Success criteria:** Agree the selected outcomes in [What you proved](#-what-you-proved) before testing.

## Topics and time guide

Approximate hands-on estimates after the [prerequisites](prerequisites.md) are complete. Preparation estimates are on that page; service waiting time is separate.

| Topic | Estimated hands-on time |
|---|---|
| [8.1 Required permissions](#81-required-permissions) | ~5 min |
| [8.2 Review agent risk in the Agent 365 registry](#82-review-agent-risk-in-the-agent-365-registry) | ~5-10 min |
| [8.3 Review the AI agent inventory in Defender](#83-review-the-ai-agent-inventory-in-defender) | ~5-10 min |
| [8.4 Hunt for agent activity with Advanced Hunting](#84-hunt-for-agent-activity-with-advanced-hunting) | ~10-15 min |
| [8.5 Test runtime protection end to end](#85-test-runtime-protection-end-to-end) | ~15-25 min |
| [8.6 Test local runtime protection (optional)](#86-test-local-runtime-protection-optional) | ~10-15 min |
| [8.7 Evidence](#87-evidence) | ~5-10 min |
| [8.8 Troubleshooting](#88-troubleshooting) | As needed |

[Outcome checklist](#-what-you-proved) · [References](#references)

---

## 8.1 Required permissions

Use the [shared account and role-assignment model](../README.md#least-privilege-model) with the task-specific permissions below.

| Task | Least-privilege role | Section |
|---|---|---|
| View the Agent 365 registry, **Agents at risk**, and **Risk details** | AI Reader, Global Reader, or Security Reader | 8.2, 8.5.5 |
| Open the Microsoft Defender deep link from **Risk details** | Global Reader, Security Reader, Security Administrator, or AI Administrator | 8.2.2 |
| Block or unblock an agent in the registry | AI Administrator | 8.2.3, 8.5.6 |
| Manage alert status and classification | Security Operator | 8.5.4, 8.5.6, 8.5.7 |
| Enable or disable the prepared test-agent blocking rule during a test pass | Security Administrator | 8.5.3, 8.5.7 |
| Run the test scenarios | Standard test user | 8.5.3, 8.5.7 |
| Validation / read-only review: Advanced Hunting, alerts, Defender views opened from the registry | Security Reader | 8.6, 8.3, 8.4, 8.5.4 |

**Before you start:**
- [ ] Complete the [chapter prerequisites](prerequisites.md), including setup permissions, connections, protection rules, and approved test inputs. This page contains testing only.

---

## 8.2 Review agent risk in the Agent 365 registry
**Documentation:** [Agent Registry in Microsoft 365 admin center – Agent risks](https://learn.microsoft.com/microsoft-365/admin/manage/agent-registry#agent-risks) · [Governance and lifecycle actions for agents – Block or unblock agents](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions#block-or-unblock-agents) · [Agent management roles and permissions](https://learn.microsoft.com/microsoft-365/admin/manage/agent-roles-perms)

Risk signals in the Agent Registry are a consolidated set of agent-related security detections from multiple security platforms. IT administrators can understand what is flagged without switching between portals or elevating their permissions to different security roles, and share the details with the security team for investigation and remediation. Risk signal counts might be up to an hour behind what the security portals show, and reflect active risk signals. The Registry baseline, including the **Agents at risk** tile, is recorded in [1.3.4 Review risk signals](../chapter-01-agent-discovery/README.md#134-review-risk-signals); this section focuses on investigating and containing a flagged agent.

### 8.2.1 Open Agents at risk
Performed by **AI Reader**, **Global Reader**, or **Security Reader**.
1. Sign in to the Microsoft 365 admin center at `https://admin.cloud.microsoft`.
2. Go to **Agents** > **Overview** and review the **Agents at risk** card. It lists the three agents with the highest aggregated risk counts. Select **View agents** to open **All agents** > **Registry**, filtered and sorted by risk level.
3. Alternatively, go to **Agents** > **All agents** > **Registry** and select the **Agents at risk** tile. It opens a prefiltered view of agents with one or more risk signals.
4. Review the **Risks** column. It shows the aggregated count of risk signals for each agent.

**Check result**
- You can see the **Agents at risk** tile and the **Risks** column. A count of zero means that no active signals are currently detected for that agent.

### 8.2.2 Review risk details for a flagged agent
Performed by **AI Reader**, **Global Reader**, or **Security Reader**.
1. In the registry, select the count in the **Risks** column for a flagged agent. The **Risk details** pane opens.
2. Review the risk signals, grouped into expandable high, medium, and low severity sections, with a description and an **Occurrences** count for each signal.
3. Review **Risk signals are sourced from**. It shows the Microsoft security platforms contributing risk signals for the agent, such as Microsoft Purview, Microsoft Entra, and Microsoft Defender. Only platforms with contributing signals are shown.
4. If the agent has multiple instances, drill down into the signals for the selected instance.
5. Select a platform name to follow the deep link into that portal. The Microsoft Defender deep link requires Global Administrator, Global Reader, Security Reader, Security Administrator, or AI Administrator.

**Check result**
- For one agent, you can show which platforms contributed its risk signals and open the corresponding portal.

> Purview risk signals come from the Insider Risk Management agent policy verified in [7.8 Insider Risk Management verification](../chapter-07-sensitive-data-protection/README.md#78-insider-risk-management-verification). Entra ID Protection for agents is covered in [3.9 Detect and respond with ID Protection](../chapter-03-identity-ownership/README.md#39-detect-and-respond-with-id-protection). The Microsoft Purview IRM alerts deep link requires IRM Analyst or IRM Investigator; Global Administrator alone is insufficient.

### 8.2.3 Block a risky agent from the registry
Performed by **AI Administrator**.

Use this procedure for containment in 8.5.6.
1. Sign in to the Microsoft 365 admin center and select **Agents** > **All agents**.
2. Select the agent from the list.
3. In the agent details pane, immediately under the agent's name, select **Block**.
4. In the **Block agent** pane, select **Block agent**, then select **Save**.

To unblock, select **Unblock** in the agent details pane, then in the **Unblock agent** pane select **Unblock agent** and **Save**.

Blocking an agent restricts access to it across the organization, preventing any user from using it. For agents created with Microsoft Copilot Agent Builder and Microsoft Copilot Studio, blocking affects availability and functionality in Microsoft Copilot and in other host products, such as Outlook and Teams. Blocking an agent created with SharePoint or Microsoft Foundry only affects its availability in Microsoft Copilot Chat.

**Check result**
- The agent details pane now offers **Unblock** for the agent.

> Ownerless agents are handled in [5.5 Govern ownerless agents](../chapter-05-lifecycle-audit/README.md#55-govern-ownerless-agents). Blocking and unblocking in the lifecycle context is covered in [5.3.1 Block or unblock an agent](../chapter-05-lifecycle-audit/README.md#531-block-or-unblock-an-agent).

---

## 8.3 Review the AI agent inventory in Defender
**Documentation:** [Discover AI agents and assess security posture using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-inventory) · [AI agent posture risk in Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-risk-assessment)

Microsoft Defender provides a centralized inventory of AI agents and assesses their security posture. The inventory includes agents built with Microsoft Copilot Studio, Microsoft Foundry, Microsoft 365, and supported non-Microsoft platforms, and local AI agents discovered on endpoint devices.

### 8.3.1 Open the AI agents inventory
Performed by **Security Reader**.
1. Sign in to the Microsoft Defender portal at `https://security.microsoft.com`.
2. In the left navigation pane, select **Assets** > **AI agents**, then select the **Agents** tab.
3. Review the risk-related columns:
   - **Risk level**: the overall risk level calculated from the agent's active risk indicators: **High**, **Medium**, **Low**, **No known risk**, or **Not evaluated**.
   - **Risk indicators**: the conditions contributing to the agent's risk level. Examples include **Weak Instructions**, **High-usage Agent**, **Indirect Prompt Injection Exposure**, **Privileged Business-system Access**, and **Active Threat** (active security alerts are associated with the agent).
   - **Recommendations**: the number and severity of active security recommendations for the agent.
   - **Active alerts**: the number and severity of active alerts associated with the agent.
4. Use the filter bar to narrow the inventory by properties such as **Agent name**, **Platform**, **Publish status**, **Risk level**, or **Risk indicators**. Select **Customize columns** to add, remove, or reorder columns.
5. Filter on the Copilot Studio test agent and the other PoC agents.

**Check result**
- The PoC agents are listed in the inventory.

> Not all risk indicators apply to all agent platforms. Defender assesses an indicator only when the required platform support and data are available.

### 8.3.2 Review the agent details pane and agent page
Performed by **Security Reader**.
1. Select the Copilot Studio test agent to open its details pane. The pane displays the risk and configuration information available for the agent.
2. Select **Open Agent page**. The **Overview** tab shows the security and configuration information available for the agent, which can include risk level and active risk indicators, agent configuration details, identity and authentication information, endpoint and user context, attack-surface relationships, active alerts, security recommendations, tools, and MCP servers.
3. Record the agent's risk level and risk indicators as the baseline before the test in 8.5.

A risk indicator isn't always something that can be remediated; it might reflect the agent's intended purpose or design.

### 8.3.3 Review recommendations and incidents for the agent
Performed by **Security Reader**.
1. On the agent page, select **Security recommendations**. Select a recommendation to review its description and supporting evidence on the **Overview** tab, corrective actions on the **Remediation steps** tab, and affected agents on the **Exposed assets** tab.
2. Select **Incidents and alerts** to review security incidents and alerts associated with the agent. Select an incident to open its details pane, or select **Open incident page** for the full investigation experience.

The available tabs depend on the agent platform and the security information associated with the agent.

**Check result**
- You can open the **Security recommendations** and **Incidents and alerts** tabs for the test agent, where available.

> Recommendations are determined separately from the risk level. A high-risk agent might have no recommendations, and a lower-risk agent might receive one. Review risk level and recommendations together.

---

## 8.4 Hunt for agent activity with Advanced Hunting
**Documentation:** [Detect and investigate threats to AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection) · [Advanced hunting overview](https://learn.microsoft.com/defender-xdr/advanced-hunting-overview) · [AgentsInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-agentsinfo-table) · [CloudAppEvents table](https://learn.microsoft.com/defender-xdr/advanced-hunting-cloudappevents-table) · [BehaviorInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-behaviorinfo-table) · [AlertInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-alertinfo-table) · [AlertEvidence table](https://learn.microsoft.com/defender-xdr/advanced-hunting-alertevidence-table) · [Troubleshoot Direct OTel Observability – Defender advanced-hunting query](https://learn.microsoft.com/microsoft-agent-365/developer/direct-open-telemetry-troubleshooting) · [Create custom detection rules](https://learn.microsoft.com/defender-xdr/custom-detection-rules) · [Manage existing custom detection rules](https://learn.microsoft.com/defender-xdr/custom-detection-manage)

| Table | Contents for AI agent investigation |
|---|---|
| `AgentsInfo` | Inventory and configuration details for AI agents, including agent identity, platform, ownership, and metadata (replaces `AIAgentsInfo`) |
| `CloudAppEvents` | Agent 365 observability data for AI agent activity, including agent actions, tool invocations, and data access events |
| `BehaviorInfo` | Behaviors that record real-time protection rule activity, including audit and block events |
| `AlertInfo` | Alert metadata, including alerts related to near-real-time detections |
| `AlertEvidence` | Entities and artifacts associated with alerts |

Go to **Investigation & response** > **Hunting** > **Advanced hunting**. To use the prebuilt queries maintained by Microsoft, select the **Queries** tab, and then select **AI Agents**. Security Reader grants full read access to advanced hunting data.

### 8.4.1 Query the agent inventory
Performed by **Security Reader**.

The `AgentsInfo` table stores multiple snapshots of each agent over time. Use `arg_max(Timestamp, *)` to return the latest state of each agent.

```kql
AgentsInfo
| summarize arg_max(Timestamp, *) by AgentId
| where LifecycleStatus != "Deleted"
| project Timestamp, Name, Platform, PublishedStatus, LifecycleStatus, Availability,
          Owners, InstanceCount, Model, CreatedDateTime, EntraAgentID, SourceAgentId
| sort by CreatedDateTime desc
```

**Expected result**
- The PoC agents are listed. `PublishedStatus` is `Draft` or `Published`; `LifecycleStatus` is `Active`, `Blocked`, `Uninstalled`, or `Deleted`.
- Record the `AgentId`, `EntraAgentID`, and `SourceAgentId` of the Copilot Studio test agent.

### 8.4.2 Hunt for weak agent configuration
Performed by **Security Reader**.

This query lists active agents with no system prompt in `Instructions`, together with their guardrails, tools, and MCP servers for review.

```kql
AgentsInfo
| summarize arg_max(Timestamp, *) by AgentId
| where LifecycleStatus == "Active"
| where isempty(Instructions)
| project Name, Platform, PublishedStatus, Availability, Guardrails, DeclaredTools,
          McpServers, Owners, CreatedDateTime, EntraAgentID
```

**Expected result**
- A clean environment can return no rows. Review any returned agent with its owner, and compare with the **Weak Instructions** risk indicator in 8.3.1.

> To find and govern ownerless agents, use [5.5 Govern ownerless agents](../chapter-05-lifecycle-audit/README.md#55-govern-ownerless-agents).

### 8.4.3 Trace agent activity in CloudAppEvents
Performed by **Security Reader**.

List the activity recorded for the standard test user after they used the agent (replace the object ID):

```kql
CloudAppEvents
| where Timestamp > ago(1d)
| where AccountObjectId == "<standard test user object ID>"
| summarize Events = count() by Application, ActionType
| sort by Events desc
```

Trace agent invocations, inference calls, and tool executions (action types and `RawEventData` fields as documented in the Agent 365 Defender advanced-hunting query):

```kql
CloudAppEvents
| where Timestamp > ago(1d)
| where ActionType in ("InvokeAgent", "InferenceCall", "ExecuteToolBySDK", "ExecuteToolByGateway", "ExecuteToolByMCPServer")
| extend resData = parse_json(tostring(RawEventData))
| extend AgentId = tostring(resData.AgentId),
         TargetAgentId = tostring(resData.TargetAgentId),
         PlatformTargetAgentId = tostring(resData.PlatformTargetAgentId)
| project Timestamp, ActionType, AccountDisplayName, AccountObjectId, IPAddress,
          AgentId, TargetAgentId, PlatformTargetAgentId, ReportId
| sort by Timestamp desc
```

**Expected result**
- Rows for the test user's activity with the agent are returned. Record the agent identifier from `AgentId`, `TargetAgentId`, or `PlatformTargetAgentId` for the test agent; 8.4.5 uses it.
- No unexpected users or IP addresses appear.

### 8.4.4 Query alerts and real-time protection events
Performed by **Security Reader**.

Alerts in which the standard test user is an evidence entity:

```kql
let testUser = "<standard test user UPN>";
AlertEvidence
| where Timestamp > ago(1d)
| where AccountUpn =~ testUser
| distinct AlertId
| join kind=inner (AlertInfo | where Timestamp > ago(1d)) on AlertId
| project Timestamp, AlertId, Title, Category, Severity, ServiceSource, DetectionSource
| sort by Timestamp desc
```

Entities and artifacts associated with one alert:

```kql
AlertEvidence
| where AlertId == "<AlertId from the previous query>"
| project Timestamp, EntityType, EvidenceRole, AccountUpn, Application, OAuthApplicationId,
          CloudResource, AdditionalFields
```

Recent behaviors, including real-time protection audit and block events:

```kql
BehaviorInfo
| where Timestamp > ago(1d)
| project Timestamp, BehaviorId, ActionType, Title, Description, Categories,
          ServiceSource, DetectionSource, AccountUpn, AdditionalFields
| sort by Timestamp desc
```

**Expected result**
- After the audit pass in 8.5.3, the first query returns the alerts from the test.
- After the optional blocking pass, `BehaviorInfo` returns the block events.

### 8.4.5 Validate a custom detection (optional)
Performed by **standard test user** (activity) and **Security Reader** (review).

1. Confirm the [custom detection prerequisite](prerequisites.md#prepare-a-custom-detection-rule-optional) is complete.
2. Run an agreed benign prompt that invokes the selected tool on the PoC agent. Record the time and confirm the tool execution in 8.4.3.
3. Open **Hunting** > **Custom detection rules**, select the prepared rule, and review **Triggered alerts** after its scheduled run.

**Expected result**
- A triggered alert correlates with the test agent and tool execution. A successful benign tool call isn't itself evidence of a malicious action.


---

## 8.5 Test runtime protection end to end
**Documentation:** [Detect and investigate threats to AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection) · [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection) · [Enable external threat detection and protection for Copilot Studio custom agents – How it works](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider#how-it-works) · [Orchestrate agent behavior with generative AI](https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions)

Use the audit pass to validate detection, incident correlation, registry risk, and containment for the Copilot Studio test agent. Use the optional blocking pass to validate enforcement and behavior telemetry separately; a blocking rule suppresses near-real-time detection alerts for the covered agent.

Microsoft Defender detects threats such as jailbreak attempts, indirect prompt injection (XPIA) attempts, malicious content propagation, secret and credential leakage, evasion techniques, large language model (LLM) reconnaissance, and suspicious user or IP access.

### 8.5.1 Verify test readiness
Performed by **Security Reader** with the **standard test user**.

1. Review the completed [test preparation and baselines](prerequisites.md#prepare-test-cases-and-baselines).
2. Confirm the agreed test account can open the agent and that the selected audit or blocking mode matches the planned pass.

**Expected result**
- The test starts from the recorded baseline with approved prompts. Stop and resolve unmet prerequisites before proceeding.


### 8.5.2 Test scenarios
The PoC team provides the prompts. Use only the test agent, the standard test user, and test data.

| # | Scenario | Prompt | Expected result |
|---|---|---|---|
| 1 | Indirect prompt injection via knowledge document | `<to be added>` | Audit: verify a matching detection and agent activity. Block: verify enforcement only if a tool invocation matches the selected rule |
| 2 | Direct prompt injection / jailbreak | `<to be added>` | Verify a matching detection if the attempt reaches Defender; a built-in agent refusal alone doesn't prove Defender enforcement |
| 3 | Data exfiltration via tool call | `<to be added>` | Audit: verify matching activity. Block: verify that a tool invocation matching the selected detection type is stopped |
| 4 | Benign control prompt that uses the same tool | `<to be added>` | The agent proceeds with no visible effect or interruption |

Use the agreed prompts from the prerequisites; placeholders aren't runnable test cases. Map blocking tests to the supported detection types: **Malicious content propagation**, **Secret exfiltration**, **Evasion techniques**, or **Unsafe email domain**. For Copilot Studio, external protection evaluates tool invocations, not every user prompt. A refusal by built-in safeguards without corroborating Defender evidence doesn't satisfy the Defender test.

### 8.5.3 Run the scenarios as the standard test user
Performed by **standard test user** (and **Security Administrator** to enable or disable the custom rule).

**Pass A – audit.** Only the **Default** rule applies.
1. Sign in as the standard test user and open the Copilot Studio test agent in Microsoft 365 Copilot or Teams. Start a new conversation for each scenario.
2. Run scenario 4 (benign control) first.
3. Run scenarios 1 to 3, one per conversation. For each, record the time, the scenario number, and the agent's response (screenshot).

**Pass B – blocking (optional).** The Security Administrator selects the test-agent rule prepared in the [prerequisites](prerequisites.md#prepare-real-time-protection-rules) on the **Real-time protection** page and selects **Enable**.
1. Repeat scenarios 1 to 4 as the standard test user and record the same evidence.
2. After the pass, the Security Administrator selects the rule and selects **Disable**.

**Expected result**
- Pass A: matching activity is recorded as a behavior without stopping the action, and near-real-time detections surface as alerts.
- Pass B: matching actions are blocked before they execute and recorded as behaviors in `BehaviorInfo`. When the threat detection system blocks a tool invocation, the agent immediately stops processing and notifies the user that their message is blocked. Near-real-time alerts aren't generated for an agent covered by a blocking rule.
- Scenario 4: the agent proceeds with no visible effect or interruption.

### 8.5.4 Verify the alert and incident in Defender
Performed by **Security Reader** (review) or **Security Operator** (manage alerts).
1. In the Microsoft Defender portal, open the incidents queue and find the incident that contains the alert from Pass A.
2. Use the incident graph and investigation experience to review the relationships between the involved entities and the blast radius.
3. If prompt evidence collection is enabled, open the alert and review the prompt snippets included as evidence.
4. Go to **Assets** > **AI agents** > **Agents**, select the test agent, select **Open Agent page**, then select **Incidents and alerts** and confirm that the incident is listed.
5. On the **Agents** tab, review **Active alerts**, **Risk level**, and **Risk indicators** for the test agent.
6. Run the queries in 8.4.3 and 8.4.4 to correlate the alert with the agent's tool invocations and any block events.
7. As Security Operator, set the alert status and classification.

**Expected result**
- Defender correlates the AI agent alert into an incident.
- The incident is listed on the test agent's **Incidents and alerts** tab.
- The hunting queries return the alert and the related agent activity.

### 8.5.5 Verify the risk signal in the Agent 365 registry
Performed by **AI Reader**, **Global Reader**, or **Security Reader**.
1. Open **Agents** > **All agents** > **Registry** in the Microsoft 365 admin center. Risk signal counts might be up to an hour behind the security portals.
2. Select the **Agents at risk** tile and confirm that the test agent is listed.
3. Select its **Risks** count and confirm that **Microsoft Defender** appears under **Risk signals are sourced from**.
4. Select **Microsoft Defender** to follow the deep link into the Defender portal. The deep link requires Global Reader, Security Reader, Security Administrator, AI Administrator, or Global Administrator; AI Reader can't follow it.

**Expected result**
- IT sees what is flagged for the test agent from the Microsoft 365 admin center, without switching between portals or elevating to security roles.

### 8.5.6 Contain the agent and verify
Performed by **AI Administrator** (block), **standard test user** (verify), and **Security Operator** (alert status).
1. Block the test agent as described in 8.2.3. Record the time.
2. As the standard test user, try to use the test agent in Microsoft 365 Copilot and in Teams.
3. As Security Operator, set the alert status and classification, and record the containment time.

**Expected result**
- Blocking restricts access to the agent across the organization, preventing any user from using it; the test user can't use the agent in Microsoft Copilot or Teams.
- The time from the first alert to the block is the PoC containment metric.

> For identity-level containment of an agent with a Microsoft Entra agent identity, see [3.11.1 Disable and re-enable an individual agent identity](../chapter-03-identity-ownership/README.md#3111-disable-and-re-enable-an-individual-agent-identity).

### 8.5.7 Run the Foundry test agent scenarios (optional)
**Documentation:** [Detect and investigate threats to AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection) · [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection)

Performed by **standard test user** (scenarios), **Security Reader** (review), **Security Administrator** (optional blocking pass), and **Security Operator** (alert status).

Confirm the [Foundry prerequisites](prerequisites.md#prepare-a-published-foundry-agent-optional) before testing. These are Agent 365 agent-security tests in the Microsoft Defender portal, not Defender for Cloud model-security tests.

Use the agreed prompts, the published Foundry test agent, and synthetic test data only.

| # | Scenario | Prompt | Expected result |
|---|---|---|---|
| F1 | Direct prompt injection / jailbreak | `<to be added>` | Audit: inspect the matching agent detection and related activity; distinguish a model or Prompt Shields refusal from Defender rule enforcement |
| F2 | Secret leakage using approved synthetic test material | `<to be added>` | Audit: inspect the matching detection; optional block pass: verify an interaction matching **Secret exfiltration** is stopped and recorded as a behavior |
| F3 | Indirect prompt injection via grounding data | `<to be added>` | Audit: inspect the matching agent detection; optional block pass: verify a match to a selected supported detection type |
| F4 | Benign control prompt | `<to be added>` | The agent responds normally |

1. With only the **Default** audit rule applying to the test agent, run F4 first, then F1 to F3 in separate conversations in its published channel. Record the time, scenario, agent identity, and response.
2. In the Microsoft Defender portal, find any matching agent alert and open its incident. On **Assets** > **AI agents** > **Agents**, open the Foundry agent page and review **Incidents and alerts**.
3. Use the queries in 8.4.3 and 8.4.4 to correlate agent activity, alerts, and behaviors by agent identity and test time. Record an absent detection as not demonstrated; don't substitute an unrelated model alert.
4. (Optional) The Security Administrator enables the prepared rule scoped to the Foundry test agent. Repeat F4 and the scenarios mapped to its detection types, then disable the rule. Record the blocked interaction and the corresponding `BehaviorInfo` event. Foundry protection can evaluate user requests, agent responses, tool invocations, and tool responses.
5. As Security Operator, set the status and classification of the audit-pass alert.

**Expected result**
- Audit: a matching agent detection is visible in Microsoft Defender, correlated into an incident, and associated with the published Foundry agent.
- Optional block: a matching interaction is stopped and recorded in `BehaviorInfo`; don't require a near-real-time alert for an agent covered by a blocking rule.
- F4 succeeds. If prompt evidence collection is enabled, inspect the suspicious snippets in the alert; otherwise, use the remaining alert and activity evidence.

---

## 8.6 Test local runtime protection (optional)

**Documentation:** [AI agent runtime protection demonstration](https://learn.microsoft.com/defender-endpoint/defender-endpoint-demonstration-ai-agent-runtime-protection)

Confirm [local runtime preparation](prerequisites.md#prepare-local-runtime-protection-optional) before this test.
Performed on the test device; alert review by **Security Reader**.
1. Close any terminal windows used to run agents, and open a new terminal.
2. Follow [AI agent runtime protection demonstration](https://learn.microsoft.com/defender-endpoint/defender-endpoint-demonstration-ai-agent-runtime-protection) and submit the benign test prompt from that article in a new session of a supported local agent.
3. In the Microsoft Defender portal, review the alert.

**Expected result**
- Defender raises a **Suspicious AI prompt injection** alert. The alert appears on the device timeline, and related alerts are correlated into incidents.
- In audit mode, the alert is **Informational**. In block mode, the alert severity is **Critical**, **High**, **Medium**, or **Low** based on assessed risk.
- In block mode, the agent terminal displays a block message and, if Windows Security notifications are enabled, a Windows toast notification appears. The detection is also listed under **Windows Security** > **Virus & threat protection** > **Current threats** and in the **Protection history**.

---

## 8.7 Evidence
- Screenshot of **Settings** > **Security for AI** > **Policies & rules** > **Real-time protection** with the **Default** rule and (optional) the custom rule.
- Screenshot of **Assets** > **AI agents** > **Agents** with the PoC agents, and the test agent page before and after the test (risk level, risk indicators, **Active alerts**).
- Exported results of the queries in 8.4.1, 8.4.3, and 8.4.4.
- Per scenario in 8.5.2: time, scenario number, pass (A or B), and the agent's response.
- The incident page for the test incident and the **Incidents and alerts** tab of the test agent.
- Screenshot of the registry **Agents at risk** view and the **Risk details** pane for the test agent.
- Screenshot of the **Block agent** pane and the test user's attempt to use the blocked agent.
- (Optional) Custom detection rule details page with **Triggered alerts**.
- (Optional) **Suspicious AI prompt injection** alert from 8.6.3.
- Timeline: first alert time, block time.
- (Optional, Foundry in scope) Per scenario in 8.5.7: time, scenario number, agent response, the Agent 365 agent alert and incident in Defender, and any optional block event in `BehaviorInfo`.

---

## 8.8 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Copilot Studio activity is blocked but no alerts or incidents appear | Microsoft 365 connector not connected | Connect the connector ([Microsoft 365 connector](prerequisites.md#connect-the-microsoft-365-connector)). |
| No Defender decision for the test agent | The agent uses classic orchestration, or the environment isn't configured | Use generative orchestration and configure threat detection for the agent's environment. |
| Tool runs although the threat detection system didn't answer | No decision within one second; default error behavior is **Allow the agent to respond** | Review **Set error behavior** ([Power Platform connection](prerequisites.md#configure-threat-detection-in-the-power-platform-admin-center)). |
| Blocking pass produces no alert | Near-real-time alerts aren't generated for an agent covered by a blocking rule | Query `BehaviorInfo` (8.4.4) for the block events. |
| `CloudAppEvents` returns no agent rows | The **Microsoft 365 activities** component isn't selected, or the agent hasn't been used | Check [Microsoft 365 connector](prerequisites.md#connect-the-microsoft-365-connector), use the agent as the test user, and rerun 8.4.3. |
| Queries fail on `AIAgentsInfo`, `AgentName`, or `EntraAgentId` | Table and column names | Use `AgentsInfo`, `Name`, `EntraAgentID` and `EntraBlueprintID`. Run `AgentsInfo \| getschema` to list the columns in your tenant. |
| **Risks** count in the registry is still zero after an alert | Risk signal counts might be up to an hour behind the security portals | Wait and refresh. |
| You can't block an agent | Signed in with a role that can view but not manage agents (Global Reader, AI Reader, Security Administrator, Security Reader) | Use AI Administrator. |
| Custom detection can't be created | Read-only role, or Security Operator without **Manage Security Settings** when Defender for Endpoint RBAC is on | Use Security Administrator, or assign the permission. |
| No **Suspicious AI prompt injection** alert in 8.6 | Device prerequisites not met, Beta Channel not configured, or the terminal wasn't reopened after enabling protection | Fix the prerequisite, close agent and terminal sessions, open a new terminal, and rerun the demonstration. |
| Alert has no prompt snippets | Prompt evidence collection may be disabled | Check the agreed [prompt evidence setting](prerequisites.md#prepare-real-time-protection-rules); don't change evidence collection without approval. |
| No threat detection for the Foundry test agent | The agent isn't published, or it's used only in a playground environment | Publish the Foundry agent and test it through its published channel. |

---

## ✅ What you proved

- [ ] The Copilot Studio test agent appears in **Assets** > **AI agents** > **Agents**, and its agent page opens with **Open Agent page**.
- [ ] The `AgentsInfo` inventory query in Advanced Hunting returns the PoC agents.
- [ ] After the standard test user runs the audit pass in 8.5.3, an alert for the test agent is listed on the agent's **Incidents and alerts** tab.
- [ ] (Optional) In the blocking pass, the risky tool invocation doesn't run, the agent tells the test user that the message is blocked, and the block event is recorded in `BehaviorInfo`.
- [ ] The test agent appears under **Agents at risk** in the Agent 365 registry, and its **Risk details** pane lists **Microsoft Defender** as a source.
- [ ] An AI Administrator blocks the test agent from the registry, and the test user can no longer use it.
- [ ] (Optional) A custom detection rule built on agent activity runs and lists a triggered alert.
- [ ] (Optional, local agents in scope) The Microsoft demonstration prompt in 8.6 raises a **Suspicious AI prompt injection** alert in the Defender portal.
- [ ] (Optional, Foundry in scope) The published Foundry agent's audit test produces a matching agent alert and incident in Microsoft Defender; any selected blocking test is verified separately in `BehaviorInfo`.

---

## References

- [Agent Registry in Microsoft 365 admin center – Agent risks](https://learn.microsoft.com/microsoft-365/admin/manage/agent-registry#agent-risks)
- [Governance and lifecycle actions for agents – Block or unblock agents](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions#block-or-unblock-agents)
- [Agent management roles and permissions](https://learn.microsoft.com/microsoft-365/admin/manage/agent-roles-perms)
- [Discover AI agents and assess security posture using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-inventory)
- [AI agent posture risk in Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-risk-assessment)
- [Detect and investigate threats to AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection)
- [Advanced hunting overview](https://learn.microsoft.com/defender-xdr/advanced-hunting-overview)
- [AgentsInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-agentsinfo-table)
- [CloudAppEvents table](https://learn.microsoft.com/defender-xdr/advanced-hunting-cloudappevents-table)
- [BehaviorInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-behaviorinfo-table)
- [AlertInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-alertinfo-table)
- [AlertEvidence table](https://learn.microsoft.com/defender-xdr/advanced-hunting-alertevidence-table)
- [Troubleshoot Direct OTel Observability – Defender advanced-hunting query](https://learn.microsoft.com/microsoft-agent-365/developer/direct-open-telemetry-troubleshooting)
- [Create custom detection rules](https://learn.microsoft.com/defender-xdr/custom-detection-rules)
- [Manage existing custom detection rules](https://learn.microsoft.com/defender-xdr/custom-detection-manage)
- [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection)
- [Enable external threat detection and protection for Copilot Studio custom agents – How it works](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider#how-it-works)
- [Orchestrate agent behavior with generative AI](https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions)
- [AI agent runtime protection demonstration](https://learn.microsoft.com/defender-endpoint/defender-endpoint-demonstration-ai-agent-runtime-protection)

---

[Runbook index](../README.md) · Previous: [Chapter 7 – Sensitive data protection (Purview)](../chapter-07-sensitive-data-protection/README.md) · Next: [Chapter 9 – Shadow AI and local agents](../chapter-09-shadow-ai-local-agents/README.md)
