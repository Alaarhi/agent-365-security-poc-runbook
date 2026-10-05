# Chapter UC3 - Least-Privilege Access

**Pillar:** Govern
**What it proves:** a compromised agent reaches only what you scoped it to. Broad standing access is replaced by a bounded, just-in-time, revocable grant, and the deny is provable in the sign-in log.

## Section 1 - Roles, portals, and prerequisites

| Task | Role | Notes |
|---|---|---|
| Create and enforce Conditional Access policies for agents | **Conditional Access Administrator** | Required to create, edit, and enable CA policies. |
| Mark an agent as risky for the test (Graph `confirmCompromised`) | **Security Administrator** or **Security Operator** | Required to call Identity Protection APIs. |
| Create access packages and JIT policies | **Identity Governance Administrator** | Required for Entitlement Management. |
| Configure Lifecycle Workflows (sponsor change) | **Lifecycle Workflows Administrator** | Required only if sponsor-change workflows are in scope. |
| Read-only / validation | **Global Reader** or **Reports Reader** | Sufficient to view CA policies, sign-in logs, and access package assignments. Use for reviewers. |
| Read-only for sign-in logs only | **Security Reader** | Alternative least-privilege role for reading sign-in logs and blocked-token events. |

Grant the read-only role first. Only the person creating the policy needs the Conditional Access Administrator role.

### Task 1 - open the required portals

- Microsoft Entra admin center - <https://entra.microsoft.com>
  - **Protection** > **Conditional Access** - policies for agent identities.
  - **Identity Governance** > **Entitlement management** > **Access packages** - JIT grants.
  - **Identity Governance** > **Lifecycle Workflows** - sponsor changes.
  - **Monitoring** > **Sign-in logs** - allow/deny evidence.

### Task 2 - review documentation

| Topic | Documentation |
|---|---|
| Conditional Access for agents | [Conditional Access for agents](https://learn.microsoft.com/entra/identity/conditional-access/agent-id) |
| Target agent identities in CA | [Target agent identities in Conditional Access](https://learn.microsoft.com/entra/identity/conditional-access/howto-target-agent-identities) |
| Recommended policies for autonomous agents | [Recommended policies for autonomous agents](https://learn.microsoft.com/entra/identity/conditional-access/policy-autonomous-agents) |
| Lab reference - risk and custom security attributes | [Conditional Access for Agents: Blocking Agent Identities with Risk and Custom Security Attributes](https://derkvanderwoude.medium.com/conditional-access-for-agents-blocking-agent-identities-with-risk-and-custom-security-attributes-2ec3d6bf995b) |
| Entitlement management | [What is entitlement management?](https://learn.microsoft.com/entra/id-governance/entitlement-management-overview) |
| Lifecycle workflows | [Lifecycle Workflows overview](https://learn.microsoft.com/entra/id-governance/what-are-lifecycle-workflows) |

### Task 3 - confirm prerequisites

Complete [Chapter 0 - Prerequisites](../chapter-0-prerequisites/README.md), [UC1](../chapter-uc1-agent-discovery/README.md), and [UC2](../chapter-uc2-identity-ownership/README.md).

---

## Section 2 - Conditional Access

### Task 1 - setup CA policy to block high-risk agents

Performed by **Conditional Access Administrator**.

1. Open <https://entra.microsoft.com> > **Protection** > **Conditional Access** > **Policies** > **New policy**.
2. Name: `Block high-risk agent identities`.
3. **Assignments** > **Users, agents or workload identities** > **Agents** > **All agent identities**.
4. **Target resources** > **All resources**.
5. **Conditions** > **Agent risk** > **High**.
6. **Access controls** > **Grant** > **Block access**.
7. **Enable policy** = **Report-only** first (lets you observe the deny in the sign-in log without actually blocking the agent), then **On** after validation.
8. **Create**.

### Task 2 - make an agent risky and confirm it is blocked

#### Agent type required for this flow

Use a **non-OBO Agent 365 agent identity**: an autonomous agent registered in Agent 365 whose **agent blueprint app** authenticates with **client credentials** (client secret or certificate) and then exchanges the token for the **agent identity** through the FMI/token-exchange flow.

Do **not** use an OBO / delegated-user AI Teammate flow for this test. This scenario is meant to prove Conditional Access enforcement on the **agent identity's service-principal token exchange**, not a user-delegated OBO token. If the agent only obtains tokens on behalf of a signed-in user, this lab will not clearly prove the high-risk agent identity block.

The expected authentication shape is:

1. **T1 - blueprint token-exchange token:** the blueprint app uses `client_credentials` with scope `api://AzureADTokenExchange/.default` and `fmi_path=<agent-object-id>`.
2. **T2 - resource token as the agent identity:** the agent identity uses T1 as a JWT bearer client assertion to request the resource token, for example `https://graph.microsoft.com/.default`.
3. Conditional Access for agents evaluates the **T2** request. T1 can still succeed; the block is proven when T2 fails.

#### Step 1 - make the lab agent high-risk

Rather than wait for real risky behavior, flag a lab agent directly through Microsoft Graph. Any user with permission to run the Identity Protection `confirmCompromised` action can do this (for example from Graph Explorer):

```http
POST https://graph.microsoft.com/beta/identityProtection/riskyAgents/confirmCompromised
Content-Type: application/json

{ "agentIds": [ "<agent-object-id>" ] }
```

A `204 No Content` response confirms the risk state. The agent appears under **Entra ID** > **Protection** > **ID Protection** > **Risky agents** as **High** risk.

#### Step 2 - exercise the agent

Have the **non-OBO, client-credentials-based agent** attempt a call that requires a new resource token (for example a Microsoft Graph request as part of its normal flow).

For a deterministic lab test, run a two-leg token-exchange script against the same agent identity:

1. Request T1 with the blueprint app credential, `scope=api://AzureADTokenExchange/.default`, and `fmi_path=<agent-object-id>`.
2. Request T2 with `client_assertion=T1`, `client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer`, and the target resource scope, for example `https://graph.microsoft.com/.default`.
3. Treat a T2 failure with the Conditional Access policy in the sign-in log as the successful test result.

The reference article includes a sample PowerShell script for this exact T1-to-T2 validation pattern: [AgentID-AuthenticationFlow.ps1](https://github.com/Blue161616/Agent-Identity/blob/main/AgentID-AuthenticationFlow.ps1).

#### Step 3 - confirm the block in the sign-in log

Performed by anyone with **Global Reader**, **Reports Reader**, or **Security Reader**.

1. Open <https://entra.microsoft.com> > **Monitoring & health** > **Sign-in logs**.
2. Switch to the **Service principal sign-ins** tab.
3. Filter by the agent's name or App ID.
4. Confirm a **Failure** entry with **Conditional Access = Failure** and the policy name `Block high-risk agent identities`.

#### Expected result

- The agent's token request fails after it is marked high-risk.
- The failure is on the **T2 resource-token request** for the **agent identity**, not on a user OBO token.
- The sign-in log shows the deny with the policy name attached.
- A separate run against a low-risk agent (no `confirmCompromised` flag) succeeds, proving the policy fires on risk, not on identity.

#### Cleanup

Dismiss or confirm-safe the risk state on the lab agent when you are done so it does not sit in a confirmed-compromised state:

**Entra ID** > **Protection** > **ID Protection** > **Risky agents** > select the agent > **Confirm safe** (or **Dismiss**).

---

## Section 3 - Lifecycle Workflow sponsor change

### Task 1 - setup sponsor change via Lifecycle Workflows

Performed by **Lifecycle Workflows Administrator**.

1. Open <https://entra.microsoft.com> > **Identity Governance** > **Lifecycle Workflows**.
2. Create a new workflow from the template **"Agent sponsor job profile change"** (Mover / Agents category).
3. Configure the scope condition to match the attribute change you want to trigger on (for example `department -eq "Compliance"`).
4. Review the two default tasks:
   - Send email to manager about sponsorship changes.
   - Transfer agent identity sponsorships to manager.
5. Save.

### Task 2 - test sponsor change workflow

Performed by anyone with **Global Reader** on the workflow history.

1. Change the sponsor's attribute so they leave scope (for example department change).
2. Run the workflow on demand.

#### Expected result

- The sponsor is transferred to the manager automatically.
- The notification email is sent to the manager.
- The workflow run history shows the transfer with the actor, timestamp, and target agent.

---

## Section 4 - Just-in-time access via access package (Optional)

### Task 1 - setup just-in-time access via access package

Performed by **Identity Governance Administrator**.

1. Open <https://entra.microsoft.com> > **Identity Governance** > **Entitlement management** > **Access packages** > **New access package**.
2. Scope the package to the specific resource(s) the agent needs.
3. Set expiry (for example 8 hours) so grants are time-bounded.
4. Assign to the agent identity (or a group containing agent identities).

### Task 2 - test JIT grant expiry

Performed by anyone with **Global Reader**.

1. Confirm the agent can invoke the target resource inside the grant window.
2. After the grant window expires, retry.

#### Expected result

- Inside the grant window: the call succeeds.
- After the grant expires: the call fails and appears as denied in the sign-in log.

## Section 5 - Evidence

### Task 1 - capture evidence

- Screenshot of the CA policy in **Report-only** and then in **On** state.
- Sign-in log export showing at least one Deny and one Allow for the same agent identity within a short window.
- Access package assignment record with expiry.
- Lifecycle workflow run history if sponsor change is tested.

## Section 6 - Troubleshooting

### Task 1 - troubleshoot common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| CA policy has no effect | Left in Report-only | Flip to On after the sign-in log looks correct. |
| Risk-based policy does not fire for a known risky agent | Agent risk level does not match the policy condition | Confirm **Entra ID > Protection > ID Protection > Risky agents** shows **High** risk; synthesize the risk via Graph `confirmCompromised` if needed. |
| Sign-in log shows no service principal entries | Wrong log view (interactive vs service principal) | Switch to the **Service principal sign-ins** tab. |
| Agent still calls a resource after grant expiry (JIT) | Cached token still valid | Wait for token expiry, or force token refresh; grants become effective for new tokens. |
| Lifecycle workflow does not fire | Scope condition does not match, or user was not "in scope" at the time | Adjust the scope filter to match the value you change to; re-run on demand. |

---

Previous: [UC2 - Identity & Ownership](../chapter-uc2-identity-ownership/README.md) · Next: [UC4 - Sensitive Data Protection](../chapter-uc4-sensitive-data-protection/README.md)
