# Chapter UC3 - Least-Privilege Access

**Pillar:** Govern
**What it proves:** a compromised agent reaches only what you scoped it to. Broad standing access is replaced by a bounded, just-in-time, revocable grant, and the deny is provable in the sign-in log.

## Roles - least privilege

| Task | Role | Notes |
|---|---|---|
| Create and enforce Conditional Access policies for agents | **Conditional Access Administrator** | Required to create, edit, and enable CA policies. |
| Create access packages and JIT policies | **Identity Governance Administrator** | Required for Entitlement Management. |
| Configure Lifecycle Workflows (sponsor change) | **Lifecycle Workflows Administrator** | Required only if sponsor-change workflows are in scope. |
| Read-only / validation | **Global Reader** or **Reports Reader** | Sufficient to view CA policies, sign-in logs, and access package assignments. Use for reviewers. |
| Read-only for sign-in logs only | **Security Reader** | Alternative least-privilege role for reading sign-in logs and blocked-token events. |

Grant the read-only role first. Only the person creating the policy needs the Conditional Access Administrator role.

## Portals

- Microsoft Entra admin center - <https://entra.microsoft.com>
  - **Protection** > **Conditional Access** - policies for agent identities.
  - **Identity Governance** > **Entitlement management** > **Access packages** - JIT grants.
  - **Identity Governance** > **Lifecycle Workflows** - sponsor changes.
  - **Monitoring** > **Sign-in logs** - allow/deny evidence.

## Documentation

| Topic | Documentation |
|---|---|
| Conditional Access for agents | [Conditional Access for agents](https://learn.microsoft.com/entra/identity/conditional-access/agent-id) |
| Target agent identities in CA | [Target agent identities in Conditional Access](https://learn.microsoft.com/entra/identity/conditional-access/howto-target-agent-identities) |
| Recommended policies for autonomous agents | [Recommended policies for autonomous agents](https://learn.microsoft.com/entra/identity/conditional-access/policy-autonomous-agents) |
| Entitlement management | [What is entitlement management?](https://learn.microsoft.com/entra/id-governance/entitlement-management-overview) |
| Lifecycle workflows | [Lifecycle Workflows overview](https://learn.microsoft.com/entra/id-governance/what-are-lifecycle-workflows) |

## Prerequisites

Complete [Chapter 0 - Prerequisites](../chapter-0-prerequisites/README.md), [UC1](../chapter-uc1-agent-discovery/README.md), and [UC2](../chapter-uc2-identity-ownership/README.md).

## Setup - Conditional Access policy for agent identities (Report-only)

Performed by **Conditional Access Administrator**.

1. Open <https://entra.microsoft.com> > **Protection** > **Conditional Access** > **Policies** > **New policy**.
2. Name: `PoC - Agent access boundary (Report-only)`.
3. **Assignments** > **Users, agents or workload identities** > **What does this policy apply to?** > **Agents**.
   - **Select agent identities**: pick the PoC agents (their `-AgentIdentity` service principals).
   - Alternatively: select the agent blueprint principal(s) to cover every agent derived from those blueprints, including future ones.
4. **Target resources** > **Include** > **Select resources**: pick only the resources the PoC agents actually call (for example Microsoft Graph and any Foundry / Power Platform APIs). This scopes the boundary.
5. Optionally, **Conditions** > **Agent risk (Preview)** > `High` (and `Medium`) so the policy fires only on risky-agent signals.
6. **Access controls** > **Grant** > **Block**. Block is the only enforcement control available for agent identities (there is no interactive remediation for an agent).
7. **Enable policy** = **Report-only**.
8. **Create**.

Report-only lets the agent keep working while every token request is evaluated and written to the sign-in log as "would have been blocked / granted". Flip to **On** after the log looks correct.

## Setup - just-in-time access via access package (optional)

Performed by **Identity Governance Administrator**.

1. Open <https://entra.microsoft.com> > **Identity Governance** > **Entitlement management** > **Access packages** > **New access package**.
2. Scope the package to the specific resource(s) the agent needs.
3. Set expiry (for example 8 hours) so grants are time-bounded.
4. Assign to the agent identity (or a group containing agent identities).

**Check result (Setup role)**

- Access package assignment appears on the agent.
- The agent can invoke the target resource only within the grant window.

## Setup - sponsor change via Lifecycle Workflows (optional)

Performed by **Lifecycle Workflows Administrator**.

1. Open <https://entra.microsoft.com> > **Identity Governance** > **Lifecycle Workflows**.
2. Create a new workflow from the template **"Agent sponsor job profile change"** (Mover / Agents category).
3. Configure the scope condition to match the attribute change you want to trigger on (for example `department -eq "Compliance"`).
4. Review the two default tasks:
   - Send email to manager about sponsorship changes.
   - Transfer agent identity sponsorships to manager.
5. Save.

## Test - CA block is provable in sign-in logs

Performed by anyone with **Global Reader**, **Reports Reader**, or **Security Reader**.

1. Have the PoC agent attempt an action outside the scoped resources (for example a Graph endpoint not on the allow list).
2. Open <https://entra.microsoft.com> > **Monitoring** > **Sign-in logs** > **Service principal sign-ins**.
3. Filter by the agent's `AppId` or Display name.
4. Confirm a **Failure** entry with **Conditional Access = Failure** and the policy name matching your PoC policy.

**Expected result**

- The out-of-scope call is logged as blocked with the policy name attached.
- A parallel in-scope call is logged as allowed.

## Test - JIT grant expires

Performed by anyone with **Global Reader**.

1. Confirm the agent can invoke the target resource inside the grant window.
2. After the grant window expires, retry and confirm the call fails and appears as denied in the sign-in log.

## Test - sponsor change workflow (if configured)

Performed by anyone with **Global Reader** on the workflow history.

1. Change the sponsor's attribute so they leave scope (for example department change).
2. Run the workflow on demand.
3. Confirm the sponsor is transferred to the manager and the notification email is sent.

## Evidence to capture

- Screenshot of the CA policy in **Report-only** and then in **On** state.
- Sign-in log export showing at least one Deny and one Allow for the same agent identity within a short window.
- Access package assignment record with expiry.
- Lifecycle workflow run history if used.

## Common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| CA policy has no effect | Left in Report-only, or the agent identity not selected in Assignments | Flip to On; confirm the correct `-AgentIdentity` service principal is selected. |
| Sign-in log shows no service principal entries | Wrong log view (interactive vs service principal) | Switch to the **Service principal sign-ins** tab. |
| Agent still calls a resource after grant expiry | Cached token still valid | Wait for token expiry, or force token refresh; grants become effective for new tokens. |
| Lifecycle workflow does not fire | Scope condition does not match, or user was not "in scope" at the time | Adjust the scope filter to match the value you change to; re-run on demand. |

---

Previous: [UC2 - Identity & Ownership](../chapter-uc2-identity-ownership/README.md) · Next: [UC4 - Sensitive Data Protection](../chapter-uc4-sensitive-data-protection/README.md)
