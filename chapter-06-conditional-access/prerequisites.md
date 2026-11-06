# Prerequisites - Chapter 6: Conditional Access and least privilege

> **Goal:** Prepare the accounts, access, and test assets needed for this chapter and its selected optional paths.

Apply the [shared PoC preparation guidance](../README.md#prerequisites-and-reading-order) and agree the [chapter outcomes](README.md#-what-you-proved). Finish dependent build steps before their tests.

## Table of contents

- [Tenant readiness](#tenant-readiness)
- [Prepare accounts and role assignments](#prepare-accounts-and-role-assignments)
- [Prepare groups](#prepare-groups)
- [Test assets and dependencies](#test-assets-and-dependencies)
- [References](#references)

---

## Tenant readiness

**Documentation:** [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started) · [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview) · [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)

Use the task-specific roles in [6.1 Required permissions](README.md#61-required-permissions). Confirm availability rather than assuming the tenant is ready.

Follow the [shared tenant readiness check](../README.md#tenant-readiness) using the chapter permissions and feature prerequisites linked above.

---

## Prepare accounts and role assignments

Alongside the [shared setup and reviewer accounts](../README.md#least-privilege-model), prepare the following scenario accounts:

| Account | Purpose |
|---|---|
| Standard test user | Sponsors the approved agent and runs the access-package tests. No admin role. |
| PoC approver | Approves access package requests. No admin role. |

Assign the roles in [6.1 Required permissions](README.md#61-required-permissions) using the shared model. Verify each account can access the pages needed for its tasks.

---

## Prepare groups

**Documentation:** [Assign Microsoft Entra roles](https://learn.microsoft.com/entra/identity/role-based-access-control/manage-roles-portal) · [Microsoft Entra built-in roles](https://learn.microsoft.com/entra/identity/role-based-access-control/permissions-reference) · [Roles and role groups in Microsoft Purview](https://learn.microsoft.com/purview/purview-permissions)

Performed by **Groups Administrator**.

Create or verify these PoC groups before the tasks that use them:

| Group | Members |
|---|---|
| `PoC-Agent-Resource-Access` | None at the start |

Use assigned (not dynamic) membership for `PoC-Agent-Resource-Access`, with no members before the access-package test.

**Check result**
- Group membership matches the table, and the groups are recorded as PoC assets.

---

## Test assets and dependencies

**Documentation:** [Conditional Access for agents](https://learn.microsoft.com/entra/identity/conditional-access/agent-id) · [Target agents in Conditional Access policies](https://learn.microsoft.com/entra/identity/conditional-access/howto-target-agent-identities) · [Secure autonomous agents with Conditional Access](https://learn.microsoft.com/entra/identity/conditional-access/policy-autonomous-agents) · [Conditional Access report-only mode](https://learn.microsoft.com/entra/identity/conditional-access/concept-conditional-access-report-only) · [Access packages for agent identities](https://learn.microsoft.com/entra/agent-id/agent-access-packages) · [Create and manage a catalog](https://learn.microsoft.com/entra/id-governance/entitlement-management-catalog-create) · [Change resource roles for an access package](https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-resources) · [Change lifecycle settings for an access package](https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-lifecycle-policy) · [Request access packages on behalf of other identities](https://learn.microsoft.com/entra/id-governance/entitlement-management-request-behalf) · [View, add, and remove assignments](https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-assignments) · [accessPackageAssignmentRequest](https://learn.microsoft.com/graph/api/entitlementmanagement-post-assignmentrequests)

- Verify the required inventory using [Chapter 1 – Agent discovery and inventory](../chapter-01-agent-discovery/README.md) so you know which agents exist and which ones must keep working.
- Verify the required identity setup using [Chapter 3 – Agent identity and ownership](../chapter-03-identity-ownership/README.md). Sponsors must be assigned (3.5), and you need the sign-in log filters (3.8) and the Risky agents report (3.9). Sponsor transitions with Lifecycle Workflows are covered in [3.10 Keep sponsorship continuous with Lifecycle Workflows](../chapter-03-identity-ownership/README.md#310-keep-sponsorship-continuous-with-lifecycle-workflows).
- Prepare a lab agent identity blueprint with a client secret you control, for example with [2.8 Create the agent blueprint with a365 setup](../chapter-02-third-party-custom-agents/agent-365-sdk.md#28-create-the-agent-blueprint-with-a365-setup). Then, as an **Agent ID Administrator**, create the three agent identities below from that blueprint: open <https://entra.microsoft.com> > **Entra ID** > **Agents** > **Agent identities** > **New agent identity (Preview)**, select the lab blueprint under **Agent blueprint**, enter the name in **Agent identity name**, and complete the wizard with **Create**. Record each agent identity's ID. For agent identities, the object ID and app ID are always the same value.

| Test object | Purpose | Approved (excluded from default deny) |
|---|---|---|
| `PoC-Agent-Approved` | Control agent for all tests; receives the access package | Yes |
| `PoC-Agent-Risk` | Marked as compromised in the optional risk test (6.9) | Yes |
| `PoC-Agent-Unapproved` | Not on the allow list | No |
| `PoC-Agent-Resource-Access` (security group prepared on this page) | Resource granted through the access package | – |
| PoC approver (test user prepared on this page) | Approves access package requests | – |

- Set the standard test user as a sponsor of `PoC-Agent-Approved`, as in [3.5.1 Assign owners and sponsors to an agent identity](../chapter-03-identity-ownership/README.md#351-assign-owners-and-sponsors-to-an-agent-identity). The standard test user is the sponsor in 6.6.3 and uses the published agent in 6.8.3.
- For 6.7, have a member of your organization submit a test agent for admin approval, so that it appears in **Agents** > **All agents** > **Requests** in the Microsoft 365 admin center with state **Pending review**.
- Security defaults must be off in the tenant. Conditional Access policies don't apply while security defaults are enabled.

Build guidance: [6.7 Apply Conditional Access and custom security attributes at publish time](README.md#67-apply-conditional-access-and-custom-security-attributes-at-publish-time-policy-templates)


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
- [Conditional Access for agents](https://learn.microsoft.com/entra/identity/conditional-access/agent-id)
- [Target agents in Conditional Access policies](https://learn.microsoft.com/entra/identity/conditional-access/howto-target-agent-identities)
- [Secure autonomous agents with Conditional Access](https://learn.microsoft.com/entra/identity/conditional-access/policy-autonomous-agents)
- [Conditional Access report-only mode](https://learn.microsoft.com/entra/identity/conditional-access/concept-conditional-access-report-only)
- [Access packages for agent identities](https://learn.microsoft.com/entra/agent-id/agent-access-packages)
- [Create and manage a catalog](https://learn.microsoft.com/entra/id-governance/entitlement-management-catalog-create)
- [Change resource roles for an access package](https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-resources)
- [Change lifecycle settings for an access package](https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-lifecycle-policy)
- [Request access packages on behalf of other identities](https://learn.microsoft.com/entra/id-governance/entitlement-management-request-behalf)
- [View, add, and remove assignments](https://learn.microsoft.com/entra/id-governance/entitlement-management-access-package-assignments)
- [accessPackageAssignmentRequest](https://learn.microsoft.com/graph/api/entitlementmanagement-post-assignmentrequests)

---

> **Ready?** Continue to the [chapter](README.md). →
