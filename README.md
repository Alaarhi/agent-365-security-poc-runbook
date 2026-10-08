# Microsoft Agent 365 PoC Runbook

Setup steps, tests and evidence checks for a Microsoft Agent 365 proof of concept across the three Agent 365 pillars: **Observe**, **Govern** and **Secure**.

## Chapters

| # | Pillar | Chapter | What it proves |
|---|---|---|---|
| 0 | All | [Prerequisites and PoC preparation](chapter-00-prerequisites/README.md) | The tenant, accounts, roles, test agents and data are ready. |
| 1 | Observe | [Agent Discovery and Inventory](chapter-01-agent-discovery/README.md) | Every agent appears in one registry with owner, status and risk, in the portal and through Microsoft Graph. |
| 2 | Observe | [Third-Party and Custom Agents](chapter-02-third-party-custom-agents/README.md) | Agents on non-Microsoft platforms (Amazon Bedrock, Databricks Genie, Google Vertex AI and others) and custom SDK agents land in the same registry. |
| 3 | Govern | [Agent Identity and Ownership](chapter-03-identity-ownership/README.md) | Every agent has a Microsoft Entra Agent ID with accountable owners and sponsors. |
| 4 | Govern | [Tools and MCP Server Governance](chapter-04-tools-mcp-governance/README.md) | Plugins, skills, MCP servers and connectors are inventoried, approved and centrally blockable. |
| 5 | Govern | [Agent Lifecycle and Audit](chapter-05-lifecycle-audit/README.md) | An agent can be installed, blocked, reassigned, deleted, restored and permanently deleted, with an audit trail. |
| 6 | Secure | [Conditional Access and Least Privilege](chapter-06-conditional-access/README.md) | Only approved, low-risk agent identities get tokens, and access to resources is time-bound. |
| 7 | Secure | [Sensitive Data Protection (Purview)](chapter-07-sensitive-data-protection/README.md) | Sensitivity labels and DLP stop Copilot and agents from processing or emailing regulated content, and Communication Compliance and Insider Risk Management supervise agents. |
| 8 | Secure | [Threat Detection and Runtime Protection (Defender)](chapter-08-threat-detection/README.md) | Risky agent actions are detected or blocked at runtime and reach the SOC as incidents. |
| 9 | Secure | [Shadow AI and Local Agents](chapter-09-shadow-ai-local-agents/README.md) | Unapproved AI apps and developer agent tools on managed devices are visible and can be blocked. |

Start with Chapter 0. Chapters 1 and 3 are the foundation for the others. The **Before you start** list at the top of each chapter names its dependencies.

## How each chapter is organized

Every chapter follows the same order:

1. **What it proves** and **Success criteria**: binary, observable outcomes to agree with the customer before testing.
2. **N.1 Required permissions**: the least-privilege role for each task, split into setup roles and read-only validation roles, followed by **Before you start**.
3. **Setup sections (N.2, N.3, …)**: each section starts with a **Documentation** line linking to the Microsoft Learn articles it is based on, then numbered tasks (N.2.1, N.2.2, …) with the role that performs them and a **Check result**.
4. **Test and validation**: the tests to run, who runs them, and the expected result.
5. **Evidence**, **Troubleshooting** and, where test artifacts are created, **Cleanup**.

## Least-privilege model

- **Setup / configuration role**: the role needed only to make a change. Assign it as Active for the PoC window to the person who makes the change.
- **Read-only / validation role**: the smallest role that can view configuration, evidence and logs. Use it for reviewers, auditors and anyone verifying results.

Grant read-only roles first. Keep the split: the person who makes a change doesn't review it, and the reviewer doesn't hold the setup role. A summary of all roles is in [0.1 Required permissions](chapter-00-prerequisites/README.md#01-required-permissions).

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

## Repository content

- `chapter-NN-*/README.md`: one chapter per folder.
- `chapter-01-agent-discovery/samples/`: Copilot Studio declarative agent and Microsoft Foundry agent samples.
- `chapter-02-third-party-custom-agents/samples/sdk/`: Agent 365 SDK agent samples for Node.js, Python and .NET.
- `Agent-365-Security-PoC-Runbook.pdf`: all chapters combined in one PDF.

Several features covered in this runbook are in preview. Preview features might change before general availability.
