# Prerequisites - Chapter 3: Agent identity and ownership

> **Goal:** Prepare the accounts, access, and test assets needed for this chapter and its selected optional paths.

Apply the [shared PoC preparation guidance](../README.md#prerequisites-and-reading-order) and agree the [chapter outcomes](README.md#-what-you-proved). Finish dependent build steps before their tests.

## Table of contents

- [Tenant readiness](#tenant-readiness)
- [Prepare accounts and role assignments](#prepare-accounts-and-role-assignments)
- [Test assets and dependencies](#test-assets-and-dependencies)
- [References](#references)

---

## Tenant readiness

**Documentation:** [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started) · [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview) · [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)

Use the task-specific roles in [3.1 Required permissions](README.md#31-required-permissions). Confirm availability rather than assuming the tenant is ready.

Follow the [shared tenant readiness check](../README.md#tenant-readiness) using the chapter permissions and feature prerequisites linked above.

---

## Prepare accounts and role assignments

Alongside the [shared setup and reviewer accounts](../README.md#least-privilege-model), prepare the following scenario accounts:

| Account | Purpose |
|---|---|
| Standard test user | Runs the identity tests and acts as a sponsor where required. No admin role. |
| Developer account | Prepares the blueprint and agent identity if a custom or SDK-built agent is in scope. |
| PoC Sponsor and PoC Sponsor Manager | Sponsor continuity test with Lifecycle Workflows. The **Manager** attribute of PoC Sponsor is set to PoC Sponsor Manager. |

Assign the roles in [3.1 Required permissions](README.md#31-required-permissions) using the shared model. Verify each account can access the pages needed for its tasks.

---

## Test assets and dependencies

**Documentation:** [Fundamental concepts in Microsoft Entra Agent ID](https://learn.microsoft.com/entra/agent-id/key-concepts) · [Owners, sponsors, and managers](https://learn.microsoft.com/entra/agent-id/agent-owners-sponsors-managers) · [Agent's user account](https://learn.microsoft.com/entra/agent-id/agent-users) · [View and filter agent identities in your tenant](https://learn.microsoft.com/entra/agent-id/agent-lists) · [Disable agent identities in your tenant](https://learn.microsoft.com/entra/agent-id/disable-agent-identities) · [Add and manage owners and sponsors for agent identities and blueprints](https://learn.microsoft.com/entra/agent-id/manage-owners-sponsors-agents) · [Manage agents in end user experience](https://learn.microsoft.com/entra/agent-id/manage-agent-identities-end-user) · [Agent identity sponsor tasks in Lifecycle Workflows](https://learn.microsoft.com/entra/id-governance/agent-sponsor-tasks) · [Lifecycle Workflows templates](https://learn.microsoft.com/entra/id-governance/lifecycle-workflow-templates) · [Lifecycle Workflows tasks](https://learn.microsoft.com/entra/id-governance/lifecycle-workflow-tasks) · [Run a workflow on-demand](https://learn.microsoft.com/entra/id-governance/on-demand-workflow) · [Check status of a workflow](https://learn.microsoft.com/entra/id-governance/check-status-workflow)

- Verify the required inventory using [Chapter 1 – Agent discovery and inventory](../chapter-01-agent-discovery/README.md) so you know which agents are in scope.
- If you use custom or SDK-built agents, complete [2.8 Create the agent blueprint with a365 setup](../chapter-02-third-party-custom-agents/README.md#28-create-the-agent-blueprint-with-a365-setup) so their blueprint and agent identities exist in your tenant.
- Confirm that the **PoC Sponsor** and **PoC Sponsor Manager** accounts from [Prepare accounts and role assignments](#prepare-accounts-and-role-assignments) exist, and that the **Manager** attribute of PoC Sponsor is set to PoC Sponsor Manager. The sponsorship transfer task in 3.10 requires a populated manager attribute, and the email tasks notify the manager and co-sponsors.
- Pick one non-production test agent that you can disable, mark as risky, and re-enable during the tests.
- Access packages for agents are covered in [6.6 Grant time-bound access with access packages](../chapter-06-conditional-access/README.md#66-grant-time-bound-access-with-access-packages). This chapter only links to it.

Build guidance: [1.2 Discover Microsoft-native agents](../chapter-01-agent-discovery/README.md#12-discover-microsoft-native-agents)


**Check result**
- Each asset needed for the selected paths is prepared or has a named build task that will finish before its dependent tests.

---

## References

- [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started)
- [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview)
- [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)
- [Fundamental concepts in Microsoft Entra Agent ID](https://learn.microsoft.com/entra/agent-id/key-concepts)
- [Owners, sponsors, and managers](https://learn.microsoft.com/entra/agent-id/agent-owners-sponsors-managers)
- [Agent's user account](https://learn.microsoft.com/entra/agent-id/agent-users)
- [View and filter agent identities in your tenant](https://learn.microsoft.com/entra/agent-id/agent-lists)
- [Disable agent identities in your tenant](https://learn.microsoft.com/entra/agent-id/disable-agent-identities)
- [Add and manage owners and sponsors for agent identities and blueprints](https://learn.microsoft.com/entra/agent-id/manage-owners-sponsors-agents)
- [Manage agents in end user experience](https://learn.microsoft.com/entra/agent-id/manage-agent-identities-end-user)
- [Agent identity sponsor tasks in Lifecycle Workflows](https://learn.microsoft.com/entra/id-governance/agent-sponsor-tasks)
- [Lifecycle Workflows templates](https://learn.microsoft.com/entra/id-governance/lifecycle-workflow-templates)
- [Lifecycle Workflows tasks](https://learn.microsoft.com/entra/id-governance/lifecycle-workflow-tasks)
- [Run a workflow on-demand](https://learn.microsoft.com/entra/id-governance/on-demand-workflow)
- [Check status of a workflow](https://learn.microsoft.com/entra/id-governance/check-status-workflow)

---

> **Ready?** Continue to the [chapter](README.md). →
