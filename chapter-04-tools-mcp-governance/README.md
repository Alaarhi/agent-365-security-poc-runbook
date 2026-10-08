# Chapter 4 – Tools and MCP Server Governance

**Pillar:** Govern
**What it proves:** Every tool an agent can call (plugins, skills, MCP servers, and connectors) is inventoried in one registry, is approved before agents can use it, and can be blocked centrally so that every dependent agent loses access at runtime.

**Success criteria**
- The Tools registry in the Microsoft 365 admin center lists plugins, skills, MCP servers, and connectors with their status, type, and publisher.
- A test bring-your-own (BYO) MCP server registered with the Agent 365 CLI appears as a request on the **Requests (preview)** tab, and is listed as **Available** in the registry only after an administrator approves it and grants consent.
- After the test MCP server is blocked, a test agent in Copilot Studio can no longer invoke it; after it is unblocked, the agent can invoke it again.
- A plugin scoped to a pilot group is available to the group member, appears to a non-member as blocked by organizational policy with **Request access**, and the request appears on the **Requests** tab for approval or rejection.
- Microsoft Defender advanced hunting returns tool-invocation records for the test MCP server.
- (Optional) MCP servers registered in a connected Azure API Management, Azure AI Gateway, or LiteLLM gateway appear in the registry under the **AI gateway** source without per-server registration.

## 4.1 Required permissions

Grant the read-only role to reviewers first, give the setup roles only to the person who makes each change, and assign roles as Active (not eligible) for the duration of the PoC window.

| Task | Least-privilege role | Section |
|---|---|---|
| View the Tools registry, plugins, connectors, and settings (read-only) | AI Reader or Global Reader | 4.2 |
| Block or unblock tools; set plugin availability; upload, install, uninstall, delete, or block plugins and skills; review plugin access requests | AI Administrator | 4.2.2, 4.3, 4.7.3, 4.7.4 |
| Review and approve MCP server requests and grant tenant-wide consent; block, unblock, or delete MCP servers; manage individual tools | AI Administrator (Global Administrator also meets both requirements) | 4.4, 4.6.4, 4.7.1, 4.7.2, 4.7.5, 4.10 |
| Connect a Tools Gateway, grant the one-time tenant-wide consent, and govern discovered servers | Global Administrator | 4.5, 4.7.5 |
| Provision the Agent 365 Tools service principal (one-time per tenant) | Global Administrator | 4.6.1 |
| Register a BYO MCP server with the Agent 365 CLI, and use the approved server in a supported client | Developer | 4.6.1, 4.6.2, 4.6.5, 4.7.1, 4.7.2 |
| Evaluate MCP tool-definition quality with the Agent 365 CLI | Developer (no admin role required) | 4.6.3 |
| Grant a BYO MCP server's permission to agent identities that are missing it (`a365 develop-mcp grant-agents-access`; needs a CLI version later than 1.1.221) | Global Administrator | 4.9 |
| Discover plugins and request access in the Copilot channel | Standard test user and second test user (no admin role) | 4.7.3, 4.7.4 |
| Validation / read-only review of MCP activity in advanced hunting | Security Reader | 4.6.6, 4.7.6 |

**Before you start:**
- Complete [Chapter 0 – Prerequisites and PoC preparation](../chapter-00-prerequisites/README.md). This chapter uses the **standard test user** and the **second test user** from [0.4.1 Create the PoC accounts](../chapter-00-prerequisites/README.md#041-create-the-poc-accounts), and the `A365-PoC-Plugin-Pilot` group (standard test user only) from [0.4.2 Create the PoC groups](../chapter-00-prerequisites/README.md#042-create-the-poc-groups).
- Identify one plugin to restrict in 4.3.2. To also test **Delete**, use a plugin that your organization uploaded (packaged as described in [Build plugins for Copilot Cowork](https://learn.microsoft.com/microsoft-365/copilot/cowork/cowork-plugin-development)); if you upload it yourself, complete 4.3.4 before 4.3.2. Delete isn't available for plugins from the Microsoft 365 Store.
- Prepare a test remote MCP server that you own, with a publicly accessible HTTPS endpoint (for example, `https://<your-host>/mcp`) and one of the supported authentication types (`NoAuth`, `APIKey`, `ExternalOAuth`, or `EntraOAuth`). Don't use a production server. During preview, you can't republish new versions of a registered server.
- Prepare a Copilot Studio environment and a test custom agent that you can add tools to.
- (Optional, for 4.5) An Azure API Management or Azure AI Gateway instance with at least one MCP server registered in it, or a LiteLLM gateway with its URL and API key.
- Confirm that Microsoft Defender advanced hunting is available to the security reviewer. See [Chapter 8 – Threat Detection and Runtime Protection (Defender)](../chapter-08-threat-detection/README.md).
- Tools Gateway, BYO MCP server, Power Platform connector usage, and the **Requests (preview)** tab are preview features and aren't meant for production use. Tool-level granular control is rolling out to tenants.

## 4.2 Review the Tools page and registry
**Documentation:** [Overview of the Tools page in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-tools-overview) · [Agent management roles and permissions](https://learn.microsoft.com/microsoft-365/admin/manage/agent-roles-perms) · [How do enterprises control what agents can do?](https://learn.microsoft.com/microsoft-agent-365/guidance/govern-tools)

### 4.2.1 Open the Tools registry and identify the four tool types
Performed by **AI Reader** (or Global Reader).
1. Sign in to the Microsoft 365 admin center at `https://admin.cloud.microsoft`.
2. Select **Agents** > **Tools** > **Registry**.
3. Review the tool types that the page brings together:

| Tool type | What it is |
|---|---|
| Plugins | Installable packages that bundle capabilities an agent can use, such as skills, MCP servers, and connectors. |
| Skills | Reusable instructions or workflows that teach an agent how to do a task consistently. |
| MCP servers | Standardized servers that expose tools and resources that an agent can dynamically discover and use. |
| Connectors | Prebuilt links to external systems and data sources that an agent can read from and write to. |

4. Note the two tabs: **Registry** (discover and manage tools in the tenant) and **Requests** (review and approve requests for tools).

**Check result**
- The registry loads and shows tools of more than one type.
- As AI Reader or Global Reader, you can view tools and settings but can't change them.

### 4.2.2 Filter the registry and act on a tool
Performed by **AI Reader** (view) and **AI Administrator** (actions).
1. On **Agents** > **Tools** > **Registry**, filter by **Status** (**Available** or **Blocked**).
2. Filter by **Publisher** to separate Microsoft tools from tools published by other providers.
3. Review the columns:

| Column | Description |
|---|---|
| Name | Display name of the tool, for example **Microsoft Teams MCP Server**. |
| Status | **Available** or **Blocked**. |
| Type | Tool category, for example **MCP Server**. |
| Publisher | Who published the tool, for example Microsoft for first-party tools. |

4. Select a tool to open its overview page. As AI Administrator, you can select **Block** to prevent agents or workflows from using the tool, or **Unblock** to restore access. Don't block tools in this step; blocking is tested in 4.7.2.

**Check result**
- Filters narrow the list to the selected status or publisher.
- AI Reader and Global Reader have read-only access to tools and settings; AI Administrator can take the **Block** and **Unblock** actions.

### 4.2.3 Review Power Platform connector usage (preview)
Performed by **AI Reader** (or Global Reader).

This view provides visibility into which Power Platform connectors agents use. It doesn't include management controls.
1. Select **Agents** > **Tools** > **Registry**.
2. Select **Connectors**.
3. Review the list of Power Platform connectors used by agents in your organization.
4. Select a connector to view the agents that use it. The connector's overview page shows the agents associated with the selected connector.
5. Note the **View in Power Platform** option on the connector's overview page. It opens the Power Platform admin center (`https://admin.powerplatform.microsoft.com`), where the connector's use is blocked, allowed, and governed (see [Advanced connector policies](https://learn.microsoft.com/power-platform/admin/advanced-connector-policies)). This chapter doesn't change connector policies.

**Check result**
- At least one connector shows the agents that use it.

## 4.3 Govern plugins and skills
**Documentation:** [Manage plugins, skills, and MCP servers in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/manage-plugins-skills-mcp-servers) · [Build plugins for Copilot Cowork](https://learn.microsoft.com/microsoft-365/copilot/cowork/cowork-plugin-development)

Plugins are primarily available to end users in the Copilot channel. Managing a skill uses the same actions and steps as managing a plugin, so every task in this section applies to both.

### 4.3.1 Set organization-level plugin availability by publisher category
Performed by **AI Administrator**.
1. In the Microsoft 365 admin center, select **Agents** > **Settings** > **Agent and plugin access**.
2. Record the publisher categories that are currently selected, so that you can restore them in 4.10.
3. Under the installation settings, choose which publisher categories users can access: **Microsoft**, **your organization**, or **certified external publishers**.
4. Select a category to allow users to discover and install plugins from that publisher type. To block all third-party plugins, clear **certified external publishers**.

**Check result**
- Plugins from a category that isn't selected remain discoverable but display "This plugin is blocked by your organization's policy." Eligible users can still select **Request access**. This is tested in 4.7.4.

### 4.3.2 Restrict a plugin to specific users and groups
Performed by **AI Administrator**.
1. Select **Agents** > **Tools** > **Plugins**.
2. Select the plugin you identified in **Before you start**.
3. Open **Users** and choose one of the availability options:
   - **All users** – available to everyone in the organization.
   - **No users** – unavailable to all users.
   - **Specific users and groups** – available only to the selected users or groups.
4. For the PoC, select **Specific users and groups** and add `A365-PoC-Plugin-Pilot`.
5. Review the selection, and then save the changes.

**Check result**
- The plugin's **Users** setting shows only the pilot group. The end-user result is validated in 4.7.3.

### 4.3.3 Review plugin access requests
Performed by **AI Administrator**.

A plugin access request is created when a user selects **Request access** on a restricted plugin. The end-to-end flow is tested in 4.7.3.
1. Select **Agents** > **Tools** > **Requests**.
2. Select the plugin access request that you want to review.
3. Review the request details, including the user and the requested plugin.
4. Select **Approve** to grant access, or **Reject** to deny the request.

**Check result**
- **Approve** grants the user access to the plugin; **Reject** denies the request.

### 4.3.4 Upload a plugin or skill
Performed by **AI Administrator**.

A developer must first package the plugin or skill into a manifest file.
1. Select **Agents** > **Tools** > **Registry**.
2. Select **Upload**.
3. Upload the manifest file for the plugin or skill.
4. Review the components included in the package, such as MCP servers and skills, and then select **Next**.
5. In the **Scope users** pane, select **All users** or **Specific users or groups**. For the PoC, scope it to `A365-PoC-Plugin-Pilot`.
6. Review the configuration, and then select **Install**.

**Check result**
- The upload wizard listed the components included in the package, such as MCP servers and skills, and the installation completed for the selected users.

### 4.3.5 Install or uninstall a plugin or skill
Performed by **AI Administrator**.

Install a plugin or skill so that users don't have to install it manually:
1. Select **Agents** > **Tools** > **Plugins**.
2. Select a plugin or skill. The **Overview** pane opens.
3. Select **Install**.
4. In the **Select users** pane, confirm the details and choose **All users** or **specific users or groups**.
5. Select **Next**.
6. In the **Review and install** pane, confirm the details and select **Install**.

Uninstall a plugin or skill so that agents can't use it unless it's installed again:
1. Select **Agents** > **Tools** > **Plugins**.
2. Select the plugin or skill. The **Overview** pane opens.
3. Select **Uninstall**, and then confirm by selecting **Uninstall**.

**Check result**
- After install, the plugin or skill is ready to use for the selected users without manual installation by end users.
- After uninstall, it isn't available to agents unless you install it again.

### 4.3.6 Delete or block a plugin or skill
Performed by **AI Administrator**.

Perform these actions only on test plugins or skills.

| Action | Effect | Applies to |
|---|---|---|
| Uninstall | Removes the plugin or skill from the environment. It isn't available to agents unless it's installed again. | Any installed plugin or skill |
| Delete | Removes the package across the organization. Agents can no longer use it, and it's removed from the registry. | Only plugins and skills uploaded to your tenant (not Microsoft 365 Store items) |
| Block | Prevents users and agents across the organization from accessing it, without deleting the package. Can be reversed with **Unblock**. | Any plugin or skill |

To delete:
1. Select **Agents** > **Tools** > **Plugins**.
2. Select the plugin or skill. The **Overview** pane opens.
3. Select **Delete**, and then confirm by selecting **Delete**.

To block:
1. Select **Agents** > **Tools** > **Plugins**.
2. Select the plugin or skill. The **Overview** pane opens.
3. Select **Block**, and then confirm by selecting **Block**.

> Caution: Blocking cascades. Blocking a plugin prevents users from accessing the plugin and any agents that depend on it; its associated MCP servers and connectors remain available to other plugins. Blocking an MCP server also blocks dependent plugins and linked connectors. Blocking a plugin package blocks the agents included in it, because they share the same governance controls; unblocking the package restores access to those agents. To see which plugins use an MCP server, select the MCP server in the registry before you block it.

**Check result**
- A blocked plugin or skill can no longer be used by agents. A deleted plugin or skill is removed from the registry.

## 4.4 Govern MCP servers
**Documentation:** [Manage plugins, skills, and MCP servers – Review and approve MCP requests](https://learn.microsoft.com/microsoft-365/admin/manage/manage-plugins-skills-mcp-servers#review-and-approve-mcp-requests) · [Grant tenant-wide admin consent to an application](https://learn.microsoft.com/entra/identity/enterprise-apps/grant-admin-consent) · [Agent 365 tooling servers overview](https://learn.microsoft.com/microsoft-agent-365/tooling-servers-overview)

To approve an MCP server, the reviewer must have access to the **Tools** page and must be able to grant tenant-wide consent. AI Administrator and Global Administrator meet both requirements; use AI Administrator for least privilege. Each MCP server corresponds to a permission on the Agent 365 application, and agents gain access to the server only after consent. A blocked MCP server is blocked for every user and every agent. The ability to allow or disallow tooling and MCP servers in the Microsoft 365 admin center might not be available in your region yet ([Agent 365 tooling servers overview](https://learn.microsoft.com/microsoft-agent-365/tooling-servers-overview)).

### 4.4.1 Review and approve MCP server requests
Performed by **AI Administrator**.
1. Sign in to the Microsoft 365 admin center at `https://admin.cloud.microsoft`.
2. Select **Agents** > **Tools**, and then select the **Requests (preview)** tab.
3. Review the server name, publisher, requester, and request date.
4. Review the server information and declared tools for accuracy and compliance.
5. Select **Approve** to make the server available in the organizational registry, or **Reject** to deny the request.
6. After approval, consent to the Microsoft Entra permissions that the MCP server requires. The server becomes available to agent-building surfaces only after consent is granted.

**Check result**
- The server appears in **Agents** > **Tools** > **Registry** with status **Available**.
- After approval and consent, allow up to 30 minutes for the server to appear in all Copilot Studio environments in the tenant.

### 4.4.2 Block or unblock an MCP server
Performed by **AI Administrator**.
1. Select **Agents** > **Tools**, and then select the **Registry** tab.
2. Select an MCP server to open its overview pane. Selecting the server shows the plugins that use it.
3. Select **Block** to restrict the server across the organization, or **Unblock** to restore access to a previously blocked server.
4. If one or more plugins use the server, you can also block all linked plugins when you block the server.

**Check result**
- The server status is **Blocked** (or **Available** after unblocking). Blocking disables all the tools the server exposes.

### 4.4.3 Enable or disable individual tools (where supported)
Performed by **AI Administrator**.

Tool-level granular control is rolling out to tenants and supports only specific types of MCP servers registered on Agent 365, and MCP servers registered in an AI Gateway tier of Azure API Management. Support for BYO MCP servers is planned for a future release. Use it to keep high-risk tools (for example, tools that write, delete, or process payments) disabled while lower-risk tools on the same server stay enabled.
1. Select **Agents** > **Tools**, and then select the **Registry** tab.
2. Select an MCP server to open its overview pane.
3. Select the **Tools** tab. The list shows every tool the server exposes, its description, and an **Enabled** or **Disabled** toggle.
4. Turn individual tools on or off as needed.
5. Select **Save** to apply your changes, or **Discard changes** to cancel.

**Check result**
- The tool's toggle is **Disabled** after you save. The policy applies wherever the tool is used and is enforced at runtime by the Agent 365 Tooling Gateway.
- If the **Tools** tab shows that the server doesn't support tool discovery, use 4.4.2 to block or allow the whole server instead.

## 4.5 Connect a Tools Gateway (preview)
**Documentation:** [Manage Tools Gateway in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/manage-tools-gateway) · [About MCP servers in Azure API Management](https://learn.microsoft.com/azure/api-management/mcp-server-overview) · [AI Gateway tier overview](https://learn.microsoft.com/azure/api-management/ai-gateway-overview)

Tools Gateway connects an existing Azure API Management (APIM) instance, Azure AI Gateway, or LiteLLM gateway to the Microsoft 365 admin center. After a Global Administrator grants a single tenant-wide consent, the MCP servers registered in that gateway appear on the Tools page and are governed like any other MCP server. Servers added to the gateway later are discovered automatically.

### 4.5.1 Confirm gateway prerequisites
Performed by **Global Administrator**.
1. Confirm that an AI Gateway or APIM instance is configured.
2. Confirm that at least one MCP server is registered in the gateway (in APIM, for example by [exposing a REST API as an MCP server](https://learn.microsoft.com/azure/api-management/export-rest-mcp-server) or [exposing an existing MCP server](https://learn.microsoft.com/azure/api-management/expose-existing-mcp-server)).
3. Confirm that a Global Administrator is available to grant consent and has access to the Microsoft 365 admin center.
4. For a LiteLLM gateway, collect the gateway name, gateway URL, and API key.

**Check result**
- You can name at least one MCP server that is registered in the gateway, to look for in 4.5.3.

### 4.5.2 Connect an Azure or LiteLLM gateway
Performed by **Global Administrator**.
1. Sign in to the Microsoft 365 admin center as a Global Administrator.
2. Go to **Agents** > **Settings**.
3. Select **Gateways**.
4. Under **Gateways**, connect one of the following:
   - **Microsoft Azure**: turn on the toggle to connect an Azure API Management service or Azure AI Gateway, and then review and accept the requested permissions.
   - **LiteLLM gateway**: select **Connect a gateway**, and then enter the gateway name, gateway URL, and API key.

**Check result**
- Consent is granted once per tenant and applies to all MCP servers in the connected gateway; individual servers don't require separate consent.
- Discovery starts automatically after consent is granted.

### 4.5.3 Govern gateway-discovered MCP servers
Performed by **Global Administrator**.

Discovery starts automatically after consent and typically completes within a few minutes.
1. Go to **Agents** > **Tools**.
2. Filter the list by source, and then select **AI gateway**.
3. Review the discovered MCP servers.
4. Block or allow each server as in 4.4.2. For servers in an AI Gateway tier of APIM, you can also manage individual tools as in 4.4.3.

**Check result**
- The MCP server you noted in 4.5.1 appears under the **AI gateway** source.
- Only MCP servers registered in the connected gateway are discovered. New servers added to the gateway appear on subsequent refreshes.

## 4.6 Bring your own MCP server (preview)
**Documentation:** [Bring your own (BYO) MCP server in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/manage-byo-mcp-server) · [Agent 365 CLI develop-mcp command reference](https://learn.microsoft.com/microsoft-agent-365/developer/reference/cli/develop-mcp) · [Install and use the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-cli) · [Add and manage tools – Set up service principal](https://learn.microsoft.com/microsoft-agent-365/developer/tooling#set-up-service-principal) · [Advanced hunting overview](https://learn.microsoft.com/defender-xdr/advanced-hunting-overview) · [CloudAppEvents table](https://learn.microsoft.com/defender-xdr/advanced-hunting-cloudappevents-table)

BYO MCP server routes an organization's internally built remote MCP servers through the Agent 365 Tooling Gateway, so administrators control them in the Microsoft 365 admin center and security teams get observability. The flow is:
1. A developer registers the server with the Agent 365 CLI (server URL, authentication type, and tools).
2. An administrator reviews and approves or rejects the request, and then grants the required Microsoft Entra permissions.
3. Supported clients use the approved server. During preview, the supported clients are Copilot Studio, Visual Studio Code, Claude Code, and GitHub Copilot CLI. Azure AI Foundry and Microsoft 365 declarative agents aren't supported.
4. The security team monitors activity and tool invocations in Microsoft Defender advanced hunting.

### 4.6.1 Confirm developer prerequisites
Performed by **developer**, with **Global Administrator** for the service principal.
1. Install the Agent 365 CLI (requires .NET; .NET 8.0 is recommended):

   ```powershell
   dotnet tool install --global Microsoft.Agents.A365.DevTools.Cli
   ```

   If it's already installed, update it:

   ```powershell
   dotnet tool update --global Microsoft.Agents.A365.DevTools.Cli
   ```

2. Verify the installation by running the `--help` command. BYO MCP server registration requires Agent 365 CLI version **1.1.165-preview or later**. For available versions, see the [Microsoft.Agents.A365.DevTools.Cli NuGet page](https://www.nuget.org/packages/Microsoft.Agents.A365.DevTools.Cli).

   ```powershell
   a365 -h
   ```

3. Confirm that the Agent 365 service principal associated with app ID `ea9ffc3e-8a23-4a7d-836d-234d7c7565c1` is provisioned in your tenant.
4. If you can't find it, a Global Administrator provisions it once per tenant: download [New-Agent365ToolsServicePrincipalProdPublic.ps1](https://github.com/microsoft/Agent365-devTools/blob/main/scripts/cli/Auth/New-Agent365ToolsServicePrincipalProdPublic.ps1), open PowerShell as Administrator, go to the script directory, run the script, and sign in by using your Azure credentials when prompted:

   ```powershell
   .\New-Agent365ToolsServicePrincipalProdPublic.ps1
   ```

5. Confirm that the test MCP server has a publicly accessible endpoint and uses one of the supported authentication types: `NoAuth`, `APIKey` (header or query parameter), `ExternalOAuth`, or `EntraOAuth`.
6. Plan the target tenant for registration: the registration command's `--tenant-id` option defaults to the current `az login` tenant. Pass `--tenant-id` with the PoC tenant ID to target the PoC tenant explicitly.

**Check result**
- `a365 -h` displays the help information, and the service principal is provisioned.

### 4.6.2 Register the MCP server with the Agent 365 CLI
Performed by **developer**.

Rules from the CLI reference:
- The server name must start with `ext_` and be at most 20 characters, for example `ext_PocTest`.
- Tool names must exactly match the names exposed by the remote MCP server. Mismatched names cause tool invocations to fail at runtime.
- Command-line options override values in a JSON input file. Omitted required values are prompted for interactively.
- If registration fails after the Microsoft Entra app registrations are created, they aren't rolled back automatically. Delete them manually in the Azure portal before you retry.

1. Register the server by using one of the following methods.

   Option A – command-line options. This example is for a server that requires no authentication (Bash syntax):

   ```bash
   a365 develop-mcp register-external-mcp-server \
   --server-name "ext_PocTest" \
   --server-url "https://<your-host>/mcp" \
   --publisher "Contoso" \
   --description "PoC test MCP server" \
   --auth-type "NoAuth" \
   --tools "tool1,tool2"
   ```

   For a server that takes an API key in a header, use these authentication options instead:

   ```bash
   a365 develop-mcp register-external-mcp-server \
   --server-name "ext_PocTest" \
   --server-url "https://<your-host>/mcp" \
   --publisher "Contoso" \
   --description "PoC test MCP server" \
   --auth-type APIKey \
   --api-key-location Header \
   --api-key-name token \
   --tools "tool1,tool2"
   ```

   For `EntraOAuth`, use `--auth-type EntraOAuth --remote-scopes "<scope>"`. For `ExternalOAuth`, also pass `--idp-authorization-url`, `--idp-token-url`, `--idp-scopes`, `--idp-client-id`, `--idp-client-secret`, and `--remote-scopes`, and after registration add the redirect URI that the CLI displays to your external identity provider application. For complete examples of each type, see the [BYO MCP server article](https://learn.microsoft.com/microsoft-365/admin/manage/manage-byo-mcp-server#register-your-mcp-server).

   Option B – JSON file. Create `ext-poctest.json` by using the structure of the Learn `NoAuth` example:

   ```json
   {
     "serverName": "ext_PocTest",
     "serverUrl": "https://<your-host>/mcp",
     "authType": "NoAuth",
     "description": "PoC test MCP server",
     "publisherName": "Contoso",
     "tools": [
       {
         "name": "tool1",
         "description": "<what tool1 does>"
       }
     ],
     "remoteScopes": null,
     "externalOAuth": null,
     "apiKey": null
   }
   ```

   Preview the actions with `--dry-run`, and then register:

   ```powershell
   a365 develop-mcp register-external-mcp-server -f ./ext-poctest.json --dry-run
   a365 develop-mcp register-external-mcp-server -f ./ext-poctest.json
   ```

2. After successful registration, submit the MCP server for admin review in the Microsoft 365 admin center, and ask the AI Administrator to review it. Before the request is approved, run steps 1–2 of 4.7.1.

**Check result**
- The registered server appears in the Microsoft 365 admin center on **Agents** > **Tools** > **Requests (preview)** for review and approval.

### 4.6.3 Evaluate tool-definition quality
Performed by **developer** (no admin role required).

`a365 develop-mcp evaluate` reads the server's tool schemas through a standard MCP `tools/list` call and produces a report with a score and prioritized improvements. Semantic checks are scored by a coding agent CLI (GitHub Copilot CLI or Claude Code) that runs locally under the developer's own account. The command doesn't send tool-schema data to Microsoft and doesn't call Azure or Microsoft Graph. Run it only against MCP servers you trust.

1. (Optional, for semantic scoring) Install one coding agent CLI locally, for example GitHub Copilot CLI:

   ```powershell
   npm install -g @github/copilot
   ```

2. Run the evaluation against the test server:

   ```powershell
   a365 develop-mcp evaluate --server-url "https://<your-host>/mcp" --output-dir "./eval"
   ```

   If the server requires authentication, supply the bearer token through the `A365_MCP_AUTH_TOKEN` environment variable instead of the command line:

   ```powershell
   $env:A365_MCP_AUTH_TOKEN = "<bearer-token>"
   a365 develop-mcp evaluate --server-url "https://<your-host>/mcp" --output-dir "./eval"
   ```

   To skip AI scoring and generate the checklist only, so that you can score it with your own LLM:

   ```powershell
   a365 develop-mcp evaluate --server-url "https://<your-host>/mcp" --eval-engine none
   ```

3. Open `<server-name>_eval_report.html` from the output directory (`./eval` in these examples; the current directory if you omit `--output-dir`). Review the overall score (0-100), the maturity level, the per-tool scores (tool name, tool description, parameter name, parameter description, schema structure), and the prioritized action items.

**Check result**
- The output directory contains `<server-name>_checklist.json`, `<server-name>_eval_report.html`, and `<server-name>_eval_report.json`.
- Keep the HTML report as PoC evidence that the tool definitions were evaluated.

### 4.6.4 Review, approve, and consent
Performed by **AI Administrator**.

Complete steps 1–2 of 4.7.1 before you approve the request.
1. Follow 4.4.1 for the `ext_PocTest` request: review the server name, publisher, requester, request date, server information, and declared tools.
2. Compare the declared tools with the evaluation report from 4.6.3.
3. Select **Approve**, and then consent to the Microsoft Entra permissions that the server requires.

The governance controls that apply to a BYO MCP server are:

| Control | Description |
|---|---|
| Approval or rejection | An administrator approves or rejects each BYO MCP server before it can be used. |
| Server-level block | An administrator can block an approved server at any time. |
| Runtime enforcement | Blocked MCP servers can't be invoked at runtime from any client surface. |
| Tool-level block | Rolling out for supported MCP servers registered on Agent 365; support for BYO MCP servers is planned for a future release. |
| Tools snapshot | An administrator can view the tools declared by each MCP server. |
| Delete | An administrator can delete a registered BYO MCP server that's no longer needed. |

**Check result**
- `ext_PocTest` has status **Available** in the organizational registry, and it becomes available to agent-building surfaces after consent is granted.

### 4.6.5 Use the approved server in Copilot Studio
Performed by **developer**.

After approval and consent, the server can take up to 30 minutes to appear in all Copilot Studio environments in the tenant.
1. Go to Copilot Studio (`https://copilotstudio.microsoft.com`) in the test environment.
2. Create a new custom agent, or open the test agent.
3. Go to the **Tools** section and select **MCP Server**.
4. Select `ext_PocTest` from the registry.
5. Test the agent by entering a prompt that invokes one of the server's tools.
6. If you're prompted to complete a one-time connection setup (for example, entering the API key for an `APIKey` server), follow the provided URL to create the connection, return to the agent, and retry the prompt.

**Check result**
- After a successful invocation, the MCP server returns the tool output.

To invoke the approved server from Visual Studio Code, Claude Code, or GitHub Copilot CLI, see [Agent 365 tooling servers overview](https://learn.microsoft.com/microsoft-agent-365/tooling-servers-overview#extend-your-agents-with-available-or-custom-mcp-servers).

### 4.6.6 Monitor MCP activity in Microsoft Defender
Performed by **Security Reader**.
1. Sign in to the Microsoft Defender portal (`https://security.microsoft.com`).
2. Go to **Advanced hunting**.
3. Run the sample query from Learn, replacing `<tool name>` with a tool exposed by `ext_PocTest`:

   ```kusto
   CloudAppEvents
   | where ActionType in ("ExecuteToolByGateway")
   | where RawEventData contains "<tool name>"
   ```

4. To review all gateway tool invocations for the PoC window:

   ```kusto
   CloudAppEvents
   | where Timestamp > ago(7d)
   | where ActionType == "ExecuteToolByGateway"
   | project Timestamp, ActionType, AccountDisplayName, RawEventData
   | order by Timestamp desc
   ```

**Check result**
- The query returns details including agent name, MCP server name, and invocation metadata for the test prompt from 4.6.5.

## 4.7 Test and validation
**Documentation:** [Manage plugins, skills, and MCP servers](https://learn.microsoft.com/microsoft-365/admin/manage/manage-plugins-skills-mcp-servers) · [Bring your own (BYO) MCP server](https://learn.microsoft.com/microsoft-365/admin/manage/manage-byo-mcp-server) · [Manage Tools Gateway](https://learn.microsoft.com/microsoft-365/admin/manage/manage-tools-gateway)

### 4.7.1 Approved BYO MCP server appears in the registry only after approval
Performed by **developer** and **AI Administrator**.
1. After registration (4.6.2) and before approval (4.6.4), as AI Administrator, open **Agents** > **Tools** > **Requests (preview)** and confirm that the `ext_PocTest` request is listed.
2. As the developer, in Copilot Studio, confirm that `ext_PocTest` isn't yet available to select as an MCP server.
3. As AI Administrator, approve the request and grant consent (4.6.4).
4. Open **Agents** > **Tools** > **Registry** and locate `ext_PocTest`.
5. As the developer, add the server to the test agent and invoke it (4.6.5).

**Expected result**
- Before approval and consent, the server is a request on the **Requests (preview)** tab and isn't available to agent-building surfaces.
- After approval and consent, the server is **Available** in the organizational registry, and the test agent's invocation returns the tool output.

### 4.7.2 Blocking the MCP server stops the dependent agent
Performed by **AI Administrator** and **developer**.
1. In Copilot Studio, confirm that the test agent successfully invokes `ext_PocTest`.
2. In the Microsoft 365 admin center, block `ext_PocTest` (4.4.2). If any plugins use the server, you can also block all linked plugins.
3. In Copilot Studio, enter the same prompt in the test agent.
4. Unblock `ext_PocTest`, and then repeat the prompt.

**Expected result**
- While blocked, the server's status is **Blocked**, and runtime enforcement prevents agents from invoking it.
- After unblocking, access to the server is restored and the MCP server returns the tool output again.

### 4.7.3 Plugin restricted to a group triggers Request access
Performed by **AI Administrator**, **standard test user** (member of `A365-PoC-Plugin-Pilot`), and **second test user** (not a member).
1. As AI Administrator, confirm that the plugin from 4.3.2 is set to **Specific users and groups** with `A365-PoC-Plugin-Pilot`.
2. As the standard test user, find the plugin in the Copilot channel.
3. As the second test user, find the same plugin in the Copilot channel, and select **Request access**.
4. As AI Administrator, open **Agents** > **Tools** > **Requests**, select the request, review the user and the requested plugin, and select **Approve** (or **Reject** to test denial).

**Expected result**
- The plugin is available to the standard test user, because it's available to the selected group.
- The second test user can still discover the plugin, which appears as blocked by organizational policy, and can select **Request access**.
- The request is sent to the Microsoft 365 admin center and is listed on the **Requests** tab with the user and the requested plugin.
- **Approve** grants the user access; **Reject** denies the request.

### 4.7.4 (Optional) Organization-level publisher category block
Performed by **AI Administrator** and **second test user**.
1. As AI Administrator, in **Agents** > **Settings** > **Agent and plugin access**, clear **certified external publishers** (4.3.1).
2. As the second test user, find a plugin from a certified external publisher in the Copilot channel.
3. As AI Administrator, restore the publisher categories that you recorded in 4.3.1.

**Expected result**
- The plugin is still discoverable but displays "This plugin is blocked by your organization's policy."

### 4.7.5 (Optional) Tool-level control and gateway discovery
Performed by **Global Administrator** (gateway) and **AI Administrator** (tool-level control).
1. If you connected a gateway (4.5), as Global Administrator, go to **Agents** > **Tools**, filter the list by source, select **AI gateway**, and confirm that the server you noted in 4.5.1 is listed.
2. Register another MCP server in the gateway, and then refresh the Tools page.
3. As AI Administrator, for a server whose **Tools** tab lists its tools, disable one tool and select **Save** (4.4.3).

**Expected result**
- Gateway servers are listed under **AI gateway** without separate per-server consent, and the newly registered server is discovered during a subsequent refresh.
- The disabled tool's toggle is **Disabled**. The policy applies wherever the tool is used and is enforced at runtime by the Agent 365 Tooling Gateway, while the other enabled tools on the same server remain available.

### 4.7.6 MCP invocations are visible in Defender
Performed by **Security Reader**.
1. Run the queries from 4.6.6 for the PoC window.

**Expected result**
- The query returns details including agent name, MCP server name, and invocation metadata for the invocations made in 4.7.1 and 4.7.2.

## 4.8 Evidence
- Screenshot of **Agents** > **Tools** > **Registry** showing the tool categories, with the **Status** and **Publisher** filters applied (4.2.1, 4.2.2).
- Screenshot of a connector's overview page showing the agents that use it (4.2.3).
- Screenshot of **Agents** > **Settings** > **Agent and plugin access** showing the selected publisher categories (4.3.1).
- Screenshot of the restricted plugin's **Users** setting with only `A365-PoC-Plugin-Pilot` selected (4.3.2).
- CLI output of the `register-external-mcp-server` command, with secrets removed (4.6.2).
- The `<server-name>_eval_report.html` evaluation report (4.6.3).
- Screenshot of the `ext_PocTest` request on the **Requests (preview)** tab before approval (4.7.1).
- Screenshot of `ext_PocTest` with status **Available** in the registry, and of the Microsoft Entra consent prompt (4.7.1).
- Screenshots of the Copilot Studio test agent: successful invocation, the invocation attempt while the server is blocked with the server's **Blocked** status, and successful invocation after unblocking, with timestamps (4.7.1, 4.7.2).
- Screenshots of the plugin available to the standard test user, the plugin blocked by organizational policy with **Request access** for the second test user, and the request on the **Requests** tab with its decision (4.7.3).
- (Optional) Screenshot of the "This plugin is blocked by your organization's policy." message (4.7.4).
- (Optional) Screenshot of **Agents** > **Settings** > **Gateways** after connecting the gateway, the registry filtered by source **AI gateway**, and an MCP server's **Tools** tab with a disabled tool (4.7.5).
- Advanced hunting query results exported to CSV (4.7.6).

## 4.9 Troubleshooting
| Symptom | Likely cause | Fix |
|---|---|---|
| Reviewer can't approve an MCP server request or the consent step fails | The account can't grant tenant-wide consent | Use AI Administrator or Global Administrator. |
| Registration fails because the server name is rejected | Name doesn't start with `ext_` or is longer than 20 characters | Use a name such as `ext_PocTest`. |
| Registration fails partway and a retry fails | Microsoft Entra app registrations created by the failed run aren't automatically rolled back | Delete them manually in the Azure portal, and then retry. |
| The Agent 365 service principal can't be found in the tenant | The service principal associated with app ID `ea9ffc3e-8a23-4a7d-836d-234d7c7565c1` isn't provisioned | Have a Global Administrator run `New-Agent365ToolsServicePrincipalProdPublic.ps1` (4.6.1). |
| Registration targets the wrong tenant | `--tenant-id` defaults to the current `az login` tenant | Pass `--tenant-id` with the PoC tenant ID. |
| Approved server isn't listed in Copilot Studio | Consent not granted, or the server hasn't yet appeared in all environments | Confirm consent was granted; after approval and consent, the server can take up to 30 minutes to appear in all Copilot Studio environments. |
| Tool invocations fail at runtime after approval | Tool names in the registration don't exactly match the names exposed by the remote MCP server | Register tool names that exactly match the names exposed by the server. You can't republish new versions of a remote MCP server during preview. |
| First invocation of an `APIKey` server prompts for setup | One-time connection setup is required | Follow the provided URL to create the connection, enter the API key, return to the agent, and retry the prompt. |
| An agent identity can't call the BYO server | Agent identities are missing the `Tools.ListInvoke.All` permission for the server | A Global Administrator runs `a365 develop-mcp grant-agents-access --mcp-server-name <NAME> --agent-blueprint-id <GUID>` (use `--dry-run` to report without granting). The command isn't available in Agent 365 CLI 1.1.221; update the CLI (`dotnet tool update --global Microsoft.Agents.A365.DevTools.Cli`) and confirm it appears in `a365 develop-mcp -h`. |
| `evaluate` returns `Unauthorized` from `tools/list` | Wrong or expired bearer token | Reacquire the token and pass it through `A365_MCP_AUTH_TOKEN`. |
| `evaluate` stops after step `[2/5]` | No coding agent on `PATH` | Install GitHub Copilot CLI or Claude Code, or score the checklist yourself and rerun. |
| `evaluate` reports `Unknown eval engine` | Invalid `--eval-engine` value | Use `auto`, `github-copilot`, `claude-code`, or `none`. |
| `evaluate` reports `Failed to read existing checklist` | The checklist file is locked or malformed | Delete the checklist file to force a fresh discovery on the next run. |
| No servers appear under source **AI gateway** | Discovery not yet complete, or the servers aren't registered in the connected gateway | Refresh the Tools page and allow more time. Only MCP servers registered in the connected gateway are discovered. |
| **Tools** tab shows that the server doesn't support tool discovery | Individual tools aren't available to manage for this server | Block or allow the whole server (4.4.2). |
| Blocking a server affected plugins and connectors | Blocking an MCP server also blocks dependent plugins and linked connectors | Select the server to view the plugins that use it before blocking; unblock to restore access. |
| Allow or block options for tooling and MCP servers aren't available | The capability might not be available in your region yet | See [Agent 365 tooling servers overview](https://learn.microsoft.com/microsoft-agent-365/tooling-servers-overview). |

## 4.10 Cleanup
- As the developer, remove `ext_PocTest` from the Copilot Studio test agent, or delete the test agent if you created it for this chapter.
- As AI Administrator, delete the BYO test server: **Agents** > **Tools** > **Registry** > select `ext_PocTest` > **Delete** > confirm **Delete**. Deleting removes it from the registry, and agents can no longer invoke it.
- As AI Administrator, restore the restricted plugin's **Users** setting, and restore the publisher categories that you recorded in 4.3.1.
- As AI Administrator, unblock, uninstall, or delete any test plugins or skills that you blocked, installed, or uploaded in 4.3.
- As AI Administrator, re-enable any tools that you disabled on an MCP server's **Tools** tab (4.4.3, 4.7.5).
- (Optional) Remove the MCP server that you registered in the gateway for 4.7.5 by using the gateway's own management tools.
- As the developer, delete `ext-poctest.json` and the local evaluation output files (`<server-name>_checklist.json`, `<server-name>_eval_report.html`, `<server-name>_eval_report.json`) from the output directory, and clear `A365_MCP_AUTH_TOKEN` from the shell.
- When the PoC ends, remove the role assignments granted for this chapter.

---
Previous: [Chapter 3 – Agent Identity and Ownership](../chapter-03-identity-ownership/README.md) · Next: [Chapter 5 – Agent Lifecycle and Audit](../chapter-05-lifecycle-audit/README.md)
