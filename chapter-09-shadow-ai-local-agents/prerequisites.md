# Prerequisites - Chapter 9: Shadow AI and local agents

> **Goal:** Prepare the accounts, access, and test assets needed for this chapter and its selected optional paths.

Apply the [shared PoC preparation guidance](../README.md#prerequisites-and-reading-order) and agree the [chapter outcomes](README.md#-what-you-proved). Finish dependent build steps before their tests.

## Table of contents

- [Tenant readiness](#tenant-readiness)
- [Prepare accounts and role assignments](#prepare-accounts-and-role-assignments)
- [Test assets and dependencies](#test-assets-and-dependencies)
- [Plan propagation and test timing](#plan-propagation-and-test-timing)
- [References](#references)

---

## Tenant readiness

**Documentation:** [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started) · [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview) · [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)

Use the task-specific roles in [9.1 Required permissions](README.md#91-required-permissions). Confirm availability rather than assuming the tenant is ready.

Follow the [shared tenant readiness check](../README.md#tenant-readiness) using the chapter permissions and feature prerequisites linked above.

For Frontier opt-in and device readiness, follow [9.2 Tenant and device prerequisites](README.md#92-tenant-and-device-prerequisites). Verify each **Check result** before detection or blocking tests.

---

## Prepare accounts and role assignments

Alongside the [shared setup and reviewer accounts](../README.md#least-privilege-model), prepare the following scenario accounts:

| Account | Purpose |
|---|---|
| Standard test user | Signs in to the managed test device and runs approved test tools. No admin role. |

Assign the roles in [9.1 Required permissions](README.md#91-required-permissions) using the shared model. Verify each account can access the pages needed for its tasks.

---

## Test assets and dependencies

**Documentation:** [Understand Shadow AI in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-shadow-ai) · [Understand Local Agents in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-local) · [Preview Agent 365 features through the Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier) · [Discover local AI agents with Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/discover-local-ai-agents) · [Device action: Sync](https://learn.microsoft.com/intune/device-management/actions/sync) · [Tutorial: Enable Internet Access traffic forwarding](https://learn.microsoft.com/entra/global-secure-access/tutorial-internet-access-enable-traffic-forwarding) · [onboarded to Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/onboard-configure)

- [Chapter 1 – Agent discovery and inventory](../chapter-01-agent-discovery/README.md) covers the overall agent inventory in the Microsoft 365 admin center.
- [Chapter 8 – Threat detection and runtime protection (Defender)](../chapter-08-threat-detection/README.md) covers the optional Defender for Endpoint runtime protection for local agents: complete its [preparation](../chapter-08-threat-detection/prerequisites.md#prepare-local-runtime-protection-optional), then run [8.6 Test local runtime protection](../chapter-08-threat-detection/README.md#86-test-local-runtime-protection-optional).
- Prepare at least one dedicated Windows test device that's enrolled in Microsoft Intune and onboarded to Microsoft Defender for Endpoint, and one standard test user who signs in to it.
- Get written approval from the customer's security team for the exact list of AI tools that you may install on the test device (see [9.5.1 Agree the test scope and prepare the test device](README.md#951-agree-the-test-scope-and-prepare-the-test-device)). Don't install any tool that isn't on the approved list.
- Agree with the customer, before you test blocking, that a block created from the Microsoft 365 admin center creates a Microsoft Intune policy that automatically propagates to all managed Windows devices enrolled in Intune (see 9.3.4, 9.4.4 and 9.4.6).

Build guidance: [9.2 Tenant and device prerequisites](README.md#92-tenant-and-device-prerequisites)


**Check result**
- Each asset needed for the selected paths is prepared or has a named build task that will finish before its dependent tests.

---

## Plan propagation and test timing

**Documentation:** [Understand Shadow AI in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-shadow-ai)

| Configuration | Documented propagation window |
|---|---|
| Intune block policy from the Shadow AI or Local Agents page to a device | 15 minutes up to 8 hours |

> ⚠️ **Watch out:** Allow for the documented propagation window and verify the actual configuration or signal before testing. Elapsed time alone is not proof that a change has applied.

---

## References

- [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started)
- [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview)
- [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)
- [Understand Shadow AI in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-shadow-ai)
- [Understand Local Agents in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-local)
- [Discover local AI agents with Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/discover-local-ai-agents)
- [Device action: Sync](https://learn.microsoft.com/intune/device-management/actions/sync)
- [Tutorial: Enable Internet Access traffic forwarding](https://learn.microsoft.com/entra/global-secure-access/tutorial-internet-access-enable-traffic-forwarding)
- [onboarded to Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/onboard-configure)

---

> **Ready?** Continue to the [chapter](README.md). →
