# Prerequisites - Chapter 4: Tools and MCP server governance

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

Use the task-specific roles in [4.1 Required permissions](README.md#41-required-permissions). Confirm availability rather than assuming the tenant is ready.

Follow the [shared tenant readiness check](../README.md#tenant-readiness) using the chapter permissions and feature prerequisites linked above.

---

## Prepare accounts and role assignments

Alongside the [shared setup and reviewer accounts](../README.md#least-privilege-model), prepare the following scenario accounts:

| Account | Purpose |
|---|---|
| Standard test user | Tests plugin availability as a pilot-group member and invokes the test MCP tools. No admin role. |
| Second test user | User outside the plugin pilot group. No admin role. |
| Developer account | Builds and registers custom agents and MCP servers with the Agent 365 CLI. |

Assign the roles in [4.1 Required permissions](README.md#41-required-permissions) using the shared model. Verify each account can access the pages needed for its tasks.

---

## Prepare groups

**Documentation:** [Assign Microsoft Entra roles](https://learn.microsoft.com/entra/identity/role-based-access-control/manage-roles-portal) · [Microsoft Entra built-in roles](https://learn.microsoft.com/entra/identity/role-based-access-control/permissions-reference) · [Roles and role groups in Microsoft Purview](https://learn.microsoft.com/purview/purview-permissions)

Performed by **Groups Administrator**.

Create or verify these PoC groups before the tasks that use them:

| Group | Members |
|---|---|
| `A365-PoC-Plugin-Pilot` | Standard test user only |

**Check result**
- Group membership matches the table, and the groups are recorded as PoC assets.

---

## Test assets and dependencies

**Documentation:** [Manage plugins, skills, and MCP servers in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/manage-plugins-skills-mcp-servers) · [Build plugins for Copilot Cowork](https://learn.microsoft.com/microsoft-365/copilot/cowork/cowork-plugin-development) · [Bring your own (BYO) MCP server in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/manage-byo-mcp-server) · [Agent 365 CLI develop-mcp command reference](https://learn.microsoft.com/microsoft-agent-365/developer/reference/cli/develop-mcp) · [Install and use the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-cli) · [Add and manage tools – Set up service principal](https://learn.microsoft.com/microsoft-agent-365/developer/tooling#set-up-service-principal) · [Advanced hunting overview](https://learn.microsoft.com/defender-xdr/advanced-hunting-overview) · [CloudAppEvents table](https://learn.microsoft.com/defender-xdr/advanced-hunting-cloudappevents-table) · [BYO MCP server article](https://learn.microsoft.com/microsoft-365/admin/manage/manage-byo-mcp-server#register-your-mcp-server) · [Connect MCP servers to developer clients](https://learn.microsoft.com/microsoft-agent-365/add-mcp-tools-developer-experiences#connect-mcp-servers-to-developer-clients)

- Identify one plugin to restrict in 4.3.2. To also test **Delete**, use a plugin that your organization uploaded (packaged as described in [Build plugins for Copilot Cowork](https://learn.microsoft.com/microsoft-365/copilot/cowork/cowork-plugin-development)); if you upload it yourself, complete 4.3.4 before 4.3.2. Delete isn't available for plugins from the Microsoft 365 Store.
- Prepare a test remote MCP server that you own, with a publicly accessible HTTPS endpoint (for example, `https://<your-host>/mcp`) and one of the supported authentication types (`NoAuth`, `APIKey`, `ExternalOAuth`, or `EntraOAuth`). Don't use a production server. During preview, you can't republish new versions of a registered server.
- Prepare a Copilot Studio environment and a test custom agent that you can add tools to.
- (Optional, for 4.5) An Azure API Management or Azure AI Gateway instance with at least one MCP server registered in it, or a LiteLLM gateway with its URL and API key.
- Confirm that Microsoft Defender advanced hunting is available to the security reviewer. See [Chapter 8 – Threat detection and runtime protection (Defender)](../chapter-08-threat-detection/README.md).
- Tools Gateway, BYO MCP server, Power Platform connector usage, and the **Requests (preview)** tab are preview features and aren't meant for production use. Tool-level granular control is rolling out to tenants.

Build guidance: [4.6 Bring your own MCP server](README.md#46-bring-your-own-mcp-server-preview)


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
- [Manage plugins, skills, and MCP servers in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/manage-plugins-skills-mcp-servers)
- [Build plugins for Copilot Cowork](https://learn.microsoft.com/microsoft-365/copilot/cowork/cowork-plugin-development)
- [Bring your own (BYO) MCP server in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/manage-byo-mcp-server)
- [Agent 365 CLI develop-mcp command reference](https://learn.microsoft.com/microsoft-agent-365/developer/reference/cli/develop-mcp)
- [Install and use the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-cli)
- [Add and manage tools – Set up service principal](https://learn.microsoft.com/microsoft-agent-365/developer/tooling#set-up-service-principal)
- [Advanced hunting overview](https://learn.microsoft.com/defender-xdr/advanced-hunting-overview)
- [CloudAppEvents table](https://learn.microsoft.com/defender-xdr/advanced-hunting-cloudappevents-table)
- [BYO MCP server article](https://learn.microsoft.com/microsoft-365/admin/manage/manage-byo-mcp-server#register-your-mcp-server)
- [Connect MCP servers to developer clients](https://learn.microsoft.com/microsoft-agent-365/add-mcp-tools-developer-experiences#connect-mcp-servers-to-developer-clients)

---

> **Ready?** Continue to the [chapter](README.md). →
