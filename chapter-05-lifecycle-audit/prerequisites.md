# Prerequisites - Chapter 5: Agent lifecycle and audit

> **Goal:** Prepare the accounts, access, and test assets needed for this chapter and its selected optional paths.

Apply the [shared PoC preparation guidance](../README.md#prerequisites-and-reading-order) and agree the [chapter outcomes](README.md#-what-you-proved). Finish dependent build steps before their tests.

## Table of contents

- [Tenant readiness](#tenant-readiness)
- [Prepare accounts and role assignments](#prepare-accounts-and-role-assignments)
- [Prepare groups](#prepare-groups)
- [Audit recording](#audit-recording)
- [Test assets and dependencies](#test-assets-and-dependencies)
- [References](#references)

---

## Tenant readiness

**Documentation:** [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started) · [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview) · [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)

Use the task-specific roles in [5.1 Required permissions](README.md#51-required-permissions). Confirm availability rather than assuming the tenant is ready.

Follow the [shared tenant readiness check](../README.md#tenant-readiness) using the chapter permissions and feature prerequisites linked above.

---

## Prepare accounts and role assignments

Alongside the [shared setup and reviewer accounts](../README.md#least-privilege-model), prepare the following scenario accounts:

| Account | Purpose |
|---|---|
| Standard test user | Tests installation, availability, and the ownership transfer. No admin role. |
| Maker account | Creates the disposable lifecycle agent and any additional Agent Builder or Foundry assets. |

Assign the roles in [5.1 Required permissions](README.md#51-required-permissions) using the shared model. Verify each account can access the pages needed for its tasks.

---

## Prepare groups

**Documentation:** [Assign Microsoft Entra roles](https://learn.microsoft.com/entra/identity/role-based-access-control/manage-roles-portal) · [Microsoft Entra built-in roles](https://learn.microsoft.com/entra/identity/role-based-access-control/permissions-reference) · [Roles and role groups in Microsoft Purview](https://learn.microsoft.com/purview/purview-permissions)

Performed by **Groups Administrator**.

Create or verify these PoC groups before the tasks that use them:

| Group | Members |
|---|---|
| `A365-PoC-Users` | Standard test user |

**Check result**
- Group membership matches the table, and the groups are recorded as PoC assets.

---

## Audit recording

**Documentation:** [Turn auditing on or off](https://learn.microsoft.com/purview/audit-log-enable-disable) · [Audit logs for Copilot and AI applications](https://learn.microsoft.com/purview/audit-copilot)

Confirm auditing before test activity that must appear in Microsoft Purview or the Microsoft 365 connector.

### Confirm that auditing is on
Performed by a member of the **Audit Manager** role group.
1. Open the Microsoft Purview portal (<https://purview.microsoft.com>) and go to **Audit**.
2. If a banner prompts you to start recording user and admin activity, select it.
3. Record the date and time.

**Check result**
- **Audit** search is available and no banner asks you to start recording.

---

## Test assets and dependencies

**Documentation:** [Governance and lifecycle actions for agents – Install agents and Activate agents](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions) · [Agent requests in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-requests) · [Policy templates](https://learn.microsoft.com/microsoft-agent-365/admin/policy-template) · [Search the audit log](https://learn.microsoft.com/purview/audit-search) · [Audit logs for Copilot and AI applications](https://learn.microsoft.com/purview/audit-copilot) · [Audit log activities – Agent 365 activities](https://learn.microsoft.com/purview/audit-log-activities) · [Agent sign-in and audit logs in Microsoft Entra](https://learn.microsoft.com/entra/agent-id/sign-in-audit-logs-agents) · [Access activity logs in Microsoft Entra](https://learn.microsoft.com/entra/identity/monitoring-health/howto-access-activity-logs) · [Discover AI agents in Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-inventory) · [AgentsInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-agentsinfo-table)

- Verify the required inventory using [Chapter 1 – Agent discovery and inventory](../chapter-01-agent-discovery/README.md) so the test agents are visible in **Agents** > **All agents** > **Registry**.
- Review [Chapter 3 – Agent identity and ownership](../chapter-03-identity-ownership/README.md) for owners and sponsors in Microsoft Entra. This chapter covers ownership as managed in the Microsoft 365 admin center.
- Complete [Enable security for AI](../chapter-08-threat-detection/prerequisites.md#enable-security-for-ai) and [Connect the Microsoft 365 connector](../chapter-08-threat-detection/prerequisites.md#connect-the-microsoft-365-connector) before you run the Advanced Hunting tasks in 5.9.4.
- As the maker, create the lifecycle test agent `PoC-Lifecycle-Agent`: a shared Agent Builder or Copilot Studio agent that you're allowed to delete permanently. **Assign new owner** is only available for shared Agent Builder and Copilot Studio agents. The maker is the agent's first owner; the standard test user becomes the new owner in 5.10.6.
- For 5.4.2 and 5.4.3, use an Agent Builder agent, because Agent Builder agents support multiple owners. If `PoC-Lifecycle-Agent` isn't an Agent Builder agent, create a separate one with [Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/agent-builder).
- For the optional 5.3.2, use the Microsoft Foundry test agent from [1.2.2 Create and publish a Foundry test agent](../chapter-01-agent-discovery/README.md#122-create-and-publish-a-foundry-test-agent).
- Note the PoC start time in UTC. The audit searches in 5.9 and 5.10 start from this time.

Build guidance: [1.2 Discover Microsoft-native agents](../chapter-01-agent-discovery/README.md#12-discover-microsoft-native-agents)


**Check result**
- Each asset needed for the selected paths is prepared or has a named build task that will finish before its dependent tests.

---

## References

- [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started)
- [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview)
- [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)
- [Assign Microsoft Entra roles](https://learn.microsoft.com/entra/identity/role-based-access-control/manage-roles-portal)
- [Microsoft Entra built-in roles](https://learn.microsoft.com/entra/identity/role-based-access-control/permissions-reference)
- [Roles and role groups in Microsoft Purview](https://learn.microsoft.com/purview/purview-permissions)
- [Turn auditing on or off](https://learn.microsoft.com/purview/audit-log-enable-disable)
- [Audit logs for Copilot and AI applications](https://learn.microsoft.com/purview/audit-copilot)
- [Governance and lifecycle actions for agents – Install agents and Activate agents](https://learn.microsoft.com/microsoft-365/admin/manage/agent-actions)
- [Agent requests in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-requests)
- [Policy templates](https://learn.microsoft.com/microsoft-agent-365/admin/policy-template)
- [Search the audit log](https://learn.microsoft.com/purview/audit-search)
- [Audit log activities – Agent 365 activities](https://learn.microsoft.com/purview/audit-log-activities)
- [Agent sign-in and audit logs in Microsoft Entra](https://learn.microsoft.com/entra/agent-id/sign-in-audit-logs-agents)
- [Access activity logs in Microsoft Entra](https://learn.microsoft.com/entra/identity/monitoring-health/howto-access-activity-logs)
- [Discover AI agents in Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-inventory)
- [AgentsInfo table](https://learn.microsoft.com/defender-xdr/advanced-hunting-agentsinfo-table)
- [Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/agent-builder)

---

> **Ready?** Continue to the [chapter](README.md). →
