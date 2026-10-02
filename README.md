# Microsoft Agent 365 Security PoC Runbook

Setup, tests, and result checks for the six Agent 365 PoC use cases across the Observe, Govern, and Secure pillars.

## Least-privilege model used in this runbook

Every chapter has a **Roles** section that splits access into:

- **Setup / configuration role** — the elevated role required only to make a change (create a policy, enable a feature, publish a label). Assign Active for the PoC window; PIM-elevate if needed.
- **Read-only / validation role** — the least-privilege role sufficient to view configuration, evidence, and logs. Use this for reviewers, auditors, and everyone who does not need to change anything.

Anyone verifying results or reviewing evidence should use the read-only role. Setup roles stay with the admin who is actually making the change.

## Structure

| Pillar | Use case | Folder |
|---|---|---|
| — | Chapter 0 – Prerequisites and PoC preparation | [`chapter-0-prerequisites`](chapter-0-prerequisites/README.md) |
| Observe | UC1 – Agent Discovery | [`chapter-uc1-agent-discovery`](chapter-uc1-agent-discovery/README.md) |
| Govern | UC2 – Identity & Ownership | [`chapter-uc2-identity-ownership`](chapter-uc2-identity-ownership/README.md) |
| Govern | UC3 – Least-Privilege Access | [`chapter-uc3-least-privilege`](chapter-uc3-least-privilege/README.md) |
| Secure (Purview) | UC4 – Sensitive Data Protection | [`chapter-uc4-sensitive-data-protection`](chapter-uc4-sensitive-data-protection/README.md) |
| Secure (Defender) | UC5 – Threat Detection & Protection | [`chapter-uc5-threat-detection`](chapter-uc5-threat-detection/README.md) |
| Observe / Govern | UC6 – Lifecycle & Audit | [`chapter-uc6-lifecycle-audit`](chapter-uc6-lifecycle-audit/README.md) |

Combined PDF at the root: `Agent-365-Security-PoC-Runbook.pdf`.

## Portals used

| Portal | URL | Purpose |
|---|---|---|
| Microsoft 365 admin center | admin.cloud.microsoft | Agents, registry, approvals, connected platforms |
| Microsoft Entra admin center | entra.microsoft.com | Agent ID, Conditional Access, access packages, lifecycle workflows, sign-in logs |
| Microsoft Purview portal | purview.microsoft.com | Labels, DLP, audit, Communication Compliance, IRM |
| Microsoft Defender portal | security.microsoft.com | AI agent inventory, alerts, Advanced Hunting |
| Power Platform admin center | admin.powerplatform.microsoft.com | Copilot Studio environment, security integrations |
| Copilot Studio | copilotstudio.microsoft.com | Build and publish Copilot Studio agents |

## Final readiness checklist

Before the joint test session, confirm:

- [ ] PoC agents are published and accessible to the test user.
- [ ] Agent 365 is connected in Defender.
- [ ] Defender Security for AI agents is enabled.
- [ ] Power Platform admin is available if Copilot Studio real-time protection is in scope.
- [ ] Microsoft 365 app connector is connected if near-real-time detections are required.
- [ ] Purview Audit is enabled.
- [ ] Sensitivity labels are published and visible to test users.
- [ ] `A365-Restricted` and `A365-Open` files are uploaded and labeled.
- [ ] DLP policy for Copilot / Copilot Chat is enabled.
- [ ] DLP policy for Exchange email is enabled.
- [ ] Test user has SharePoint access and can invoke the PoC agent.
- [ ] Propagation windows have passed.
- [ ] Defender and Purview admins are available during the test window.
