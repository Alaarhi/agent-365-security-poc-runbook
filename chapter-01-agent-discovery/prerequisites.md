# Prerequisites - Chapter 1: Agent discovery and inventory

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

Use the task-specific roles in [1.1 Required permissions](README.md#11-required-permissions). Confirm availability rather than assuming the tenant is ready.

Follow the [shared tenant readiness check](../README.md#tenant-readiness) using the chapter permissions and feature prerequisites linked above.

---

## Prepare accounts and role assignments

Alongside the [shared setup and reviewer accounts](../README.md#least-privilege-model), prepare the following scenario accounts:

| Account | Purpose |
|---|---|
| Standard test user | Discovers or installs the PoC agents made available for the test. No admin role. |
| Maker account | Builds the Copilot Studio or Foundry test agents and prepares the test knowledge source. |
| Developer account | Creates and publishes the Foundry test agent when that platform is in scope. |

Assign the roles in [1.1 Required permissions](README.md#11-required-permissions) using the shared model. Verify each account can access the pages needed for its tasks.

---

## Test assets and dependencies

**Documentation:** [Connect existing agents to Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/connect-existing-agents) · [Agent registry integration for Copilot Studio](https://learn.microsoft.com/microsoft-agent-365/builder/agent-registry) · [Agent identity integration for Copilot Studio](https://learn.microsoft.com/microsoft-agent-365/builder/identity) · [Microsoft Agent 365 integration with Foundry](https://learn.microsoft.com/azure/foundry/agents/concepts/agent-365-integration) · [Publish your agent as an Agent Application](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-agent) · [Agent overview in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview) · [Get started with agents in SharePoint](https://learn.microsoft.com/sharepoint/get-started-sharepoint-agents)

- Prepare at least one Microsoft-native test agent per platform in scope, as described in [1.2](README.md#12-discover-microsoft-native-agents). Use the samples in [`samples/`](samples/README.md).
- Prepare a test SharePoint site to use as a knowledge source for the Copilot Studio sample.
- Chapter 2 has separate guides for [Connected platforms](../chapter-02-third-party-custom-agents/README.md) (Amazon Bedrock, Google Vertex AI, and others) and [Agent 365 SDK agents](../chapter-02-third-party-custom-agents/agent-365-sdk.md). Local agents and Shadow AI are covered in [Chapter 9 – Shadow AI and local agents](../chapter-09-shadow-ai-local-agents/README.md).
- If you plan to use Microsoft Graph PowerShell (1.7.3), install PowerShell 7, which is the recommended version for the Microsoft Graph PowerShell SDK.


**Check result**
- Each asset needed for the selected paths is prepared or has a named build task that will finish before its dependent tests.

---

## Plan propagation and test timing

**Documentation:** [Agent Registry](https://learn.microsoft.com/microsoft-365/admin/manage/agent-registry)

| Configuration | Propagation window to plan for |
|---|---|
| Risk signals in the Agent Registry compared with the source security portals | Up to 1 hour |

> ⚠️ **Watch out:** Allow for the documented propagation window and verify the actual configuration or signal before testing. Elapsed time alone is not proof that a change has applied.

---

## References

- [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started)
- [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview)
- [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)
- [Connect existing agents to Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/connect-existing-agents)
- [Agent registry integration for Copilot Studio](https://learn.microsoft.com/microsoft-agent-365/builder/agent-registry)
- [Agent identity integration for Copilot Studio](https://learn.microsoft.com/microsoft-agent-365/builder/identity)
- [Microsoft Agent 365 integration with Foundry](https://learn.microsoft.com/azure/foundry/agents/concepts/agent-365-integration)
- [Publish your agent as an Agent Application](https://learn.microsoft.com/azure/foundry/agents/how-to/publish-agent)
- [Get started with agents in SharePoint](https://learn.microsoft.com/sharepoint/get-started-sharepoint-agents)
- [Agent Registry](https://learn.microsoft.com/microsoft-365/admin/manage/agent-registry)

---

> **Ready?** Continue to the [chapter](README.md). →
