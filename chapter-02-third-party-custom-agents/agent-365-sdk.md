# Chapter 2 - Agent 365 SDK

**Pillar:** Observe
**What it proves:** Custom agents are registered through the Agent 365 CLI with a Microsoft Entra agent identity blueprint and agent identity, then deployed and published for governance.

For no-code discovery from supported third-party platforms, use [Connected platforms](README.md). A platform connection isn't required for this SDK path.

**Success criteria:** Agree the selected outcomes in [What you proved](#-what-you-proved) before testing.

## Topics and time guide

Approximate hands-on estimates for the selected scope, with [prerequisites](prerequisites.md) prepared. Service waiting time is separate.

| Topic | Estimated hands-on time |
|---|---|
| [2.1 Required permissions](#21-required-permissions) | ~5 min |
| [2.7 Prepare the custom-agent toolchain](#27-prepare-the-custom-agent-toolchain) | ~15-20 min |
| [2.8 Create the agent blueprint with a365 setup](#28-create-the-agent-blueprint-with-a365-setup) | ~15-20 min |
| [2.9 Deploy the agent runtime to Azure (optional)](#29-deploy-the-agent-runtime-to-azure-optional) | ~15-25 min |
| [2.10 Publish the agent and verify it in the registry](#210-publish-the-agent-and-verify-it-in-the-registry) | ~10-15 min |
| [2.11 Add observability and data protection (optional)](#211-add-observability-and-data-protection-optional) | ~20-40 min |
| [2.12 Test and validation](#212-test-and-validation) | ~15-20 min |
| [2.13 Evidence](#213-evidence) | ~5-10 min |
| [2.14 Troubleshooting](#214-troubleshooting) | As needed |

[Outcome checklist](#-what-you-proved) · [References](#references)

---

## 2.1 Required permissions

Use the [shared account and role-assignment model](../README.md#least-privilege-model) with the task-specific permissions below.

| Task | Least-privilege role | Section |
|---|---|---|
| Configure API permissions and consent on a tenant-owned **Agent 365 CLI** client app (only when the Microsoft-managed app isn't available) | Application Administrator (or Cloud Application Administrator) | 2.7.3 |
| Run `a365 setup all` (blueprint, inheritable permissions, agent identity, agent registration) and `a365 setup blueprint` (messaging endpoint) | Agent ID Developer plus Contributor on the Azure subscription | 2.8, 2.9.4 |
| Grant OAuth2 permissions (admin consent) for the blueprint; run `a365 setup permissions` subcommands | Global Administrator | 2.8.4, 2.8.6 |
| Grant service-to-service (S2S) agent identity grants (`--authmode s2s` or `both`) | Application Administrator or Global Administrator | 2.8.2 |
| Deploy the agent code to Azure | Contributor on the Azure subscription | 2.9 |
| Upload the published `manifest.zip` in the Microsoft 365 admin center | Global Administrator | 2.10.2 |
| Validation / read-only review | AI Reader (registry); any Microsoft Entra user (agent identities and blueprints lists); Directory Readers (`a365 query-entra`); **Security operations** > **Security data** > **Security data basics (read)** in Defender unified RBAC (advanced hunting) | 2.8.5, 2.12 |

- Agent ID Developer and Agent ID Administrator can complete every `a365 setup all` step except the OAuth2 permission grants (admin consent), which require a Global Administrator. When setup completes, the CLI prints the next steps for the Global Administrator (2.8.4).

**Before you start:**
- [ ] Confirm the [shared tenant checks](prerequisites.md#tenant-readiness) and the [Agent 365 SDK preparation](prerequisites.md#agent-365-sdk-preparation).

---

## 2.7 Prepare the custom-agent toolchain
**Documentation:** [Install and use the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-cli) · [Agent 365 Skills for guided agent setup](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-skills) · [Quickstart: Connect an existing agent to Agent 365](https://learn.microsoft.com/microsoft-agent-365/developer/get-started) · [Custom client app registration for Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/custom-client-app-registration) · [Onboard a single agent with the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/admin/agent-365-onboarding-cli)

### 2.7.1 Understand the custom-agent journey

A custom agent goes through three stages:

1. **Blueprint (2.8):** The agent blueprint defines the agent's identity, permissions, and infrastructure requirements. Every agent instance is created from it. `a365 setup all` creates the blueprint in Microsoft Entra, configures permissions (including inheritable permissions for agent instances), creates an agent identity, and registers the agent.
2. **Deploy (2.9, optional):** You deploy the agent code to the cloud. You can skip this step if the agent is already deployed to a cloud; it doesn't need to be Azure.
3. **Publish (2.10):** `a365 publish` packages the agent, and you upload the package to the Microsoft 365 admin center. After publishing, you can create agent instances and govern the agent.

The Agent 365 SDK isn't an alternative to your agent framework. Build the agent with your framework first (for example, the Microsoft 365 Agents SDK, as in [`samples/sdk/`](samples/sdk/README.md)), then bring it into Agent 365.

### 2.7.2 Install the Agent 365 CLI and sign in to Azure

Performed by the **developer**.

1. Install .NET 8.0 or later and the Azure CLI.
2. Install the Agent 365 CLI as a global .NET tool, or update it if it's already installed:

   ```powershell
   dotnet tool install --global Microsoft.Agents.A365.DevTools.Cli
   # If the CLI is already installed:
   dotnet tool update --global Microsoft.Agents.A365.DevTools.Cli
   ```

3. Verify the installation:

   ```powershell
   a365 --version
   ```

4. Sign in to Azure with the account that holds the roles in 2.1, and select the subscription in the tenant where you onboard the agent. The CLI detects the tenant from the active Azure CLI account, and setup fails with authentication errors if you aren't signed in:

   ```azurecli
   az login
   az account list --output table
   az account set --subscription "<subscription-id-or-name>"
   az account show --query "{tenantId:tenantId, subscriptionId:id, subscriptionName:name}" --output table
   ```

**Check result**
- `a365 --version` returns a version, and `az account show` returns the PoC tenant and subscription.

### 2.7.3 Confirm the CLI client application

By default, Agent 365 setup uses the Microsoft-managed **Agent 365 CLI** enterprise application (application ID `f54280f4-395e-4ea8-9e48-bf2d4952aa14`) when it's available in your tenant. On native Windows it uses Web Account Manager (WAM); on Windows Subsystem for Linux, macOS, and Linux it uses device code. Security Defaults or a Conditional Access policy can block device code authentication and return `AADSTS530035`.

1. Open the Microsoft Entra admin center at https://entra.microsoft.com.
2. Select **Enterprise applications** > **All applications** and search for the application ID `f54280f4-395e-4ea8-9e48-bf2d4952aa14`.
3. If the application is present, continue with 2.8. Don't modify the Microsoft-managed application.
4. If it isn't present, config-free setup looks for a tenant-owned app named **Agent 365 CLI**. Create it by following [Custom client app registration for Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/custom-client-app-registration). Configuring its API permissions requires **Application Administrator** (recommended), **Cloud Application Administrator**, or **Global Administrator**. A Global Administrator can also create it from the `a365 setup requirements` prompt (2.8.1).

**Check result**
- Either the Microsoft-managed **Agent 365 CLI** enterprise application or a tenant-owned app named **Agent 365 CLI** exists in the tenant.

### 2.7.4 (Optional) Use the Agent 365 Skills in a coding assistant

Agent 365 Skills run in Claude Code, GitHub Copilot CLI, and VS Code agent mode. You state the outcome you want (for example, *set up this project for Agent 365* or *register this agent with Agent 365*), and the skill identifies the project, gathers the required values, makes the integration changes, and checks the result. `a365-setup` is the entry point and routes to `make-a365-agent` (standard agent) or `make-ai-teammate` (AI teammate, Frontier preview program only).

Installation options and the skill catalog are in [`samples/sdk/README.md`](samples/sdk/README.md#use-the-agent-365-skills). The rest of this chapter shows the equivalent CLI commands.

---

## 2.8 Create the agent blueprint with a365 setup
**Documentation:** [Set up agent blueprint](https://learn.microsoft.com/microsoft-agent-365/developer/registration) · [Agent 365 CLI setup command reference](https://learn.microsoft.com/microsoft-agent-365/developer/reference/cli/setup) · [Onboard a single agent with the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/admin/agent-365-onboarding-cli) · [Agent 365 CLI query-entra command reference](https://learn.microsoft.com/microsoft-agent-365/developer/reference/cli/query-entra) · [View and filter agent identities](https://learn.microsoft.com/entra/agent-id/agent-lists) · [View and manage agent identity blueprints](https://learn.microsoft.com/entra/agent-id/manage-agent-blueprint)

### 2.8.1 Validate the prerequisites

Performed by **Agent ID Developer** (with Contributor on the Azure subscription).

1. Run the requirements check from any directory:

   ```powershell
   a365 setup requirements
   ```

2. Resolve every failed required check. The command checks authentication, Azure access, tenant enrollment, roles, and the client application, and continues after a failed check so you can review all detected issues together.
3. If neither the Microsoft-managed application nor a tenant-owned app named **Agent 365 CLI** is available, the command prompts for a custom client app ID. A Global Administrator can enter `C` at the prompt to create and configure a tenant-owned app.

**Check result**
- All required checks pass.

### 2.8.2 Choose the setup variant

| Scenario | Command | Notes |
|---|---|---|
| Agent, with `a365.config.json` | `a365 setup all` | Creates Azure infrastructure if it doesn't already exist (resource group, App Service plan, Azure Web App with managed identity enabled), registers the agent blueprint, configures API permissions, and saves generated IDs to `a365.generated.config.json`. |
| Agent, config-free | `a365 setup all --agent-name "<name>"` | No config file needed. The tenant ID is detected from `az account show` (override with `--tenant-id`). Display names are derived as `<name> Agent` (identity) and `<name> Blueprint` (blueprint). Infrastructure is always skipped (external hosting assumed). |
| Microsoft 365 agent (Teams, Copilot) | `a365 setup all --m365` (optionally `--messaging-endpoint <url>`) | Registers the messaging endpoint. If the endpoint is deferred, register it after deployment (2.9.4). |
| AI teammate (Frontier preview program only) | `a365 setup all --aiteammate` | Requires a manually created `a365.config.json`. Not used in this PoC. |
| Agent identity grants | `--authmode obo` (default), `s2s`, or `both` | `obo` creates principal-scoped delegated grants and needs no admin role. `s2s` creates app role assignments and requires Application Administrator or Global Administrator; if the role is absent, the CLI prints a PowerShell fallback. Not supported with `--aiteammate`. |
| Preview | add `--dry-run` | Shows what the command would do without executing it. |

For this PoC, use a config-free standard agent with the default `obo` mode and a test base name, for example `PoC Custom`.

### 2.8.3 Run the setup

Performed by **Agent ID Developer** (with Contributor on the Azure subscription), or by **Global Administrator** to complete all steps in one run.

1. Create an empty working directory and change to it:

   ```powershell
   New-Item -ItemType Directory -Path .\poc-custom-agent
   Set-Location .\poc-custom-agent
   ```

2. Preview the changes without creating tenant objects:

   ```powershell
   a365 setup all `
       --agent-name "PoC Custom" `
       --aiteammate false `
       --dry-run
   ```

3. Review the tenant ID, derived object names, selected client application, permissions, and authentication mode.
4. Run the same command without `--dry-run`:

   ```powershell
   a365 setup all `
       --agent-name "PoC Custom" `
       --aiteammate false
   ```

5. If you sign in as Global Administrator, complete any consent prompt that opens during setup. If you use the Agent ID Developer role, no browser window appears; the CLI completes the steps allowed by your role and prints the consent actions for a Global Administrator (2.8.4).

The blueprint agent flow runs these steps in sequence: requirements validation, blueprint creation, batch permissions (Microsoft Graph, Agent 365 Tools, Messaging Bot API, Power Platform, and any custom resources), agent identity creation, agent registration, and config sync. The CLI sets `managerApplications` on the blueprint, which is required for platform manageability. Setup typically takes 3 to 5 minutes.

**Check result**
- The setup summary shows each required step as completed, or lists the consent actions for a Global Administrator.

### 2.8.4 Complete the OAuth2 grants (Agent ID Developer path)

When you run `a365 setup all` without Global Administrator, the CLI completes all steps it can (blueprint creation and inheritable permissions), generates per-resource admin consent URLs and saves them to `a365.generated.config.json`, and displays the next steps for a Global Administrator.

| Step | Who | Action |
|---|---|---|
| 1 | **Agent ID Developer** | Run `a365 setup all`. The CLI prints the next steps, including a consent URL for a Global Administrator to open. |
| 2 | **Agent ID Developer** | Share the consent URL from the CLI output with the Global Administrator. |
| 3 | **Global Administrator** | Open the consent URL in a browser signed in as Global Administrator and grant the requested permissions. |

**Check result**
- The Global Administrator completed every consent URL printed by the CLI.

### 2.8.5 Verify the blueprint and agent identity

Performed by the **developer** (configuration file), **Directory Readers** (`a365 query-entra`), and any Microsoft Entra user (agent identities and blueprints lists).

1. Inspect the generated configuration:

   ```powershell
   Get-Content .\a365.generated.config.json | ConvertFrom-Json
   ```

   Confirm that `agentBlueprintId` and `agentBlueprintObjectId` are populated, `completed` is `true`, and `resourceConsents` contains resources such as Microsoft Graph, Agent 365 Tools, and Messaging Bot API. If you ran setup as Agent ID Administrator or Agent ID Developer, `resourceConsents` might be empty and `completed` might be `false` until a Global Administrator completes the OAuth2 permission grants.

2. Check the blueprint's permissions and inheritance:

   ```powershell
   a365 query-entra blueprint-scopes --agent-name "PoC Custom"
   a365 query-entra inheritance --agent-name "PoC Custom"
   ```

   `blueprint-scopes` shows the delegated scopes and app role assignments granted on the blueprint service principal (the same as the **API permissions** blade). `inheritance` reports `Effective inheritance: OK` when agent identities created from the blueprint will inherit permissions for a resource. `NONE` means no grants exist on the blueprint service principal (run `a365 setup permissions` as Global Administrator); `BROKEN` means the entry doesn't use `allAllowed` (run `a365 setup permissions` to reconcile).

   `a365 setup` configures every inheritable permission entry with `allAllowed` for both scopes and roles. What agent identities actually inherit is limited to the permissions granted on the blueprint service principal, so review `blueprint-scopes` before you grant more. Inheritable permissions on blueprints are described in [3.6 Configure inheritable permissions on a blueprint](../chapter-03-identity-ownership/README.md#36-configure-inheritable-permissions-on-a-blueprint-optional).

3. In the Microsoft Entra admin center (https://entra.microsoft.com), search for your `agentBlueprintId` or the agent name. Verify that the App Registration and Enterprise Application appear, that the **API permissions** tab of the blueprint app registration shows all permissions, and that the status shows **Granted for <your tenant>**.
4. Browse to **Entra ID** > **Agents** > **Agent blueprints**, add the **Blueprint App ID** filter with the `agentBlueprintId`, open the blueprint, and select **Linked agent identities**.
5. Browse to **Entra ID** > **Agents** > **Agent identities**, add the **Blueprint App ID** filter with the `agentBlueprintId`, and confirm that the agent identity is listed. Assign owners and sponsors as described in [Chapter 3 – Agent identity and ownership](../chapter-03-identity-ownership/README.md).

Blueprints must have `managerApplications` set to be accepted by the platform. The CLI sets this automatically. If you have an existing blueprint created before this requirement was introduced, delete it and run `a365 setup all` again, or patch it via the Graph API.

Save both `a365.config.json` (if used) and `a365.generated.config.json`; you need these values for deployment and troubleshooting.

**Check result**
- The blueprint and the agent identity exist in Microsoft Entra with the same Blueprint App ID, and all permissions show **Granted for <your tenant>**.

### 2.8.6 (Optional) Apply custom permissions to the blueprint

Performed by **Global Administrator**.

1. Apply the additional scopes the agent needs inline, for example Microsoft Graph delegated scopes:

   ```powershell
   a365 setup permissions custom `
     --agent-name "PoC Custom" `
     --resource-app-id 00000003-0000-0000-c000-000000000000 `
     --scopes Mail.Read,Mail.Send,Chat.Read,Chat.ReadWrite,Chat.Create,User.Read
   ```

2. Run `a365 query-entra blueprint-scopes --agent-name "PoC Custom"` and confirm the new scopes.

The command configures OAuth2 delegated permission grants with admin consent, sets inheritable permissions, and reconciles Microsoft Entra with the configuration (it adds new permissions and removes any permissions that you deleted from the config).

**Check result**
- The new scopes appear in the `blueprint-scopes` output.

---

## 2.9 Deploy the agent runtime to Azure (optional)
**Documentation:** [Deploy agent to Azure](https://learn.microsoft.com/microsoft-agent-365/developer/deploy-agent-azure) · [Use agent code deployed in Amazon Web Services](https://learn.microsoft.com/microsoft-agent-365/developer/deploy-agent-aws) · [Use agent code deployed in Google Cloud Platform](https://learn.microsoft.com/microsoft-agent-365/developer/deploy-agent-gcp)

Skip this section if the agent is already deployed to a cloud. If it's deployed to Amazon Web Services or Google Cloud Platform, follow the corresponding article to update the messaging endpoint.

### 2.9.1 Prepare the deployment

Performed by the **developer**.

Confirm that you have:
- An Azure subscription with contributor access.
- An Azure Web App to deploy to. `a365 setup all` with an `a365.config.json` file creates the resource group, App Service plan, and Web App if they don't already exist (2.8.2). Config-free setup (`--agent-name`) doesn't create Azure hosting resources.
- Working agent code with a valid and reachable messaging endpoint, tested locally (and optionally tested with Microsoft 365 using Dev Tunnels).
- A valid agent blueprint from 2.8.
- Up-to-date configuration files `a365.config.json` (if used), `a365.generated.config.json`, and the config file in the code (for example, `.env`).
- The Azure CLI installed and authenticated.

### 2.9.2 Deploy the code and store secrets safely

Performed by the **developer** (Contributor on the Azure subscription).

1. Build the project. Example for .NET:

   ```powershell
   dotnet publish -c Release -o ./publish
   ```

2. Deploy to the Azure Web App:

   ```powershell
   az webapp deploy --name <your-web-app> --resource-group <your-resource-group> --src-path ./publish
   ```

   You can also use the Azure portal or the Azure Web Apps Deploy action for GitHub Actions.

3. Store environment variables, including API keys and secrets, as Azure App Settings rather than in code or configuration files. For production environments, use Azure Key Vault for sensitive secrets. Never commit `.env` files with sensitive information to source control.

### 2.9.3 Verify the deployment

Performed by the **developer**.

| Check | How to verify |
|---|---|
| Deployment command completed without errors | Azure portal > your web app > **Deployment** > **Deployment Center** > logs for your latest deployment |
| Web app is running | `az webapp show --name <your-web-app> --resource-group <your-resource-group> --query state` returns `Running` |
| Application logs show successful startup | Azure portal > your web app > **Overview** > **Logs** > **Log Stream**, or `az webapp log tail --name <your-web-app> --resource-group <your-resource-group>` |
| Environment variables are configured | Azure portal > your web app > **Settings** > **Environment Variables** |
| Messaging endpoint responds | Test the endpoint shown on the web app **Overview** page |

**Check result**
- All five checks pass.

### 2.9.4 Register or update the messaging endpoint (Microsoft 365 agents)

Performed by **Agent ID Developer**. Needed only when the messaging endpoint was deferred during `a365 setup all --m365`, or when it changes.

1. Register the messaging endpoint for the existing blueprint:

   ```powershell
   a365 setup blueprint --agent-name "PoC Custom" --endpoint-only `
     --messaging-endpoint https://your-app.azurewebsites.net/api/messages
   ```

2. To delete the existing messaging endpoint and register a new one instead, run `a365 setup blueprint --agent-name "PoC Custom" --update-endpoint <url>`.

---

## 2.10 Publish the agent and verify it in the registry
**Documentation:** [Publish agent to Microsoft admin center](https://learn.microsoft.com/microsoft-agent-365/developer/publish) · [Agent 365 CLI publish command reference](https://learn.microsoft.com/microsoft-agent-365/developer/reference/cli/publish) · [Upload Microsoft Copilot custom agents](https://learn.microsoft.com/microsoft-365/copilot/agent-essentials/agent-lifecycle/agent-upload-agents)

### 2.10.1 Package the agent with a365 publish

Performed by the **developer**.

1. Confirm that the agent blueprint exists (2.8), the agent was tested locally, and `a365.config.json` (if used) and `a365.generated.config.json` are up to date. For agents provisioned with `--agent-name`, make sure `a365.generated.config.json` exists in your working directory, because the command reads the blueprint ID from this file.
2. Run the publish command (`a365 publish -h` shows all options):

   ```powershell
   a365 publish
   ```

   The command updates `manifest.json` with your agent blueprint ID, packages `manifest.json` and icons into `manifest.zip`, and displays step-by-step instructions for uploading via the Microsoft 365 admin center.

3. Confirm that the manifest folder and files exist:

   ```powershell
   Test-Path <deploymentProjectPath>/manifest/
   Test-Path <deploymentProjectPath>/manifest/manifest.json
   Test-Path <deploymentProjectPath>/manifest/manifest.zip
   # All should return: True
   ```

**Check result**
- The CLI shows `Manifest updated successfully` and `manifest.zip created successfully`, and prints the upload instructions.

### 2.10.2 Upload the package in the Microsoft 365 admin center

Performed by **Global Administrator**.

1. Open the Microsoft 365 admin center at https://admin.cloud.microsoft.
2. Navigate to **Agents** > **All agents**.
3. Select **Upload custom agent**.
4. Select **Choose File** and select the `manifest.zip` file from the `manifest` folder in your project. The ZIP file is validated.
5. Verify the agent's name, icon, and host products. Then select **Next**.
6. Select the assigned users. For testing, you can select a small audience, for example **Just me** or a single test group. Then select **Next**.
7. Review the agent's permissions and capabilities. Then select **Next**.
8. Select **Finish deployment**.

**Check result**
- The deployment finishes without validation errors.

### 2.10.3 Verify the custom agent in the registry

Performed by **AI Reader**.

1. After uploading, allow 5 to 10 minutes for the agent to appear in the Microsoft 365 admin center and Teams.
2. Go to **Agents** > **All agents** and confirm that your agent appears in the list.
3. Check **Name** (from `manifest.json`), **Version**, **Publisher** (your organization name), and **Availability**.
4. In **Agents** > **All agents**, find the agent identity that `a365 setup all` registered (**PoC Custom Agent**), open it, and confirm that its identity and registration details match `a365.generated.config.json`.

**Check result**
- The custom agent is listed with the expected name, version, publisher, and availability, and its identity details match the generated configuration.

---

## 2.11 Add observability and data protection (optional)
**Documentation:** [Microsoft OpenTelemetry Distro](https://learn.microsoft.com/microsoft-agent-365/developer/microsoft-opentelemetry) · [Agent 365 observability data model and concepts](https://learn.microsoft.com/microsoft-agent-365/developer/observability-concepts) · [Quickstart: Connect an existing agent to Agent 365](https://learn.microsoft.com/microsoft-agent-365/developer/get-started)

### 2.11.1 Instrument the agent for observability

Performed by the **developer**.

1. Add observability with one of these options:
   - In a coding assistant with the Agent 365 Skills installed, ask *add observability to this agent* (`instrument-observability`). When prompted, choose the authentication mode your agent uses: OBO, Agentic-User (Frontier preview program), or S2S.
   - Or install the Microsoft OpenTelemetry Distro and enable the Agent 365 exporter as described in the article: `pip install microsoft-opentelemetry` (Python), `npm install @microsoft/opentelemetry` (Node.js), or `dotnet add package Microsoft.OpenTelemetry` (.NET).
2. For blueprint agents, use S2S with an app-only token resolver. By default, the distro exports on the delegated route, which needs the delegated `Agent365.Observability.OtelWrite` permission and admin consent; `a365 setup all` doesn't configure that permission for blueprint agents. A registered agent instance can export on the S2S route without an Observability permission or admin consent.
3. Make sure each run has a valid `invoke_agent` span at its root. The Microsoft 365 admin center, Microsoft Defender agent-activity views, and Microsoft Purview depend on it. A run with only `chat`, `execute_tool`, or `output_messages` spans is queryable only in Defender advanced hunting (`CloudAppEvents`).
4. Redeploy the agent (2.9) and send test requests.

**Check result**
- Test runs appear in Defender advanced hunting (tested in 2.12.6).

### 2.11.2 Add the Purview DLP guard

Performed by the **developer**.

1. In a coding assistant with the Agent 365 Skills installed, ask *add Purview DLP to this agent* (`purview-dlp-integration`). The skill adds Microsoft Graph `processContent` checks that block prompts before they reach the LLM when an input-blocking policy matches, and guides permission and DLP policy setup. Optional response checks audit responses but don't filter sensitive output. By default, errors and timeouts stop the turn.
2. The skill supports agentic delegated authentication and Node.js S2S with client-secret FMI authentication. For .NET, verify the best-effort guard against your SDK version.
3. Configure the DLP policy and permissions as described in the skill's documentation: [`purview-dlp-integration`](https://github.com/microsoft/agent365-skills/tree/main/plugins/agent365/skills/purview-dlp-integration) and [processContent API](https://learn.microsoft.com/graph/api/userdatasecurityandgovernance-processcontent).

**Check result**
- The guard is added to the agent project and the DLP policy is configured.

---

## 2.12 Test and validation

### 2.12.5 Test: the custom agent appears with its blueprint and agent identity

Performed by the **developer** (configuration file), **AI Reader**, any Microsoft Entra user, and **Directory Readers**.

1. Open `a365.generated.config.json` and confirm that `completed` is `true` and note the `agentBlueprintId`.
2. In the Microsoft 365 admin center, open **Agents** > **All agents** and find **PoC Custom Agent** and the published agent (2.10.3).
3. In the Microsoft Entra admin center, browse to **Entra ID** > **Agents** > **Agent identities**, add the **Blueprint App ID** filter with the `agentBlueprintId`, and confirm that the agent identity is listed.
4. Browse to **Entra ID** > **Agents** > **Agent blueprints**, open the blueprint, and confirm that **Linked agent identities** lists the agent identity.
5. Run `a365 query-entra inheritance --agent-name "PoC Custom"` and confirm `Effective inheritance: OK` for each resource the agent uses. A resource shows `NONE` until permissions for it are granted on the blueprint service principal (2.8.4, 2.8.6).

**Expected result**
- `completed` is `true`, the custom agent and the published agent are listed in the Microsoft 365 admin center, and the agent identity is linked to the PoC blueprint with the same Blueprint App ID.

### 2.12.6 Test: custom agent activity is observable

Performed by the **developer** (send requests) and a user with **Security data basics (read)** (review). Requires 2.11.1 and the Microsoft 365 connector in Microsoft Defender ([Connect the Microsoft 365 connector](../chapter-08-threat-detection/prerequisites.md#connect-the-microsoft-365-connector)). Without the connector, `CloudAppEvents` returns no rows.

1. Send a few requests to the custom agent.
2. In the Microsoft Defender portal (https://security.microsoft.com), open [advanced hunting](https://learn.microsoft.com/defender-xdr/advanced-hunting-overview) and run:

   ```kql
   CloudAppEvents
   | where Timestamp > ago(1d)
   | where ActionType in ("InvokeAgent", "InferenceCall", "ExecuteToolBySDK", "ExecuteToolByGateway", "ExecuteToolByMCPServer")
   | project Timestamp, ActionType, AccountDisplayName, RawEventData
   | order by Timestamp desc
   ```

3. Confirm that `InvokeAgent` rows exist for the test runs. The per-span fields are inside `RawEventData`.

**Expected result**
- Each test run produces an `InvokeAgent` event.

---

## 2.13 Evidence

- `a365 setup all` summary output and a copy of `a365.generated.config.json` with the client secret and consent URLs removed.
- Output of `a365 query-entra blueprint-scopes` and `a365 query-entra inheritance`.
- Screenshots of the blueprint and the agent identity in the Microsoft Entra admin center with the matching Blueprint App ID.
- (If deployed) Output of `az webapp show ... --query state`.
- `a365 publish` output and a screenshot of the custom agent in **Agents** > **All agents** (name, version, publisher, availability).
- (Optional) Advanced hunting results for the custom agent's `InvokeAgent` events.

---

## 2.14 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `a365 setup` reports insufficient permissions | Missing Agent ID Developer (or Global Administrator) role, or missing Azure subscription contributor or owner access | Assign the roles, sign in again, and rerun the requirements check. |
| Microsoft-managed **Agent 365 CLI** application isn't available | Staged rollout hasn't reached the tenant | Update the CLI and run `a365 setup requirements` again, or use a tenant-owned app named **Agent 365 CLI**. |
| Device code authentication is blocked (`AADSTS530035`) | Security Defaults or Conditional Access block device code on WSL, macOS, or Linux | Don't disable the security policy. Run the CLI on native Windows to use WAM, or work with your identity administrator to use a tenant-owned custom application. |
| Authentication fails with `AADSTS70007` | Older CLI version | Run `dotnet tool update --global Microsoft.Agents.A365.DevTools.Cli` and retry. |
| Setup completes but lists outstanding consent actions | OAuth2 grants require a Global Administrator | Have a Global Administrator open every consent URL printed by the CLI and grant the requested permissions. |
| `a365 query-entra inheritance` reports `Effective inheritance: NONE` | No grants on the blueprint service principal; most commonly a missing `wids` optional claim on the client app | Run `a365 setup requirements` to detect and repair the claim, then run `a365 setup permissions` as Global Administrator. |
| The blueprint or identity exists, but the agent isn't in **All agents** | Agent registration failure | Review the setup summary, resolve the error, then run `a365 setup all --agent-name "PoC Custom" --agent-registration-only`. |
| An existing blueprint isn't accepted by the platform | Blueprint created before `managerApplications` was required | Delete it and run `a365 setup all` again, or patch it via the Graph API. |
| `a365 publish` reports `Agent blueprint ID not found` | Blueprint setup isn't complete | Run `a365 setup` to complete blueprint setup. |
| `a365 publish` reports `Permissions missing` | Blueprint permissions not configured | Rerun setup with the `a365 setup permissions` command. |
| Upload fails in the admin center | Insufficient permissions, or an invalid or outdated `manifest.zip` | Use the Global Administrator role, run `a365 publish` again to generate a fresh `manifest.zip`, and upload again. |
| Web app is running but `/api/messages` returns 404 | Route or endpoint handler not registered, or wrong entry point | Verify the route configuration and endpoint handler in the agent code and the entry point in the deployment. |
| App crashes on startup | Missing dependencies, missing environment variables, runtime version mismatch, or code errors | Check `az webapp log tail`, list and set app settings with `az webapp config appsettings list` and `az webapp config appsettings set`, then redeploy. |
| No custom-agent telemetry appears | No valid `invoke_agent` span at the root of the run, or an authentication mode that doesn't match the environment | Confirm that the run emits a root `invoke_agent` span and that the selected authentication mode matches your environment. Ask your coding assistant to *validate this Agent 365 integration*. |
| `CloudAppEvents` returns no rows at all | The Microsoft 365 connector isn't connected in Microsoft Defender | Connect it as described in [Connect the Microsoft 365 connector](../chapter-08-threat-detection/prerequisites.md#connect-the-microsoft-365-connector), then run the agent again. |

---

## ✅ What you proved

- [ ] For the custom test agent, `a365.generated.config.json` shows `completed: true`, and the agent identity blueprint and agent identity exist in Microsoft Entra with the same blueprint app ID.
- [ ] The custom test agent appears in **Agents** > **All agents** after registration, and the published package appears with the expected name, version, and publisher.
- [ ] (Optional) Test runs of the instrumented custom agent appear in Microsoft Defender advanced hunting (`CloudAppEvents`).

---

## References

- [Install and use the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-cli)
- [Agent 365 Skills for guided agent setup](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-skills)
- [Quickstart: Connect an existing agent to Agent 365](https://learn.microsoft.com/microsoft-agent-365/developer/get-started)
- [Custom client app registration for Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/custom-client-app-registration)
- [Onboard a single agent with the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/admin/agent-365-onboarding-cli)
- [Set up agent blueprint](https://learn.microsoft.com/microsoft-agent-365/developer/registration)
- [Agent 365 CLI setup command reference](https://learn.microsoft.com/microsoft-agent-365/developer/reference/cli/setup)
- [Agent 365 CLI query-entra command reference](https://learn.microsoft.com/microsoft-agent-365/developer/reference/cli/query-entra)
- [View and filter agent identities](https://learn.microsoft.com/entra/agent-id/agent-lists)
- [View and manage agent identity blueprints](https://learn.microsoft.com/entra/agent-id/manage-agent-blueprint)
- [Deploy agent to Azure](https://learn.microsoft.com/microsoft-agent-365/developer/deploy-agent-azure)
- [Use agent code deployed in Amazon Web Services](https://learn.microsoft.com/microsoft-agent-365/developer/deploy-agent-aws)
- [Use agent code deployed in Google Cloud Platform](https://learn.microsoft.com/microsoft-agent-365/developer/deploy-agent-gcp)
- [Publish agent to Microsoft admin center](https://learn.microsoft.com/microsoft-agent-365/developer/publish)
- [Agent 365 CLI publish command reference](https://learn.microsoft.com/microsoft-agent-365/developer/reference/cli/publish)
- [Upload Microsoft Copilot custom agents](https://learn.microsoft.com/microsoft-365/copilot/agent-essentials/agent-lifecycle/agent-upload-agents)
- [Microsoft OpenTelemetry Distro](https://learn.microsoft.com/microsoft-agent-365/developer/microsoft-opentelemetry)
- [Agent 365 observability data model and concepts](https://learn.microsoft.com/microsoft-agent-365/developer/observability-concepts)
- [processContent API](https://learn.microsoft.com/graph/api/userdatasecurityandgovernance-processcontent)
- [advanced hunting](https://learn.microsoft.com/defender-xdr/advanced-hunting-overview)

### Additional resources

- [`purview-dlp-integration`](https://github.com/microsoft/agent365-skills/tree/main/plugins/agent365/skills/purview-dlp-integration)

---

[Runbook index](../README.md) · [Connected platforms](README.md) · Next: [Chapter 3 – Agent identity and ownership](../chapter-03-identity-ownership/README.md)
