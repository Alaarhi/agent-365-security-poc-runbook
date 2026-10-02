# Chapter 0 - Prerequisites and PoC preparation

Baseline steps and readiness checks before running any of the six use cases.

## What this chapter covers

- Which use cases are in scope for this PoC.
- Access and licensing.
- Test identities (least-privilege split).
- Which portals every team needs.
- Test agents to prepare.
- SharePoint content for Purview tests (UC4).
- Propagation windows.

## Least-privilege model

Every chapter in this runbook uses the same pattern:

- **Setup / configuration role** - elevated role required only to make a change. Assign Active for the PoC window.
- **Read-only / validation role** - least-privilege role sufficient to view configuration and evidence. Use this for reviewers, auditors, and anyone who does not need to change anything.

Grant read-only roles first. Only grant setup roles to whoever will actually make the change.

## 0.1 Confirm PoC scope

Agree upfront which use cases the customer wants to validate:

| Use case | Pillar | Included in this guide |
|---|---|---|
| UC1 - Agent Discovery | Observe | Yes |
| UC2 - Identity & Ownership | Govern | Yes |
| UC3 - Least-Privilege Access | Govern | Yes |
| UC4 - Sensitive Data Protection (Purview) | Secure | Yes |
| UC5 - Threat Detection & Protection (Defender) | Secure | Yes |
| UC6 - Lifecycle & Audit | Observe / Govern | Yes |

## 0.2 Confirm access and licensing

The customer should confirm the PoC team has:

- Agent 365 trial license or equivalent Agent 365 access for the PoC.
- Access to the Microsoft 365 admin center (<https://admin.cloud.microsoft>).
- Access to the Microsoft Entra admin center (<https://entra.microsoft.com>).
- Access to the Microsoft Purview portal (<https://purview.microsoft.com>).
- Access to the Microsoft Defender portal (<https://security.microsoft.com>).
- Access to the Power Platform admin center (if Copilot Studio is in scope).

## 0.3 Roles at a glance

Assign these Active for the PoC window. Full role detail is in each chapter.

| Use case | Setup role | Read-only / validation role |
|---|---|---|
| UC1 - Agent Discovery | AI Administrator | AI Reader or Global Reader |
| UC2 - Identity & Ownership | Agent ID Developer, Agent Registry Administrator, Attribute Definition Administrator, Attribute Assignment Administrator | Directory Readers, AI Reader |
| UC3 - Least-Privilege Access | Conditional Access Administrator, Identity Governance Administrator, Lifecycle Workflows Administrator | Global Reader, Reports Reader, Security Reader |
| UC4 - Sensitive Data Protection | Compliance Administrator, Information Protection Administrator, Purview Workload Content Admin, Communication Compliance Administrator, Insider Risk Management Administrator | Audit Reader, Global Reader, Compliance Reader |
| UC5 - Threat Detection & Protection | Security Administrator, Security Operator, Power Platform Administrator (for Copilot Studio integration), Application Administrator or Cloud Application Administrator | Security Reader |
| UC6 - Lifecycle & Audit | AI Administrator, Compliance Administrator | Audit Reader, AI Reader, Security Reader, Global Reader |
| Setup only | Global Administrator (initial setup / admin consent only, via PIM / just-in-time) | - |

Two rules that save PoC time:

1. Roles assigned as **eligible-only** show up as "you lack permission" to the admin at the moment they try to act. Always assign the role **Active** for the PoC window. Use PIM only for Global Administrator.
2. Split the role assignments explicitly - do not give the admin who executes a change the read-only reviewer's role, and do not give the reviewer the admin role.

## 0.4 Confirm test identities

Prepare at least two accounts:

| Account | Purpose | Roles assigned |
|---|---|---|
| Test admin | Configures Agent 365, Entra, Purview, Defender, SharePoint, labels, policies, and agent publishing. | Setup roles per the table in 0.3, scoped to the use cases in scope. |
| Standard test user | Runs the agent tests. Permission trimming, labels, and DLP evaluate against this user. | Standard user with access to the PoC agent, SharePoint site, and Teams / M365 Copilot as required. |
| Reviewer / auditor (optional) | Views evidence without making changes. | Read-only / validation roles per the table in 0.3. |

## 0.5 Prepare agents

Before starting UC1:

1. Ensure the PoC agent or agents are published and visible to the intended test users.
2. If using Copilot Studio, publish the agent to Microsoft 365 Copilot and Teams.
3. If using Agent 365 registration, confirm the agent appears in the Agent 365 registry.
4. Exercise the agent with a few baseline prompts so activity exists for logs, hunting, and audit.

## 0.6 Prepare SharePoint content for Purview tests (UC4)

Create a dedicated SharePoint site or folder for PoC content. A dedicated site is preferred for clean permissions and easy teardown.

Recommended content categories:

| Content category | Label | Purpose |
|---|---|---|
| Sensitive customer / financial documents | Confidential | Used to prove Copilot grounding is restricted. |
| Public or broadly shareable operational documents | General | Used as the positive control for allowed grounding. |
| Financial identifiers in invoice or ledger content | Confidential | Used to prove Exchange DLP blocks outbound email exfiltration. |

Sample files are provided for UC4 testing. See [UC4 - Sensitive Data Protection](../chapter-uc4-sensitive-data-protection/README.md#2-6-prepared-sample-content) for the file list, labeling guidance, and the samples folder (`chapter-uc4-sensitive-data-protection/samples/`).

All sample files use publicly documented test values (Visa/MC/Amex/Discover sandbox card numbers and Federal Reserve public test routing numbers). No real PII.

## 0.7 Important propagation windows

Plan for propagation time:

| Configuration | Expected delay |
|---|---|
| Sensitivity label publishing | Up to 24 hours |
| DLP policy activation | Up to 24 hours |
| Communication Compliance policy | Up to 24 hours |
| Insider Risk Management agent policy | Up to 24 hours |
| Advanced Hunting / audit ingestion | Often 15-30 minutes, sometimes longer |
| Agent Registry discovery | Up to 24 hours after agent enablement |

---

Next: [UC1 - Agent Discovery](../chapter-uc1-agent-discovery/README.md)
