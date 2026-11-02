# Prerequisites - Chapter 8: Threat detection and runtime protection (Defender)

> **Goal:** Prepare the accounts, access, and test assets needed for this chapter and its selected optional paths.

Apply the [shared PoC preparation guidance](../README.md#prerequisites-and-reading-order) and agree the [chapter outcomes](README.md#-what-you-proved). Finish dependent build steps before their tests.

## Table of contents

- [Tenant readiness](#tenant-readiness)
- [Prepare accounts and role assignments](#prepare-accounts-and-role-assignments)
- [Audit recording](#audit-recording)
- [Test assets and dependencies](#test-assets-and-dependencies)
- [Security for AI preparation sequence](#security-for-ai-preparation-sequence)
- [Plan propagation and test timing](#plan-propagation-and-test-timing)
- [References](#references)

---

## Tenant readiness

**Documentation:** [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started) · [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview) · [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)

Use the task-specific roles in [8.1 Required permissions](README.md#81-required-permissions). Confirm availability rather than assuming the tenant is ready.

Follow the [shared tenant readiness check](../README.md#tenant-readiness) using the chapter permissions and feature prerequisites linked above.

---

## Prepare accounts and role assignments

Alongside the [shared setup and reviewer accounts](../README.md#least-privilege-model), prepare the following scenario accounts:

| Account | Purpose |
|---|---|
| Standard test user | Runs the runtime-protection test prompts and verifies containment. No admin role. |
| Maker account | Prepares the published Copilot Studio agent and any optional Foundry test agent. |
| Controlled recipient mailbox | Receives any permitted test email from the Copilot Studio agent. Use only the controlled recipient prepared for the email-agent tests. |

Assign the roles in [8.1 Required permissions](README.md#81-required-permissions) using the shared model. Verify each account can access the pages needed for its tasks.

---

## Audit recording

**Documentation:** [Turn auditing on or off](https://learn.microsoft.com/purview/audit-log-enable-disable) · [Audit logs for Copilot and AI applications](https://learn.microsoft.com/purview/audit-copilot)

Performed by a member of **Audit Manager**. Follow the [shared audit recording check](../chapter-05-lifecycle-audit/prerequisites.md#audit-recording) before the activity to be reviewed.

---

## Test assets and dependencies

**Documentation:** [Enable security for AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai) · [Protect AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/defender-security-for-ai) · [Enable security for AI agents using Microsoft Defender – Connect data sources](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai#connect-data-sources) · [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider) · [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection)

- Verify the required inventory using [Chapter 1 – Agent discovery and inventory](../chapter-01-agent-discovery/README.md). Agent 365 must be onboarded in the tenant before you enable security for AI agents.
- **Copilot Studio test agent:** use the Copilot Studio email agent from [7.6 Copilot Studio email agent and publication](../chapter-07-sensitive-data-protection/README.md#76-copilot-studio-email-agent-and-publication). It has a SharePoint knowledge source and the **Send an email (V2)** tool, and is published to Microsoft 365 Copilot and Teams. It must use generative orchestration, because external threat detection is only called on agents that use generative orchestration. Complete the Chapter 7 tests before you run 8.10, because 8.10.6 blocks this agent.
- (Optional, Foundry in scope) Create and publish the Foundry test agent as described in [1.2.2 Create and publish a Foundry test agent](../chapter-01-agent-discovery/README.md#122-create-and-publish-a-foundry-test-agent), and identify the Azure subscription that contains its Foundry resources (8.5).
- (Optional, local agents in scope) Prepare the Windows test device onboarded to Defender for Endpoint, as described in [9.2 Tenant and device prerequisites](../chapter-09-shadow-ai-local-agents/README.md#92-tenant-and-device-prerequisites), with a supported local AI agent installed (8.6).
- Ownerless-agent governance (identify ownerless agents, reassign ownership, Agent management rules) is covered in [5.5 Govern ownerless agents](../chapter-05-lifecycle-audit/README.md#55-govern-ownerless-agents). This chapter only links to it.
- Shadow AI and local agent discovery in the Microsoft 365 admin center are covered in [Chapter 9 – Shadow AI and local agents](../chapter-09-shadow-ai-local-agents/README.md). This chapter only covers the optional Defender for Endpoint runtime protection for local agents (8.6).
- Detection and investigation of AI agent threats in Microsoft Defender is in public preview. Copilot Studio external threat detection and real-time protection for Copilot Studio agents are in preview.


**Check result**
- Each asset needed for the selected paths is prepared or has a named build task that will finish before its dependent tests.

---

## Security for AI preparation sequence

**Documentation:** [Enable security for AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai) · [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider) · [Enable threat protection for AI services](https://learn.microsoft.com/azure/defender-for-cloud/ai-onboarding) · [AI agent runtime protection in Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/configure-ai-agent-runtime-protection)

Complete [8.2 Enable Security for AI](README.md#82-enable-security-for-ai) and [8.3 Connect the Microsoft 365 connector](README.md#83-connect-the-microsoft-365-connector) before testing. For Copilot Studio, configure [8.4 Real-time protection](README.md#84-turn-on-copilot-studio-real-time-protection). Add [8.5 Foundry protection](README.md#85-turn-on-threat-protection-for-microsoft-foundry-agents-defender-for-cloud) or [8.6 Local runtime protection](README.md#86-turn-on-local-ai-agent-runtime-protection-in-defender-for-endpoint-optional) only when those paths are in scope.

**Check result**
- Each selected setup section's **Check result** is confirmed before its dependent tests.

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
- [Turn auditing on or off](https://learn.microsoft.com/purview/audit-log-enable-disable)
- [Audit logs for Copilot and AI applications](https://learn.microsoft.com/purview/audit-copilot)
- [Enable security for AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai)
- [Protect AI agents using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/defender-security-for-ai)
- [Enable security for AI agents using Microsoft Defender – Connect data sources](https://learn.microsoft.com/defender-xdr/security-for-ai/get-started-defender-security-for-ai#connect-data-sources)
- [Enable external threat detection and protection for Copilot Studio custom agents](https://learn.microsoft.com/microsoft-copilot-studio/external-security-provider)
- [Protect AI agents in real time using Microsoft Defender](https://learn.microsoft.com/defender-xdr/security-for-ai/ai-agent-real-time-protection)
- [Enable threat protection for AI services](https://learn.microsoft.com/azure/defender-for-cloud/ai-onboarding)
- [AI agent runtime protection in Microsoft Defender for Endpoint](https://learn.microsoft.com/defender-endpoint/configure-ai-agent-runtime-protection)
- [Agent Registry](https://learn.microsoft.com/microsoft-365/admin/manage/agent-registry)

---

> **Ready?** Continue to the [chapter](README.md). →
