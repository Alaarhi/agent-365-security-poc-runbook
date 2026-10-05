# Chapter UC6 - Lifecycle & Audit

**Pillar:** Observe / Govern
**What it proves:** an agent can be retired cleanly and provably. Block, deactivate, delete - no orphaned identity, no leftover permission, and an audit trail that satisfies an auditor.

## Section 1 - Roles, portals, and prerequisites

| Task | Role | Notes |
|---|---|---|
| Block / deactivate / delete an agent | **AI Administrator** | Required for lifecycle actions on Agent 365-managed agents. |
| Configure Purview Audit and view Copilot / agent interactions | **Compliance Administrator** (config) + **Audit Reader** (view) | Compliance Admin to enable and configure; Audit Reader to search. |
| View Advanced Hunting entries for the retired agent | **Security Reader** | Least-privilege role to run KQL and read `AgentsInfo`, `CloudAppEvents`. |
| Read-only / validation | **AI Reader** + **Audit Reader** + **Global Reader** | Sufficient to view lifecycle state, audit search, and directory presence. |

Reviewers should hold only the read-only roles. The AI Administrator role is required only when the lifecycle action is executed.

### Task 1 - open the required portals

- Microsoft 365 admin center - <https://admin.cloud.microsoft> > **Agents** > lifecycle actions.
- Microsoft Purview portal - <https://purview.microsoft.com> > **Audit**.
- Microsoft Defender portal - <https://security.microsoft.com> > **Hunting** > **Advanced hunting**.
- Microsoft Entra admin center - <https://entra.microsoft.com> > **Enterprise applications** (confirm Agent ID retired).

### Task 2 - review documentation

| Topic | Documentation |
|---|---|
| Search the audit log | [Search the audit log in Microsoft Purview](https://learn.microsoft.com/purview/audit-search) |
| Advanced hunting overview | [Advanced hunting overview](https://learn.microsoft.com/defender-xdr/advanced-hunting-overview) |
| `AgentsInfo` table | [`AgentsInfo` advanced hunting table](https://learn.microsoft.com/defender-xdr/advanced-hunting-agentsinfo-table) |
| Agent lifecycle in Agent 365 | [Overview of Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/overview) |

### Task 3 - confirm prerequisites

Complete Chapters 0, UC1, UC2, UC4, and UC5. Purview Audit must be on, and the agents should have generated real activity (prompts, tool calls, outputs) before you attempt lifecycle actions - the point of this UC is to prove the trail is complete.

## Section 2 - Lifecycle and audit validation tasks

### Task 1 - retrieve an end-to-end audit trail for one agent

Performed by **Audit Reader**.

1. Open <https://purview.microsoft.com> > **Audit**.
2. Set the search window to cover the agent's active period.
3. Filter by **Workload = Copilot** (or the equivalent for the agent surface) and by the agent identity where possible.
4. Include the `CopilotInteraction` record type (RecordType 261 in the raw log).
5. Export the results.

**Expected result**

- The export contains every interaction across the window.
- Records include `AgentId`, `AccessedResources`, `PolicyDetails`, `Status`, and `SensitivityLabelId` where applicable.
- Any DLP or Purview policy decisions from UC4 appear in the same trail.

Cross-check the same window in Advanced Hunting:

```kql
CloudAppEvents
| where Timestamp between (datetime(START) .. datetime(END))
| where AccountObjectId == "<agent-app-id-or-object-id>"
| project Timestamp, Application, ActionType, AccountDisplayName, IPAddress, RawEventData
| sort by Timestamp desc
```

### Task 2 - block the agent

Performed by **AI Administrator**.

1. Open <https://admin.cloud.microsoft> > **Agents** > select the PoC agent.
2. Choose **Block**.
3. Have the test user (Chapter 0) attempt to invoke the agent.

**Expected result**

- The invocation fails.
- The failure appears in the audit log tied to the agent identity.

### Task 3 - deactivate the agent

Performed by **AI Administrator**.

1. In the Agents view, choose **Deactivate**.
2. Confirm the agent's Entra Agent ID status transitions to reflect the deactivation (see Chapter UC2 and the Entra admin center).
3. Attempt to acquire a token as the agent. Confirm the deny is written to the sign-in log.

**Expected result**

- The Agent ID is paused / disabled in Entra.
- No new tokens are issued to the agent.
- Audit trail shows the deactivate action with actor, timestamp, and target.

### Task 4 - delete the agent (final retire)

Performed by **AI Administrator**.

1. In the Agents view, choose **Delete**.
2. Confirm the confirmation prompt.
3. After deletion, verify:
   - The Agent ID no longer appears in the Agent Registry.
   - The service principal is removed (or tombstoned) in **Entra > Enterprise applications**.
   - `AgentsInfo` in Advanced Hunting reflects `LifecycleStatus = "Deleted"` for the agent.
4. Confirm the retention window for deleted-agent data matches your tenant's configured value (default: 30 days).

**Expected result**

- No orphaned Agent ID.
- No leftover permission grants for the retired agent.
- Historical audit records are preserved for the retention window.

## Section 3 - Evidence and common issues

### Task 1 - capture evidence

- Audit search export for the agent's full active window.
- Screenshots or log entries for the Block, Deactivate, and Delete actions with actor + timestamp.
- Advanced Hunting export showing `LifecycleStatus = "Deleted"`.
- Confirmation that the Entra Agent ID no longer exists (or is disabled).
- Retention window confirmed against tenant setting.

### Task 2 - troubleshoot common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| Audit search returns nothing | Purview Audit not enabled long enough, or wrong workload filter | Confirm audit was on during the activity window; broaden the workload filter and retry. |
| Blocked agent still responds to a user | Cached client session, or the user is hitting a cached response | Wait for cache expiry; retry from a fresh session. |
| Entra Agent ID persists after deletion | Deletion propagation delay | Wait for propagation (up to 30 minutes); confirm in **Enterprise applications**. |
| Advanced Hunting still shows `Active` after deletion | Snapshot ingestion delay | `AgentsInfo` is a periodic snapshot - wait for the next snapshot before treating it as a mismatch. |

---

Previous: [UC5 - Threat Detection & Protection](../chapter-uc5-threat-detection/README.md)
