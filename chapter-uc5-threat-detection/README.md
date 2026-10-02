# Chapter UC5 - Threat Detection & Protection (Defender)

**Pillar:** Secure
**What it proves:** your SOC sees agents as first-class actors. A simulated risky action alerts the SOC, and the owner contains it within minutes.

## Roles - least privilege

| Task | Role | Notes |
|---|---|---|
| Enable Security for AI, connect Microsoft 365 connector, enable Copilot Studio real-time protection | **Security Administrator** or higher in Microsoft Entra ID | Required to change Defender settings. Assign Active for the PoC window. |
| Configure the Power Platform side of the Copilot Studio integration | **Power Platform Administrator** | Required in addition to Security Admin. Hands the App ID back to the Security Admin. |
| Register the Entra ID application used by the external security provider | **Application Administrator** or **Cloud Application Administrator** | Required only if the Entra app is created fresh. |
| Create custom detection rules from KQL | **Security Operator** or **Security Administrator** | Required to create and edit custom detections. |
| Read-only / validation - hunting, alerts, inventory | **Security Reader** | Sufficient to run KQL, read alerts, and see the AI agent inventory. Use this role for reviewers, auditors, and SOC analysts on read-only rotations. |

Grant Security Reader first. Escalate to Security Administrator or Security Operator only when a change is actually being made.

## 1.1 Objective

Connect Agent 365 to Microsoft Defender so you can validate:

- Agent inventory and posture visibility.
- Security for AI data collection and detections.
- Real-time protection for Copilot Studio custom agents.
- Advanced Hunting visibility over agent activity.
- Optional custom detection rules.

> AI agent protection in Microsoft Defender is currently in **public preview**. The Microsoft Defender preview terms apply.

## 1.2 Documentation links

| Topic | Documentation |
|---|---|
| Enable security for AI agents | [Enable security for AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai) |
| Detect and investigate threats to AI agents | [Detect and investigate threats to AI agents using Microsoft Defender (Preview)](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection) |
| Protect AI agents overview | [Protect AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/defender-security-for-ai) |
| Real-time protection | [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection) |
| AI agent inventory | [AI agent inventory in Microsoft Defender XDR](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-inventory) |
| Local agent protection | [AI agent runtime protection in Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/configure-ai-agent-runtime-protection) |
| Advanced Hunting overview | [Advanced hunting overview](https://learn.microsoft.com/defender-xdr/advanced-hunting-overview) |
| `AgentsInfo` table | [`AgentsInfo` advanced hunting table](https://learn.microsoft.com/defender-xdr/advanced-hunting-agentsinfo-table) |
| Custom detections | [Create and manage custom detection rules](https://learn.microsoft.com/defender-xdr/custom-detection-rules) |
| Copilot Studio external security provider | [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider) |

## 1.3 Defender prerequisites

Before starting:

1. Agent 365 is onboarded.
2. The PoC agents are published and visible as managed agents.
3. The setup owner has **Security Administrator** or higher in Microsoft Entra ID.
4. For Copilot Studio real-time protection, a **Power Platform Administrator** is available.
5. (Optional) For local agent protection, Microsoft Defender for Endpoint is running in **active mode**.

## 1.4 Setup - open the Security for AI Get started wizard

Performed by **Security Administrator**.

1. Sign in to the [Microsoft Defender portal](https://security.microsoft.com).
2. Go to **Settings** > **Security for AI** > **Get started**.
3. Confirm the **Enable** toggle is **on** (it is on by default once Agent 365 is onboarded).
4. On the setup checklist, confirm **Agent 365** shows **Done**. This happens automatically after Agent 365 onboarding and provides unified visibility into AI agents.

The remaining steps in this chapter walk through the other items in the checklist: Microsoft 365 connector and Copilot Studio real-time protection.

**Check result**

- The **Enable** toggle is on.
- **Agent 365** on the setup checklist is marked **Done**.

## 1.5 Setup - connect the Microsoft 365 connector

Required for investigation and Advanced Hunting over AI agent activity. Performed by **Security Administrator**.

1. On the **Get started** page, select the **Microsoft 365 connector** step.
2. On the **Select Microsoft 365 components** step, select at least:
   - **Microsoft Entra ID Management events** (audit of admin activities in Entra ID).
   - **Microsoft 365 activities** (audit of user activities in Microsoft 365 apps).
   - **Microsoft Entra Users and groups** is a prerequisite and is selected by default.
3. Select **Connect Microsoft 365** and complete the consent prompt.

**Check result**

- The Microsoft 365 connector status shows **Connected**.
- The **Get started** checklist marks the step **Connected**.

> If the Microsoft 365 connector is not connected, Copilot Studio real-time protection continues to block suspicious actions during runtime, but related alerts and incidents will not appear in the Defender portal.

## 1.6 Setup - connect Copilot Studio real-time protection

Required only if Copilot Studio custom agents are in scope. Performed jointly by **Security Administrator** (Defender) and **Power Platform Administrator** (Power Platform).

### 1.6.1 In the Defender portal (Security Admin)

1. On the **Get started** page, select the **Copilot Studio** step. The **Copilot Studio real-time protection** pane opens.
2. Toggle **Real-time protection** on.
3. Under **Enable Power Platform Integration**, copy the URL shown. Share it with the Power Platform Administrator.

The **Get started** page shows a list of **Identified Power Platform Admins** who have permission to complete the Power Platform side.

### 1.6.2 In Power Platform (Power Platform Admin)

Follow the current docs for [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider):

1. **Step 1 - Register the Microsoft Entra application.** Create a single-tenant Entra ID app, configure a Federated Identity Credential pointing at Defender, and copy the **Application (client) ID**.
2. **Step 2 - Configure the threat detection system in Power Platform admin center.** In <https://admin.powerplatform.microsoft.com>, go to the environment > **Security** > **Threat detection** > **Additional threat detection**. Enter the Entra app ID and the endpoint URL shared by the Security Admin, allow Copilot Studio to share data, and save.
3. Share the **App ID** back with the Security Admin.

> The App ID used in Power Platform must be the **same** as the App ID used in the Microsoft Entra ID application.

### 1.6.3 Finish in the Defender portal (Security Admin)

1. In the **Copilot Studio real-time protection** pane, paste the App ID into the **App ID** field.
2. Select **Save**.

If the App ID was recently updated in Power Platform, allow up to one minute for propagation before saving.

**Check result**

- Real-time protection toggle is **on**.
- App ID is saved without a validation error.
- The **Get started** checklist marks the **Copilot Studio** step **Connected**.

## 1.7 Setup (optional) - local AI agent runtime protection

Required only if the PoC covers AI agents that run locally on endpoints.

1. Confirm Microsoft Defender for Endpoint is deployed and in **active mode** on the target endpoints.
2. Follow [AI agent runtime protection in Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/configure-ai-agent-runtime-protection) to onboard local agents.

Local agents are onboarded separately from cloud agents.

**Check result**

- Local agent protection is enabled on in-scope endpoints.

## 1.8 Test - agent inventory in Advanced Hunting

Open **Defender portal** > **Hunting** > **Advanced hunting** and run:

```kql
AgentsInfo
| summarize arg_max(Timestamp, *) by AgentId
| where LifecycleStatus != "Deleted"
| project Timestamp, Name, Platform, Model, PublishedStatus, LifecycleStatus,
          Owners, CreatedDateTime, EntraAgentID
| sort by CreatedDateTime desc
```

**Expected result**

- Your PoC agents appear in the result set.
- Agent names, platforms, owners, and lifecycle state match the PoC configuration.

## 1.9 Test - cloud app activity

Run:

```kql
CloudAppEvents
| where Timestamp > ago(7d)
| where Application has_any ("Microsoft 365 Copilot", "Copilot Studio", "Power Apps", "Microsoft Teams")
| project Timestamp, Application, ActionType, AccountDisplayName, AccountId, IPAddress, RawEventData
| sort by Timestamp desc
```

**Expected result**

- Relevant Copilot, Teams, or cloud app activity appears after the test user exercises the agent.
- No unexpected users or locations are present.

## 1.10 Test - weak agent configuration hunt

Run:

```kql
AgentsInfo
| summarize arg_max(Timestamp, *) by AgentId
| where LifecycleStatus == "Active"
| extend NoInstructions = isempty(Instructions) or Instructions == "N/A"
| extend NoGuardrails = isnull(Guardrails) or tostring(Guardrails) in ("", "[]", "{}")
| where NoInstructions or NoGuardrails
| project Name, Platform, PublishedStatus, NoInstructions, NoGuardrails,
          Owners, CreatedDateTime, EntraAgentID
```

**Expected result**

- A clean environment may return no rows.
- If rows appear, review whether the agents are missing instructions or guardrails before progressing.

## 1.11 Test - ownerless agent hunt

Run:

```kql
AgentsInfo
| summarize arg_max(Timestamp, *) by AgentId
| where LifecycleStatus != "Deleted"
| extend Raw = todynamic(RawAgentInfo)
| extend OwnerId = tostring(Owners[0])
| extend AcquiredStatus = tostring(Raw.acquiredStatus)
| extend AcquisitionState = tostring(Raw.acquisitionState)
| extend Ownerless = isempty(OwnerId) or OwnerId == "00000000-0000-0000-0000-000000000000"
| extend NotDeployed = AcquisitionState == "unacquired" or AcquiredStatus == "acquiredForNone"
| where Ownerless and not(NotDeployed)
| project Name, Platform, PublishedStatus, InstanceCount,
          AcquiredStatus, AcquisitionState, LifecycleStatus, CreatedDateTime, EntraAgentID
| sort by InstanceCount desc, CreatedDateTime desc
```

**Expected result**

- No ownerless active PoC agents.
- Any result should be triaged with the agent owner or identity governance team.

## 1.12 Optional - save a custom detection

1. Take a validated hunting query.
2. Select **Save** > **Save as**.
3. Select **Create detection rule**.
4. Configure schedule, severity, title, and impacted entities.
5. Save the rule.

**Check result**

- Query is saved.
- Optional detection rule is created and visible in Defender.

---

Previous: [UC4 - Sensitive Data Protection](../chapter-uc4-sensitive-data-protection/README.md) · Next: [UC6 - Lifecycle & Audit](../chapter-uc6-lifecycle-audit/README.md)
