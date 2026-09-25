# Chapter 1 - Defender setup, tests, and result checks

## 1.1 Objective

Connect Agent 365 to Microsoft Defender so the customer can validate:

- Agent inventory and posture visibility.
- AI agent security settings.
- Real-time protection and investigation.
- Advanced Hunting visibility.
- Optional custom detections.

## 1.2 Documentation links

Use these Microsoft documentation links before starting the Defender configuration:

| Topic | Documentation |
|---|---|
| Defender protection for AI agents | [Detect, block, and investigate threats to AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection) |
| Agent 365 and Defender | [How Microsoft Defender supports Agent 365](https://learn.microsoft.com/microsoft-agent-365/leadership/defender-agent-365) |
| AI agent inventory | [AI agent inventory in Microsoft Defender XDR](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-inventory) |
| Advanced Hunting overview | [Advanced hunting overview](https://learn.microsoft.com/defender-xdr/advanced-hunting-overview) |
| `AgentsInfo` table | [`AgentsInfo` advanced hunting table](https://learn.microsoft.com/defender-xdr/advanced-hunting-agentsinfo-table) |
| Custom detections | [Create and manage custom detection rules](https://learn.microsoft.com/defender-xdr/custom-detection-rules) |
| Copilot Studio external security provider | [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider) |

## 1.3 Defender prerequisites

The customer should confirm:

1. The organization is onboarded to Agent 365.
2. The PoC agents are published and visible as managed agents.
3. The setup owner has a Defender role that can change settings, for example Security Administrator.
4. The hunting user has at least Security Reader.
5. If custom detections will be created, the user has Security Operator or Security Administrator.
6. If Microsoft 365 app connector setup is required, the user has Application Administrator or Cloud Application Administrator.
7. If Copilot Studio real-time protection is in scope, a Power Platform Administrator or environment admin is available.

## 1.4 Setup - enable Defender preview features

1. Open the Microsoft Defender portal: <https://security.microsoft.com>.
2. Go to **System** > **Settings** > **Microsoft Defender XDR**.
3. Enable **Preview features**.
4. Save the setting.

**Check result**

- Defender preview features are enabled.
- AI agent evidence and inventory experiences are visible in the Defender portal.

## 1.5 Setup - turn on Security for AI agents

1. In the Defender portal, go to **System** > **Settings** > **Security for AI agents**.
2. Turn on **Security for AI agents**.
3. Under **AI real-time protection & investigation**, confirm **Agent 365** shows as **Connected**.

**Check result**

- Agent 365 connection status is **Connected**.
- Agent 365-managed agents are in scope for posture, detection, and real-time protection.

## 1.6 Setup - Copilot Studio real-time protection

Use this step only if the customer will test Copilot Studio agent protection.

1. In Defender, go to **System** > **Settings** > **Security for AI agents**.
2. Under **AI real-time protection & investigation**, open **Copilot Studio real-time protection**.
3. Turn **Real-time protection** on.
4. Copy the **Power Platform Integration URL** shown by Defender.
5. Register a Microsoft Entra application for the integration.
6. Configure the Federated Identity Credential using the organization-specific identifier and Defender endpoint.
7. Copy the Entra application's **Application (client) ID**.
8. Paste the App ID back into the Defender Copilot Studio protection pane and save.
9. If the customer environment requires configuration through the Power Platform admin center, open **Power Platform admin center** at <https://aka.ms/ppac>, then go to **Security** > **Threat detection** > **Additional threat detection**. Choose the environment, allow Copilot Studio to share data, paste the App ID and endpoint link, then save.

**Power Platform admin dependency**

The customer should have a Power Platform Administrator or environment admin available for this step. The integration may require environment-level configuration in the Power Platform admin center, not only Defender configuration.

**Check result**

- Copilot Studio real-time protection is enabled.
- The App ID and endpoint are saved successfully.
- Defender shows Copilot Studio / Agent 365 as connected for real-time protection.

## 1.7 Setup - connect Microsoft 365 app connector for near-real-time detections

This supports Microsoft 365 audit events flowing into Defender for Cloud Apps and Advanced Hunting scenarios.

1. In Defender, go to **Settings** > **Cloud Apps**.
2. Under **Connected apps**, select **App Connectors**.
3. Select **+ Connect an app**.
4. Choose **Microsoft 365**.
5. Leave all Microsoft 365 components selected unless the customer has a specific reason to limit scope.
6. Select **Connect**.
7. Complete the consent prompt.
8. Confirm connector status is **Connected**.

**Check result**

- Microsoft 365 connector status is **Connected**.
- New events begin appearing after ingestion delay.

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

- The customer's PoC agents appear in the result set.
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
- If rows appear, the customer should review whether the agents are missing instructions or guardrails.

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

Previous: [Chapter 0 - Prerequisites](../chapter-0-prerequisites/README.md) · Next: [Chapter 2 - Purview](../chapter-2-purview/README.md)
