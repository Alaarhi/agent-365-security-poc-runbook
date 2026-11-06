# Chapter 2 - Connected platforms

**Pillar:** Observe
**What it proves:** Agents on supported third-party platforms are discovered through Connected platforms without code and appear in the Microsoft 365 agent registry with their metadata.

For agents you integrate in code, use the separate [Agent 365 SDK guide](agent-365-sdk.md). These are independent paths.

**Success criteria:** Agree the selected outcomes in [What you proved](#-what-you-proved) before testing.

## Topics and time guide

Approximate hands-on estimates for the selected scope, with [prerequisites](prerequisites.md) prepared. Service waiting time is separate.

| Topic | Estimated hands-on time |
|---|---|
| [2.1 Required permissions](#21-required-permissions) | ~5 min |
| [2.2 Connect a third-party agent platform](#22-connect-a-third-party-agent-platform) | ~10-15 min |
| [2.3 Example: connect Amazon Bedrock](#23-example-connect-amazon-bedrock) | ~20-30 min |
| [2.4 Example: connect Databricks Genie](#24-example-connect-databricks-genie) | ~15-20 min |
| [2.5 Example: connect Google Vertex AI](#25-example-connect-google-vertex-ai) | ~20-30 min |
| [2.6 Connect other supported platforms](#26-connect-other-supported-platforms) | ~15-25 min |
| [2.12 Test and validation](#212-test-and-validation) | ~15-20 min |
| [2.13 Evidence](#213-evidence) | ~5-10 min |
| [2.14 Troubleshooting](#214-troubleshooting) | As needed |

[Outcome checklist](#-what-you-proved) · [References](#references)

Choose the platform example for your environment; the examples are alternative paths.

---

## 2.1 Required permissions

Use the [shared account and role-assignment model](../README.md#least-privilege-model) with the task-specific permissions below.

| Task | Least-privilege role | Section |
|---|---|---|
| Create, validate, sync, edit, and delete connected-platform connections | AI Administrator | 2.2 to 2.6 |
| Amazon Bedrock: provide the AWS access key ID and secret access key, grant the IAM permissions, configure Bedrock activity | Platform administrator (AWS) | 2.3 |
| Databricks Genie: create the service principal and client secret, grant the permissions required to read the Genie agents in the workspace, rotate or revoke the secret | Platform administrator (Databricks) | 2.4 |
| Google Vertex AI: create the service account and JSON key, grant the Vertex AI permissions and observability roles, configure Google Cloud telemetry | Platform administrator (Google Cloud) | 2.5 |
| Other supported platforms: create source-platform credentials, grant source-platform permissions, enable source telemetry | Platform administrator (source platform) | 2.6 |
| Validation / read-only review | AI Reader (registry and agent activity) | 2.12.1 to 2.12.4 |

- For connected platforms, the AI Administrator creates and manages the connection in the Microsoft 365 admin center; the platform administrator creates the source-platform credentials, grants the required permissions, and enables platform-side telemetry when applicable.

**Before you start:**
- [ ] Confirm the [shared tenant checks](prerequisites.md#tenant-readiness) and the [connected-platform preparation](prerequisites.md#connected-platform-preparation).

---

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
| Covered in | This guide, 2.2 to 2.6 | [Agent 365 SDK guide, 2.7 to 2.11](agent-365-sdk.md#27-prepare-the-custom-agent-toolchain) |

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

---

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

---

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

---

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

---

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

---

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

---

## 2.13 Evidence

- Screenshot of the **Connected platforms** page with the details of each PoC connection (Amazon Bedrock, Databricks Genie, Google Vertex AI, or other): provider, scope, last run date, latest synchronization status, number of synchronized agents.
- Screenshot of the synchronization results and errors, if any.
- The list of source-platform permissions granted to the connection credentials.
- Registry export (CSV) and a screenshot of the registry filtered by platform, showing the synchronized agents.
- (Optional) Screenshot of the **Activity** tab of a synchronized third-party agent.

---

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

---

## ✅ What you proved

- [ ] A connection to at least one supported third-party platform validates, **Sync agents** runs, and the connection shows the expected number of synchronized agents with no synchronization errors.
- [ ] Every expected third-party test agent appears in **Agents** > **All agents** > **Registry** with its metadata.
- [ ] (Optional, Frontier preview) The **Activity** tab of a synchronized third-party agent shows sessions after the agent runs on the source platform.

---

## References

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
- [Troubleshoot connected platforms](https://learn.microsoft.com/microsoft-agent-365/admin/troubleshoot-connected-platforms)

---

[Runbook index](../README.md) · Previous: [Chapter 1 – Agent discovery and inventory](../chapter-01-agent-discovery/README.md) · [Agent 365 SDK guide](agent-365-sdk.md) · Next: [Chapter 3 – Agent identity and ownership](../chapter-03-identity-ownership/README.md)
