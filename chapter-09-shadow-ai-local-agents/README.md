# Chapter 9 – Shadow AI and Local Agents

**Pillar:** Secure
**What it proves:** Unapproved AI apps and developer agent tools that run on managed Windows devices are visible in the Microsoft 365 admin center (which agent, on which devices, how many users, and how much network traffic), and administrators can block supported agents centrally through a Microsoft Intune policy.

**Success criteria**
- The **Shadow AI (Frontier)** and **Local Agents (Frontier)** pages open for the PoC reviewer and list the agents that can be detected.
- At least one approved test tool installed on a managed Windows test device appears on the matching page, and the test device is listed on the agent's **Detected devices** tab with a **Last Seen** value.
- If Global Secure Access is enabled, the **Users**, **Most recent activity**, **Last scanned** and **Total traffic** fields are populated for the detected agent.
- After **Block** > **Apply Policies** on a Shadow AI agent, the **Security policies** tile shows that a blocking Intune policy is applied, and the policy (for OpenClaw, **A365 - Block OpenClaw**) is found in Microsoft Intune.
- After the policy applies to the test device, the common ways of running the blocked agent are blocked on that device.
- After cleanup, the block is removed (for a Shadow AI agent, the **Security policies** tile no longer displays a blocking Intune policy), and the test tools are uninstalled.

**Shadow AI and local agents at a glance**

| | Shadow AI | Local agents |
|---|---|---|
| What it is | Consumer-facing AI applications and standalone agents deployed across the organization without IT visibility or approval, which can operate autonomously on user devices | Developer-controlled tools and extensions (IDE plugins, CLIs, code editors) intentionally integrated into development workflows with explicit configuration |
| Microsoft 365 admin center page | **Agents** > **Shadow AI** | **All Agents** > **Local Agents (Frontier)** |
| Blocking mechanism | Microsoft Intune policy created from the Microsoft 365 admin center | Microsoft Intune policy created from the Microsoft 365 admin center; VS Code extension policy for agents that run as Visual Studio Code extensions |
| Device scope | Managed Windows devices enrolled in Microsoft Intune | Managed Windows devices enrolled in Microsoft Intune |

Local agents are intentionally chosen developer tools managed within known environments, while Shadow AI consists of unmanaged, autonomous applications deployed without organizational awareness. Both experiences are part of the Frontier preview program and are in public preview. Features, supported agents and behaviors might change before general availability.

## 9.1 Required permissions

Grant the read-only role first, give setup roles only to the people who make each change, and assign roles as Active (not eligible) for the PoC window.

| Task | Least-privilege role | Section |
|---|---|---|
| Enable Agent 365 Frontier for the tenant | Global Administrator | 9.2.1 |
| Confirm the Microsoft Defender for Endpoint discovery prerequisites on the test device | The customer's Defender for Endpoint administrator | 9.2.2 |
| Review Intune-enrolled Windows test devices | Intune Administrator | 9.2.3 |
| Enable Internet Access traffic forwarding, assign test users, and remove the assignment at cleanup (optional) | Global Secure Access Administrator | 9.2.4, 9.8 |
| View the **Shadow AI (Frontier)** and **Local Agents (Frontier)** pages, and block agents from these pages | Any one of: Security Administrator, AI Administrator, Global Reader, Security Reader, Security Operator, Reports Reader, User Experience Success Manager, Intune Administrator | 9.3, 9.4, 9.5.4 |
| Review the block policy in Intune, and remove the block at cleanup | Intune Administrator | 9.3.5, 9.5.5, 9.8 |
| Import the VS Code ADMX template, create the VS Code extension policy profile, and delete both at cleanup | Policy and Profile Manager (Intune built-in role) | 9.4.5, 9.5.5, 9.8 |
| Sync the test device from Intune | Help Desk Operator or Endpoint Security Manager (Intune built-in roles) | 9.5.6, 9.8 |
| Install and use the approved test tools on the test device | Standard test user (no admin role) | 9.5.2, 9.5.6 |
| Validation / read-only review | Security Reader or Reports Reader | 9.5.3 |

**Before you start:**
- Complete [Chapter 0 – Prerequisites and PoC preparation](../chapter-00-prerequisites/README.md): PoC accounts and role assignments ([0.4](../chapter-00-prerequisites/README.md#04-prepare-accounts-groups-and-role-assignments)), the test device ([0.6](../chapter-00-prerequisites/README.md#06-prepare-test-agents-and-test-devices)) and the propagation times ([0.7](../chapter-00-prerequisites/README.md#07-plan-for-propagation-times)).
- [Chapter 1 – Agent Discovery and Inventory](../chapter-01-agent-discovery/README.md) covers the overall agent inventory in the Microsoft 365 admin center.
- [Chapter 8 – Threat Detection and Runtime Protection (Defender)](../chapter-08-threat-detection/README.md) covers the optional Defender for Endpoint runtime protection for local agents ([8.6](../chapter-08-threat-detection/README.md#86-turn-on-local-ai-agent-runtime-protection-in-defender-for-endpoint-optional)).
- Prepare at least one dedicated Windows test device that's enrolled in Microsoft Intune and onboarded to Microsoft Defender for Endpoint, and one standard test user who signs in to it.
- Get written approval from the customer's security team for the exact list of AI tools that you may install on the test device (see 9.5.1). Don't install any tool that isn't on the approved list.
- Agree with the customer, before you test blocking, that a block created from the Microsoft 365 admin center creates a Microsoft Intune policy that automatically propagates to all managed Windows devices enrolled in Intune (see 9.3.4, 9.4.4 and 9.4.6).

## 9.2 Tenant and device prerequisites

**Documentation:** [Understand Shadow AI in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-shadow-ai) · [Understand Local Agents in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-local) · [Preview Agent 365 features through the Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier) · [Discover local AI agents with Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/discover-local-ai-agents) · [Device action: Sync](https://learn.microsoft.com/intune/device-management/actions/sync) · [Tutorial: Enable Internet Access traffic forwarding](https://learn.microsoft.com/entra/global-secure-access/tutorial-internet-access-enable-traffic-forwarding)

This section covers configuration only. Both pages require the Frontier preview opt-in and Microsoft Intune enrollment for managed Windows devices. Shadow AI also requires Microsoft Defender for Endpoint on devices for shadow agent detection. Global Secure Access is optional and adds metadata about how detected agents are being used.

### 9.2.1 Opt in to the Frontier preview

Skip this task if Frontier was already enabled in [0.3.2](../chapter-00-prerequisites/README.md#032-enable-the-frontier-program-only-if-needed).

Performed by **Global Administrator**. Only a Global Administrator can enable Agent 365 Frontier.
1. Sign in to the Microsoft 365 admin center at `https://admin.cloud.microsoft`.
2. Go to **Agents** > **Overview**.
3. In the banner, select **Try now**, and then select **I agree** to accept the Agent 365 Terms of Service.

**Check result**
- The Agent 365 Terms of Service are accepted. This is how you check that the tenant is enrolled in Agent 365 Frontier.

### 9.2.2 Confirm Microsoft Defender for Endpoint on the test devices

Performed by the administrator who manages Microsoft Defender for Endpoint onboarding in the customer's organization.

Shadow AI requires Microsoft Defender for Endpoint on devices for shadow agent detection. The Defender local AI agent discovery prerequisites are:
- The environment is in the commercial cloud. Sovereign and national clouds aren't supported.
- The devices are [onboarded to Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/onboard-configure).
- The devices run a supported version of Windows, and Microsoft Defender Antivirus is updated with current monthly platform and engine updates.
- Microsoft Defender Antivirus runs in active mode on the devices, with real-time protection enabled.

No other deployment, configuration or scripts are needed beyond device onboarding. When a device meets all the prerequisites, agent discovery starts automatically.

**Check result**
- The test device meets every prerequisite in the list.

### 9.2.3 Confirm Intune enrollment of the Windows test devices

Performed by **Intune Administrator**.

Detection and blocking on both pages apply only to managed Windows devices enrolled in Microsoft Intune.

1. Sign in to the Microsoft Intune admin center at `https://intune.microsoft.com`.
2. Go to **Devices** > **All devices**.
3. Select the test device from the devices list.

**Check result**
- The Windows test device is listed in Intune.

### 9.2.4 Enable Global Secure Access for traffic metadata (optional)

Performed by **Global Secure Access Administrator** (steps 1–6). Steps 7–9 are performed on the test device.

Enable Global Secure Access for the tenant and the enrolled devices to view more metadata about how detected agents are being used. The fields that need Global Secure Access are listed in 9.3.2 and 9.4.2.

1. Sign in to the Microsoft Entra admin center at `https://entra.microsoft.com`.
2. Go to **Global Secure Access** > **Connect** > **Traffic forwarding**.
3. Select the **Internet access profile** checkbox to enable it.
4. In the **Internet access profile** section, under **User and group assignments**, select **View**.
5. Under **Assigned**, select **0 users, 0 groups assigned**, and then select **Add user/group**.
6. Search for and select the PoC test user (or a PoC test group), and then select **Assign**.
7. On the test device, download the Global Secure Access client for Windows 11 from `https://aka.ms/GlobalSecureAccess-Windows` (or `https://aka.ms/GlobalSecureAccess-WindowsOnArm` for Arm-based devices), and complete the installation wizard.
8. Confirm that the Global Secure Access client icon appears in the Windows system tray.
9. Right-click the icon, select **Advanced Diagnostics** > **Forwarding profile**, and confirm that the Internet Access rules are present.

**Check result**
- The Internet Access traffic forwarding profile is enabled and assigned to the PoC test users or group.
- The client on the test device shows the Internet Access rules. The client checks for forwarding profile changes every five minutes. If the rules aren't shown yet, wait five minutes and then select **Refresh**.

## 9.3 Shadow AI

**Documentation:** [Understand Shadow AI in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-shadow-ai) · [Assign device profiles in Microsoft Intune](https://learn.microsoft.com/intune/device-configuration/assign-device-profile) · [Understand Local Agents in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-local) · [Settings list for the Local AI Agent Baseline - OpenClaw security baseline in Intune](https://learn.microsoft.com/intune/device-security/security-baselines/ref-openclaw-settings)

Shadow AI refers to consumer-facing AI applications and standalone agents deployed across the organization without IT visibility or approval. Unmanaged usage introduces risks such as data leakage, compliance violations, security vulnerabilities, and lack of auditability and governance. The **Shadow AI (Frontier)** page is a dedicated experience, separate from the **All agents** page, that focuses on unmanaged AI agents that require detection and governance.

### 9.3.1 Open the Shadow AI (Frontier) page

Performed by any viewing role from 9.1 (for example **Security Reader**).
1. Sign in to the Microsoft 365 admin center at `https://admin.cloud.microsoft`.
2. Select **Agents** > **Shadow AI**.
3. Review the list of known Shadow AI agents that can be detected in your environment.

During public preview, the Shadow AI experience provides the following capabilities:

| Agent | Detection | Blocking |
|---|---|---|
| OpenClaw | Available | Available |
| ChatGPT Desktop | Available | Not available |
| Ollama Desktop | Available | Not available |
| Poe Desktop | Available | Not available |
| Claw/ZeroClaw | Available | Not available |
| OpenCode | Available | Not available |
| Claude Desktop | Available | Not available |

**Check result**
- The **Shadow AI (Frontier)** page opens and lists the known Shadow AI agents.

### 9.3.2 Review Shadow AI agent details

Performed by any viewing role from 9.1 (for example **Security Reader**).
1. On the **Shadow AI (Frontier)** page, select the Shadow AI agent from the list. The details pane opens.
2. Confirm that **Details** is selected, and review the agent information:
   - **Details** tile: **First accessed** (date the agent was first accessed), **Most recent activity** (date the agent was last used), **Last scanned** (date the agent was last detected).
   - **Detections** tile: **Devices** (count of devices that this agent is detected running on), **Users** (unique count of users that are detected using this agent).
   - **Security policies** tile: displays whether a blocking Intune policy has been applied to prevent this agent from running.
   - **Total traffic** tile: **Unique endpoints** (number of unique FQDNs the agent accessed), **Requests** (number of network requests made by the agent), **Data sent**, **Data received**.

The following fields and tiles are populated only if Global Secure Access is enabled (9.2.4):
- **Total traffic** tile
- **Users** field
- **Most recent activity** field
- **Last scanned** field

**Check result**
- The details pane opens for the selected agent, and **Devices** shows the count of devices that the agent is detected running on.

### 9.3.3 Review detected devices for a Shadow AI agent

Performed by any viewing role from 9.1 (for example **Security Reader**).
1. In the Shadow AI agent details pane, select the **Detected devices** tab.
2. Search for the test device name.
3. Review the device data: **Device name**, **Model** (Desktop, Virtual Machine, Server, Laptop and so on), **Operating system**, and **Last Seen** (the last time Microsoft Defender detected the agent on the device).

**Check result**
- The test device is listed with a **Last Seen** value.

### 9.3.4 Block a Shadow AI agent

Performed by any role from 9.1 that can view the page (for example **Intune Administrator**).

After the Shadow AI agent is identified in your environment, you can block it to prevent execution on managed devices. When you block a Shadow AI agent, such as OpenClaw, it blocks common ways of running it by creating a new Microsoft Intune policy that automatically propagates to **all managed Windows devices enrolled in Intune**.

> Caution: depending on how Intune is configured in your organization, the Intune policy update can take anywhere from 15 minutes up to 8 hours to apply. Show the policy being applied in a live demo, and check the device in a later session.

> Caution: OpenClaw is a Node.js-based agent. Node.js-based agents share a single run type, so blocking one blocks them all (see 9.4.6).

1. Open the details pane of a Shadow AI agent for which blocking is available (see 9.3.1).
2. Select **Security policies**.
3. Under **Security policies**, select **Block** > **Apply Policies**.
4. Record the date and time of the block.

**Check result**
- The **Security policies** tile displays that a blocking Intune policy has been applied to prevent this agent from running.

### 9.3.5 Review the block policy in Intune

Performed by **Intune Administrator**.

Full policy details, including when the Intune policy applies, can be found in Intune. Policies can also be edited in Intune to add more controls. For the Node.js block, see [Settings list for the Local AI Agent Baseline - OpenClaw security baseline in Intune](https://learn.microsoft.com/intune/device-security/security-baselines/ref-openclaw-settings). That baseline limits the use of unauthorized local AI agents such as OpenClaw by configuring device settings that disrupt commonly used execution paths, including firewall rules that restrict outbound network communication from Node.js. Its settings might not fully block all agent execution paths, and it might also block other processes in addition to OpenClaw.

1. Sign in to the Microsoft Intune admin center at `https://intune.microsoft.com`.
2. Search for the policy name **A365 - Block OpenClaw**.
3. Review the policy details.

**Check result**
- The **A365 - Block OpenClaw** policy is found in Intune, and its details are recorded.

## 9.4 Local agents

**Documentation:** [Understand Local Agents in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-local) · [Assign device profiles in Microsoft Intune](https://learn.microsoft.com/intune/device-configuration/assign-device-profile) · [Settings list for the Local AI Agent Baseline - OpenClaw security baseline in Intune](https://learn.microsoft.com/intune/device-security/security-baselines/ref-openclaw-settings) · [Import custom and third-party partner ADMX templates in Microsoft Intune](https://learn.microsoft.com/intune/device-configuration/settings-catalog/import-custom-admx-templates) · [Manage extensions in enterprise environments (Visual Studio Code)](https://code.visualstudio.com/docs/enterprise/extensions) · [Centrally manage VS Code settings with policies](https://code.visualstudio.com/docs/enterprise/policies)

Local agents are developer-controlled tools and extensions, such as IDE plugins, CLIs and code editors, that are intentionally integrated into development workflows with explicit configuration. They include extensions for VS Code and similar developer-focused applications. The **Local Agents (Frontier)** page is a dedicated experience, separate from the **All agents** page.

### 9.4.1 Open the Local Agents (Frontier) page

Performed by any viewing role from 9.1 (for example **Security Reader**).
1. Sign in to the Microsoft 365 admin center at `https://admin.cloud.microsoft`.
2. Select **All Agents** > **Local Agents (Frontier)**.
3. Review the list of known local agents that you can detect in your environment.

During public preview, the Local Agents experience can detect the following local agents:

| Name | Detection | Blocking |
|---|---|---|
| Antigravity CLI | Available | Not Available |
| Antigravity Desktop | Available | Not Available |
| Antigravity IDE | Available | Not Available |
| Claude Code | Available | Not Available |
| Codex CLI | Available | Not Available |
| Codex Desktop | Available | Not Available |
| Cursor | Available | Not Available |
| Devin Desktop | Available | Not Available |
| GitHub Copilot App | Available | Not Available |
| GitHub Copilot CLI | Available | Not Available |
| Junie CLI | Available | Not Available |
| Kiro CLI | Available | Not Available |
| Kiro IDE | Available | Not Available |
| Microsoft Scout | Available | Not Available |
| Warp | Available | Not Available |
| Windsurf | Available | Not Available |
| Gemini CLI | Available | Available |
| VSCode Claude Code Extension | Available | Available |
| VSCode Cline Extension | Available | Available |
| VSCode Codex Extension | Available | Available |
| VSCode Gemini Code Assist Extension | Available | Available |
| VSCode GitHub Copilot Extension | Available | Available |
| VSCode Roo Code Extension | Available | Available |

**Check result**
- The **Local Agents (Frontier)** page opens and lists the known local agents.

### 9.4.2 Review local agent details

Performed by any viewing role from 9.1 (for example **Security Reader**).
1. Select the agent from the **Local Agents** list on the **Local Agents (Frontier)** page. The **Details** pane opens.
2. Select the **Details** tab and review the agent information:
   - **Details** tile: **First accessed**, **Most recent activity**, **Last scanned**.
   - **Detections** tile: **Devices** (count of devices that this agent is detected running on), **Users** (unique count of users that are detected using this agent).
   - **Total traffic** tile: **Unique endpoints** (number of unique FQDNs the agent accessed), **Requests**, **Data sent**, **Data received**.

The following fields are populated only if Global Secure Access is enabled (9.2.4): **Users**, **Most recent activity**, **Last scanned**, **Unique endpoints**, **Requests**, **Data sent** and **Data received**.

**Check result**
- The **Details** pane opens for the selected agent, and **Devices** shows the count of devices that the agent is detected running on.

### 9.4.3 Review detected devices for a local agent

Performed by any viewing role from 9.1 (for example **Security Reader**).
1. Select the agent from the **Local Agents** list on the **Local Agents (Frontier)** page.
2. Select the **Detected devices** tab.
3. View the devices in the device table, or search for the test device name.

| Device information | Description |
|---|---|
| Device name | Name of the device |
| Model | Type of device, such as Desktop, Virtual Machine, Server or Laptop |
| Operating system | Operating system installed on the device |
| Last Seen | The last time Microsoft Defender detected the agent on the device |

**Check result**
- The test device is listed with a **Last Seen** value.

### 9.4.4 Block a local agent with an Intune policy

Performed by any role from 9.1 that can view the page (for example **Intune Administrator**).

After you identify the local AI agent in your environment, you can block it to prevent execution on managed devices. When you block a local AI agent, it blocks common ways of running it by creating a new Microsoft Intune policy that automatically propagates to **all managed Windows devices enrolled in Intune**. Depending on how Intune is configured in your organization, the policy update can take anywhere from 15 minutes up to 8 hours to apply. To view the policy details, search Intune for the policy name **A365 - Block OpenClaw** (9.3.5).

> Caution: Gemini CLI is a Node.js-based agent. Blocking it blocks all Node.js-based agents (see 9.4.6).

1. Open the details pane of a local agent for which blocking is available (see 9.4.1).
2. Select **Security policies**.
3. Under **Security policies**, select **Block agent** > **Apply Policies**.
4. Record the date and time of the block.

**Check result**
- **Block agent** > **Apply Policies** completes for the selected agent, and the Intune policy is found in Intune (9.3.5).

### 9.4.5 Block VS Code extension agents with a VS Code extension policy

Performed by **Policy and Profile Manager**.

Agents that run as Visual Studio Code extensions (the **VSCode ... Extension** entries in 9.4.1) are blocked by using a VS Code extension policy. The policy is deployed to managed devices and enforced by Visual Studio Code. You can view blocked VS Code extension agents in Visual Studio Code under the allowed extension list.

The VS Code extension policy is the `AllowedExtensions` policy, which manages the `extensions.allowed` setting (supported from VS Code version 1.96). Use the full extension ID (`<publisher>.<extension>`) to allow or block a specific extension. The more specific selector takes precedence, and `"*"` is the only supported wildcard. If you block an extension that's already installed, the extension is disabled. For cloud-managed devices, VS Code documents Microsoft Intune as an MDM solution for configuring the imported VS Code administrative template policies.

1. Get the `vscode.admx` file and its ADML file from the `policies` folder of an existing VS Code installation (version 1.69 or later) or of the extracted VS Code zip archive.
2. Sign in to the Microsoft Intune admin center at `https://intune.microsoft.com`.
3. Select **Devices** > **Manage devices** > **Configuration** > **Import ADMX** tab > **Import**.
4. Upload the ADMX file and the ADML file for the default language, select **Next**, and in **Review + Create** select **Create**. Select **Refresh** to see the upload **Status**.
5. Select **Devices** > **Manage devices** > **Configuration** > **Create** > **New policy**.
6. For **Platform**, select **Windows 10 and later**. For **Profile type**, select **Templates** > **Imported Administrative templates (Preview)**, and then select **Create**.
7. In **Basics**, enter a name such as `PoC - VS Code - Block <extension>`, and then select **Next**.
8. In **Configuration settings**, configure the `AllowedExtensions` policy with a value that blocks the test extension while allowing others, and then select **Next**:

   ```json
   {
     "*": true,
     "<publisher>.<extension>": false
   }
   ```

9. In **Assignments**, select the PoC test group that contains the test device or test user, and then select **Next**.
10. In **Review + create**, select **Create**.

If there's a syntax error in the policy value, the `extensions.allowed` setting isn't applied. To check for errors, open the Command Palette in VS Code and run **Show Window Log**.

**Check result**
- The VS Code ADMX template is imported, and the policy profile is created, shown in the profiles list and assigned to the PoC test group.
- After the test device receives the policy (9.5.6), the blocked extension is disabled in VS Code.

### 9.4.6 Understand the Node.js shared run type

Node.js-based agents share a single run type, so blocking one blocks them all. When you block any of the following agents, you block all of them:
- OpenClaw
- QClaw
- Claw/Nanobot
- Gemini CLI

> Caution: blocking a Node.js-based agent blocks all agents and processes of that run type on managed devices. Make sure that no legitimate business processes depend on these agents before you apply the policy. Removing a block on any Node.js-based agent removes the Node.js block for all other Node.js-based agents, not just the one you selected.

For the settings of this Intune policy, see [Settings list for the Local AI Agent Baseline - OpenClaw security baseline in Intune](https://learn.microsoft.com/intune/device-security/security-baselines/ref-openclaw-settings).

## 9.5 Test and validation

Run these tests on a dedicated test device. Plan the block check (9.5.6) for a block created from the Microsoft 365 admin center at least 15 minutes and up to 8 hours after the block, because of the documented Intune policy update window.

### 9.5.1 Agree the test scope and prepare the test device

Performed by the **PoC lead** together with the customer's security team.
1. Choose the test tools from the lists in 9.3.1 and 9.4.1, and get the customer's written approval for each one. A minimal set:
   - **Detection only:** one Shadow AI desktop app (for example, Claude Desktop or ChatGPT Desktop) and one local developer tool (for example, GitHub Copilot CLI), if the customer approves them.
   - **Detection and blocking:** one VS Code extension agent that the customer approves (for example, the VSCode GitHub Copilot Extension). Test Gemini CLI or OpenClaw only if the customer explicitly accepts the Node.js block described in 9.4.6 for all managed Windows devices enrolled in Intune.
2. Confirm that the test device meets 9.2.2 and 9.2.3 (and 9.2.4 if Global Secure Access metadata is in scope).
3. Record the test device name, test user, approved tools and versions, and the agreed block window.

**Expected result**
- A signed-off list of approved test tools and a test device that meets all prerequisites.

### 9.5.2 Install the approved test tools and generate activity

Performed by the **standard test user** on the test device.
1. Install each approved tool from its official source.
2. Use each tool for a short task that contains no company data.
3. Record the time of the activity.

**Expected result**
- Each approved tool is installed and has been used on the test device.

### 9.5.3 Confirm detection in the Microsoft 365 admin center

Performed by **Security Reader** or **Reports Reader**.
1. For each Shadow AI test tool, complete 9.3.1 to 9.3.3.
2. For each local agent test tool, complete 9.4.1 to 9.4.3.

**Expected result**
- For each approved test tool, **Devices** shows the count of devices that the agent is detected running on, and the test device is listed on **Detected devices** with a **Last Seen** value.
- If Global Secure Access is enabled, **Users**, **Most recent activity**, **Last scanned** and the **Total traffic** values are populated.

### 9.5.4 Apply the block

Performed by any viewing role from 9.1 (for example **Intune Administrator**) for 9.3.4 and 9.4.4, and by **Policy and Profile Manager** for 9.4.5.
1. Confirm that the customer accepts the scope of the block: all managed Windows devices enrolled in Intune, and the Node.js shared run type if a Node.js-based agent is in scope.
2. For a Shadow AI test tool for which blocking is available, complete 9.3.4. For a local agent test tool for which blocking is available, complete 9.4.4. For a VS Code extension agent, complete 9.4.5.
3. Record the date and time of the block.

**Expected result**
- For a Shadow AI agent, the **Security policies** tile displays that a blocking Intune policy has been applied.
- For a local agent, **Block agent** > **Apply Policies** completes.
- For a VS Code extension agent, the VS Code policy profile is created and assigned to the PoC test group.

### 9.5.5 Confirm the policy in Intune

Performed by **Intune Administrator** (block policy) or **Policy and Profile Manager** (VS Code policy profile).
1. For a block applied from the Microsoft 365 admin center, complete 9.3.5.
2. For a VS Code extension policy, go to **Devices** > **Manage devices** > **Configuration** and confirm that the profile from 9.4.5 is in the profiles list.

**Expected result**
- The block policy is found in Intune, and the VS Code policy profile (if used) is in the profiles list.

### 9.5.6 Confirm the block on the test device

Performed by **Help Desk Operator** or **Endpoint Security Manager** (device sync) and the **standard test user** (device test).
1. In the Microsoft Intune admin center, select **Devices** > **All devices**, and select the test device.
2. At the top of the device overview pane, select **Sync**, and then select **Yes** to confirm. To track progress, select the **Device sync status** tab (this tab requires the **Preview new device view** toggle at the top right of the Intune admin center to be on).
3. On the test device, try to run the blocked tool again in the same way as in 9.5.2.
4. For a VS Code extension block, open Visual Studio Code and review the allowed extension list.

**Expected result**
- For a block created from the Microsoft 365 admin center, after the Intune policy applies (15 minutes up to 8 hours, depending on Intune configuration), the common ways of running the blocked agent are blocked on the test device.
- For a VS Code extension block, the blocked extension is disabled and the blocked VS Code extension agent is shown under the allowed extension list.

## 9.6 Evidence

- Screenshot of the **Shadow AI (Frontier)** page and the **Local Agents (Frontier)** page with the list of known agents.
- Screenshot of the details pane (**Details**, **Detections**, **Security policies**, **Total traffic**) for each detected test tool.
- Screenshot of the **Detected devices** tab with the test device and **Last Seen**.
- Screenshot of the **Security policies** tile after **Block** > **Apply Policies** (Shadow AI), or of the completed **Block agent** > **Apply Policies** action (local agents), with the date and time of the block.
- Screenshot of the block policy details in Intune, and of the VS Code policy profile if used.
- Screenshot of the Intune **Device sync status** tab for the test device.
- Screenshot from the test device that shows the blocked tool or the disabled VS Code extension.
- The signed-off list of approved test tools (9.5.1).
- Screenshot of the **Security policies** tile after cleanup, and confirmation that the test tools are uninstalled (9.8).

## 9.7 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| The **Shadow AI** or **Local Agents (Frontier)** page isn't available | The tenant hasn't opted in to the Frontier preview, or the account doesn't hold one of the required roles | Complete 9.2.1. Assign one of the roles listed in 9.1. |
| The test tool is installed but not detected on the Shadow AI page | Microsoft Defender for Endpoint discovery prerequisites aren't met, or the device isn't enrolled in Intune | Recheck 9.2.2 and 9.2.3. |
| The test tool isn't listed on either page | The tool isn't in the list of agents supported during public preview, or the device isn't a managed Windows device enrolled in Intune | Compare with the tables in 9.3.1 and 9.4.1, and recheck 9.2.3. |
| **Users**, **Most recent activity**, **Last scanned** or **Total traffic** are empty | Global Secure Access isn't enabled for the tenant and enrolled devices | Complete 9.2.4. |
| Blocking isn't available for an agent | Blocking isn't available for that agent during public preview | Check the **Blocking** column in 9.3.1 and 9.4.1, and choose a test tool for which blocking is available. |
| The policy is applied but the agent still runs on the device | The Intune policy update hasn't applied yet (15 minutes up to 8 hours, depending on Intune configuration) | Sync the device (9.5.6), and check again within the documented window. |
| Other Node.js-based agents or processes stopped running on managed devices | Node.js-based agents share a single run type, and blocking one blocks all agents and processes of that run type | Expected behavior (9.4.6). If the impact isn't acceptable, remove the block (9.8). |
| The VS Code extension isn't blocked | Syntax error in the policy value, or VS Code version earlier than 1.96 | Run **Show Window Log** in VS Code to check for errors, and use VS Code 1.96 or later. |

## 9.8 Cleanup

Performed by the roles listed in 9.1 for each step (Intune Administrator, Policy and Profile Manager, Help Desk Operator or Endpoint Security Manager, Global Secure Access Administrator, and the standard test user on the test device).

1. Remove the block for the test agent. The block is a Microsoft Intune policy that you can find in Intune by its name (for example, **A365 - Block OpenClaw**, see 9.3.5). Removing a block on any Node.js-based agent removes the Node.js block for all other Node.js-based agents.
2. Delete the PoC VS Code policy profile. Then, if the VS Code ADMX template was imported only for the PoC, delete it from the **Import ADMX** tab. Delete the profiles that use an imported ADMX file before you delete the file.
3. Sync the test device (9.5.6).
4. Uninstall all test tools from the test device, and remove any accounts or keys created for them.
5. If Global Secure Access was enabled only for the PoC, remove the test users from the Internet Access profile assignment (9.2.4), and uninstall the client from the test device.
6. Remove the temporary PoC role assignments from 9.1.

**Check result**
- The block is removed (for a Shadow AI agent, the **Security policies** tile of the test agent no longer displays a blocking Intune policy).
- The PoC VS Code policy profile is no longer in the profiles list.
- The test tools are uninstalled from the test device.

---
Previous: [Chapter 8 – Threat Detection and Runtime Protection (Defender)](../chapter-08-threat-detection/README.md) · Next: [Runbook overview](../README.md)
