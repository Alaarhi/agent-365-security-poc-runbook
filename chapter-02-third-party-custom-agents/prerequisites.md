# Prerequisites - Chapter 2: Third-party and custom agents

> **Goal:** Prepare the accounts, access, and test assets needed for this chapter and its selected optional paths.

Choose [Connected platforms](README.md) or [Agent 365 SDK](agent-365-sdk.md); the paths are independent. Apply the [shared PoC preparation guidance](../README.md#prerequisites-and-reading-order) and agree the selected guide's outcome checklist before testing.

## Table of contents

- [Tenant readiness](#tenant-readiness)
- [Prepare accounts and role assignments](#prepare-accounts-and-role-assignments)
- [Test assets and dependencies](#test-assets-and-dependencies)
- [Connected-platform preparation](#connected-platform-preparation)
- [Agent 365 SDK preparation](#agent-365-sdk-preparation)
- [References](#references)

---

## Tenant readiness

**Documentation:** [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started) · [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview) · [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)

Use the task-specific roles for [Connected platforms](README.md#21-required-permissions) or [Agent 365 SDK](agent-365-sdk.md#21-required-permissions). Confirm availability rather than assuming the tenant is ready.

Follow the [shared tenant readiness check](../README.md#tenant-readiness) using the chapter permissions and feature prerequisites linked above.

### Frontier opt-in, only for selected preview features

Performed by **Global Administrator**. Skip this task if no selected feature requires Frontier or opt-in is already verified.

1. In **Agents** > **Overview**, use the **Try now** banner and select **I agree** to accept the terms.
2. Record the date and time, then verify the selected preview feature is available.

**Check result**
- The Frontier feature needed for the selected test is available. Preview terms apply.

---

## Prepare accounts and role assignments

Alongside the [shared setup and reviewer accounts](../README.md#least-privilege-model), prepare the following scenario accounts:

| Account | Purpose |
|---|---|
| Platform administrator (connected-platform path only) | Prepares source-platform credentials, permissions, and any selected observability configuration. |
| Developer account (SDK path only) | Builds and registers custom agents with the Agent 365 CLI. |

Assign the roles for the selected guide using the shared model. Verify each account can access the pages needed for its tasks.

---

## Test assets and dependencies

**Documentation:** [Connected platforms in Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms) · [Third-party agent observability (Frontier)](https://learn.microsoft.com/microsoft-agent-365/admin/third-party-agent-observability) · [Choose an Agent 365 integration option](https://learn.microsoft.com/microsoft-agent-365/developer/choose-integration-option) · [Connect Amazon Bedrock](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-amazon-bedrock) · [Connect Google Vertex AI](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-google-vertex-ai) · [Connect Salesforce Agentforce](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-salesforce-agent-force) · [Connect Databricks Genie](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-databricks-genie) · [Connect Anthropic Claude Managed Agents](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-anthropic-claude) · [Connect Oracle Generative AI Agents](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-oracle-generative-ai) · [Connect Snowflake Cortex](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-snowflake-cortex) · [Install and use the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-cli) · [Agent 365 Skills for guided agent setup](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-skills) · [Quickstart: Connect an existing agent to Agent 365](https://learn.microsoft.com/microsoft-agent-365/developer/get-started) · [Custom client app registration for Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/custom-client-app-registration) · [Onboard a single agent with the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/admin/agent-365-onboarding-cli)

- Verify the required inventory using [Chapter 1 – Agent discovery and inventory](../chapter-01-agent-discovery/README.md) and export the registry before you start, so you can show what this chapter adds.
- Never commit `.env` files or other files with sensitive information to source control.

### Connected-platform preparation

Prepare a non-production account on the selected source platform with at least one test agent, and a platform administrator. Choose one supported platform; you don't need the SDK toolchain for this path.

Continue with [2.2 Connect a third-party agent platform](README.md#22-connect-a-third-party-agent-platform) and its provider-specific instructions.

### Agent 365 SDK preparation

Prepare .NET 8.0 or later, the Azure CLI, an Azure subscription in the same tenant, a test agent project (you can start from [`samples/sdk/`](samples/sdk/README.md)), and a Global Administrator available to complete consent. A connected-platform connection isn't required.

Continue with [2.7 Prepare the custom-agent toolchain](agent-365-sdk.md#27-prepare-the-custom-agent-toolchain).

**Check result**
- Each asset needed for the selected paths is prepared or has a named build task that will finish before its dependent tests.

---

## References

- [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started)
- [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview)
- [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)
- [Connected platforms in Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms)
- [Third-party agent observability (Frontier)](https://learn.microsoft.com/microsoft-agent-365/admin/third-party-agent-observability)
- [Choose an Agent 365 integration option](https://learn.microsoft.com/microsoft-agent-365/developer/choose-integration-option)
- [Connect Amazon Bedrock](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-amazon-bedrock)
- [Connect Google Vertex AI](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-google-vertex-ai)
- [Connect Salesforce Agentforce](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-salesforce-agent-force)
- [Connect Databricks Genie](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-databricks-genie)
- [Connect Anthropic Claude Managed Agents](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-anthropic-claude)
- [Connect Oracle Generative AI Agents](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-oracle-generative-ai)
- [Connect Snowflake Cortex](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-snowflake-cortex)
- [Install and use the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-cli)
- [Agent 365 Skills for guided agent setup](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-skills)
- [Quickstart: Connect an existing agent to Agent 365](https://learn.microsoft.com/microsoft-agent-365/developer/get-started)
- [Custom client app registration for Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/custom-client-app-registration)
- [Onboard a single agent with the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/admin/agent-365-onboarding-cli)

---

> **Ready?** Continue to [Connected platforms](README.md) or [Agent 365 SDK](agent-365-sdk.md). →
