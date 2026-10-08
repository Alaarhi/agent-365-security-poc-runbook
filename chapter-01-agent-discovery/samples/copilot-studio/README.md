# Copilot Studio sample agent

A minimal declarative agent definition that you can use as the reference configuration for a Copilot Studio test agent.

## Files

- `declarative-agent.json`: an agent definition that uses the declarative agent schema 1.2. It contains a name, a description, instructions, conversation starters, web search and one SharePoint knowledge source.

## How to use it

1. Replace `https://contoso.sharepoint.com/sites/trailguide-poc` with your PoC SharePoint site.
2. Create a new agent in Copilot Studio (`https://copilotstudio.microsoft.com`). Use the name, description and instructions from the JSON file, and add the SharePoint site as a knowledge source.
3. Publish the agent. Then open the configuration panel for the **Teams and Microsoft Copilot** channels, select **Availability options**, and share the agent with the organization by submitting it for admin approval.

The file contains no credentials or secrets.

## Discovery path in the Agent Registry

| Step | What happens |
|---|---|
| 1. Create | When you create a Copilot Studio agent, an Agent ID is created and the agent appears in the agent registry immediately. Metadata changes are synchronized automatically. |
| 2. Submit for approval | An agent submitted for admin approval appears in the Microsoft 365 admin center under **Agents** > **All agents** > **Requests**. |
| 3. Approve | An AI Administrator selects **Publish to store**, selects the users or groups that can install the agent, applies a policy template, reviews permissions and publishes the agent. |

All Copilot Studio app-based agents share a single blueprint, and an Agent ID is created for each agent.

## Documentation

- [Agent registry integration for Copilot Studio](https://learn.microsoft.com/microsoft-agent-365/builder/agent-registry)
- [Agent identity integration for Copilot Studio](https://learn.microsoft.com/microsoft-agent-365/builder/identity)
- [Declarative agent schema 1.2 for Microsoft 365 Copilot](https://learn.microsoft.com/microsoft-365-copilot/extensibility/declarative-agent-manifest-1.2)
- [Connect and configure an agent for Teams and Microsoft 365](https://learn.microsoft.com/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams)
- [Manage agent requests in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-requests)
