# Custom agent samples (Agent 365 SDK path)

Minimal custom engine agents used in [Chapter 2 – Third-Party and Custom Agents](../../README.md), sections 2.7 to 2.11. Each file is the agent code only, built on the Microsoft 365 Agents SDK hosting layer. Registering the agent with Agent 365 (agent identity blueprint, agent identity, permissions, registration) is a separate step that you run with the Agent 365 CLI or the Agent 365 Skills.

## Files

| File | Language | Package to install | Based on |
|---|---|---|---|
| [`nodejs/agent.ts`](nodejs/agent.ts) | Node.js / TypeScript | `@microsoft/agents-hosting`, `@microsoft/agents-hosting-express` | [Quickstart (Node.js)](https://learn.microsoft.com/microsoft-365/agents-sdk/quickstart?pivots=nodejs) |
| [`python/agent.py`](python/agent.py) | Python | `microsoft-agents-hosting-aiohttp`, `microsoft-agents-authentication-msal`, `python-dotenv` (imports `microsoft_agents.*`) | [Quickstart (Python)](https://learn.microsoft.com/microsoft-365/agents-sdk/quickstart?pivots=python) and the [Python quickstart sample](https://github.com/microsoft/Agents/tree/main/samples/python/quickstart) |
| [`dotnet/Agent.cs`](dotnet/Agent.cs) | .NET (`Program.cs` of a `dotnet new web` project) | `Microsoft.Agents.Hosting.AspNetCore` | [Quickstart (.NET)](https://learn.microsoft.com/microsoft-365/agents-sdk/quickstart?pivots=dotnet) |

The samples use the messaging endpoint `/api/messages`, so you can test them locally with Microsoft 365 Agents Playground before you register or deploy them, as in the quickstarts. The Node.js sample runs locally in anonymous mode, as in the Node.js quickstart. For the .NET sample, set the application URL in `launchSettings.json` as described in the .NET quickstart. The Python sample reads its service connection settings (`CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENTID`, `__CLIENTSECRET`, `__TENANTID`) from environment variables or a `.env` file, as in the Python quickstart sample. Never commit `.env` files with sensitive information to source control. These samples aren't production starter kits.

## Path from code to the Agent 365 registry

| Step | Agent 365 Skill (coding assistant) | Equivalent manual step | Result |
|---|---|---|---|
| 1. Validate prerequisites and detect the stack | `a365-setup` | Install the Agent 365 CLI, run `a365 setup requirements` | CLI installed, Azure sign-in and roles checked. `a365-setup` routes you to step 2a or 2b. |
| 2a. Register a standard agent | `make-a365-agent` | `a365 setup all` (or `a365 setup all --agent-name <name>`) | Agent identity blueprint and agent identity in Microsoft Entra, permissions configured, agent registered. Generated IDs saved in `a365.generated.config.json`. |
| 2b. Make it an AI teammate (Frontier preview program only) | `make-ai-teammate` | `a365 setup all --aiteammate` (requires a manually created `a365.config.json`) | The CLI provisions the blueprint and permissions; the skill also adds the hosting layer, message routing, and notifications. The agent gets its own user account. |
| 3. Deploy the runtime (optional) | – | `az webapp deploy` (see [Deploy agent to Azure](https://learn.microsoft.com/microsoft-agent-365/developer/deploy-agent-azure)) | Agent code running behind a reachable messaging endpoint. |
| 4. Publish | – | `a365 publish`, then upload `manifest.zip` in the Microsoft 365 admin center | Agent listed in **Agents** > **All agents**. |
| 5. Add observability (optional) | `instrument-observability` | Microsoft OpenTelemetry Distro (`@microsoft/opentelemetry`, `microsoft-opentelemetry`, `Microsoft.OpenTelemetry`) | Spans with a root `invoke_agent` span reach Microsoft Defender, Microsoft Purview, and the Microsoft 365 admin center. |
| 6. Add Work IQ tools (optional) | `add-workiq-tools` | `a365 develop add-mcp-servers`, then `a365 setup permissions mcp` by a Global Administrator | Governed Microsoft 365 MCP tools. Requires a delegated (OBO) permission model. |
| 7. Add Purview DLP (optional) | `purview-dlp-integration` | – | Guard that calls Microsoft Graph `processContent` before the model call. See [2.11.2 Add the Purview DLP guard](../../README.md#2112-add-the-purview-dlp-guard). |
| 8. Validate the integration (optional) | `a365-code-validator` | `a365 query-entra blueprint-scopes`, `a365 query-entra inheritance` | Report of gaps in instrumentation, Entra artifacts, and permissions. |

## Use the Agent 365 Skills

The [`microsoft/agent365-skills`](https://github.com/microsoft/agent365-skills) repository packages the skills listed above for Claude Code, GitHub Copilot CLI, and VS Code agent mode. You don't type the skill name; you open your agent project in the coding assistant and state the outcome you want, for example *set up this project for Agent 365*, *register this agent with Agent 365*, or *add observability to this agent*. The assistant must run in a mode with terminal access (in VS Code, use agent mode; Ask and Edit modes can't run commands).

Install the skills with one of the methods documented in the repository README and on Microsoft Learn:

- **GitHub CLI `gh skill` (GitHub Copilot CLI, VS Code agent mode, Claude Code).** The `gh skill` command is in preview in the GitHub CLI; `gh skill add` is an alias of `gh skill install`. The default installation scope is `project` (inside the current Git repository), and at project scope GitHub Copilot uses the `.agents/skills` directory. Use `--scope user` to install in your home directory, and `--agent` to select the coding assistant. Restart your assistant afterward so it picks up the new skills.

  ```powershell
  gh skill install microsoft/agent365-skills --all
  # For Claude Code instead of GitHub Copilot:
  gh skill install microsoft/agent365-skills --all --agent claude-code
  ```

- **Claude Code plugin marketplace.** Inside an active Claude Code session:

  ```text
  /plugin marketplace add https://github.com/microsoft/agent365-skills
  /plugin install agent365@agent365-skills
  ```

- **Project-scoped copy (`.agents/skills/` open standard).** Clone the repository and run its installer from your agent project folder. VS Code agent mode, the Copilot cloud agent, and Copilot CLI load skills from `.agents/skills/`.

  ```powershell
  git clone https://github.com/microsoft/agent365-skills.git
  cd <your-agent-project>
  node <path-to>\agent365-skills\scripts\install.js
  ```

In GitHub Copilot CLI or VS Code, list the installed skills with `/skills list`. Skills are additive and idempotent: they don't delete or restructure existing code, and rerunning a skill doesn't duplicate completed work. Review the code, manifest, and configuration changes each skill makes.

## Documentation

- [`microsoft/agent365-skills` README](https://github.com/microsoft/agent365-skills) · [GitHub CLI `gh skill install`](https://cli.github.com/manual/gh_skill_install)
- [Agent 365 Skills for guided agent setup](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-skills)
- [Quickstart: Connect an existing agent to Agent 365](https://learn.microsoft.com/microsoft-agent-365/developer/get-started)
- [Install and use the Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/agent-365-cli) · [Agent 365 CLI reference](https://learn.microsoft.com/microsoft-agent-365/developer/reference/cli/)
- [Set up the agent blueprint](https://learn.microsoft.com/microsoft-agent-365/developer/registration) · [Deploy agent to Azure](https://learn.microsoft.com/microsoft-agent-365/developer/deploy-agent-azure) · [Publish agent to the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-agent-365/developer/publish)
- [Microsoft OpenTelemetry Distro](https://learn.microsoft.com/microsoft-agent-365/developer/microsoft-opentelemetry)
- [Custom client app registration for Agent 365 CLI](https://learn.microsoft.com/microsoft-agent-365/developer/custom-client-app-registration)
- [Microsoft 365 Agents SDK quickstart](https://learn.microsoft.com/microsoft-365/agents-sdk/quickstart)
