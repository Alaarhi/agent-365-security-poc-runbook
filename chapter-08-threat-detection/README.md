# Chapter 8 – Threat Detection and Runtime Protection (Defender)

**Pillar:** Secure
**What it proves:** The SOC sees AI agents as first-class assets in Microsoft Defender. A risky agent action is detected (and, where a blocking rule applies, blocked) at runtime, raises an alert that Defender correlates into an incident associated with the agent, surfaces as a risk signal in the Agent 365 registry, and can be contained by blocking the agent.

**Success criteria**
- **Settings** > **Security for AI** > **Get started** shows **Agent 365** as **Done**, and the **Microsoft 365 connector** and **Copilot Studio** steps as **Connected**.
- The Copilot Studio test agent appears in **Assets** > **AI agents** > **Agents**, and its agent page opens with **Open Agent page**.
- The `AgentsInfo` inventory query in Advanced Hunting returns the PoC agents.
- After the standard test user runs the audit pass in 8.10.3, an alert for the test agent is listed on the agent's **Incidents and alerts** tab.
- (Optional) In the blocking pass, the risky tool invocation doesn't run, the agent tells the test user that the message is blocked, and the block event is recorded in `BehaviorInfo`.
- The test agent appears under **Agents at risk** in the Agent 365 registry, and its **Risk details** pane lists **Microsoft Defender** as a source.
- An AI Administrator blocks the test agent from the registry, and the test user can no longer use it.
- (Optional) A custom detection rule built on agent activity runs and lists a triggered alert.
- (Optional, local agents in scope) The Microsoft demonstration prompt in 8.6.3 raises a **Suspicious AI prompt injection** alert in the Defender portal.
- (Optional, Foundry in scope) **AI services** is **On** in Defender for Cloud for the PoC subscription, and the Foundry test scenarios in 8.10.7 produce AI alerts in Defender for Cloud **Security alerts** and in the Defender portal alert queue.

## 8.1 Required permissions

Grant the read-only role first; assign setup roles only to the person who makes each change, and assign them as Active (not Eligible) for the PoC window.

| Task | Least-privilege role | Section |
|---|---|---|
| Enable Security for AI, connect the Microsoft 365 connector, turn on Copilot Studio real-time protection, save the App ID | Security Administrator | 8.2, 8.3, 8.4.1, 8.4.4 |
| Manage real-time protection rules and prompt evidence collection | Security Administrator | 8.4.5 |
| Register the Microsoft Entra application and its federated identity credential, and delete it at cleanup | A user with permissions to create application registrations in your Microsoft Entra tenant | 8.4.2, 8.13 |
| Configure and disconnect threat detection for the Power Platform environment | Power Platform Administrator | 8.4.3, 8.13 |
| (Optional) Enable or disable the Defender for Cloud **AI services** plan and its components | Owner or Contributor on the Azure subscription | 8.5.1, 8.5.2, 8.13 |
| (Optional) Publish the Foundry test agent to Microsoft 365 Copilot and Teams | Azure Bot Service Contributor (or Contributor or Owner) on the resource group, and Foundry User on the Foundry project | 8.10.7 |
| (Optional) View Defender for Cloud alerts in the Azure portal | Security Reader (Azure role in Defender for Cloud) | 8.5.3, 8.10.7 |
| (Optional) View Defender for Cloud alerts in the Defender portal | Microsoft Defender XDR Unified RBAC role for Defender for Cloud, or Global Administrator or Security Administrator | 8.5.3, 8.10.7 |
| (Optional) Deploy local AI agent runtime protection from the Defender portal | Permission to manage endpoint security policies in the Defender portal | 8.6.2 |
| (Optional) Deploy local AI agent runtime protection from Intune | Intune role with permission to create, update, and assign device configurations, such as Policy and Profile Manager | 8.6.2 |
| View the Agent 365 registry, **Agents at risk**, and **Risk details** | AI Reader, Global Reader, or Security Reader | 8.7, 8.10.5 |
| Open the Microsoft Defender deep link from **Risk details** | Global Reader, Security Reader, Security Administrator, or AI Administrator | 8.7.2 |
| Block or unblock an agent in the registry | AI Administrator | 8.7.3, 8.10.6, 8.13 |
| (Optional) Delete the Foundry test agent after the PoC | As listed in [5.1 Required permissions](../chapter-05-lifecycle-audit/README.md#51-required-permissions) | 8.13 |
| Manage alert status and classification | Security Operator | 8.10.4, 8.10.6, 8.10.7, 8.13 |
| Create, turn off, or delete custom detection rules | Security Administrator (or Security Operator, see note) | 8.9.5, 8.13 |
| Add and remove the test document in the SharePoint knowledge source of the Copilot Studio test agent | PoC maker account (as in 7.4 and 7.6) | 8.10.1, 8.13 |
| Run the test scenarios | Standard test user | 8.10.3, 8.10.7 |
| Validation / read-only review: Advanced Hunting, alerts, Defender views opened from the registry | Security Reader | 8.6.3, 8.8, 8.9, 8.10.4 |

Notes:
- Security Operator can manage custom detections only when role-based access control (RBAC) is turned off in Microsoft Defender for Endpoint. If RBAC is turned on, the Security Operator also needs the **Manage Security Settings** permission in Defender for Endpoint.
- Copilot Studio real-time protection needs collaboration between the Security Administrator (Defender portal) and a Power Platform Administrator (Power Platform admin center). The **Get started** page lists the **Identified Power Platform Admins** who have permission to complete the setup in Power Platform.

**Before you start:**
- Complete [Chapter 0 – Prerequisites and PoC preparation](../chapter-00-prerequisites/README.md): test admin, standard test user, reviewer account, and published PoC agents.
- Complete [Chapter 1 – Agent Discovery and Inventory](../chapter-01-agent-discovery/README.md). Agent 365 must be onboarded in the tenant before you enable security for AI agents.
- **Copilot Studio test agent:** use the Copilot Studio email agent from [7.6 Copilot Studio email agent and publication](../chapter-07-sensitive-data-protection/README.md#76-copilot-studio-email-agent-and-publication). It has a SharePoint knowledge source and the **Send an email (V2)** tool, and is published to Microsoft 365 Copilot and Teams. It must use generative orchestration, because external threat detection is only called on agents that use generative orchestration. Complete the Chapter 7 tests before you run 8.10, because 8.10.6 blocks this agent.
- (Optional, Foundry in scope) Create and publish the Foundry test agent as described in [1.2.2 Create and publish a Foundry test agent](../chapter-01-agent-discovery/README.md#122-create-and-publish-a-foundry-test-agent), and identify the Azure subscription that contains its Foundry resources (8.5).
- (Optional, local agents in scope) Prepare the Windows test device onboarded to Defender for Endpoint, as described in [9.2 Tenant and device prerequisites](../chapter-09-shadow-ai-local-agents/README.md#92-tenant-and-device-prerequisites), with a supported local AI agent installed (8.6).
- Ownerless-agent governance (identify ownerless agents, reassign ownership, Agent management rules) is covered in [5.5 Govern ownerless agents](../chapter-05-lifecycle-audit/README.md#55-govern-ownerless-agents). This chapter only links to it.
- Shadow AI and local agent discovery in the Microsoft 365 admin center are covered in [Chapter 9 – Shadow AI and Local Agents](../chapter-09-shadow-ai-local-agents/README.md). This chapter only covers the optional Defender for Endpoint runtime protection for local agents (8.6).
- Detection and investigation of AI agent threats in Microsoft Defender is in public preview. Copilot Studio external threat detection and real-time protection for Copilot Studio agents are in preview.

## 8.2 Enable Security for AI
**Documentation:** [Enable security for AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai) · [Protect AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/defender-security-for-ai)

When you onboard to Agent 365, security for AI agents is enabled automatically, including AI agent discovery, security posture assessment, and threat detection.

### 8.2.1 Review the Get started checklist
Performed by **Security Administrator**.
1. Sign in to the Microsoft Defender portal at `https://security.microsoft.com`.
2. Go to **Settings** > **Security for AI** > **Get started**.
3. Confirm that the **Enable** toggle is on. It is on by default. Switching it to **Off** stops collecting data for AI agents; leave it on for the PoC.
4. Review the setup checklist. It shows the status of the required and optional data sources:
   - **Agent 365**: provides unified visibility into AI agents and is marked **Done** automatically.
   - **Microsoft 365 connector**: connected in 8.3.
   - **Copilot Studio**: connected in 8.4.
5. Note the names under **Identified Power Platform Admins**. One of them completes 8.4.3.

**Check result**
- The **Enable** toggle is on.
- **Agent 365** shows **Done**.

## 8.3 Connect the Microsoft 365 connector
**Documentation:** [Enable security for AI agents using Microsoft Defender – Connect data sources](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai#connect-data-sources) · [Detect and investigate threats to AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection)

The Microsoft 365 connector provides investigation and advanced hunting capabilities for AI agent activity, and collects the Agent 365 observability data that near-real-time detections rely on.

### 8.3.1 Connect Microsoft 365 components
Performed by **Security Administrator**.
1. On **Settings** > **Security for AI** > **Get started**, select the **Microsoft 365 connector** step.
2. On the **Select Microsoft 365 components** step, select at least the two components required for AI agent monitoring:
   - **Microsoft Entra ID Management events**: audit admin activities performed in Microsoft Entra ID.
   - **Microsoft 365 activities**: audit activities performed by users in your Microsoft 365 apps.

   **Microsoft Entra Users and groups** is a prerequisite for all monitoring capabilities and is selected by default.
3. Select **Connect Microsoft 365** to complete the connector setup.

**Check result**
- The **Microsoft 365 connector** step shows **Connected** on the **Get started** page.

> For Copilot Studio agents, if the Microsoft 365 connector isn't connected, real-time protection continues to block suspicious activity during runtime, but alerts and incidents related to these actions don't appear in the Microsoft Defender portal. Connect it before you run the tests in 8.10.

## 8.4 Turn on Copilot Studio real-time protection
**Documentation:** [Enable security for AI agents using Microsoft Defender – Connect data sources](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai#connect-data-sources) · [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider) · [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection)

With this integration, every time a Copilot Studio agent's orchestrator considers invoking a tool, it sends relevant data about the proposed tool use to the threat detection endpoint, which returns a decision to allow or block the tool invocation. If a security issue is detected, the agent immediately stops processing and notifies the user that their message is blocked. If the operation is approved, the agent proceeds with no visible effect for the user.

Data shared with the threat detection provider includes the user's recent prompt and the latest chat history, outputs of previous tools, conversation metadata (agent, user, tenant, and trigger where applicable), and the tool the agent wants to invoke, including the agent-generated reasoning and the proposed inputs.

The setup has four parts, in this order:

| Step | Who | Where | Output |
|---|---|---|---|
| 8.4.1 | Security Administrator | Defender portal | Real-time protection on; integration URL copied |
| 8.4.2 | User with permissions to create application registrations | Microsoft Entra | App ID of an application with a federated identity credential |
| 8.4.3 | Power Platform Administrator | Power Platform admin center | Threat detection configured for the test environment |
| 8.4.4 | Security Administrator | Defender portal | App ID saved; Copilot Studio step **Connected** |

Important:
- External threat detection is only called on agents that use generative orchestration. It is skipped for classic agents.
- The external security provider is configured per environment. There is no global or tenant-wide setting. Turn on threat detection for new environments after you create them.

### 8.4.1 Turn on real-time protection in the Defender portal
Performed by **Security Administrator**.
1. On **Settings** > **Security for AI** > **Get started**, select the **Copilot Studio** step. The **Copilot Studio real-time protection** pane opens.
2. Toggle **Real-time protection** to on.
3. Under **Enable Power Platform Integration**, copy the URL provided. This is the endpoint used in 8.4.2 and 8.4.3.
4. Share the URL with your Power Platform administrator and with the person who registers the Microsoft Entra application.

**Check result**
- **Real-time protection** is on and you have the integration URL.

### 8.4.2 Register the Microsoft Entra application
Performed by a **user with permissions to create application registrations** in your Microsoft Entra tenant.

The agent uses Federated Identity Credentials (FIC) as a secure, secret-less authentication method with the threat detection system. Use one of the two options below. You need your tenant ID and the endpoint URL from 8.4.1.

**Option A – PowerShell script (recommended)**
1. Download the [Create-CopilotWebhookApp.ps1](https://www.powershellgallery.com/packages/Create-CopilotWebhookApp/1.0.1) script.
2. Open Windows PowerShell 5.1 or later as an administrator and go to the directory that contains the script.
3. Run the script with your values. With the optional `-DryRun` flag, the script performs a validation run without creating resources.

   ```powershell
   .\Create-CopilotWebhookApp.ps1 `
   -TenantId "<your tenant ID>" `
   -Endpoint "<integration URL from 8.4.1>" `
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

### 8.4.3 Configure threat detection in the Power Platform admin center
Performed by **Power Platform Administrator**.
1. Sign in to the Power Platform admin center at `https://admin.powerplatform.microsoft.com`.
2. On the side navigation, select **Security**, then select **Threat detection**.
3. Select **Additional threat detection**. A pane opens.
4. Select the environment that hosts the Copilot Studio test agent and select **Set up**.
5. Select **Allow Copilot Studio to share data with a threat detection provider**.
6. Under **Azure Entra App ID**, enter the App ID from 8.4.2.
7. Enter the **Endpoint link**: the integration URL from 8.4.1, the same base URL used for the Microsoft Entra application.
8. Under **Set error behavior**, define the default behavior when the threat detection system doesn't respond in time or responds with an error. The default is **Allow the agent to respond**; you can choose **Block the query** to further reduce risk.
9. Select **Save**.
10. Share the App ID with the Security Administrator.

**Check result**
- The save succeeds. The save fails if the Microsoft Entra app isn't properly configured in Microsoft Entra or not properly authorized with the provider.

> If the agent doesn't receive a decision from the threat detection system within one second, by default it allows the tool to execute. **Set error behavior** changes this default.

### 8.4.4 Save the App ID in the Defender portal
Performed by **Security Administrator**.
1. Return to **Settings** > **Security for AI** > **Get started** and select the **Copilot Studio** step.
2. Paste the App ID from the Power Platform administrator into the **App ID** field. The Power Platform administrator must use the same App ID as the Microsoft Entra application.
3. Select **Save**.

**Check result**
- The App ID saves. If you recently changed the App ID in Power Platform, it can take up to one minute to propagate; if you get a validation error, wait a short time and try again.
- When the Power Platform administrator completes the onboarding steps, the **Copilot Studio** step shows **Connected**.

### 8.4.5 Review real-time protection rules and prompt evidence
Performed by **Security Administrator**.

For cloud agents, there are two types of real-time protection rules:
- **Default rule**: audits all agents, recording matching activity as a behavior without stopping the action.
- **Custom rules**: block matching actions before they execute and record the behavior.

When Defender audits or blocks an action, it records the event as a behavior in the `BehaviorInfo` table. Near-real-time detections continue to surface as alerts only in audit mode. When a blocking rule covers an agent, near-real-time alerts aren't generated for that agent.

1. Go to **Settings** > **Security for AI** > **Policies & rules** > **Real-time protection**.
2. Confirm that the built-in **Default** rule is listed.
3. Go to **Settings** > **Security for AI** > **Prompt evidence collection** and review the **Enabled** toggle. When enabled (the default), each alert includes as evidence only the portions of user prompts or agent responses identified as suspicious, with sensitive data and secrets redacted. Agree with the customer whether to keep it on for the PoC.
4. (Optional, for the blocking pass in 8.10.3) Create a custom rule for the test agent:
   1. Select **Create rule**.
   2. On the **Rule details** step, set the rule **Status** to off, enter the **Rule name** `A365 PoC - block test agent` and a **Rule description**, then select **Next**.
   3. Under **Scope**, choose specific agents and select the Copilot Studio test agent.
   4. Under **Detection types**, select the threat scenarios that the rule applies to, then select **Apply**.
   5. Select **Next**, confirm the rule name, description, action, scope, detection rules, and status, then select **Create**.

**Check result**
- The **Default** rule is listed, and prompt evidence collection is set as agreed.
- (Optional) The custom rule is listed, scoped to the test agent, and not enabled until 8.10.3.

## 8.5 Turn on threat protection for Microsoft Foundry agents (Defender for Cloud)
**Documentation:** [Enable threat protection for AI services](https://learn.microsoft.com/azure/defender-for-cloud/ai-onboarding) · [AI threat protection in Microsoft Defender for Cloud](https://learn.microsoft.com/azure/defender-for-cloud/ai-threat-protection) · [Alerts for AI services](https://learn.microsoft.com/azure/defender-for-cloud/alerts-ai-workloads) · [Manage and respond to security alerts](https://learn.microsoft.com/azure/defender-for-cloud/manage-respond-alerts) · [Alerts and incidents in Microsoft Defender XDR for Microsoft Defender for Cloud](https://learn.microsoft.com/azure/defender-for-cloud/concept-integration-365) · [Permissions in Microsoft Defender for Cloud](https://learn.microsoft.com/azure/defender-for-cloud/permissions) · [Transition Microsoft Copilot Studio and Microsoft Foundry agent security capabilities to Microsoft Agent 365](https://learn.microsoft.com/defender-xdr/security-for-ai/transition-agent-security-to-agent-365)

Run this section only if Microsoft Foundry agents are in scope.

Threat protection for AI services in Microsoft Defender for Cloud protects Microsoft Foundry workloads on an Azure subscription by providing insights to threats that might affect your generative AI applications and agents. It works with Azure AI Content Safety Prompt Shields and Microsoft threat intelligence to provide security alerts for threats like data leakage, data poisoning, jailbreak, and credential theft. It integrates with Microsoft Defender XDR, so security teams can centralize and correlate AI workload alerts and incidents in the Microsoft Defender portal.

How this plan relates to the rest of this chapter:
- The Defender for AI Services plan supports Foundry Models such as Azure OpenAI. Supported AI services are Azure OpenAI supported models and Azure AI Model Inference service supported models. Defender for Cloud supports text tokens only; image and audio tokens aren't scanned.
- Agent-specific threat detection for Foundry agents runs over Agent 365 observability logs and appears in the Microsoft Defender portal (8.2, 8.3, 8.10). Foundry agents send observability data to Microsoft 365 by default. Threat detection is supported only for published Foundry agents; unpublished agents, including agents used only in a playground environment, aren't supported.
- Real-time protection for Foundry agents (Preview) evaluates user requests, agent responses, tool invocations, and tool responses, and uses the rules in 8.4.5. Block events from Microsoft Prompt Shields for Foundry are recorded as behaviors in `BehaviorInfo`.
- Threat protection for AI services is available in commercial clouds. It isn't available in Azure Government, Microsoft Azure operated by 21Vianet, or connected AWS accounts.

Prerequisites:
- An Azure subscription that contains the Foundry resources of the PoC.
- [Defender for Cloud enabled](https://learn.microsoft.com/azure/defender-for-cloud/get-started#enable-defender-for-cloud-on-your-azure-subscription) on the Azure subscription.
- **Owner** or **Contributor** on the subscription to enable the plan.

### 8.5.1 Enable the AI services plan
Performed by **Owner** or **Contributor** on the Azure subscription.
1. Sign in to the Azure portal at `https://portal.azure.com`.
2. Search for and select **Microsoft Defender for Cloud**.
3. In the Defender for Cloud menu, select **Environment settings**.
4. Select the Azure subscription that contains the PoC Foundry resources.
5. On the **Defender plans** page, toggle **AI services** to **On**.

**Check result**
- On the **Defender plans** page of the subscription, **AI services** is **On**.

### 8.5.2 Configure the plan components
Performed by **Owner** or **Contributor** on the Azure subscription.

With the AI services plan enabled, you can control the components of the plan:
- **Suspicious prompt evidence**: alerts include suspicious portions of user prompts and model responses, with sensitive data automatically redacted. The prompt snippets appear in the Defender portal as part of each alert's evidence.
- **Data security for AI interactions**: allows Microsoft Purview to access and analyze prompts, responses, and related metadata. Microsoft Purview integration doesn't include data or context from Foundry agents, so this chapter doesn't use it. Purview controls are covered in [Chapter 7 – Sensitive Data Protection (Purview)](../chapter-07-sensitive-data-protection/README.md).
- **AI model security**: scans models registered in Azure Machine Learning registries. Not used in this chapter.

To turn on suspicious prompt evidence:
1. In the Azure portal, go to **Microsoft Defender for Cloud** > **Environment settings** and select the subscription.
2. Locate **AI services** and select **Settings**.
3. Toggle **Enable user prompt evidence** to **On**.
4. Select **Continue**.

User prompt evidence consists of prompts and model responses, and both are considered your data. Evidence is available through the Azure portal, the Defender portal, and any attached partner integrations. If user prompt evidence is disabled, Defender for Cloud continues analyzing prompts and responses for threat detection, but the prompt content is masked in alerts. Agree with the customer whether to turn it on for the PoC.

**Check result**
- In the **AI services** settings, **Enable user prompt evidence** is set as agreed.

### 8.5.3 Review AI alerts in Defender for Cloud and the Defender portal
Performed by **Security Reader** (Azure role in Defender for Cloud) in the Azure portal; in the Defender portal, by a user with the Microsoft Defender XDR Unified RBAC role for Defender for Cloud, or a **Global Administrator** or **Security Administrator**.
1. In the Azure portal, go to **Microsoft Defender for Cloud** > **Security alerts**.
2. (Optional) Filter the alerts list. Add extra filters by selecting **Add filter**.
3. Select an alert to open the pane with the alert description and affected resources, then select **View full details** to see the **Alert details** and **Take action** tabs.
4. In the Microsoft Defender portal, open the alert queue and use the **alert subscription ID** filter to view Defender for Cloud alerts for the PoC subscription.

Defender for Cloud alerts are integrated into the Defender portal alert queue and correlated into incidents. Informational alerts from Defender for Cloud aren't integrated into the Defender portal. Alert status changes are synchronized between Defender for Cloud and the Defender portal.

**Check result**
- You can open **Security alerts** in Defender for Cloud and filter the Defender portal alert queue by the PoC subscription ID.

## 8.6 Turn on local AI agent runtime protection in Defender for Endpoint (optional)
**Documentation:** [Set up AI agent runtime protection with Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/configure-ai-agent-runtime-protection) · [AI agent runtime protection with Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/ai-agent-runtime-protection-overview) · [AI agent runtime protection demonstration](https://learn.microsoft.com/defender-endpoint/defender-endpoint-demonstration-ai-agent-runtime-protection)

Run this section only if local AI agents are in scope. Local agents are onboarded separately from cloud agents. Runtime protection inspects the user prompt, tool requests before execution, and tool responses after execution, detects prompt injection, and audits or blocks supported agent actions. Discovery of local agents and Shadow AI is covered in [Chapter 9 – Shadow AI and Local Agents](../chapter-09-shadow-ai-local-agents/README.md).

Prerequisites on each test device:
- The device is onboarded to Defender for Endpoint, and Microsoft Defender Antivirus is running in active mode with real-time protection enabled.
- The device runs a supported version of Windows, and Microsoft Defender Antivirus has the latest platform, engine, and security intelligence updates.
- One or more supported local AI agents are installed for the runtime protection approach you plan to enable.
- During public preview, the test device receives Microsoft Defender platform and engine updates from the **Beta Channel**.

Two runtime protection methods are available, each with the modes `Disabled`, `Audit`, and `Block`:
- `AiAgentProtection`: agent-native event inspection, for agents that expose vendor-supported agent event interfaces (such as Claude Code, Codex CLI, and GitHub Copilot CLI).
- `AiAgentNetworkInspection`: network inspection, for agents that don't expose vendor-supported agent event interfaces. Network inspection doesn't support agents that use certificate pinning or HTTP/3.

Microsoft recommends a phased rollout: **Test** in audit mode on a small set of devices, **Review** alerts for one to two weeks, **Deploy** in audit mode to more device groups, then **Enforce** with block mode.

### 8.6.1 Turn on runtime protection on a single test device
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

### 8.6.2 Deploy runtime protection with a policy
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

### 8.6.3 Validate with the Microsoft demonstration prompt
Performed on the test device; alert review by **Security Reader**.
1. Close any terminal windows used to run agents, and open a new terminal.
2. Follow [AI agent runtime protection demonstration](https://learn.microsoft.com/defender-endpoint/defender-endpoint-demonstration-ai-agent-runtime-protection) and submit the benign test prompt from that article in a new session of a supported local agent.
3. In the Microsoft Defender portal, review the alert.

**Expected result**
- Defender raises a **Suspicious AI prompt injection** alert. The alert appears on the device timeline, and related alerts are correlated into incidents.
- In audit mode, the alert is **Informational**. In block mode, the alert severity is **Critical**, **High**, **Medium**, or **Low** based on assessed risk.
- In block mode, the agent terminal displays a block message and, if Windows Security notifications are enabled, a Windows toast notification appears. The detection is also listed under **Windows Security** > **Virus & threat protection** > **Current threats** and in the **Protection history**.

## 8.7 Review agent risk in the Agent 365 registry
**Documentation:** [Agent Registry in Microsoft 365 admin center – Agent risks](https://learn.microsoft.com/microsoft-365/admin/manage/agent-registry#agent-risks) · [Governance and lifecycle actions for agents – Block or unblock agents](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions#block-or-unblock-agents) · [Agent management roles and permissions](https://learn.microsoft.com/microsoft-365/admin/manage/agent-roles-perms)

Risk signals in the Agent Registry are a consolidated set of agent-related security detections from multiple security platforms. IT administrators can understand what is flagged without switching between portals or elevating their permissions to different security roles, and share the details with the security team for investigation and remediation. Risk signal counts might be up to an hour behind what the security portals show, and reflect active risk signals. The Registry baseline, including the **Agents at risk** tile, is recorded in [1.3.4 Review risk signals](../chapter-01-agent-discovery/README.md#134-review-risk-signals); this section focuses on investigating and containing a flagged agent.

### 8.7.1 Open Agents at risk
Performed by **AI Reader**, **Global Reader**, or **Security Reader**.
1. Sign in to the Microsoft 365 admin center at `https://admin.cloud.microsoft`.
2. Go to **Agents** > **Overview** and review the **Agents at risk** card. It lists the three agents with the highest aggregated risk counts. Select **View agents** to open **All agents** > **Registry**, filtered and sorted by risk level.
3. Alternatively, go to **Agents** > **All agents** > **Registry** and select the **Agents at risk** tile. It opens a prefiltered view of agents with one or more risk signals.
4. Review the **Risks** column. It shows the aggregated count of risk signals for each agent.

**Check result**
- You can see the **Agents at risk** tile and the **Risks** column. A count of zero means that no active signals are currently detected for that agent.

### 8.7.2 Review risk details for a flagged agent
Performed by **AI Reader**, **Global Reader**, or **Security Reader**.
1. In the registry, select the count in the **Risks** column for a flagged agent. The **Risk details** pane opens.
2. Review the risk signals, grouped into expandable high, medium, and low severity sections, with a description and an **Occurrences** count for each signal.
3. Review **Risk signals are sourced from**. It shows the Microsoft security platforms contributing risk signals for the agent, such as Microsoft Purview, Microsoft Entra, and Microsoft Defender. Only platforms with contributing signals are shown.
4. If the agent has multiple instances, drill down into the signals for the selected instance.
5. Select a platform name to follow the deep link into that portal. The Microsoft Defender deep link requires Global Administrator, Global Reader, Security Reader, Security Administrator, or AI Administrator.

**Check result**
- For one agent, you can show which platforms contributed its risk signals and open the corresponding portal.

> Purview risk signals come from the Insider Risk Management agent policy verified in [7.8 Insider Risk Management verification](../chapter-07-sensitive-data-protection/README.md#78-insider-risk-management-verification). Entra ID Protection for agents is covered in [3.9 Detect and respond with ID Protection](../chapter-03-identity-ownership/README.md#39-detect-and-respond-with-id-protection). The Microsoft Purview IRM alerts deep link requires IRM Analyst or IRM Investigator; Global Administrator alone is insufficient.

### 8.7.3 Block a risky agent from the registry
Performed by **AI Administrator**.

Use this procedure for containment in 8.10.6.
1. Sign in to the Microsoft 365 admin center and select **Agents** > **All agents**.
2. Select the agent from the list.
3. In the agent details pane, immediately under the agent's name, select **Block**.
4. In the **Block agent** pane, select **Block agent**, then select **Save**.

To unblock, select **Unblock** in the agent details pane, then in the **Unblock agent** pane select **Unblock agent** and **Save**.

Blocking an agent restricts access to it across the organization, preventing any user from using it. For agents created with Microsoft Copilot Agent Builder and Microsoft Copilot Studio, blocking affects availability and functionality in Microsoft Copilot and in other host products, such as Outlook and Teams. Blocking an agent created with SharePoint or Microsoft Foundry only affects its availability in Microsoft Copilot Chat.

**Check result**
- The agent details pane now offers **Unblock** for the agent.

> Ownerless agents are handled in [5.5 Govern ownerless agents](../chapter-05-lifecycle-audit/README.md#55-govern-ownerless-agents). Blocking and unblocking in the lifecycle context is covered in [5.3.1 Block or unblock an agent](../chapter-05-lifecycle-audit/README.md#531-block-or-unblock-an-agent).

## 8.8 Review the AI agent inventory in Defender
**Documentation:** [Discover AI agents and assess security posture using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-inventory) · [AI agent posture risk in Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-risk-assessment)

Microsoft Defender provides a centralized inventory of AI agents and assesses their security posture. The inventory includes agents built with Microsoft Copilot Studio, Microsoft Foundry, Microsoft 365, and supported non-Microsoft platforms, and local AI agents discovered on endpoint devices.

### 8.8.1 Open the AI agents inventory
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

### 8.8.2 Review the agent details pane and agent page
Performed by **Security Reader**.
1. Select the Copilot Studio test agent to open its details pane. The pane displays the risk and configuration information available for the agent.
2. Select **Open Agent page**. The **Overview** tab shows the security and configuration information available for the agent, which can include risk level and active risk indicators, agent configuration details, identity and authentication information, endpoint and user context, attack-surface relationships, active alerts, security recommendations, tools, and MCP servers.
3. Record the agent's risk level and risk indicators as the baseline before the test in 8.10.

A risk indicator isn't always something that can be remediated; it might reflect the agent's intended purpose or design.

### 8.8.3 Review recommendations and incidents for the agent
Performed by **Security Reader**.
1. On the agent page, select **Security recommendations**. Select a recommendation to review its description and supporting evidence on the **Overview** tab, corrective actions on the **Remediation steps** tab, and affected agents on the **Exposed assets** tab.
2. Select **Incidents and alerts** to review security incidents and alerts associated with the agent. Select an incident to open its details pane, or select **Open incident page** for the full investigation experience.

The available tabs depend on the agent platform and the security information associated with the agent.

**Check result**
- You can open the **Security recommendations** and **Incidents and alerts** tabs for the test agent, where available.

> Recommendations are determined separately from the risk level. A high-risk agent might have no recommendations, and a lower-risk agent might receive one. Review risk level and recommendations together.

## 8.9 Hunt for agent activity with Advanced Hunting
**Documentation:** [Detect and investigate threats to AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection) · [Advanced hunting overview](https://learn.microsoft.com/defender-xdr/advanced-hunting-overview) · [AgentsInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-agentsinfo-table) · [CloudAppEvents table](https://learn.microsoft.com/defender-xdr/advanced-hunting-cloudappevents-table) · [BehaviorInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-behaviorinfo-table) · [AlertInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-alertinfo-table) · [AlertEvidence table](https://learn.microsoft.com/defender-xdr/advanced-hunting-alertevidence-table) · [Troubleshoot Direct OTel Observability – Defender advanced-hunting query](https://learn.microsoft.com/microsoft-agent-365/developer/direct-open-telemetry-troubleshooting) · [Create custom detection rules](https://learn.microsoft.com/defender-xdr/custom-detection-rules) · [Manage existing custom detection rules](https://learn.microsoft.com/defender-xdr/custom-detection-manage)

| Table | Contents for AI agent investigation |
|---|---|
| `AgentsInfo` | Inventory and configuration details for AI agents, including agent identity, platform, ownership, and metadata (replaces `AIAgentsInfo`) |
| `CloudAppEvents` | Agent 365 observability data for AI agent activity, including agent actions, tool invocations, and data access events |
| `BehaviorInfo` | Behaviors that record real-time protection rule activity, including audit and block events |
| `AlertInfo` | Alert metadata, including alerts related to near-real-time detections |
| `AlertEvidence` | Entities and artifacts associated with alerts |

Go to **Investigation & response** > **Hunting** > **Advanced hunting**. To use the prebuilt queries maintained by Microsoft, select the **Queries** tab, and then select **AI Agents**. Security Reader grants full read access to advanced hunting data.

### 8.9.1 Query the agent inventory
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

### 8.9.2 Hunt for weak agent configuration
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
- A clean environment can return no rows. Review any returned agent with its owner, and compare with the **Weak Instructions** risk indicator in 8.8.1.

> To find and govern ownerless agents, use [5.5 Govern ownerless agents](../chapter-05-lifecycle-audit/README.md#55-govern-ownerless-agents).

### 8.9.3 Trace agent activity in CloudAppEvents
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
- Rows for the test user's activity with the agent are returned. Record the agent identifier from `AgentId`, `TargetAgentId`, or `PlatformTargetAgentId` for the test agent; 8.9.5 uses it.
- No unexpected users or IP addresses appear.

### 8.9.4 Query alerts and real-time protection events
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
- After the audit pass in 8.10.3, the first query returns the alerts from the test.
- After the optional blocking pass, `BehaviorInfo` returns the block events.

### 8.9.5 Create a custom detection rule (optional)
Performed by **Security Administrator**.

This rule alerts on tool executions by the PoC test agent. It shows that agent activity can drive custom SOC detections; turn it off after the PoC.

1. In **Advanced hunting**, run the following query with the agent identifier recorded in 8.9.3. It returns `Timestamp` and `ReportId` from the same event, and `AccountObjectId` to map the impacted account.

   ```kql
   let pocAgentIds = dynamic(["<agent identifier from 8.9.3>"]);
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
- The rule is listed. After the test user triggers a tool call, the rule details page lists an alert under **Triggered alerts**.

## 8.10 Test runtime protection end to end
**Documentation:** [Detect and investigate threats to AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-detection-protection) · [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection) · [Enable external threat detection and protection for Copilot Studio custom agents – How it works](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider#how-it-works) · [Orchestrate agent behavior with generative AI](https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions) · [Alerts for AI services](https://learn.microsoft.com/azure/defender-for-cloud/alerts-ai-workloads)

This test proves the full chain: a risky action by the standard test user against the Copilot Studio test agent is detected (and blocked where a blocking rule applies), raises an alert that is associated with the agent, appears in the Agent 365 registry, and is contained by blocking the agent.

Microsoft Defender detects threats such as jailbreak attempts, indirect prompt injection (XPIA) attempts, malicious content propagation, secret and credential leakage, evasion techniques, large language model (LLM) reconnaissance, and suspicious user or IP access.

### 8.10.1 Prepare the test
Performed by **Security Administrator** with the **PoC maker account**.

| # | Precondition | How to check |
|---|---|---|
| 1 | Security for AI is enabled; Microsoft 365 connector and Copilot Studio show **Connected** | 8.2.1, 8.3.1, 8.4.4 |
| 2 | Threat detection is configured for the environment that hosts the test agent | 8.4.3 |
| 3 | The test agent uses generative orchestration | In Copilot Studio (`https://copilotstudio.microsoft.com`), open the agent's **Settings** page; in the **Generative AI** section, check **Orchestration**. New agents use generative orchestration by default. |
| 4 | The test agent has a knowledge source and at least one tool: the SharePoint knowledge source and the **Send an email (V2)** tool of the 7.6 agent | Agent configuration in Copilot Studio (7.6.2, 7.6.3) |
| 5 | The test agent is published to Microsoft 365 Copilot and Teams, and the standard test user can use it there | Test user opens the agent (7.9.6) |
| 6 | The test agent appears in **Assets** > **AI agents** and in `AgentsInfo` | 8.8.1, 8.9.1 |
| 7 | The **Default** real-time protection rule is listed; the optional custom block rule exists and is not enabled | 8.4.5 |
| 8 | Baseline captured: risk level and risk indicators in Defender, **Risks** count in the registry | 8.8.2, 8.7.1 |
| 9 | For scenario 1, the PoC maker account has added an unlabeled test document with the injected content to the SharePoint site that the agent uses as knowledge (7.4) | The document is listed in the site library |

> Custom agents created in Copilot Studio include built-in protection against user prompt-injection attacks (UPIA) and cross-domain prompt injection attacks (XPIA), and block these attacks at runtime. Record the agent's response for each scenario.

### 8.10.2 Test scenarios
The PoC team provides the prompts. Use only the test agent, the standard test user, and test data.

| # | Scenario | Prompt | Expected result |
|---|---|---|---|
| 1 | Indirect prompt injection via knowledge document | `<to be added>` | Audit pass: alert raised. Blocking pass: tool invocation blocked |
| 2 | Direct prompt injection / jailbreak | `<to be added>` | Audit pass: alert raised. Blocking pass: tool invocation blocked |
| 3 | Data exfiltration via tool call | `<to be added>` | Audit pass: alert raised. Blocking pass: tool invocation blocked |
| 4 | Benign control prompt that uses the same tool | `<to be added>` | The agent proceeds with no visible effect or interruption |

### 8.10.3 Run the scenarios as the standard test user
Performed by **standard test user** (and **Security Administrator** to enable or disable the custom rule).

**Pass A – audit.** Only the **Default** rule applies.
1. Sign in as the standard test user and open the Copilot Studio test agent in Microsoft 365 Copilot or Teams. Start a new conversation for each scenario.
2. Run scenario 4 (benign control) first.
3. Run scenarios 1 to 3, one per conversation. For each, record the time, the scenario number, and the agent's response (screenshot).

**Pass B – blocking (optional).** The Security Administrator selects the custom rule from 8.4.5 on the **Real-time protection** page and selects **Enable**.
1. Repeat scenarios 1 to 4 as the standard test user and record the same evidence.
2. After the pass, the Security Administrator selects the rule and selects **Disable**.

**Expected result**
- Pass A: matching activity is recorded as a behavior without stopping the action, and near-real-time detections surface as alerts.
- Pass B: matching actions are blocked before they execute and recorded as behaviors in `BehaviorInfo`. When the threat detection system blocks a tool invocation, the agent immediately stops processing and notifies the user that their message is blocked. Near-real-time alerts aren't generated for an agent covered by a blocking rule.
- Scenario 4: the agent proceeds with no visible effect or interruption.

### 8.10.4 Verify the alert and incident in Defender
Performed by **Security Reader** (review) or **Security Operator** (manage alerts).
1. In the Microsoft Defender portal, open the incidents queue and find the incident that contains the alert from Pass A.
2. Use the incident graph and investigation experience to review the relationships between the involved entities and the blast radius.
3. If prompt evidence collection is enabled, open the alert and review the prompt snippets included as evidence.
4. Go to **Assets** > **AI agents** > **Agents**, select the test agent, select **Open Agent page**, then select **Incidents and alerts** and confirm that the incident is listed.
5. On the **Agents** tab, review **Active alerts**, **Risk level**, and **Risk indicators** for the test agent.
6. Run the queries in 8.9.3 and 8.9.4 to correlate the alert with the agent's tool invocations and any block events.
7. As Security Operator, set the alert status and classification.

**Expected result**
- Defender correlates the AI agent alert into an incident.
- The incident is listed on the test agent's **Incidents and alerts** tab.
- The hunting queries return the alert and the related agent activity.

### 8.10.5 Verify the risk signal in the Agent 365 registry
Performed by **AI Reader**, **Global Reader**, or **Security Reader**.
1. Open **Agents** > **All agents** > **Registry** in the Microsoft 365 admin center. Risk signal counts might be up to an hour behind the security portals.
2. Select the **Agents at risk** tile and confirm that the test agent is listed.
3. Select its **Risks** count and confirm that **Microsoft Defender** appears under **Risk signals are sourced from**.
4. Select **Microsoft Defender** to follow the deep link into the Defender portal. The deep link requires Global Reader, Security Reader, Security Administrator, AI Administrator, or Global Administrator; AI Reader can't follow it.

**Expected result**
- IT sees what is flagged for the test agent from the Microsoft 365 admin center, without switching between portals or elevating to security roles.

### 8.10.6 Contain the agent and verify
Performed by **AI Administrator** (block), **standard test user** (verify), and **Security Operator** (alert status).
1. Block the test agent as described in 8.7.3. Record the time.
2. As the standard test user, try to use the test agent in Microsoft 365 Copilot and in Teams.
3. As Security Operator, set the alert status and classification, and record the containment time.

**Expected result**
- Blocking restricts access to the agent across the organization, preventing any user from using it; the test user can't use the agent in Microsoft Copilot or Teams.
- The time from the first alert to the block is the PoC containment metric.

> For identity-level containment of an agent with a Microsoft Entra agent identity, see [3.11.1 Disable and re-enable an individual agent identity](../chapter-03-identity-ownership/README.md#3111-disable-and-re-enable-an-individual-agent-identity).

### 8.10.7 Run the Foundry test agent scenarios (optional)
Performed by **standard test user** (scenarios), **Security Reader** (Azure role in Defender for Cloud) and a user who can view Defender for Cloud alerts in the Defender portal (alert review, see 8.1), and **Security Operator** (alert status).

Preconditions:
- **AI services** is **On** for the subscription that contains the Foundry test agent's resources (8.5.1), and user prompt evidence is set as agreed (8.5.2).
- The Foundry test agent from 1.2.2 is published. Threat detection is supported only for published Foundry agents; agents used only in a playground environment aren't supported.
- So that the standard test user can chat with it, the Foundry test agent is also published to Microsoft 365 Copilot and Teams as described in [Publish agents to Microsoft Copilot and Microsoft Teams in the Foundry portal](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-copilot). With the **Just you** scope, share the agent link with the standard test user; with **People in your organization**, an administrator approves the request in the Microsoft 365 admin center.
- The Foundry test agent appears in **Assets** > **AI agents** > **Agents** (8.8.1).

The PoC team provides the prompts. Use only the Foundry test agent, the standard test user, and test data.

| # | Scenario | Prompt | Expected result |
|---|---|---|---|
| F1 | Direct prompt injection / jailbreak | `<to be added>` | Defender for Cloud alert **A Jailbreak attempt on an Azure AI model deployment was blocked by Azure AI Content Safety Prompt Shields** or **A Jailbreak attempt on an Azure AI model deployment was detected by Azure AI Content Safety Prompt Shields** |
| F2 | Credential leakage in a model response | `<to be added>` | Defender for Cloud alert **Detected credential theft attempts on an Azure AI model deployment** |
| F3 | Indirect prompt injection via grounding data | `<to be added>` | Alert listed on the Foundry test agent's **Incidents and alerts** tab in the Defender portal |
| F4 | Benign control prompt | `<to be added>` | The agent responds normally |

1. As the standard test user, open the Foundry test agent in Microsoft 365 Copilot or Teams and run each scenario in a new conversation. Record the time, the scenario number, and the agent's response.
2. In the Azure portal, go to **Microsoft Defender for Cloud** > **Security alerts**, select the alert, and select **View full details**.
3. In the Microsoft Defender portal, open the alert queue, filter by **alert subscription ID**, and open the incident that contains the alert.
4. Go to **Assets** > **AI agents** > **Agents**, select the Foundry test agent, select **Open Agent page**, and review **Incidents and alerts**.
5. As Security Operator, set the alert status and classification. The status change is synchronized between the Defender portal and Defender for Cloud.

**Expected result**
- Defender for Cloud raises the AI alerts listed in [Alerts for AI services](https://learn.microsoft.com/azure/defender-for-cloud/alerts-ai-workloads) that match the scenarios.
- Defender for Cloud alerts, except informational alerts, appear in the Defender portal alert queue and are correlated into incidents.
- When user prompt evidence is on, the alert evidence includes the suspicious portions of the prompts and model responses, with sensitive data redacted. When it is off, the prompt content is masked in the alerts.

## 8.11 Evidence
- Screenshot of **Settings** > **Security for AI** > **Get started** with **Agent 365** **Done**, and **Microsoft 365 connector** and **Copilot Studio** **Connected**.
- Screenshot of the Power Platform admin center threat detection setup for the test environment.
- Screenshot of **Settings** > **Security for AI** > **Policies & rules** > **Real-time protection** with the **Default** rule and (optional) the custom rule.
- Screenshot of **Assets** > **AI agents** > **Agents** with the PoC agents, and the test agent page before and after the test (risk level, risk indicators, **Active alerts**).
- Exported results of the queries in 8.9.1, 8.9.3, and 8.9.4.
- Per scenario in 8.10.2: time, scenario number, pass (A or B), and the agent's response.
- The incident page for the test incident and the **Incidents and alerts** tab of the test agent.
- Screenshot of the registry **Agents at risk** view and the **Risk details** pane for the test agent.
- Screenshot of the **Block agent** pane and the test user's attempt to use the blocked agent.
- (Optional) Custom detection rule details page with **Triggered alerts**.
- (Optional) **Suspicious AI prompt injection** alert from 8.6.3.
- Timeline: first alert time, block time.
- (Optional, Foundry in scope) Screenshot of the subscription **Defender plans** page with **AI services** **On** and the **AI services** settings (user prompt evidence).
- (Optional, Foundry in scope) Per scenario in 8.10.7: time, scenario number, agent response, the Defender for Cloud alert (**View full details**), and the corresponding alert or incident in the Defender portal.

## 8.12 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| **Settings** > **Security for AI** setup isn't available | The tenant isn't onboarded to Agent 365 | Onboard to Agent 365 (prerequisite), see Chapter 0 and Chapter 1. |
| Microsoft 365 connector doesn't show **Connected** | Setup wasn't completed, or the required components weren't selected | Reopen the connector step, select **Microsoft Entra ID Management events** and **Microsoft 365 activities**, and select **Connect Microsoft 365**. |
| Copilot Studio activity is blocked but no alerts or incidents appear | Microsoft 365 connector not connected | Connect the connector (8.3). |
| Validation error when saving the App ID in Defender | The App ID was recently changed in Power Platform | Wait a short time (up to one minute) and try again. Use the same App ID as the Microsoft Entra application. |
| Power Platform: "There was a problem connecting to the protection provider. Try checking the endpoint link. If that doesn't work, contact the protection provider for help." | A call to the provided endpoint failed | Check the endpoint link (the integration URL from 8.4.1). |
| Power Platform: "There was a problem with the configuration. Try checking the details you entered and the Microsoft Entra configuration. If the problem persists, contact your admin for help." | Token acquisition failed | Check the Microsoft Entra application configuration and the Federated Identity Credentials. Select **Copy error info** for details. |
| Power Platform: "To change a configuration, make sure you have Power Platform admin permissions." | The user isn't a Power Platform Administrator | Use a user with the Power Platform Administrator role. |
| **Copilot Studio** step doesn't show **Connected** | The Power Platform administrator hasn't completed the onboarding steps | Ask one of the **Identified Power Platform Admins** to complete 8.4.3. |
| No Defender decision for the test agent | The agent uses classic orchestration, or the environment isn't configured | Use generative orchestration and configure threat detection for the agent's environment. |
| Tool runs although the threat detection system didn't answer | No decision within one second; default error behavior is **Allow the agent to respond** | Review **Set error behavior** (8.4.3). |
| Blocking pass produces no alert | Near-real-time alerts aren't generated for an agent covered by a blocking rule | Query `BehaviorInfo` (8.9.4) for the block events. |
| `CloudAppEvents` returns no agent rows | The **Microsoft 365 activities** component isn't selected, or the agent hasn't been used | Check 8.3, use the agent as the test user, and rerun 8.9.3. |
| Queries fail on `AIAgentsInfo`, `AgentName`, or `EntraAgentId` | Table and column names | Use `AgentsInfo`, `Name`, `EntraAgentID` and `EntraBlueprintID`. Run `AgentsInfo \| getschema` to list the columns in your tenant. |
| **Risks** count in the registry is still zero after an alert | Risk signal counts might be up to an hour behind the security portals | Wait and refresh. |
| You can't block an agent | Signed in with a role that can view but not manage agents (Global Reader, AI Reader, Security Administrator, Security Reader) | Use AI Administrator. |
| Custom detection can't be created | Read-only role, or Security Operator without **Manage Security Settings** when Defender for Endpoint RBAC is on | Use Security Administrator, or assign the permission. |
| No **Suspicious AI prompt injection** alert in 8.6.3 | Device prerequisites not met, Beta Channel not configured, or the terminal wasn't reopened after enabling protection | Fix the prerequisite, close agent and terminal sessions, open a new terminal, and rerun the demonstration. |
| You can't enable the **AI services** plan | Missing role on the subscription | Use Owner or Contributor on the subscription (8.5). |
| A Defender for Cloud AI alert isn't in the Defender portal | Informational alerts from Defender for Cloud aren't integrated into the Defender portal | Review the alert in **Microsoft Defender for Cloud** > **Security alerts**. |
| You can't see Defender for Cloud alerts in the Defender portal | No Microsoft Defender XDR Unified RBAC role for Defender for Cloud | Assign the Unified RBAC role for Defender for Cloud, or use Global Administrator or Security Administrator. |
| Alert prompt content is masked | User prompt evidence is disabled | Turn on **Enable user prompt evidence** (8.5.2). |
| No threat detection for the Foundry test agent | The agent isn't published, or it's used only in a playground environment | Publish the Foundry agent and test it through its published channel. |
| Image or audio content in a prompt isn't analyzed | Defender for Cloud supports text tokens only | Use text prompts for the Foundry scenarios. |

## 8.13 Cleanup
- Unblock the Copilot Studio test agent (8.7.3), unless the customer wants it to stay blocked.
- Turn off or delete the custom detection rule: **Hunting** > **Custom detection rules** > select `A365 PoC - test agent tool execution` > **Turn off** or **Delete**.
- Disable or delete the custom real-time protection rule: **Settings** > **Security for AI** > **Policies & rules** > **Real-time protection** > select `A365 PoC - block test agent` > **Disable** or **Delete**.
- Remove the test document with injected content from the SharePoint site (PoC maker account).
- Set the status and classification of the test alerts (Security Operator).
- (Optional) If the integration isn't kept after the PoC, the Power Platform Administrator disconnects it: **Security** > **Threat detection** > **Additional threat detection** > select the environment > **Set up** > unselect **Allow Copilot Studio to share data with your selected provider** > **Save**. Then delete the Microsoft Entra application registered in 8.4.2.
- (Optional) On local test devices, set `AiAgentProtection` and `AiAgentNetworkInspection` to `Disabled`, or unassign the runtime protection policy (8.6.2).
- (Optional) If the **AI services** plan was enabled only for the PoC, an Owner or Contributor goes to **Microsoft Defender for Cloud** > **Environment settings** > the subscription > **Defender plans** and toggles **AI services** to **Off**.
- (Optional) If the Foundry test agent isn't kept after the PoC, block it (8.7.3) or delete it as described in [5.8.1 Delete an agent (soft delete)](../chapter-05-lifecycle-audit/README.md#581-delete-an-agent-soft-delete).
- Keep Security for AI enabled and the Microsoft 365 connector connected; other chapters rely on them.

---
Previous: [Chapter 7 – Sensitive Data Protection (Purview)](../chapter-07-sensitive-data-protection/README.md) · Next: [Chapter 9 – Shadow AI and Local Agents](../chapter-09-shadow-ai-local-agents/README.md)
