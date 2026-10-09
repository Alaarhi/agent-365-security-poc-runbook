# Chapter 0 – Prerequisites and PoC preparation

**Pillar:** All
**What it proves:** The tenant, accounts, roles, test agents and test data are ready, so every later chapter can be run without stopping to fix access or wait for setup.

**Success criteria**
- The in-scope chapters and their success criteria are agreed and recorded (0.2).
- Every PoC account holds only the roles it needs, assigned as Active for the PoC window (0.1, 0.4).
- The **Agents** area of the Microsoft 365 admin center opens for the test admin and the reviewer (0.3).
- Microsoft Purview Audit is recording user and admin activity (0.5).
- The test agents and test devices needed by the in-scope chapters exist (0.6).
- If Chapter 8 is in scope, Defender Security for AI and the applicable integrations are ready before testing (0.6.2).
- The documented propagation times are built into the schedule (0.7) and the readiness checklist is complete (0.8).

## 0.1 Required permissions

Every chapter starts with its own **Required permissions** table. The table below summarizes them so you can request all role assignments at once. Grant the read-only roles first, grant setup roles only to the person who makes each change, and assign every role as **Active** (not Eligible) for the PoC window.

| Chapter | Setup roles | Read-only / validation roles |
|---|---|---|
| 1 – Agent Discovery and Inventory | AI Administrator; Agent ID Administrator (Graph reads of agent identities); Foundry Project Manager (publish a Foundry agent); Application Developer and Privileged Role Administrator (app-only Graph access) | AI Reader or Global Reader; Security Reader; Reports Reader |
| 2 – Third-Party and Custom Agents | AI Administrator (connected platforms); platform administrator of each source platform (AWS, Databricks, Google Cloud); Agent ID Developer plus Contributor on the Azure subscription (`a365 setup`); Application Administrator (service-to-service grants); Global Administrator (OAuth2 consent, package upload, `a365 cleanup`) | AI Reader; Directory Readers; Defender **Security data basics (read)** |
| 3 – Agent Identity and Ownership | Agent ID Administrator; Agent ID Developer (inheritable permissions); Attribute Definition Administrator; Attribute Assignment Administrator; Security Administrator (risk actions); Lifecycle Workflows Administrator; Power Platform Administrator (Copilot Studio migration) | Any Microsoft Entra user; Reports Reader; Security Reader; Attribute Assignment Reader |
| 4 – Tools and MCP Server Governance | AI Administrator; Global Administrator (Tools Gateway, Agent 365 Tools service principal, `grant-agents-access`); developer account (BYO MCP server registration and evaluation) | AI Reader or Global Reader; Security Reader |
| 5 – Agent Lifecycle and Audit | AI Administrator; Azure AI Owner (Foundry start/stop); Agent ID Administrator (optional Entra disable) | AI Reader or Global Reader; Audit Reader; Reports Reader; Security Reader |
| 6 – Conditional Access and Least Privilege | Conditional Access Administrator; Security Administrator; Identity Governance Administrator; Agent ID Administrator (lab agent identities); Groups Administrator; attribute roles (optional); Global Administrator with Attribute Assignment Administrator (policy templates) | Global Reader; Reports Reader; Security Reader |
| 7 – Sensitive Data Protection (Purview) | Data Security AI Admins or AI Administrator; Information Protection Admins; Communication Compliance Administrators; Insider Risk Management Admins; AI Administrator (agent approval) | Global Reader; Information Protection Analysts; Communication Compliance Investigators or Analysts |
| 8 – Threat Detection and Runtime Protection (Defender) | Security Administrator; user with permission to create Microsoft Entra app registrations; Power Platform Administrator; Security Operator; AI Administrator (block from registry); Azure Bot Service Contributor (or Contributor or Owner) on the resource group and Foundry User on the Foundry project (publish the Foundry agent); Owner or Contributor on the Azure subscription (optional Defender for Cloud AI services plan); permission to manage endpoint security policies in Defender (optional local runtime protection); Policy and Profile Manager or another Intune role with device-configuration permissions (optional local runtime protection) | Security Reader; Azure Security Reader (Defender for Cloud alerts); Defender for Cloud Unified RBAC role or Global Administrator/Security Administrator (Defender portal alerts) |
| 9 – Shadow AI and Local Agents | Global Administrator (Frontier); Intune Administrator; Policy and Profile Manager; Help Desk Operator or Endpoint Security Manager (device sync); Global Secure Access Administrator (optional) | Security Reader or Reports Reader |

Two rules that save PoC time:
1. Assign roles as **Active** for the PoC window, so an admin isn't stopped by an activation prompt in the middle of a task. Use Privileged Identity Management just-in-time activation only for Global Administrator.
2. Keep the split: the admin who makes a change doesn't review it, and the reviewer doesn't hold the setup role.

**Before you start:**
- Agree on the PoC tenant (a dedicated or non-production tenant is preferred) and the PoC window.
- Name a single PoC coordinator who owns the readiness checklist in 0.8.

## 0.2 Confirm the PoC scope

**Documentation:** [Overview of Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/overview)

### 0.2.1 Select the in-scope chapters
Performed by the **PoC coordinator** with the customer.

| # | Pillar | Chapter | In scope (Yes / No) |
|---|---|---|---|
| 1 | Observe | [Agent Discovery and Inventory](../chapter-01-agent-discovery/README.md) | |
| 2 | Observe | [Third-Party and Custom Agents](../chapter-02-third-party-custom-agents/README.md) | |
| 3 | Govern | [Agent Identity and Ownership](../chapter-03-identity-ownership/README.md) | |
| 4 | Govern | [Tools and MCP Server Governance](../chapter-04-tools-mcp-governance/README.md) | |
| 5 | Govern | [Agent Lifecycle and Audit](../chapter-05-lifecycle-audit/README.md) | |
| 6 | Secure | [Conditional Access and Least Privilege](../chapter-06-conditional-access/README.md) | |
| 7 | Secure | [Sensitive Data Protection (Purview)](../chapter-07-sensitive-data-protection/README.md) | |
| 8 | Secure | [Threat Detection and Runtime Protection (Defender)](../chapter-08-threat-detection/README.md) | |
| 9 | Secure | [Shadow AI and Local Agents](../chapter-09-shadow-ai-local-agents/README.md) | |

### 0.2.2 Agree the success criteria
1. Copy the **Success criteria** list from the top of each in-scope chapter into the PoC plan.
2. Remove the criteria for optional sections that are out of scope.
3. Get the customer's sign-off on the list before the first setup session.

**Check result**
- The in-scope chapters and their success criteria are signed off.

## 0.3 Confirm Agent 365 is available in the tenant

**Documentation:** [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started) · [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview) · [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)

### 0.3.1 Open the Agents area
Performed by **AI Administrator**, then repeated by **AI Reader**.
1. Sign in to the Microsoft 365 admin center (<https://admin.cloud.microsoft>).
2. Select **Agents** > **Overview**.
3. Select **Agents** > **All agents** and open the **Registry** tab.
4. Repeat steps 1 to 3 with the reviewer account (AI Reader).

**Check result**
- Both accounts can open **Agents** > **Overview** and **Agents** > **All agents** > **Registry**.

### 0.3.2 Enable the Frontier program (only if needed)
Shadow AI (Chapter 9), agents with their own identity, and third-party agent observability (Chapter 2) are Frontier features. Skip this task if none of them is in scope.

Performed by **Global Administrator**. Only a Global Administrator can enable Agent 365 Frontier.
1. In the Microsoft 365 admin center, go to **Agents** > **Overview**.
2. In the **Try now** banner, accept the terms by selecting **I agree**.
3. Record the date and time.

Frontier features are previews and preview terms apply.

**Check result**
- The Frontier features needed by the in-scope chapters are available, for example **Agents** > **Shadow AI** for Chapter 9.

## 0.4 Prepare accounts, groups and role assignments

**Documentation:** [Assign Microsoft Entra roles](https://learn.microsoft.com/entra/identity/role-based-access-control/manage-roles-portal) · [Microsoft Entra built-in roles](https://learn.microsoft.com/entra/identity/role-based-access-control/permissions-reference) · [Roles and role groups in Microsoft Purview](https://learn.microsoft.com/purview/purview-permissions)

### 0.4.1 Create the PoC accounts
Performed by **User Administrator**.

| Account | Purpose | Used in chapters |
|---|---|---|
| Test admin | Makes the configuration changes. Holds only the setup roles for the in-scope chapters. | All |
| Standard test user | Runs the agent tests and acts as a sponsor in the access package test. No admin role. | 3, 4, 5, 6, 8, 9 |
| Reviewer / auditor | Views evidence without making changes. Holds only the read-only roles. | All |
| Second test user | User outside the plugin pilot group. No admin role. | 4 |
| Maker account | Builds the Microsoft-native test agents (Copilot Studio, Agent Builder, Foundry) and the Chapter 7 SharePoint site. Permission to create agents in the PoC Copilot Studio environment and Foundry project. | 1, 5, 7, 8 |
| Developer account | Builds and registers custom agents and MCP servers with the Agent 365 CLI. | 2, 4 |
| Authorized and unauthorized test users | Chapter 7 acceptance tests: one user inside and one user outside the sharing scope of the PoC site and agents. No admin role. | 7 |
| Intended non-owner account | Discovers and installs the published Copilot Studio agent. Can be the authorized test user if it didn't create the agents. No admin role. | 7 |
| PoC Sponsor and PoC Sponsor Manager | Sponsor continuity test with Lifecycle Workflows. The **Manager** attribute of PoC Sponsor is set to PoC Sponsor Manager. | 3 |
| PoC approver | Approves access package requests. No admin role. | 6 |
| Controlled recipient mailbox | Receives the test email from the Copilot Studio email agent. Never use a real personal address. | 7 |

### 0.4.2 Create the PoC groups
Performed by **Groups Administrator**.

| Group | Members | Used in |
|---|---|---|
| `A365-PoC-Users` | Standard test user | Chapter 5 (install the test agent for a group) |
| `A365-PoC-Plugin-Pilot` | Standard test user only | Chapter 4 (plugin restricted to a group) |
| `PoC-Agent-Resource-Access` | None at the start | Chapter 6 (resource granted through an access package) |

### 0.4.3 Assign the roles
Performed by **Privileged Role Administrator** (Microsoft Entra roles) and a member of the **Organization Management** role group (Microsoft Purview role groups).
1. Assign the setup roles from 0.1 to the test admin, only for the in-scope chapters.
2. Assign the read-only roles from 0.1 to the reviewer.
3. Assign all roles as **Active** with an end date at the end of the PoC window.

**Check result**
- The test admin and the reviewer can each open the portals in 0.4.4.

### 0.4.4 Confirm portal access

| Portal | URL | Used in chapters |
|---|---|---|
| Microsoft 365 admin center | <https://admin.cloud.microsoft> | 1, 2, 4, 5, 6, 7, 8, 9 |
| Microsoft Entra admin center | <https://entra.microsoft.com> | 1, 2, 3, 5, 6, 9 |
| Microsoft Purview portal | <https://purview.microsoft.com> | 5, 7 |
| Microsoft Defender portal | <https://security.microsoft.com> | 1, 2, 4, 5, 8, 9 |
| Power Platform admin center | <https://admin.powerplatform.microsoft.com> | 3, 4, 8 |
| Copilot Studio | <https://copilotstudio.microsoft.com> | 1, 3, 4, 5, 7, 8 |
| Microsoft Intune admin center | <https://intune.microsoft.com> | 8, 9 |
| Azure portal | <https://portal.azure.com> | 2, 4, 8 |

## 0.5 Turn on Microsoft Purview Audit

**Documentation:** [Turn auditing on or off](https://learn.microsoft.com/purview/audit-log-enable-disable) · [Audit logs for Copilot and AI applications](https://learn.microsoft.com/purview/audit-copilot)

Chapter 5 uses audit records of agent actions, so turn on auditing before the test agents are used.

### 0.5.1 Confirm that auditing is on
Performed by a member of the **Audit Manager** role group.
1. Open the Microsoft Purview portal (<https://purview.microsoft.com>) and go to **Audit**.
2. If a banner prompts you to start recording user and admin activity, select it.
3. Record the date and time.

**Check result**
- **Audit** search is available and no banner asks you to start recording.

## 0.6 Prepare test agents and test devices

**Documentation:** [Microsoft Copilot Studio overview](https://learn.microsoft.com/microsoft-copilot-studio/) · [Agent Registry](https://learn.microsoft.com/microsoft-365/admin/manage/agent-registry) · [Enable security for AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai) · [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider) · [Enable threat protection for AI services](https://learn.microsoft.com/azure/defender-for-cloud/ai-onboarding) · [AI agent runtime protection in Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/configure-ai-agent-runtime-protection)

### 0.6.1 Prepare the test assets for the in-scope chapters
Performed by the **maker** or the **developer**, as described in the linked section.

| Test asset | How to build it | Used in |
|---|---|---|
| Microsoft-native test agents (Copilot Studio, Microsoft Foundry) | [1.2 Discover Microsoft-native agents](../chapter-01-agent-discovery/README.md#12-discover-microsoft-native-agents) | 1, 3, 5 |
| SharePoint communication site with the synthetic Word and Excel files labelled **Confidential** | [7.4 SharePoint communication site and PoC files](../chapter-07-sensitive-data-protection/README.md#74-sharepoint-communication-site-and-poc-files) | 7 |
| Microsoft 365 Copilot knowledge agent | [7.5 Microsoft 365 Copilot knowledge agent](../chapter-07-sensitive-data-protection/README.md#75-microsoft-365-copilot-knowledge-agent) | 7 |
| Copilot Studio email agent, published and approved | [7.6 Copilot Studio email agent and publication](../chapter-07-sensitive-data-protection/README.md#76-copilot-studio-email-agent-and-publication) | 7 |
| Copilot Studio test agent for runtime protection: the Chapter 7 email agent, and (optional) the published Microsoft Foundry test agent from 1.2.2 | [Chapter 8, Before you start](../chapter-08-threat-detection/README.md#81-required-permissions) | 8 |
| A member-submitted test agent in **Agents** > **All agents** > **Requests** with status **Pending review** (policy template test) | [6.7 Apply Conditional Access and custom security attributes at publish time](../chapter-06-conditional-access/README.md#67-apply-conditional-access-and-custom-security-attributes-at-publish-time-policy-templates) | 6 |
| `PoC-Lifecycle-Agent`: a shared Agent Builder or Copilot Studio agent you may permanently delete | [Chapter 5, Before you start](../chapter-05-lifecycle-audit/README.md#51-required-permissions) | 5 |
| Test agent on a supported third-party platform (for example an Amazon Bedrock agent, a Databricks Genie space, or a Google Vertex AI agent), in a non-production account | [2.2 Connect a third-party agent platform](../chapter-02-third-party-custom-agents/README.md#22-connect-a-third-party-agent-platform) | 2 |
| Custom agent built with the Agent 365 CLI and SDK | [2.7 Prepare the custom-agent toolchain](../chapter-02-third-party-custom-agents/README.md#27-prepare-the-custom-agent-toolchain) | 2 |
| Lab agent identity blueprint with the agent identities `PoC-Agent-Approved`, `PoC-Agent-Risk`, `PoC-Agent-Unapproved` | [6.1 Required permissions](../chapter-06-conditional-access/README.md#61-required-permissions) | 6 |
| Test remote MCP server with a public HTTPS endpoint (not a production server) | [4.6 Bring your own MCP server](../chapter-04-tools-mcp-governance/README.md#46-bring-your-own-mcp-server-preview) | 4 |
| Intune-enrolled Windows test device onboarded to Defender for Endpoint, and the customer-approved list of AI tools to install | [9.2 Tenant and device prerequisites](../chapter-09-shadow-ai-local-agents/README.md#92-tenant-and-device-prerequisites) | 8 (optional), 9 |

Use only synthetic data and controlled test accounts and recipients throughout the PoC.

**Check result**
- Every test asset needed by the in-scope chapters exists and is listed in the PoC plan with its owner.

### 0.6.2 Prepare Microsoft Defender Security for AI

Complete this setup after Agent 365 is onboarded and at least one relevant test agent is published. Chapter 8 contains the detailed steps; use this sequence to ensure all Defender components required by the PoC are ready before its tests. Setup roles are listed in 0.1 and detailed in [8.1 Required permissions](../chapter-08-threat-detection/README.md#81-required-permissions).

**Core setup for Chapter 8**

Performed by the **Security Administrator**.
1. In the Microsoft Defender portal, open **Settings** > **Security for AI** > **Get started**. Turn **Enable** on if it is off (it is on by default) and confirm that **Agent 365** shows **Done**. If Agent 365 is not onboarded, complete 0.3 and Chapter 1 first.
2. Confirm Microsoft Purview Audit is recording, as described in 0.5.1.
3. Connect the **Microsoft 365 connector** and select the components required for AI agent monitoring: **Microsoft Entra ID Management events** and **Microsoft 365 activities**. **Microsoft Entra Users and groups** is a prerequisite and is selected by default. Follow [8.3 Connect the Microsoft 365 connector](../chapter-08-threat-detection/README.md#83-connect-the-microsoft-365-connector).

**Copilot Studio real-time protection (when Copilot Studio is in scope)**

Use the published Copilot Studio test agent prepared in 0.6.1. It must be published to Microsoft 365 Copilot and Teams and use generative orchestration. The setup requires a **Security Administrator**, a **Power Platform Administrator**, and a user who can create Microsoft Entra application registrations.
Complete all four steps in [8.4 Turn on Copilot Studio real-time protection](../chapter-08-threat-detection/README.md#84-turn-on-copilot-studio-real-time-protection):
1. In Defender, turn on real-time protection and copy the integration URL.
2. Register a single-tenant Microsoft Entra application and configure its federated identity credential.
3. In the Power Platform admin center, configure threat detection for the environment containing the test agent, using the integration URL and App ID.
4. Save the same App ID in Defender.

**Check result**
- On the Defender **Get started** page, the **Copilot Studio** step shows **Connected**.

**Optional setup**
- **Microsoft Foundry agents:** if Foundry threat protection is in scope, an Azure subscription **Owner** or **Contributor** enables the **AI services** plan in Defender for Cloud. Follow [8.5 Turn on threat protection for Microsoft Foundry agents](../chapter-08-threat-detection/README.md#85-turn-on-threat-protection-for-microsoft-foundry-agents-defender-for-cloud). Use the **Security Reader** Azure role to review alerts in Defender for Cloud; use the Defender for Cloud Unified RBAC role, Global Administrator, or Security Administrator to review alerts in the Defender portal.
- **Local agents:** if local runtime protection is in scope, prepare an Intune-enrolled Windows test device onboarded to Microsoft Defender for Endpoint, with Defender for Endpoint in active mode. Then follow [8.6 Turn on local AI agent runtime protection in Defender for Endpoint](../chapter-08-threat-detection/README.md#86-turn-on-local-ai-agent-runtime-protection-in-defender-for-endpoint-optional).

**Check result**
- For the core setup, **Enable** is on, **Agent 365** shows **Done**, and the **Microsoft 365 connector** shows **Connected**.
- If Copilot Studio is in scope, its Defender **Get started** step shows **Connected**.
- If Foundry threat protection is in scope, the **AI services** plan is **On** for the PoC subscription.
- If local runtime protection is in scope, the Windows test device is onboarded to Defender for Endpoint and the runtime protection policy is configured.

## 0.7 Plan for propagation times

**Documentation:** [Create and configure sensitivity labels and their policies](https://learn.microsoft.com/purview/create-sensitivity-labels) · [Learn about the Microsoft 365 Copilot and Copilot Chat DLP location](https://learn.microsoft.com/purview/dlp-microsoft365-copilot-location-learn-about) · [Understand Shadow AI in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-shadow-ai)

| Configuration | Documented time | Chapter |
|---|---|---|
| Sensitivity label and label policy changes | Up to 24 hours | 7 |
| DLP policy changes for the Microsoft 365 Copilot and Copilot Chat location | Up to 4 hours | 7 |
| Risk signals in the Agent Registry compared with the source security portals | Up to 1 hour | 1, 8 |
| Intune block policy from the Shadow AI or Local Agents page to a device | 15 minutes up to 8 hours | 9 |

Schedule each chapter's tests after these times, not in the same session as the setup.

## 0.8 Readiness checklist

Confirm before the first joint test session. Skip items for chapters that are out of scope.

- [ ] In-scope chapters and success criteria are signed off (0.2).
- [ ] Test admin and reviewer can open the **Agents** area of the Microsoft 365 admin center (0.3.1).
- [ ] Frontier is enabled if Chapter 9 or a Frontier feature from Chapter 2 is in scope (0.3.2).
- [ ] PoC accounts and groups exist, and roles are assigned as Active (0.4).
- [ ] Purview Audit is recording (0.5).
- [ ] Test agents and test devices exist (0.6).
- [ ] Defender Security for AI is enabled, Agent 365 shows Done, and the Microsoft 365 connector is connected (0.6.2).
- [ ] If Copilot Studio protection is in scope, its Defender and Power Platform setup is complete and the Get started step shows Connected (0.6.2).
- [ ] If Foundry threat protection is in scope, the Defender for Cloud AI services plan is On for the PoC subscription (0.6.2).
- [ ] If local runtime protection is in scope, the Windows test device is onboarded to Defender for Endpoint and its protection setup is complete (0.6.2).
- [ ] Propagation times are built into the schedule (0.7).

---

Next: [Chapter 1 – Agent Discovery and Inventory](../chapter-01-agent-discovery/README.md)
