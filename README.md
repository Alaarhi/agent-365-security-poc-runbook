# Microsoft Agent 365 Security PoC Runbook

## Structure

| Chapter | Folder |
|---|---|
| Chapter 0 - Prerequisites and PoC preparation | [`chapter-0-prerequisites`](chapter-0-prerequisites/README.md) |
| Chapter 1 - Defender setup, tests, and result checks | [`chapter-1-defender`](chapter-1-defender/README.md) |
| Chapter 2 - Purview setup, tests, and result checks | [`chapter-2-purview`](chapter-2-purview/README.md) |

## Roles summary

| Area | Required owner | Minimum role/access |
|---|---|---|
| Agent 365 / agent publishing | AI admin / agent owner | Ability to publish and approve test agents in Agent 365 / Microsoft 365 admin center |
| Microsoft Defender | SOC / security admin | Security Administrator for setup; Security Reader for read-only hunting; Security Operator or Security Administrator for detections |
| Power Platform / Copilot Studio | Power Platform admin | Power Platform Administrator or environment admin for Copilot Studio real-time protection setup |
| Microsoft Purview | Compliance admin | Compliance Administrator and Purview Workload Content Admin |
| Communication Compliance | Compliance reviewer | Member of Communication Compliance role group |
| Insider Risk Management | Insider risk admin | Insider Risk Management role group / Insider Risk administrator |
| SharePoint content | Site owner | Site owner or library owner for PoC content upload, labeling, and permissions |
| Entra ID / app registration | Identity admin | Application Administrator or Cloud Application Administrator where app connectors or app registrations are required |

## Final readiness checklist

Before the joint test session, the customer should confirm:

- [ ] PoC agents are published and accessible to the test user.
- [ ] Agent 365 is connected in Defender.
- [ ] Defender Security for AI agents is enabled.
- [ ] Power Platform admin is available if Copilot Studio real-time protection is in scope.
- [ ] Microsoft 365 app connector is connected if near-real-time detections are required.
- [ ] Purview Audit is enabled.
- [ ] Sensitivity labels are published and visible to test users.
- [ ] Confidential and General files are uploaded and labeled.
- [ ] DLP policy for Copilot / Copilot Chat is enabled.
- [ ] DLP policy for Exchange email is enabled.
- [ ] Test user has SharePoint access and can invoke the PoC agent.
- [ ] Propagation windows have passed.
- [ ] Defender and Purview admins are available during the test window.
