# Chapter 0 - Prerequisites and PoC preparation

Baseline steps and readiness checks before running the Defender (Chapter 1) or Purview (Chapter 2) tracks.

## 0.1 Confirm PoC scope

Agree upfront which agent surfaces the customer wants to validate:

| Track | Included in this guide |
|---|---|
| Defender inventory and agent security posture | Yes |
| Defender real-time protection for Copilot Studio | Yes |
| Purview sensitivity labels and DLP for Copilot grounding | Yes |
| Purview Exchange DLP for outbound email | Yes |
| Communication Compliance for AI agent interactions | Optional |
| Insider Risk Management agent policy | Optional |

## 0.2 Confirm access and licensing

The customer should confirm the PoC team has:

- Agent 365 trial license or equivalent Agent 365 access for the PoC.
- Access to the Microsoft Defender portal.
- Access to the Microsoft Purview portal.
- Access to the Microsoft Entra admin center.
- Access to the Microsoft 365 admin center.

## 0.3 Confirm test identities

Prepare at least two accounts:

| Account | Purpose |
|---|---|
| Test admin | Configures Defender, Purview, SharePoint, labels, policies, and agent publishing. |
| Standard test user | Runs the agent tests. Use this account for validation so permission trimming, labels, and DLP evaluate like a real user flow. |

## 0.4 Prepare agents

Before the Defender and Purview chapters:

1. Ensure the PoC agent or agents are published and visible to the intended test users.
2. If using Copilot Studio, publish the agent to Microsoft 365 Copilot and Teams.
3. If using Agent 365 registration, confirm the agent appears in the Agent 365 registry.
4. Exercise the agent with a few baseline prompts so activity exists for logs and hunting.

## 0.5 Prepare SharePoint content for Purview tests

Create a dedicated SharePoint site or folder for PoC content. A dedicated site is preferred for clean permissions and easy teardown.

Recommended content categories:

| Content category | Label | Purpose |
|---|---|---|
| Sensitive customer / financial documents | Confidential | Used to prove Copilot grounding is restricted. |
| Public or broadly shareable operational documents | General | Used as the positive control for allowed grounding. |
| Financial identifiers in invoice or ledger content | Confidential | Used to prove Exchange DLP blocks outbound email exfiltration. |

Sample files to label (if using the sample structure):

| File | Label | Test purpose |
|---|---|---|
| `Sample_Confidential_Customer_Roster.docx` | Confidential | Sensitive customer data / direct PII prompt |
| `Sample_Confidential_Vendor_Invoice.docx` | Confidential | Financial details for email exfiltration test |
| `Sample_Confidential_Payments_Ledger.xlsx` | Confidential | Structured financial data for grounding block |
| `Sample_Confidential_Employee_Expenses.xlsx` | Confidential | Sub-agent / employee expense sensitive content test |
| `Sample_General_Public_Guide.docx` | General | Allowed grounding positive control |
| `Sample_General_Checklist.docx` | General | Allowed grounding positive control |

## 0.6 Important propagation windows

Plan for propagation time:

| Configuration | Expected delay |
|---|---|
| Sensitivity label publishing | Up to 24 hours |
| DLP policy activation | Up to 24 hours |
| Communication Compliance policy | Up to 24 hours |
| Insider Risk Management agent policy | Up to 24 hours |
| Advanced Hunting / audit ingestion | Often 15-30 minutes, sometimes longer |

---

Next: [Chapter 1 - Defender](../chapter-1-defender/README.md)
