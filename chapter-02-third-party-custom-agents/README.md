# Chapter 2 – Third-Party and Custom Agents

**Pillar:** Observe
**What it proves:** Agents that aren't built with Microsoft's own agent builders still land in the Microsoft 365 agent registry. Agents on supported third-party platforms (for example, Amazon Bedrock) are discovered through **Connected platforms** without code, and custom agents are registered through the Agent 365 CLI with a Microsoft Entra agent identity blueprint and agent identity, then deployed and published for governance.

**Success criteria**
- A connection to at least one supported third-party platform validates, **Sync agents** runs, and the connection shows the expected number of synchronized agents with no synchronization errors.
- Every expected third-party test agent appears in **Agents** > **All agents** > **Registry** with its metadata.
- (Optional, Frontier preview) The **Activity** tab of a synchronized third-party agent shows sessions after the agent runs on the source platform.
- For the custom test agent, `a365.generated.config.json` shows `completed: true`, and the agent identity blueprint and agent identity exist in Microsoft Entra with the same blueprint app ID.
- The custom test agent appears in **Agents** > **All agents** after registration, and the published package appears with the expected name, version, and publisher.
- (Optional) Test runs of the instrumented custom agent appear in Microsoft Defender advanced hunting (`CloudAppEvents`).
- All PoC connections, blueprints, and Azure resources created in this chapter are removed at the end of the PoC.

## 2.1 Required permissions

Grant the read-only roles first; assign setup roles only to the person who makes each change, and assign them as Active (not Eligible) for the PoC window.

| Task | Least-privilege role | Section |
|---|---|---|
| Create, validate, sync, edit, and delete connected-platform connections | AI Administrator | 2.2 to 2.6 |
| Amazon Bedrock: provide the AWS access key ID and secret access key, grant the IAM permissions, configure Bedrock activity | Platform administrator (AWS) | 2.3 |
| Databricks Genie: create the service principal and client secret, grant the permissions required to read the Genie agents in the workspace, rotate or revoke the secret | Platform administrator (Databricks) | 2.4 |
| Google Vertex AI: create the service account and JSON key, grant the Vertex AI permissions and observability roles, configure Google Cloud telemetry | Platform administrator (Google Cloud) | 2.5 |
| Other supported platforms: create source-platform credentials, grant source-platform permissions, enable source telemetry | Platform administrator (source platform) | 2.6 |
| Configure API permissions and consent on a tenant-owned **Agent 365 CLI** client app (only when the Microsoft-managed app isn't available) | Application Administrator (or Cloud Application Administrator) | 2.7.3 |
| Run `a365 setup all` (blueprint, inheritable permissions, agent identity, agent registration) and `a365 setup blueprint` (messaging endpoint) | Agent ID Developer plus Contributor on the Azure subscription | 2.8, 2.9.4 |
| Grant OAuth2 permissions (admin consent) for the blueprint; run `a365 setup permissions` subcommands | Global Administrator | 2.8.4, 2.8.6 |
| Grant service-to-service (S2S) agent identity grants (`--authmode s2s` or `both`) | Application Administrator or Global Administrator | 2.8.2 |
| Deploy the agent code to Azure | Contributor on the Azure subscription | 2.9 |
| Upload the published `manifest.zip` in the Microsoft 365 admin center | Global Administrator | 2.10.2 |
| Delete PoC agents from the registry | AI Administrator | 2.15 |
| Remove blueprints and Azure resources with `a365 cleanup` | Global Administrator plus Contributor on the Azure subscription | 2.15 |
| Validation / read-only review | AI Reader (registry); any Microsoft Entra user (agent identities and blueprints lists); Directory Readers (`a365 query-entra`); **Security operations** > **Security data** > **Security data basics (read)** in Defender unified RBAC (advanced hunting) | 2.8.5, 2.12 |

Notes:
- Agent ID Developer and Agent ID Administrator can complete every `a365 setup all` step except the OAuth2 permission grants (admin consent), which require a Global Administrator. When setup completes, the CLI prints the next steps for the Global Administrator (2.8.4).
- For connected platforms, the AI Administrator creates and manages the connection in the Microsoft 365 admin center; the platform administrator creates the source-platform credentials, grants the required permissions, and enables platform-side telemetry when applicable.

**Before you start:**
- Complete [Chapter 0 – Prerequisites and PoC preparation](../chapter-00-prerequisites/README.md) (test admin and reviewer accounts in 0.4.1, and the Frontier program in 0.3.2 if you test third-party observability).
- Complete [Chapter 1 – Agent Discovery and Inventory](../chapter-01-agent-discovery/README.md) and export the registry before you start, so you can show what this chapter adds.
- For sections 2.2 to 2.6: a non-production account on the source platform with at least one test agent, and a platform administrator.
- For sections 2.7 to 2.11: .NET 8.0 or later, the Azure CLI, an Azure subscription in the same tenant, a test agent project (you can start from the samples in [`samples/sdk/`](samples/sdk/README.md)), and a Global Administrator available to complete consent.
- Never commit `.env` files or other files with sensitive information to source control.

## 2.2 Connect a third-party agent platform
**Documentation:** [Connected platforms in Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms) · [Third-party agent observability (Frontier)](https://learn.microsoft.com/microsoft-agent-365/admin/third-party-agent-observability) · [Choose an Agent 365 integration option](https://learn.microsoft.com/microsoft-agent-365/developer/choose-integration-option)

### 2.2.1 Understand connected platforms

Use the **Connected platforms** page to connect supported third-party agent platforms to Agent 365. After you create a connection, Agent 365 can discover supported agents and add them to the Microsoft 365 agent registry. Synchronization, management, and observability capabilities vary by platform.

Supported platforms, as listed on the Connected platforms page:

| Platform | Supported environment | Agent synchronization | Observability | Configuration guide |
|---|---|---|---|---|
| Amazon Bedrock | Agents Classic and AgentCore | Yes | Yes | [Connect Amazon Bedrock](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-amazon-bedrock) (worked example in 2.3) |
| Google Vertex AI | Vertex AI agents | Yes | Yes | [Connect Google Vertex AI](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-google-vertex-ai) (worked example in 2.5) |
| Salesforce Agentforce | Agentforce | Yes | Coming soon | [Connect Salesforce Agentforce](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-salesforce-agent-force) |
| Databricks Genie | Genie | Yes | Coming soon | [Connect Databricks Genie](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-databricks-genie) (worked example in 2.4) |
| Anthropic Claude | Managed Agents | Yes | Yes | [Connect Anthropic Claude Managed Agents](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-anthropic-claude) |
| Oracle Generative AI Agents | Generative AI Agents | Yes | Coming soon | [Connect Oracle Generative AI Agents](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-oracle-generative-ai) |
| Snowflake Cortex | Cortex Agents | Yes | Coming soon | [Connect Snowflake Cortex](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-snowflake-cortex) |

Choose the right integration mechanism for each agent:

| | Registry sync (preview) | Agent 365 SDK |
|---|---|---|
| Applies to | Connected agent platforms, such as Google Vertex AI and Amazon Bedrock | Agents you build with an agent SDK or framework, such as the Microsoft 365 Agents SDK, Microsoft Agent Framework, OpenAI Agents SDK, LangChain, CrewAI, or LlamaIndex |
| How it's applied | Configured per platform. Imports agents for visibility and governance. | Developer integrated in your agent's code for identity, tooling, and notifications. Use Microsoft OpenTelemetry for observability. |
| SDK required | No | Yes |
| Covered in | 2.2 to 2.6 | 2.7 to 2.11 |

### 2.2.2 Plan the connection with the platform administrator

Every connection follows the same lifecycle:

1. **Prepare**: Work with the platform administrator to select the account, project, workspace, compartment, or region and prepare the required credentials and permissions.
2. **Connect**: Create and validate the connection in the Microsoft 365 admin center.
3. **Synchronize**: Start synchronization so that Agent 365 discovers supported agents and adds them to the agent registry.
4. **Verify**: Confirm the expected agents, metadata, and capabilities with the platform administrator.
5. **Operate**: Monitor synchronization, rotate credentials, review errors, and remove connections when they're no longer needed.

Responsibilities:

| Task | Agent 365 AI administrator | Platform administrator |
|---|---|---|
| Confirm Agent 365 access and role | Owns | Informed |
| Select the source account, project, workspace, or region | Consulted | Owns |
| Create credentials | Informed | Owns |
| Grant source-platform permissions | Informed | Owns |
| Create and validate the Agent 365 connection | Owns | Supports |
| Verify synchronized agents | Owns | Supports |
| Enable source telemetry | Consulted | Owns |
| Rotate or revoke credentials | Coordinates | Owns |

### 2.2.3 Create a platform connection

Performed by **AI Administrator**, after the platform administrator completes the provider-specific preparation (2.3, 2.4, 2.5, or 2.6).

1. Open the Microsoft 365 admin center at https://admin.cloud.microsoft.
2. In the navigation pane, select **Agents** > **All agents**.
3. In the **Connected platforms** web part, select **Manage**.
4. Select **+ Connect a platform**.
5. Enter a connection name and description.
6. Select the platform.
7. Enter the provider-specific values described in the provider guide (see 2.3.4 for Amazon Bedrock, 2.4.3 for Databricks Genie, 2.5.4 for Google Vertex AI, and 2.6 for the other platforms).
8. Validate the credentials.
9. Save the connection.

**Check result**
- The credentials validate and the connection is saved. Synchronization starts only when you select **Sync agents** (2.2.4).

### 2.2.4 Synchronize, verify, and manage the connection

Performed by **AI Administrator**.

1. After you save the connection, select **Sync agents** to start synchronization. Manual synchronization is required.
2. Select the connection and review:
   - The platform provider.
   - The connected account, project, workspace, compartment, or region.
   - The last run date.
   - The latest synchronization status.
   - The total number of synchronized agents.
   - The synchronization results.
   - Any synchronization errors.
3. Confirm the expected agents, metadata, and capabilities with the platform administrator.
4. To rotate credentials, change the source scope, revoke access, or remove the connection, follow the relevant provider guide.

**Check result**
- The total number of synchronized agents matches what the platform administrator expects, and no synchronization errors are listed.

### 2.2.5 Turn on observability data collection (Frontier preview)

Third-party agent observability is part of the Frontier preview program. Supported observability platforms:

| Platform | Environment |
|---|---|
| Amazon Bedrock | Agents Classic and AgentCore |
| Google Vertex AI | Vertex AI agents |
| Anthropic Claude | Managed Agents |
| Salesforce Agentforce | Agent Builder |

Performed by **AI Administrator**.

1. Make sure the platform administrator configured the source telemetry described in the provider guide (for Amazon Bedrock, see 2.3.3; for Google Vertex AI, see 2.5.3). Enabling collection doesn't create source telemetry.
2. Edit the connection and confirm that **Collect agent observability data** is selected. Data collection is enabled by default for new connections; for connections created before this capability was introduced, it's disabled by default.

**Check result**
- **Collect agent observability data** is selected for the connection. Activity is tested in 2.12.4.

## 2.3 Example: connect Amazon Bedrock
**Documentation:** [Connect Amazon Bedrock to Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-amazon-bedrock) · [Troubleshoot connected platforms](https://learn.microsoft.com/microsoft-agent-365/admin/troubleshoot-connected-platforms)

### 2.3.1 Gather the prerequisites

Performed by **AI Administrator** with the **platform administrator**.

1. Confirm that the AI Administrator can create connections in the Microsoft 365 admin center.
2. Ask the platform administrator for an AWS access key ID and secret access key.
3. Identify the AWS Regions that contain the agents you want to synchronize.
4. Grant only the permissions required for the environments you use (Agents Classic, AgentCore, or both).

### 2.3.2 Grant the AWS synchronization permissions

Performed by **platform administrator**.

1. For **Agents Classic**, grant:

   ```text
   bedrock:ListAgents
   bedrock:GetAgent
   ec2:DescribeRegions
   ```

2. For **AgentCore**, grant:

   ```text
   bedrock-agentcore:ListHarnesses
   bedrock-agentcore:GetHarness
   bedrock-agentcore:ListAgentRuntimes
   bedrock-agentcore:GetAgentRuntime
   ec2:DescribeRegions
   ```

   `bedrock:ListAgents` and the AgentCore list operations discover agents in the selected Regions. The get operations read agent details. AgentCore runtimes that belong to a harness are skipped so that an agent isn't listed twice.

3. Grant optional permissions only when the connection needs the corresponding details:

   | Capability | Permissions |
   |---|---|
   | Show Classic tools, collaborators, and knowledge sources | `bedrock:ListAgentActionGroups`, `bedrock:GetAgentActionGroup`, `bedrock:ListAgentCollaborators`, `bedrock:ListAgentKnowledgeBases`, `bedrock:ListDataSources`, `bedrock:GetDataSource` |
   | Show AgentCore tools, MCP servers, and connected agents | `bedrock-agentcore:GetGateway`, `bedrock-agentcore:ListGatewayTargets`, `bedrock-agentcore:GetGatewayTarget` |
   | Connect every account in an AWS organization | `organizations:ListAccounts`, `sts:AssumeRole` |

4. Don't grant delete permissions for a read-only connection. If you grant `bedrock:DeleteAgent`, `bedrock-agentcore:DeleteHarness`, or `bedrock-agentcore:DeleteAgentRuntime`, Agent 365 can remove the corresponding agent when an administrator explicitly performs that action.

**Check result**
- The synchronization permissions for each environment in use are granted, and no delete permissions are granted.

### 2.3.3 Configure Bedrock activity for observability

Performed by **platform administrator**. Skip this task if you don't test third-party observability (2.2.5). Agent 365 reads activity. It doesn't invoke agents, write activity records, or delete activity records.

For **Agents Classic**:

1. Enable trace capture for each agent in the Amazon Bedrock console.
2. Select an S3 activity bucket.
3. Store activity under `observability-store/<agent-id>/`, where `<agent-id>` is the Bedrock agent ID.
4. Grant `s3:ListBucket` on the activity bucket.
5. Grant `s3:GetObject` on objects in the activity bucket.
6. If the bucket uses a customer-managed key, also grant `kms:Decrypt` on that key.

For **AgentCore** (activity is stored in Amazon CloudWatch Logs):

1. Grant `logs:StartQuery` and `logs:GetQueryResults`.
2. Grant `logs:DescribeLogGroups` to allow Agent 365 to find custom agent endpoints. Without it, only the default endpoint is read.
3. Enable **Transaction Search** in the Amazon CloudWatch console. AgentCore activity is queryable only after Transaction Search is enabled for the AWS account.

**Check result**
- Classic: trace capture is enabled, activity is stored under `observability-store/<agent-id>/`, and the S3 (and, if applicable, KMS) permissions are granted.
- AgentCore: the CloudWatch Logs permissions are granted and Transaction Search is enabled.

### 2.3.4 Create the Amazon Bedrock connection

Performed by **AI Administrator**.

1. Open the Microsoft 365 admin center at https://admin.cloud.microsoft.
2. Select **Agents** > **All agents**.
3. In **Connected platforms**, select **Manage**.
4. Select **+ Connect a platform** and choose **Amazon Bedrock**.
5. Enter the connection name, AWS access key ID, secret access key, and selected Regions.
6. Validate the credentials.
7. Save the connection.
8. Select **Sync agents**.

**Check result**
- The credentials validate. If validation fails, see 2.14.

### 2.3.5 Verify the Amazon Bedrock connection

Performed by **AI Administrator**.

1. Open the connection and check the synchronization status and the number of agents.
2. Open an imported agent to verify its metadata.
3. For observability, open the agent and select **Activity** after you configure the source platform and activity is available.

**Check result**
- The expected Agents Classic and AgentCore agents are imported with their metadata.

## 2.4 Example: connect Databricks Genie
**Documentation:** [Connect Databricks Genie to Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-databricks-genie) · [Connected platforms in Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms) · [Troubleshoot connected platforms](https://learn.microsoft.com/microsoft-agent-365/admin/troubleshoot-connected-platforms)

Databricks Genie supports agent synchronization. Its observability is listed as **Coming soon** on the Connected platforms page, so this example covers synchronization only.

### 2.4.1 Gather the prerequisites

Performed by **AI Administrator** with the **platform administrator**.

1. Confirm that the AI Administrator can create connections in the Microsoft 365 admin center (2.1).
2. Obtain the Databricks workspace URL.

### 2.4.2 Create the service principal and grant permissions

Performed by **platform administrator**.

1. Create a service principal.
2. Obtain the service principal client ID.
3. Obtain the service principal client secret.
4. Grant the permissions required to read the Genie agents in the workspace.

**Check result**
- You have the workspace URL, the service principal client ID, and the client secret, and the service principal can read the Genie agents in the workspace.

### 2.4.3 Create the Databricks Genie connection

Performed by **AI Administrator**.

1. Open the Microsoft 365 admin center at https://admin.cloud.microsoft.
2. Select **Agents** > **All agents**.
3. In **Connected platforms**, select **Manage**.
4. Select **+ Connect a platform** and choose **Databricks Genie**.
5. Enter the workspace URL, client ID, and client secret.
6. Validate the credentials.
7. Save the connection.
8. Select **Sync agents**.

**Check result**
- The credentials validate. If validation fails, see 2.14.

### 2.4.4 Verify the Databricks Genie connection

Performed by **AI Administrator**.

1. Open the connection and review the synchronization status.
2. Confirm that the expected Genie agents appear in the Microsoft 365 agent registry.

**Check result**
- The expected Genie agents are listed in the registry.

### 2.4.5 Rotate or revoke Databricks access

Performed by **platform administrator** (Databricks) and **AI Administrator** (connection).

1. To rotate access, the platform administrator rotates the service principal secret in Databricks. The AI Administrator then updates the Databricks Genie connection with the new secret and validates the credentials.
2. To revoke access, the platform administrator disables the service principal or removes its workspace permissions.

**Check result**
- After rotation, the connection validates with the new secret. After revocation, the service principal is disabled or has no workspace permissions.

## 2.5 Example: connect Google Vertex AI
**Documentation:** [Connect Google Vertex AI to Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-google-vertex-ai) · [Third-party agent observability (Frontier)](https://learn.microsoft.com/microsoft-agent-365/admin/third-party-agent-observability) · [Troubleshoot connected platforms](https://learn.microsoft.com/microsoft-agent-365/admin/troubleshoot-connected-platforms)

### 2.5.1 Gather the prerequisites

Performed by **AI Administrator** with the **platform administrator**.

1. Confirm that the AI Administrator can create connections in the Microsoft 365 admin center.
2. Ask the platform administrator for the Google Cloud project ID and region. Use the project and region where the agents are deployed.
3. Ask the platform administrator to create a Google Cloud service account and a JSON key for that account (2.5.2).

### 2.5.2 Create the service account and grant the Vertex AI permissions

Performed by **platform administrator**.

1. Create a Google Cloud service account.
2. Grant the service account the Vertex AI permissions required for agent discovery and management:

   ```text
   aiplatform.reasoningEngines.list
   aiplatform.reasoningEngines.get
   aiplatform.reasoningEngines.delete
   ```

3. Create a JSON key for the service account. The JSON key must contain the complete service-account key document, including the opening and closing braces. Don't enter only the `private_key` value.

**Check result**
- The service account has the three Vertex AI permissions, and you have its complete JSON key document.

### 2.5.3 Configure Vertex AI observability (Frontier preview)

Performed by **platform administrator**. Skip this task if you don't test third-party observability (2.2.5).

1. To collect observability data, grant the same service account these roles:

   | Role | Role ID | Purpose |
   |---|---|---|
   | BigQuery Data Viewer | `roles/bigquery.dataViewer` | Read exported trace tables |
   | BigQuery Job User | `roles/bigquery.jobUser` | Run queries to retrieve spans |
   | Monitoring Viewer | `roles/monitoring.viewer` | Read request-count and latency metrics |
   | Cloud Trace User | `roles/cloudtrace.user` | Read Cloud Trace spans |

   You need both BigQuery roles. Data Viewer permits reading the tables, while Job User permits running the queries that retrieve the results.

2. On the project where you deployed the agent:
   1. Enable the Vertex AI API.
   2. Enable the BigQuery API.
   3. Enable the Cloud Trace API.
   4. Enable the Cloud Monitoring API.
   5. Enable telemetry collection on the deployed agent.
   6. Enable Trace Analytics BigQuery export.
   7. Confirm that the `trace_analytics_link` dataset and its `_AllSpans` view exist.

Agent 365 can't enable telemetry collection or trace export for you.

**Check result**
- The four roles are granted to the service account, the four APIs are enabled, telemetry collection and Trace Analytics BigQuery export are enabled, and the `trace_analytics_link` dataset and its `_AllSpans` view exist.

### 2.5.4 Create the Google Vertex AI connection

Performed by **AI Administrator**.

1. Open the Microsoft 365 admin center at https://admin.cloud.microsoft.
2. Select **Agents** > **All agents**.
3. In **Connected platforms**, select **Manage**.
4. Select **+ Connect a platform** and choose **Google Vertex AI**.
5. Enter the project ID, region, and complete service-account JSON key.
6. Validate the credentials.
7. Save the connection.
8. Select **Sync agents**.

**Check result**
- The credentials validate. If validation fails, see 2.14.

### 2.5.5 Verify the Google Vertex AI connection

Performed by **AI Administrator**.

1. Open the connection and review the synchronization status and the number of synchronized agents.
2. Confirm that the expected agents are imported into the Microsoft 365 agent registry.
3. For observability, open an imported agent and select the **Activity** tab after the agent runs.

A connection can validate and import agents while returning no telemetry if the project, region, roles, APIs, or trace export aren't configured correctly (see 2.14).

**Check result**
- The expected Vertex AI agents are imported into the registry.

## 2.6 Connect other supported platforms
**Documentation:** [Connect Salesforce Agentforce](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-salesforce-agent-force) · [Connect Anthropic Claude Managed Agents](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-anthropic-claude) · [Connect Oracle Generative AI Agents](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-oracle-generative-ai) · [Connect Snowflake Cortex](https://learn.microsoft.com/microsoft-agent-365/admin/connected-platforms-snowflake-cortex)

### 2.6.1 Prepare and connect another platform

Each platform has its own configuration guide. Follow the platform article for the source-side steps, then create, sync, and verify the connection with the same wizard as in 2.2.3 and 2.2.4.

| Platform | Platform administrator prepares | Values entered in the wizard |
|---|---|---|
| Salesforce Agentforce | Einstein Generative AI and Agentforce turned on; an external client app with the client credentials flow and a **Run As** user with API access. For activity: Data 360 and Agentforce Session Tracing. | My Domain URL without a path, consumer key, consumer secret |
| Anthropic Claude (Managed Agents) | A workspace other than the default workspace, an environment and a managed agent in the workspace, and a workspace-scoped API key (requires at least the **Developer** role) | Workspace ID, workspace-scoped API key |
| Oracle Generative AI Agents | An API-only service user in a group, an API key pair, and a least-privilege policy that grants read access to the agent resources in the selected compartment | Private key, user OCID, tenancy OCID, fingerprint, region, compartment OCID |
| Snowflake Cortex | A Snowflake user with RSA key-pair authentication, and the database and schema where the agents are created | Account identifier, database, schema, Snowflake user, private key |

Performed by **platform administrator** (source side) and **AI Administrator** (connection).

1. Ask the platform administrator to complete the source-side steps in the platform article.
2. Create the connection as in 2.2.3, selecting the platform and entering the values from the table.
3. Sync and verify as in 2.2.4.

**Check result**
- The expected agents are imported.

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
5. Browse to **Entra ID** > **Agents** > **Agent identities**, add the **Blueprint App ID** filter with the `agentBlueprintId`, and confirm that the agent identity is listed. Assign owners and sponsors as described in [Chapter 3 – Agent Identity and Ownership](../chapter-03-identity-ownership/README.md).

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

## 2.12 Test and validation

### 2.12.1 Test: third-party agents appear in the registry

Performed by **AI Administrator** (connection status) and **AI Reader** (registry).

1. In the Microsoft 365 admin center, select **Agents** > **All agents**, and in the **Connected platforms** web part select **Manage**. Select each PoC connection and confirm the latest synchronization status, the total number of synchronized agents, and that no synchronization errors are listed.
2. Open **Agents** > **All agents** > **Registry**.
3. Use the **Platform** filter to show the agents of the connected platform.
4. Confirm that every expected test agent is listed.
5. Open each agent and review its details.
6. Select **Export** to export the agents to a CSV file.

**Expected result**
- Each connection shows the expected number of synchronized agents and no synchronization errors.
- Every expected third-party agent is listed with its metadata.

### 2.12.2 Test: Databricks Genie agents appear in the registry after sync

Performed by **AI Administrator** (sync) and **AI Reader** (registry).

1. On the **Connected platforms** page, select **Sync agents** for the Databricks Genie connection (2.4.3).
2. Open the connection and review the synchronization status.
3. Open **Agents** > **All agents** > **Registry** and confirm that the expected Genie agents appear.

**Expected result**
- The expected Genie agents from the workspace appear in the Microsoft 365 agent registry.

### 2.12.3 Test: Google Vertex AI agents appear in the registry after sync

Performed by **AI Administrator** (sync) and **AI Reader** (registry).

1. On the **Connected platforms** page, select **Sync agents** for the Google Vertex AI connection (2.5.4).
2. Open the connection and review the synchronization status and the number of synchronized agents.
3. Open **Agents** > **All agents** > **Registry** and confirm that the expected Vertex AI agents are imported.

**Expected result**
- The expected Vertex AI agents from the selected project and region appear in the Microsoft 365 agent registry.

### 2.12.4 Test: third-party agent activity is observable (Frontier preview)

Performed by **platform administrator** (run the agent) and **AI Reader** (review).

1. On the source platform, run the test agent (for Amazon Bedrock, in a Region that the connection covers; for Google Vertex AI, in the project and region that the connection covers).
2. Wait for the platform-specific processing interval. Anthropic Claude activity can take 5 to 10 minutes after an interaction.
3. In the registry, select the synchronized agent and select the **Activity** tab.
4. Review **Sessions**, **Exceptions**, and **Runtime**. **Users** isn't available for third-party agents when the source platform doesn't provide Microsoft Entra user identities.

**Expected result**
- The sessions from step 1 appear on the **Activity** tab.

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

Performed by the **developer** (send requests) and a user with **Security data basics (read)** (review). Requires 2.11.1 and the Microsoft 365 connector in Microsoft Defender ([8.3 Connect the Microsoft 365 connector](../chapter-08-threat-detection/README.md#83-connect-the-microsoft-365-connector)). Without the connector, `CloudAppEvents` returns no rows.

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

## 2.13 Evidence

- Screenshot of the **Connected platforms** page with the details of each PoC connection (Amazon Bedrock, Databricks Genie, Google Vertex AI, or other): provider, scope, last run date, latest synchronization status, number of synchronized agents.
- Screenshot of the synchronization results and errors, if any.
- The list of source-platform permissions granted to the connection credentials.
- Registry export (CSV) and a screenshot of the registry filtered by platform, showing the synchronized agents.
- (Optional) Screenshot of the **Activity** tab of a synchronized third-party agent.
- `a365 setup all` summary output and a copy of `a365.generated.config.json` with the client secret and consent URLs removed.
- Output of `a365 query-entra blueprint-scopes` and `a365 query-entra inheritance`.
- Screenshots of the blueprint and the agent identity in the Microsoft Entra admin center with the matching Blueprint App ID.
- (If deployed) Output of `az webapp show ... --query state`.
- `a365 publish` output and a screenshot of the custom agent in **Agents** > **All agents** (name, version, publisher, availability).
- (Optional) Advanced hunting results for the custom agent's `InvokeAgent` events.

## 2.14 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Connection validation fails (any platform) | Credentials not current, missing discovery permissions, connection fields that don't match the provider guide, or the source platform doesn't allow the connection | Confirm credentials, permissions, and fields against the provider guide. If credentials expired or were revoked, rotate them and update the connection. |
| Amazon Bedrock validation fails | Missing `ec2:DescribeRegions`, or invalid or disabled credentials | Confirm the credentials and grant `ec2:DescribeRegions`. |
| Agents don't appear after synchronization | Agents outside the selected account, project, workspace, compartment, or region; credentials can't list the agents | Review the synchronization status and errors, confirm the scope and the discovery permissions, and select **Sync agents** again. |
| Agents appear with limited metadata | Missing get or optional metadata permissions (for Amazon Bedrock, `bedrock:GetAgent` or the AgentCore get operation) | Grant the relevant get permission and the optional metadata permissions from the provider guide. |
| Duplicate agents appear | The source platform exposes the same agent through multiple resources or environments | Verify the connection scope and synchronization results before you delete or change an agent. |
| Agent appears but no activity is shown | Source telemetry isn't enabled or **Collect agent observability data** is disabled | Enable source telemetry and **Collect agent observability data**, then run the agent. |
| Activity is delayed | Source processing or ingestion is still running | Wait for the platform-specific processing interval and check again. |
| Amazon Bedrock Classic agents have no activity | Incorrect trace capture, bucket location, bucket path, or S3 permissions | Enable trace capture and verify the bucket and object permissions. |
| Amazon Bedrock AgentCore agents have no activity | Missing Transaction Search or CloudWatch Logs permissions | Enable Transaction Search and grant `logs:StartQuery` and `logs:GetQueryResults`. |
| Amazon Bedrock AgentCore activity is incomplete | Missing `logs:DescribeLogGroups` | Grant the permission when custom endpoints are used. |
| Google Vertex AI agents import but no activity appears | Observability isn't configured | Complete the roles, API, telemetry, and trace-export steps (2.5.3). |
| Google Vertex AI: no spans, but metrics appear | BigQuery roles or trace export are missing | Grant both BigQuery roles and enable trace export. |
| Google Vertex AI: queries fail although tables are readable | `roles/bigquery.jobUser` is missing | Grant BigQuery Job User to the service account. |
| Google Vertex AI: no request-count or latency metrics | Monitoring role or API is missing | Grant Monitoring Viewer and enable Cloud Monitoring API. |
| Google Vertex AI: `_AllSpans` doesn't exist | Trace Analytics BigQuery export isn't enabled | Enable the export and verify the dataset and view. |
| Google Vertex AI agents import but telemetry is empty | Connection scope doesn't match deployment scope | Use the deployed agent's project and region. |
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
| `CloudAppEvents` returns no rows at all | The Microsoft 365 connector isn't connected in Microsoft Defender | Connect it as described in [8.3 Connect the Microsoft 365 connector](../chapter-08-threat-detection/README.md#83-connect-the-microsoft-365-connector), then run the agent again. |

## 2.15 Cleanup

Connected platforms (for each PoC connection):
1. **AI Administrator** and **platform administrator:** Confirm which agents and management actions depend on the connection, and confirm how the provider handles synchronized agent records after connection removal. If delete permissions were granted on the source platform (for example `bedrock:DeleteAgent`), Agent 365 can remove the corresponding agent when an administrator explicitly performs that action.
2. **AI Administrator:** Remove the connection in the Microsoft 365 admin center (**Agents** > **All agents** > **Connected platforms** > **Manage**).
3. **Platform administrator:** Revoke the source credentials:
   - Amazon Bedrock (2.3): revoke or rotate the AWS access key as required by your organization's security policy.
   - Databricks Genie (2.4): disable the service principal or remove its workspace permissions.
   - Google Vertex AI (2.5): revoke or rotate the service-account credentials as required by your organization's security policy.
   - Other platforms (2.6): follow the revoke steps in the platform article where documented (for example, delete the Oracle API key); otherwise revoke or rotate the credentials as required by your organization's security policy.

Custom agents:
1. **AI Administrator:** Delete the uploaded PoC agent from **Agents** > **All agents**. A deleted agent is soft deleted and can be restored within 30 days.
2. **Global Administrator** with **Contributor** on the Azure subscription: Preview and then remove the blueprint, agent instance, and Azure resources:

   ```powershell
   a365 cleanup --agent-name "PoC Custom" --dry-run
   a365 cleanup --agent-name "PoC Custom"
   ```

   For granular cleanup, use `a365 cleanup blueprint`, `a365 cleanup azure`, or `a365 cleanup instance`. `a365 cleanup blueprint` also deletes the blueprint's service principal and any agent instances linked to it; if the agent is registered in the Agent Registry, the corresponding registry entry might also be removed.
3. **Contributor:** If you created a resource group only for the PoC, delete it with `az group delete --name <your-resource-group>`. This command deletes all resources in the group.

---
Previous: [Chapter 1 – Agent Discovery and Inventory](../chapter-01-agent-discovery/README.md) · Next: [Chapter 3 – Agent Identity and Ownership](../chapter-03-identity-ownership/README.md)
