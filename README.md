# Microsoft Agent 365 PoC Runbook

> **Goal of this PoC:** Validate Microsoft Agent 365 controls across **Observe**, **Govern**, and **Secure** using documented setup steps, measurable tests, and reviewable evidence.

## Chapters

| # | Pillar | Chapter | Prerequisites | What it proves |
|---|---|---|---|---|
| 1 | Observe | [Agent discovery and inventory](chapter-01-agent-discovery/README.md) | [Preparation](chapter-01-agent-discovery/prerequisites.md) | Every agent appears in one registry with owner, status and risk, in the portal and through Microsoft Graph. |
| 2 | Observe | [Third-party and custom agents](chapter-02-third-party-custom-agents/README.md) | [Preparation](chapter-02-third-party-custom-agents/prerequisites.md) | Agents on non-Microsoft platforms (Amazon Bedrock, Databricks Genie, Google Vertex AI and others) and custom SDK agents land in the same registry. |
| 3 | Govern | [Agent identity and ownership](chapter-03-identity-ownership/README.md) | [Preparation](chapter-03-identity-ownership/prerequisites.md) | Every agent has a Microsoft Entra Agent ID with accountable owners and sponsors. |
| 4 | Govern | [Tools and MCP server governance](chapter-04-tools-mcp-governance/README.md) | [Preparation](chapter-04-tools-mcp-governance/prerequisites.md) | Plugins, skills, MCP servers and connectors are inventoried, approved and centrally blockable. |
| 5 | Govern | [Agent lifecycle and audit](chapter-05-lifecycle-audit/README.md) | [Preparation](chapter-05-lifecycle-audit/prerequisites.md) | An agent can be installed, blocked, reassigned, deleted, restored and permanently deleted, with an audit trail. |
| 6 | Secure | [Conditional Access and least privilege](chapter-06-conditional-access/README.md) | [Preparation](chapter-06-conditional-access/prerequisites.md) | Only approved, low-risk agent identities get tokens, and access to resources is time-bound. |
| 7 | Secure | [Sensitive data protection (Purview)](chapter-07-sensitive-data-protection/README.md) | [Preparation](chapter-07-sensitive-data-protection/prerequisites.md) | Sensitivity labels and DLP stop Copilot and agents from processing or emailing regulated content, and Communication Compliance and Insider Risk Management supervise agents. |
| 8 | Secure | [Threat detection and runtime protection (Defender)](chapter-08-threat-detection/README.md) | [Preparation](chapter-08-threat-detection/prerequisites.md) | Risky agent actions are detected or blocked at runtime and reach the SOC as incidents. |
| 9 | Secure | [Shadow AI and local agents](chapter-09-shadow-ai-local-agents/README.md) | [Preparation](chapter-09-shadow-ai-local-agents/prerequisites.md) | Unapproved AI apps and developer agent tools on managed devices are visible and can be blocked. |

---

## Prerequisites and reading order

Open the chapter you want to validate and start with its **Before you start** checklist and linked prerequisite page. Each prerequisite page covers the applicable tenant checks, accounts, role assignments, test assets, and preparation steps.

Chapters 1 and 3 provide inventory and identity foundations where those are required. Follow the specific dependency links in your selected chapter; you do not need to run every chapter. Agree optional paths and success criteria before setup.

Before configuration, agree the approved PoC tenant, test window, selected outcomes, and preparation owners with the change owner and reviewer. Use synthetic data and controlled test accounts and recipients. Choose a restricted evidence location and verify existing assets before reusing them.

### Tenant readiness

1. The setup administrator signs in to the [Microsoft 365 admin center](https://admin.cloud.microsoft) and opens **Agents** > **Overview** and **Agents** > **All agents** > **Registry**.
2. The reviewer verifies the pages needed for their read-only tasks with their own account.
3. Check the Microsoft Learn prerequisites linked from the selected chapter, including licensing and supported tenant or cloud availability. Record any unmet requirement before continuing.

**Check result**
- The required pages open for the assigned accounts, and the applicable feature prerequisites have been verified.

---

## How to use this runbook

Use each chapter's **Topics and time guide** to jump to a task. Estimates cover hands-on work on one agent or a small test set after preparation; service propagation, log ingestion, approval queues, and unattended installation or deployment waits are separate. New integrations may need more time.

Follow the numbered tasks using the stated role and **Documentation** links. Verify **Check result** after setup and **Expected result** during tests, then collect the listed **Evidence**. The **What you proved** checklist is the chapter's success criteria: agree the selected outcomes before testing and tick only those supported by evidence. Record optional paths that were not run as out of scope.

Each page ends with consolidated **References**, in addition to the links beside the relevant instructions.

---

## Least-privilege model

- **Test admin / setup account:** holds only the roles needed for the selected configuration tasks.
- **Reviewer / auditor:** holds read-only roles for configuration, evidence, and logs; does not hold the setup roles.

Grant read-only access first and separate the change maker from the reviewer. Use time-bound **Active** assignments for the PoC window, with just-in-time activation for Global Administrator, and record assignment expiry. Each chapter's **Required permissions** table lists its task-specific roles.

A **User Administrator** creates missing PoC accounts. A **Privileged Role Administrator** assigns Microsoft Entra roles; a member of **Organization Management** assigns applicable Microsoft Purview role groups. Use the documented role-management permissions for other services.

**Documentation:** [Assign Microsoft Entra roles](https://learn.microsoft.com/entra/identity/role-based-access-control/manage-roles-portal) · [Microsoft Entra built-in roles](https://learn.microsoft.com/entra/identity/role-based-access-control/permissions-reference) · [Roles and role groups in Microsoft Purview](https://learn.microsoft.com/purview/purview-permissions)

---

## Portals used

| Portal | URL | Purpose |
|---|---|---|
| Microsoft 365 admin center | <https://admin.cloud.microsoft> | Agent Registry, Agent Map, requests, lifecycle, tools and MCP servers, connected platforms, Shadow AI and local agents |
| Microsoft Entra admin center | <https://entra.microsoft.com> | Agent ID, owners and sponsors, Conditional Access, ID Protection, access packages, Lifecycle Workflows, sign-in and audit logs |
| Microsoft Purview portal | <https://purview.microsoft.com> | Audit, sensitivity labels, DLP, Communication Compliance, Insider Risk Management, DSPM for AI |
| Microsoft Defender portal | <https://security.microsoft.com> | Security for AI, AI agent inventory, alerts and incidents, Advanced Hunting |
| Power Platform admin center | <https://admin.powerplatform.microsoft.com> | Copilot Studio environments, threat detection integration, connector governance |
| Copilot Studio | <https://copilotstudio.microsoft.com> | Build and publish Copilot Studio test agents |
| Microsoft Intune admin center | <https://intune.microsoft.com> | Block policies for Shadow AI and local agents, device compliance |
| Azure portal | <https://portal.azure.com> | Custom agent hosting, Tools Gateway (API Management) |

---

## Repository content

- `chapter-NN-*/README.md`: one chapter per folder.
- `chapter-NN-*/prerequisites.md`: detailed preparation for that chapter.
- [Microsoft-native samples](chapter-01-agent-discovery/samples/README.md): Copilot Studio declarative agent and Microsoft Foundry agent samples.
- [Custom agent samples](chapter-02-third-party-custom-agents/samples/sdk/README.md): Agent 365 SDK agent samples for Node.js, Python and .NET.
- [Agent-365-Security-PoC-Runbook.pdf](Agent-365-Security-PoC-Runbook.pdf): combined reading copy with all chapters, prerequisites, and sample guides. Use the Markdown pages to edit the runbook.

Several features covered in this runbook are in preview. Preview features might change before general availability.

---

## Key references

- [Overview of Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/overview)
- [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started)
- [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview)
- [Assign Microsoft Entra roles](https://learn.microsoft.com/entra/identity/role-based-access-control/manage-roles-portal)
- [Microsoft Entra built-in roles](https://learn.microsoft.com/entra/identity/role-based-access-control/permissions-reference)
- [Roles and role groups in Microsoft Purview](https://learn.microsoft.com/purview/purview-permissions)

---

> **Ready?** Start with [Chapter 1 - Agent discovery and inventory](chapter-01-agent-discovery/README.md) →
