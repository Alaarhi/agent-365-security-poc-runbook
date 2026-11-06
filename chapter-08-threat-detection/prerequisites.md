# Prerequisites - Chapter 8: Threat detection and runtime protection (Defender)

> **Goal:** Prepare the accounts, access, and test assets needed for this chapter and its selected optional paths.

Apply the [shared PoC preparation guidance](../README.md#prerequisites-and-reading-order) and agree the [chapter outcomes](README.md#-what-you-proved). Finish dependent build steps before their tests.

## Table of contents

- [Tenant readiness](#tenant-readiness)
- [Prepare accounts and role assignments](#prepare-accounts-and-role-assignments)
- [Audit recording](#audit-recording)
- [Test assets and dependencies](#test-assets-and-dependencies)
- [Security for AI preparation sequence](#security-for-ai-preparation-sequence)
- [Enable security for AI](#enable-security-for-ai)
- [Connect the Microsoft 365 connector](#connect-the-microsoft-365-connector)
- [Connect Copilot Studio real-time protection](#connect-copilot-studio-real-time-protection)
- [Prepare real-time protection rules](#prepare-real-time-protection-rules)
- [Prepare a published Foundry agent (optional)](#prepare-a-published-foundry-agent-optional)
- [Prepare local runtime protection (optional)](#prepare-local-runtime-protection-optional)
- [Prepare a custom detection rule (optional)](#prepare-a-custom-detection-rule-optional)
- [Prepare test cases and baselines](#prepare-test-cases-and-baselines)
- [Setup troubleshooting](#setup-troubleshooting)
- [Plan propagation and test timing](#plan-propagation-and-test-timing)
- [References](#references)

---

## Tenant readiness

**Documentation:** [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started) · [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview) · [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)

Confirm an Agent 365-eligible license and onboarding before enabling agent security. Use the [setup permissions](#setup-permissions) for preparation and [8.1 Required permissions](README.md#81-required-permissions) for testing.

Follow the [shared tenant readiness check](../README.md#tenant-readiness) using the chapter permissions and feature prerequisites linked above.

---

## Prepare accounts and role assignments

Alongside the [shared setup and reviewer accounts](../README.md#least-privilege-model), prepare the following scenario accounts:

| Account | Purpose |
|---|---|
| Standard test user | Runs the runtime-protection test prompts and verifies containment. No admin role. |
| Maker account | Prepares the published Copilot Studio agent and any optional Foundry test agent. |
| Controlled recipient mailbox | Receives any permitted test email from the Copilot Studio agent. Use only the controlled recipient prepared for the email-agent tests. |

Assign the [setup permissions](#setup-permissions) and the [test permissions](README.md#81-required-permissions) using the shared model. Verify each account can access the pages needed for its tasks.

### Setup permissions

| Task | Least-privilege role |
|---|---|
| Enable Security for AI, connect Microsoft 365 and Copilot Studio, manage protection rules, and configure prompt evidence | Security Administrator |
| Register the provider authentication application and federated identity credential | User permitted to create application registrations in Microsoft Entra |
| Configure the Copilot Studio environment's threat detection provider | Power Platform Administrator |
| Add the synthetic test document and verify the Copilot Studio knowledge source, tools, and publication | PoC maker account from Chapter 7 |
| (Optional) Publish the Foundry test agent to Microsoft 365 Copilot and Teams | Foundry User on the Foundry project; AI Administrator for approval if organizational publication is selected |
| (Optional) Configure local runtime protection on a test device | Local administrator for elevated PowerShell |
| (Optional) Deploy local runtime protection policies | Permission to manage endpoint security policies in Defender, or an Intune role such as Policy and Profile Manager |
| (Optional) Create an Advanced Hunting custom detection | Security Administrator |

Security Operator can manage custom detections only when Defender for Endpoint RBAC is off. When it is on, the operator also needs **Manage Security Settings**. Use the documented setup roles rather than elevating the read-only reviewer.

---

## Audit recording

**Documentation:** [Turn auditing on or off](https://learn.microsoft.com/purview/audit-log-enable-disable) · [Audit logs for Copilot and AI applications](https://learn.microsoft.com/purview/audit-copilot)

Performed by a member of **Audit Manager**. Follow the [shared audit recording check](../chapter-05-lifecycle-audit/prerequisites.md#audit-recording) before the activity to be reviewed.

---

## Test assets and dependencies

**Documentation:** [Enable security for AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai) · [Protect AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/defender-security-for-ai) · [Enable security for AI agents using Microsoft Defender – Connect data sources](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai#connect-data-sources) · [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider) · [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection)

- Verify the required inventory using [Chapter 1 – Agent discovery and inventory](../chapter-01-agent-discovery/README.md). Agent 365 must be onboarded in the tenant before you enable security for AI agents.
- **Copilot Studio test agent:** use the Copilot Studio email agent from [7.6 Copilot Studio email agent and publication](../chapter-07-sensitive-data-protection/README.md#76-copilot-studio-email-agent-and-publication). It has a SharePoint knowledge source and the **Send an email (V2)** tool, and is published to Microsoft 365 Copilot and Teams. It must use generative orchestration, because external threat detection is only called on agents that use generative orchestration. Complete the Chapter 7 tests before you run 8.5, because 8.5.6 blocks this agent.
- (Optional, Foundry in scope) Prepare a published agent from [1.2.2 Create and publish a Foundry test agent](../chapter-01-agent-discovery/README.md#122-create-and-publish-a-foundry-test-agent), then complete [Foundry preparation](#prepare-a-published-foundry-agent-optional).
- (Optional, local agents in scope) Prepare the Windows test device onboarded to Defender for Endpoint, as described in [9.2 Tenant and device prerequisites](../chapter-09-shadow-ai-local-agents/README.md#92-tenant-and-device-prerequisites), with a supported local AI agent installed.
- Ownerless-agent governance (identify ownerless agents, reassign ownership, Agent management rules) is covered in [5.5 Govern ownerless agents](../chapter-05-lifecycle-audit/README.md#55-govern-ownerless-agents). This chapter only links to it.
- Shadow AI and local agent discovery in the Microsoft 365 admin center are covered in [Chapter 9 – Shadow AI and local agents](../chapter-09-shadow-ai-local-agents/README.md). This chapter only covers the optional Defender for Endpoint runtime protection for local agents (8.6).
- Detection and investigation of AI agent threats in Microsoft Defender is in public preview. Copilot Studio external threat detection and real-time protection for Copilot Studio agents are in preview.


**Check result**
- Each asset needed for the selected paths is prepared or has a named build task that will finish before its dependent tests.

---

## Security for AI preparation sequence

**Documentation:** [Enable security for AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai) · [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider) · [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection) · [AI agent runtime protection in Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/configure-ai-agent-runtime-protection)

Complete the shared cloud-agent connection, Copilot Studio integration, and rule preparation below before testing. Prepare Foundry or local runtime protection only when those paths are selected. Estimates cover hands-on work; service and approval waits are separate.

| Preparation | Estimated hands-on time |
|---|---|
| [Enable security for AI](#enable-security-for-ai) | ~5-10 min |
| [Connect Microsoft 365](#connect-the-microsoft-365-connector) | ~10-15 min |
| [Connect Copilot Studio](#connect-copilot-studio-real-time-protection) | ~20-30 min |
| [Prepare protection rules](#prepare-real-time-protection-rules) | ~5-10 min |
| [Prepare a published Foundry agent (optional)](#prepare-a-published-foundry-agent-optional) | ~10-15 min if the agent is already built |
| [Prepare local runtime protection (optional)](#prepare-local-runtime-protection-optional) | ~15-25 min |

**Check result**
- Each selected setup section's **Check result** is confirmed before its dependent tests.

---

## Enable security for AI
**Documentation:** [Enable security for AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai) · [Protect AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/defender-security-for-ai)

When you onboard to Agent 365, security for AI agents is enabled automatically, including AI agent discovery, security posture assessment, and threat detection.

### Review the Get started checklist
Performed by **Security Administrator**.
1. Sign in to the Microsoft Defender portal at `https://security.microsoft.com`.
2. Go to **Settings** > **Security for AI** > **Get started**.
3. Confirm that the **Enable** toggle is on. It is on by default. Switching it to **Off** stops collecting data for AI agents; leave it on for the PoC.
4. Review the setup checklist. It shows the status of the required and optional data sources:
   - **Agent 365**: provides unified visibility into AI agents and is marked **Done** automatically.
   - **Microsoft 365 connector**: complete [Connect the Microsoft 365 connector](#connect-the-microsoft-365-connector).
   - **Copilot Studio**: complete [Connect Copilot Studio real-time protection](#connect-copilot-studio-real-time-protection).
5. Note the names under **Identified Power Platform Admins**. One of them completes the [Power Platform connection](#configure-threat-detection-in-the-power-platform-admin-center).

**Check result**
- The **Enable** toggle is on.
- **Agent 365** shows **Done**.

---

## Connect the Microsoft 365 connector
**Documentation:** [Enable security for AI agents using Microsoft Defender – Connect data sources](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai#connect-data-sources) · [Detect and investigate threats to AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection)

The Microsoft 365 connector provides investigation and advanced hunting capabilities for AI agent activity, and collects the Agent 365 observability data that near-real-time detections rely on.

### Connect Microsoft 365 components
Performed by **Security Administrator**.
1. On **Settings** > **Security for AI** > **Get started**, select the **Microsoft 365 connector** step.
2. On the **Select Microsoft 365 components** step, select at least the two components required for AI agent monitoring:
   - **Microsoft Entra ID Management events**: audit admin activities performed in Microsoft Entra ID.
   - **Microsoft 365 activities**: audit activities performed by users in your Microsoft 365 apps.

   **Microsoft Entra Users and groups** is a prerequisite for all monitoring capabilities and is selected by default.
3. Select **Connect Microsoft 365** to complete the connector setup.

**Check result**
- The **Microsoft 365 connector** step shows **Connected** on the **Get started** page.

> For Copilot Studio agents, if the Microsoft 365 connector isn't connected, real-time protection continues to block suspicious activity during runtime, but alerts and incidents related to these actions don't appear in the Microsoft Defender portal. Connect it before you run the tests in 8.5.

---

## Connect Copilot Studio real-time protection
**Documentation:** [Enable security for AI agents using Microsoft Defender – Connect data sources](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai#connect-data-sources) · [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider) · [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection)

With this integration, every time a Copilot Studio agent's orchestrator considers invoking a tool, it sends relevant data about the proposed tool use to the threat detection endpoint, which returns a decision to allow or block the tool invocation. If a security issue is detected, the agent immediately stops processing and notifies the user that their message is blocked. If the operation is approved, the agent proceeds with no visible effect for the user.

Data shared with the threat detection provider includes the user's recent prompt and the latest chat history, outputs of previous tools, conversation metadata (agent, user, tenant, and trigger where applicable), and the tool the agent wants to invoke, including the agent-generated reasoning and the proposed inputs.

Coordinate the setup in this order:

| Step | Who | Where | Output |
|---|---|---|---|
| [Defender connection](#turn-on-real-time-protection-in-the-defender-portal) | Security Administrator | Defender portal | Real-time protection on; integration URL copied |
| [Authentication application](#register-the-microsoft-entra-application) | User with permissions to create application registrations | Microsoft Entra | App ID of an application with a federated identity credential |
| [Power Platform connection](#configure-threat-detection-in-the-power-platform-admin-center) | Power Platform Administrator | Power Platform admin center | Threat detection configured for the test environment |
| [App ID validation](#save-the-app-id-in-the-defender-portal) | Security Administrator | Defender portal | App ID saved; Copilot Studio step **Connected** |

Important:
- External threat detection is only called on agents that use generative orchestration. It is skipped for classic agents.
- The external security provider is configured per environment. There is no global or tenant-wide setting. Turn on threat detection for new environments after you create them.

### Turn on real-time protection in the Defender portal
Performed by **Security Administrator**.
1. On **Settings** > **Security for AI** > **Get started**, select the **Copilot Studio** step. The **Copilot Studio real-time protection** pane opens.
2. Toggle **Real-time protection** to on.
3. Under **Enable Power Platform Integration**, copy the URL provided. Use the same endpoint for the [authentication application](#register-the-microsoft-entra-application) and the [Power Platform connection](#configure-threat-detection-in-the-power-platform-admin-center).
4. Share the URL with your Power Platform administrator and with the person who registers the Microsoft Entra application.

**Check result**
- **Real-time protection** is on and you have the integration URL.

### Register the Microsoft Entra application
Performed by a **user with permissions to create application registrations** in your Microsoft Entra tenant.

The agent uses Federated Identity Credentials (FIC) as a secure, secret-less authentication method with the threat detection system. Use one of the two options below. You need your tenant ID and the endpoint URL from the Defender portal.

**Option A – PowerShell script (recommended)**
1. Download the [Create-CopilotWebhookApp.ps1](https://www.powershellgallery.com/packages/Create-CopilotWebhookApp/1.0.1) script.
2. Open Windows PowerShell 5.1 or later as an administrator and go to the directory that contains the script.
3. Run the script with your values. With the optional `-DryRun` flag, the script performs a validation run without creating resources.

   ```powershell
   .\Create-CopilotWebhookApp.ps1 `
   -TenantId "<your tenant ID>" `
   -Endpoint "<integration URL from the Defender portal>" `
   -DisplayName "A365 PoC - Copilot Studio Defender integration" `
   -FICName "A365PoCDefenderFIC"
   ```

4. Copy the App ID that the script outputs.

**Option B – Manual configuration in the Azure portal**
1. Sign in to the Azure portal and go to the **Microsoft Entra ID** page.
2. Under **App registrations**, select **New registration**.
3. Provide a name and select **Accounts in this organizational directory only (Single tenant)**.
4. Select **Register**, then copy the App ID.
5. In the app, select **Manage** > **Certificates & secrets** > **Federated credentials**, then select **Add credential**.
6. In the **Federated credentials scenario** drop-down, select **Other issuer**, and fill in:
   - **Issuer**: `https://login.microsoftonline.com/{tenantId}/v2.0`
   - **Type**: **Explicit subject identifier**
   - **Value**: `/eid1/c/pub/t/{base 64 encoded tenantId}/a/m1WPnYRZpEaQKq1Cceg--g/{base 64 encoded endpoint}`
   - **Name**: a descriptive name
7. Select **Add**.

To get the base64 encoding of your tenant ID and endpoint URL, use the script from the Copilot Studio article:

```powershell
# Encoding tenant ID
$tenantId = [Guid]::Parse("11111111-2222-3333-4444-555555555555")
$base64EncodedTenantId = [Convert]::ToBase64String($tenantId.ToByteArray()).Replace('+','-').Replace('/','_').TrimEnd('=')
Write-Output $base64EncodedTenantId

# Encoding the endpoint
$endpointURL = "https://provider.example.com/threat_detection/copilot"
$base64EncodedEndpointURL = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($endpointURL)).Replace('+','-').Replace('/','_').TrimEnd('=')
Write-Output $base64EncodedEndpointURL
```

Replace the placeholder tenant ID and endpoint URL with your values.

**Check result**
- You have the App ID of a single-tenant application with a federated identity credential.

### Configure threat detection in the Power Platform admin center
Performed by **Power Platform Administrator**.
1. Sign in to the Power Platform admin center at `https://admin.powerplatform.microsoft.com`.
2. On the side navigation, select **Security**, then select **Threat detection**.
3. Select **Additional threat detection**. A pane opens.
4. Select the environment that hosts the Copilot Studio test agent and select **Set up**.
5. Select **Allow Copilot Studio to share data with a threat detection provider**.
6. Under **Azure Entra App ID**, enter the App ID from the [authentication application](#register-the-microsoft-entra-application).
7. Enter the **Endpoint link**: the integration URL from the Defender portal, the same base URL used for the Microsoft Entra application.
8. Under **Set error behavior**, define the default behavior when the threat detection system doesn't respond in time or responds with an error. The default is **Allow the agent to respond**; you can choose **Block the query** to further reduce risk.
9. Select **Save**.
10. Share the App ID with the Security Administrator.

**Check result**
- The save succeeds. The save fails if the Microsoft Entra app isn't properly configured in Microsoft Entra or not properly authorized with the provider.

> If the agent doesn't receive a decision from the threat detection system within one second, by default it allows the tool to execute. **Set error behavior** changes this default.

### Save the App ID in the Defender portal
Performed by **Security Administrator**.
1. Return to **Settings** > **Security for AI** > **Get started** and select the **Copilot Studio** step.
2. Paste the App ID from the Power Platform administrator into the **App ID** field. The Power Platform administrator must use the same App ID as the Microsoft Entra application.
3. Select **Save**.

**Check result**
- The App ID saves. If you recently changed the App ID in Power Platform, it can take up to one minute to propagate; if you get a validation error, wait a short time and try again.
- When the Power Platform administrator completes the onboarding steps, the **Copilot Studio** step shows **Connected**.

---

## Prepare real-time protection rules
**Documentation:** [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection)

Performed by **Security Administrator**.

For cloud agents, there are two types of real-time protection rules:
- **Default rule**: audits all agents, recording matching activity as a behavior without stopping the action.
- **Custom rules**: block matching actions before they execute and record the behavior.

When Defender audits or blocks an action, it records the event as a behavior in the `BehaviorInfo` table. Near-real-time detections continue to surface as alerts only in audit mode. When a blocking rule covers an agent, near-real-time alerts aren't generated for that agent.

1. Go to **Settings** > **Security for AI** > **Policies & rules** > **Real-time protection**.
2. Confirm that the built-in **Default** rule is listed.
3. Go to **Settings** > **Security for AI** > **Prompt evidence collection** and review the **Enabled** toggle. When enabled (the default), each alert includes as evidence only the portions of user prompts or agent responses identified as suspicious, with sensitive data and secrets redacted. Agree with the customer whether to keep it on for the PoC.
4. (Optional, for the blocking pass in 8.5.3) Create a custom rule for the test agent:
   1. Select **Create rule**.
   2. On the **Rule details** step, set the rule **Status** to off, enter the **Rule name** `A365 PoC - block test agent` and a **Rule description**, then select **Next**.
   3. Under **Scope**, choose specific agents and select the Copilot Studio test agent. Use a separate rule scoped to the Foundry test agent if that path is selected.
   4. Under **Detection types**, select the agreed scenarios from **Malicious content propagation**, **Secret exfiltration**, **Evasion techniques**, and **Unsafe email domain**, then select **Apply**. Only agents with a Microsoft Entra agent ID appear in the selection list.
   5. Select **Next**, confirm the rule name, description, action, scope, detection rules, and status, then select **Create**.

**Check result**
- The **Default** rule is listed, and prompt evidence collection is set as agreed.
- (Optional) The custom rule is listed, scoped to the test agent, and not enabled until 8.5.3.

---

## Prepare a published Foundry agent (optional)

**Documentation:** [Detect and investigate threats to AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection) · [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection) · [Transition agent security capabilities to Agent 365](https://learn.microsoft.com/defender-xdr/security-for-ai/transition-agent-security-to-agent-365) · [Publish agents to Microsoft Copilot and Microsoft Teams](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-copilot)

**Defender for Cloud is not a prerequisite for these Foundry agent tests.** Agent discovery, posture, and agent-specific threat detection use Agent 365 and its observability data in Microsoft Defender. The Defender for AI Services plan remains relevant to Foundry **models**, such as Azure OpenAI, and separate infrastructure protection. Enable that plan only for a separately agreed model or infrastructure scenario; see [Enable threat protection for AI services](https://learn.microsoft.com/azure/defender-for-cloud/ai-onboarding).

Performed by **Foundry User** on the project (publication), **Security Administrator** (Defender configuration), and the **standard test user** (access check).

1. Complete [Enable security for AI](#enable-security-for-ai) and [Connect the Microsoft 365 connector](#connect-the-microsoft-365-connector). Foundry agents send observability data to Microsoft 365 by default; confirm activity arrives rather than assuming it does.
2. Select the tested active version of the Foundry agent and publish it to Microsoft 365 Copilot and Teams using the linked publishing guide. Threat detection doesn't support unpublished agents or playground-only sessions. Current direct publishing handles Teams bot registration; a separate Azure Bot Service resource isn't required.
3. Use a publication scope approved for the PoC. With **Just you**, sharing a link doesn't grant Foundry permissions: participants need the required project permissions. With **People in your organization**, obtain approval in the Microsoft 365 admin center and verify the applicable app access policies before testing.
4. Confirm the standard test user can open the agent in its published channel.
5. In Defender, verify the agent appears in **Assets** > **AI agents** and record its agent identifiers. Confirm a benign invocation appears in `CloudAppEvents` using [8.4.3](README.md#843-trace-agent-activity-in-cloudappevents).
6. If a blocking pass is selected, prepare a separate disabled rule scoped to the Foundry test agent as in [Prepare real-time protection rules](#prepare-real-time-protection-rules). Foundry coverage includes user requests, agent responses, tool invocations, and tool responses.

**Check result**
- The published agent is accessible to the test account, its inventory and activity are visible in Defender, and any optional block rule is scoped to it and disabled before the audit pass.

---

## Prepare local runtime protection (optional)
**Documentation:** [Set up AI agent runtime protection with Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/configure-ai-agent-runtime-protection) · [AI agent runtime protection with Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/ai-agent-runtime-protection-overview) · [AI agent runtime protection demonstration](https://learn.microsoft.com/defender-endpoint/defender-endpoint-demonstration-ai-agent-runtime-protection)

Run this section only if local AI agents are in scope. Local agents are onboarded separately from cloud agents. Runtime protection inspects the user prompt, tool requests before execution, and tool responses after execution, detects prompt injection, and audits or blocks supported agent actions. Discovery of local agents and Shadow AI is covered in [Chapter 9 – Shadow AI and local agents](../chapter-09-shadow-ai-local-agents/README.md).

Prerequisites on each test device:
- The device is onboarded to Defender for Endpoint, and Microsoft Defender Antivirus is running in active mode with real-time protection enabled.
- The device runs a supported version of Windows, and Microsoft Defender Antivirus has the latest platform, engine, and security intelligence updates.
- One or more supported local AI agents are installed for the runtime protection approach you plan to enable.
- During public preview, the test device receives Microsoft Defender platform and engine updates from the **Beta Channel**.

Two runtime protection methods are available, each with the modes `Disabled`, `Audit`, and `Block`:
- `AiAgentProtection`: agent-native event inspection, for agents that expose vendor-supported agent event interfaces (such as Claude Code, Codex CLI, and GitHub Copilot CLI).
- `AiAgentNetworkInspection`: network inspection, for agents that don't expose vendor-supported agent event interfaces. Network inspection doesn't support agents that use certificate pinning or HTTP/3.

Microsoft recommends a phased rollout: **Test** in audit mode on a small set of devices, **Review** alerts for one to two weeks, **Deploy** in audit mode to more device groups, then **Enforce** with block mode.

### Turn on runtime protection on a single test device
Performed in an elevated PowerShell session (**Run as administrator**) on the test device.
1. Verify that `AntivirusSignatureVersion` is `1.451.224.0` or later:

   ```powershell
   Get-MpComputerStatus | Select-Object AntivirusSignatureVersion
   ```

2. Enable the method or methods you need in audit mode:

   ```powershell
   Set-MpPreference -AiAgentProtection Audit
   ```

   ```powershell
   Set-MpPreference -AiAgentNetworkInspection Audit
   ```

3. Verify the current settings:

   ```powershell
   Get-MpPreference | Select-Object AiAgentProtection, AiAgentNetworkInspection
   ```

4. Close the PowerShell window and any terminal windows used to run agents. Then open a new terminal window before starting the agent.

**Check result**
- `Get-MpPreference` returns `Audit` for each method you enabled.

### Deploy runtime protection with a policy
Performed by an account with **permission to manage endpoint security policies** (Defender portal) or an Intune role such as **Policy and Profile Manager** (Intune).

From the Defender portal:
1. On the **Windows policies** tab of the **Endpoint security policies** page (`https://security.microsoft.com/policy-inventory?osPlatform=Windows`), select **Create new policy**.
2. For **Select platform**, select **Windows**. For **Select template**, select **Microsoft Defender AI agent runtime protection**.
3. On the **Configuration settings** page, set **Ai Agent Protection** to **Audit**.
4. Complete the wizard and assign the policy to a test device group. For devices managed through Defender for Endpoint security settings management that aren't enrolled in Intune, assign the policy to Microsoft Entra device groups.

From Intune:
1. In the Intune admin center at `https://intune.microsoft.com`, on the **Endpoint security | Overview** page, go to **Manage** > **Antivirus** and select **Create policy**.
2. For **Platform**, select **Windows**. For **Profile**, select **Microsoft Defender AI agent runtime protection**.
3. On the **Configuration settings** page, set **Ai Agent Protection** to **Audit**.
4. Complete the wizard, assign the policy to a test device group, and create the policy.

The **Microsoft Defender AI agent runtime protection** profile and template configure agent-native event inspection. To deploy network inspection with Intune, use a PowerShell platform script that runs `Set-MpPreference -AiAgentNetworkInspection Audit`, with **Run this script using the logged on credentials** set to **No**.

**Check result**
- In the Defender portal, open the device page, select the **Configuration management** tab, select **Effective settings**, find **Ai Agent Protection**, and confirm its effective value and configuration source.

---

## Prepare a custom detection rule (optional)
**Documentation:** [Create custom detection rules](https://learn.microsoft.com/defender-xdr/custom-detection-rules)

Performed by **Security Administrator**.

This rule alerts on tool executions by the PoC test agent. It shows that agent activity can drive custom SOC detections.

1. In **Advanced hunting**, run the following query with the agent identifier recorded in [8.4.3](README.md#843-trace-agent-activity-in-cloudappevents). It returns `Timestamp` and `ReportId` from the same event, and `AccountObjectId` to map the impacted account.

   ```kql
   let pocAgentIds = dynamic(["<agent identifier from 8.4.3>"]);
   CloudAppEvents
   | where ActionType in ("ExecuteToolBySDK", "ExecuteToolByGateway", "ExecuteToolByMCPServer")
   | extend resData = parse_json(tostring(RawEventData))
   | extend AgentId = tostring(resData.AgentId)
   | where AgentId in (pocAgentIds)
   | project Timestamp, ReportId, AccountObjectId, ActionType, AgentId
   ```

2. Select **Create detection rule**.
3. Enter the alert details: **Detection name** `A365 PoC - test agent tool execution`, **Frequency** **Every hour**, **Alert title**, **Severity**, **Category**, **Description**, and **Recommended actions**.
4. Map the impacted asset to the `AccountObjectId` column.
5. Don't add response actions. Set the rule scope, review the rule, and select **Create**. The rule runs immediately, then again based on the configured frequency.
6. Go to **Hunting** > **Custom detection rules** and confirm that the rule is listed and its **Status** is on.

**Check result**
- The rule is listed and enabled, with no automated response actions. Validate its triggered alert during [8.4.5](README.md#845-validate-a-custom-detection-optional).

---

## Prepare test cases and baselines
Performed by **Security Administrator** with the **PoC maker account**.

| # | Precondition | How to check |
|---|---|---|
| 1 | Security for AI is enabled; Microsoft 365 connector and Copilot Studio show **Connected** | [Security for AI checklist](#review-the-get-started-checklist), [Microsoft 365 connection](#connect-microsoft-365-components), [App ID validation](#save-the-app-id-in-the-defender-portal) |
| 2 | Threat detection is configured for the environment that hosts the test agent | [Power Platform connection](#configure-threat-detection-in-the-power-platform-admin-center) |
| 3 | The test agent uses generative orchestration | In Copilot Studio (`https://copilotstudio.microsoft.com`), open the agent's **Settings** page; in the **Generative AI** section, check **Orchestration**. New agents use generative orchestration by default. |
| 4 | The test agent has a knowledge source and at least one tool: the SharePoint knowledge source and the **Send an email (V2)** tool of the 7.6 agent | Agent configuration in Copilot Studio (7.6.2, 7.6.3) |
| 5 | The test agent is published to Microsoft 365 Copilot and Teams, and the standard test user can use it there | Test user opens the agent (7.9.6) |
| 6 | The test agent appears in **Assets** > **AI agents** and in `AgentsInfo` | 8.3.1, 8.4.1 |
| 7 | The **Default** real-time protection rule is listed; the optional custom block rule exists and is not enabled | [Protection rules](#prepare-real-time-protection-rules) |
| 8 | Baseline captured: risk level and risk indicators in Defender, **Risks** count in the registry | 8.3.2, 8.2.1 |
| 9 | For scenario 1, the PoC maker account has added an unlabeled test document with the injected content to the SharePoint site that the agent uses as knowledge (7.4) | The document is listed in the site library |

> Custom agents created in Copilot Studio include built-in protection against user prompt-injection attacks (UPIA) and cross-domain prompt injection attacks (XPIA), and block these attacks at runtime. Record the agent's response for each scenario.

Before testing, the PoC team replaces every `<to be added>` prompt with an approved test case, records the expected detection or rule type, and prepares any synthetic knowledge document needed for it. Never use real credentials or uncontrolled recipients. For the audit pass, verify that no existing blocking rule covers the test agent; don't change unrelated rules to force a result.

**Check result**
- All applicable preconditions are verified, test inputs are agreed, and baseline evidence is captured. Record excluded optional paths before opening the test chapter.


---

## Setup troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| **Settings** > **Security for AI** setup isn't available | The tenant isn't onboarded to Agent 365 | Onboard to Agent 365 (prerequisite), see [Tenant readiness](prerequisites.md#tenant-readiness) and [Chapter 1](../chapter-01-agent-discovery/README.md). |
| Microsoft 365 connector doesn't show **Connected** | Setup wasn't completed, or the required components weren't selected | Reopen the connector step, select **Microsoft Entra ID Management events** and **Microsoft 365 activities**, and select **Connect Microsoft 365**. |
| Validation error when saving the App ID in Defender | The App ID was recently changed in Power Platform | Wait a short time (up to one minute) and try again. Use the same App ID as the Microsoft Entra application. |
| Power Platform: "There was a problem connecting to the protection provider. Try checking the endpoint link. If that doesn't work, contact the protection provider for help." | A call to the provided endpoint failed | Check the endpoint link (the integration URL from the Defender portal). |
| Power Platform: "There was a problem with the configuration. Try checking the details you entered and the Microsoft Entra configuration. If the problem persists, contact your admin for help." | Token acquisition failed | Check the Microsoft Entra application configuration and the Federated Identity Credentials. Select **Copy error info** for details. |
| Power Platform: "To change a configuration, make sure you have Power Platform admin permissions." | The user isn't a Power Platform Administrator | Use a user with the Power Platform Administrator role. |
| **Copilot Studio** step doesn't show **Connected** | The Power Platform administrator hasn't completed the onboarding steps | Ask one of the **Identified Power Platform Admins** to complete the [Power Platform connection](#configure-threat-detection-in-the-power-platform-admin-center). |

---

## Plan propagation and test timing

**Documentation:** [Agent Registry](https://learn.microsoft.com/microsoft-365/admin/manage/agent-registry)

| Configuration | Propagation window to plan for |
|---|---|
| Risk signals in the Agent Registry compared with the source security portals | Up to 1 hour |

> ⚠️ **Watch out:** Allow for the documented propagation window and verify the actual configuration or signal before testing. Elapsed time alone is not proof that a change has applied.

---

## References

- [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started)
- [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview)
- [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)
- [Turn auditing on or off](https://learn.microsoft.com/purview/audit-log-enable-disable)
- [Audit logs for Copilot and AI applications](https://learn.microsoft.com/purview/audit-copilot)
- [Enable security for AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai)
- [Protect AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/defender-security-for-ai)
- [Enable security for AI agents using Microsoft Defender – Connect data sources](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai#connect-data-sources)
- [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider)
- [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection)
- [Enable threat protection for AI services](https://learn.microsoft.com/azure/defender-for-cloud/ai-onboarding)
- [AI agent runtime protection in Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/configure-ai-agent-runtime-protection)
- [Detect and investigate threats to AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection)
- [Transition agent security capabilities to Agent 365](https://learn.microsoft.com/defender-xdr/security-for-ai/transition-agent-security-to-agent-365)
- [Publish agents to Microsoft Copilot and Microsoft Teams](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-copilot)
- [AI agent runtime protection with Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/ai-agent-runtime-protection-overview)
- [AI agent runtime protection demonstration](https://learn.microsoft.com/defender-endpoint/defender-endpoint-demonstration-ai-agent-runtime-protection)
- [Create custom detection rules](https://learn.microsoft.com/defender-xdr/custom-detection-rules)
- [Agent Registry](https://learn.microsoft.com/microsoft-365/admin/manage/agent-registry)

### Additional resources

- [Create-CopilotWebhookApp.ps1](https://www.powershellgallery.com/packages/Create-CopilotWebhookApp/1.0.1)

---

> **Ready?** Continue to the [chapter](README.md). →
