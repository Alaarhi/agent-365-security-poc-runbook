# Chapter UC2 - Identity & Ownership

**Pillar:** Govern
**What it proves:** anonymous agents become governable identities. Every agent gets a directory identity in Microsoft Entra ID with assigned **owners** and **sponsors** and a lifecycle state, so its access can be attributed and revoked like any other workload identity.

## Section 1 - Concepts, roles, and prerequisites

Microsoft Entra Agent ID has three related objects:

| Object | What it is |
|---|---|
| **Agent identity blueprint** | The parent definition from which individual agent identities are created. Created by an **Agent ID Developer**; that user becomes the owner of the blueprint and its service principal. |
| **Agent identity** | A directory identity of type "agent" that an agent uses to call APIs. One blueprint can create many agent identities. |
| **Agent user account** (optional) | Used when the agent needs its own Microsoft 365 identity, mailbox, Teams presence, etc. (AI Teammate pattern). |

Each agent identity has:

- **Owners** - who handle technical administration of the agent.
- **Sponsors** - who are accountable for the agent's purpose and lifecycle decisions.

Owners and sponsors are shown as a single **Owners and Sponsors** column in the Entra admin center.

### Task 1 - confirm least-privilege roles

Taken directly from [Manage agent identities in your organization](https://learn.microsoft.com/entra/agent-id/manage-agent-identities-admin#prerequisites).

| Task | Required role | Notes |
|---|---|---|
| View agent identities (least privilege) | Any Microsoft Entra user account | No admin role needed to view. Reviewers and auditors need nothing extra. |
| Manage agent identities (edit, disable, assign owners/sponsors) | **Agent ID Administrator** or **Cloud Application Administrator** | Owners of a specific agent can manage their own agents without these roles. |
| Create agent blueprints | **Agent ID Developer** | The creator becomes owner of the blueprint and its service principal. |
| Create and define custom security attributes (CSA) sets | **Attribute Definition Administrator** | Required to define the attribute set and keys. |
| Assign CSA values to agent identities | **Attribute Assignment Administrator** | Required to write values on an agent identity. Split from the definition role by design. |
| View ID Protection risk reports for agents | **Security Administrator**, **Security Operator**, or **Security Reader** | Requires Microsoft Entra ID P2 (preview). |
| Configure Lifecycle Workflows for agents (sponsor change) | **Lifecycle Workflows Administrator** | Covered in [UC3](../chapter-uc3-least-privilege/README.md). |

**Least privilege for the PoC validation step** is: no admin role at all. Any user can view agent identities. Grant the admin roles only to the person who actually configures.

### Task 2 - open the identity portals

Microsoft Entra admin center - <https://entra.microsoft.com> > **Entra ID** > **Agents**:

- **Agent identities** - the primary view for this chapter.
- **Agent blueprints** - view and manage the parent blueprints.

Custom security attributes are under **Entra ID** > **Protect & secure** > **Custom security attributes**.

### Task 3 - review documentation

| Topic | Documentation |
|---|---|
| Entra Agent ID - management | [Manage agent identities in your organization](https://learn.microsoft.com/entra/agent-id/manage-agent-identities-admin) |
| View and filter agent identities | [View and filter agent identities in your tenant](https://learn.microsoft.com/entra/agent-id/agent-lists) |
| Manage blueprints | [View and manage agent identity blueprints in your tenant](https://learn.microsoft.com/entra/agent-id/manage-agent-blueprint) |
| Inheritable permissions | [Configure inheritable permissions for agent identity blueprints](https://learn.microsoft.com/entra/agent-id/configure-inheritable-permissions-blueprints) |
| Conditional Access for agents | [Conditional Access for Agents in Microsoft Entra](https://learn.microsoft.com/entra/identity/conditional-access/agent-id) |
| Custom security attributes | [Custom security attributes in Microsoft Entra ID](https://learn.microsoft.com/entra/fundamentals/custom-security-attributes-overview) |
| Migrate Copilot Studio agents to Agent ID | [Recreate Copilot Studio agents in Microsoft Entra Agent ID](https://learn.microsoft.com/entra/agent-id/migrate-copilot-studio-agents-to-agent-id) |

### Task 4 - confirm prerequisites

Complete [Chapter 0 - Prerequisites](../chapter-0-prerequisites/README.md) and [UC1 - Agent Discovery](../chapter-uc1-agent-discovery/README.md). For Copilot Studio agents, Entra Agent Identity is enabled at the Copilot Studio environment level in Section 2, Task 1 below.

## Section 2 - Identity setup and validation tasks

### Task 1 - enable Entra Agent Identity at the Copilot Studio environment level

Required only if Copilot Studio agents are in scope. Performed by a **Power Platform Administrator** or environment admin.

1. Open <https://admin.powerplatform.microsoft.com>.
2. Go to **Environments** > select the environment used for PoC agents.
3. Enable **Entra Agent Identity** for the environment.

Once enabled, every new Copilot Studio agent created in that environment automatically receives an Entra Agent ID. Legacy agents created before enablement continue using traditional app registrations and can be migrated using the docs link above.

### Task 2 - confirm and assign owners and sponsors

Performed by **Agent ID Administrator** or **Cloud Application Administrator**. (The agent's existing owner can also do this for their own agent without those roles.)

1. Sign in to <https://entra.microsoft.com>.
2. Go to **Entra ID** > **Agents** > **Agent identities**.
3. Select each PoC agent identity.
4. On the agent's management page, open **Owners and sponsors**.
5. Confirm the correct **owner** (technical administrator) and **sponsor** (business accountable) are listed. Add any missing entries.

### Task 3 - configure custom security attributes for governance (Optional)

Performed by **Attribute Definition Administrator** (step 1-2) then **Attribute Assignment Administrator** (step 3).

1. In Entra, go to **Entra ID** > **Protect & secure** > **Custom security attributes** > **Add attribute set** and create `AgentGovernance`.
2. Define two attributes inside the set:

   | Attribute | Type | Allowed values | Why |
   |---|---|---|---|
   | `Project` | String (predefined) | `Agent365PoC` | Groups everything in this PoC; one filter pulls every PoC agent. |
   | `Environment` | String (predefined) | `Pilot`, `Prod` | Prevents PoC agents from being mistaken for production. |

3. For each PoC agent identity (**Entra ID** > **Agents** > **Agent identities** > select agent > **Custom security attributes**), assign:

   | Attribute | Value |
   |---|---|
   | `Project` | `Agent365PoC` |
   | `Environment` | `Pilot` |

### Task 4 - test identity and ownership

Performed by any Microsoft Entra user.

1. Sign in to <https://entra.microsoft.com>.
2. Browse to **Entra ID** > **Agents** > **Agent identities**.
3. Use the search box to find an agent by **name** or **object ID**, or add the **Blueprint App ID** filter.
4. (Optional) Select **Choose columns** and add **Owners and Sponsors**, **Blueprint App ID**, **Status**, and **Created On**.
5. For each in-scope PoC agent, confirm:
   - The agent identity exists.
   - **Status** is active (not disabled).
   - **Owners and Sponsors** lists the expected owner and sponsor.
   - **Blueprint App ID** matches the expected blueprint (confirms it was created from the correct parent).
6. (Optional) Select an agent and open its details page to review:
   - Granted permissions.
   - Sign-in logs for the agent.
   - Audit log entries for owner / sponsor changes.
7. Cross-check in the Agent 365 Registry (<https://admin.cloud.microsoft> > **Agents**) that the same agent shows the same owner.
8. Export the agent-identities list as evidence (CSV from the view, or via Microsoft Graph - see [UC1](../chapter-uc1-agent-discovery/README.md#section-5---programmatic-discovery-with-microsoft-graph-optional)).

**Expected result**

- Every in-scope agent has an agent identity in Entra.
- Each agent identity has at least one named **owner** and one named **sponsor**.
- Each agent identity is linked to its parent **blueprint** (visible via Blueprint App ID).
- Owner is consistent between Entra and the Agent 365 Registry.
- If custom security attributes are used, filtering by `AgentGovernance/Project = Agent365PoC` returns every PoC agent in one list.

## Section 3 - Evidence

### Task 1 - capture evidence

- Export of the Agent identities list for the PoC (Name, Object ID, Status, Blueprint App ID, Owners and Sponsors, CSA values).
- Screenshot of one agent's details page showing Owners and Sponsors, granted permissions, and sign-in log entries.
- Screenshot of the Agent 365 Registry with matching owner.

## Section 4 - Troubleshooting

### Task 1 - troubleshoot common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent not visible in **Agents** > **Agent identities** | Agent is a legacy pre-enablement Copilot Studio agent, or the environment has not enabled Entra Agent Identity | Enable at the Copilot Studio environment level, or migrate legacy agents using the docs link above. |
| Agent identity has no sponsor | Sponsor was never assigned during agent creation | Add a sponsor from the agent's details page. |
| Agent identity has no owner | Owner was never assigned, or the original owner left and ownership was not transferred | Add an owner from the agent's details page, or use the sponsor-change workflow in [UC3](../chapter-uc3-least-privilege/README.md). |
| Owner in Entra does not match owner in Agent 365 Registry | Sync delay, or owner was changed in only one surface | Re-assign in Entra; wait for sync; confirm in the Registry. |
| Reviewer cannot see CSA values on an agent | Reviewer is missing the ability to read the attribute set | Grant Attribute Assignment Reader on the attribute set, or an equivalent role, to the reviewer. |

---

Previous: [UC1 - Agent Discovery](../chapter-uc1-agent-discovery/README.md) · Next: [UC3 - Least-Privilege Access](../chapter-uc3-least-privilege/README.md)
