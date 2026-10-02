# Chapter UC3 - Least-Privilege Access

**Pillar:** Govern
**What it proves:** a compromised agent reaches only what you scoped it to. Broad standing access is replaced by a bounded, just-in-time, revocable grant, and the deny is provable in the sign-in log.

## Roles - least privilege

| Task | Role | Notes |
|---|---|---|
| Create and enforce Conditional Access policies for agents | **Conditional Access Administrator** | Required to create, edit, and enable CA policies. |
| Reference a custom security attribute inside a CA policy | **Conditional Access Administrator** + **Attribute Assignment Reader** | Reader is required to resolve the attribute in the policy builder; without it the attribute does not appear. |
| Create and manage CSA attribute sets and definitions | **Attribute Definition Administrator** | Required for scaling pattern 2 (CSA-based). Global Administrator does not grant this. |
| Assign CSA values to an agent | **Attribute Assignment Administrator** | Required for scaling pattern 2. Separate from the definition role by design. |
| Create access packages and JIT policies | **Identity Governance Administrator** | Required for Entitlement Management. |
| Configure Lifecycle Workflows (sponsor change) | **Lifecycle Workflows Administrator** | Required only if sponsor-change workflows are in scope. |
| Read-only / validation | **Global Reader** or **Reports Reader** | Sufficient to view CA policies, sign-in logs, and access package assignments. Use for reviewers. |
| Read-only for sign-in logs only | **Security Reader** | Alternative least-privilege role for reading sign-in logs and blocked-token events. |

Grant the read-only role first. Only the person creating the policy needs the Conditional Access Administrator role.

## Portals

- Microsoft Entra admin center - <https://entra.microsoft.com>
  - **Protection** > **Conditional Access** - policies for agent identities.
  - **Identity Governance** > **Entitlement management** > **Access packages** - JIT grants.
  - **Identity Governance** > **Lifecycle Workflows** - sponsor changes.
  - **Monitoring** > **Sign-in logs** - allow/deny evidence.

## Documentation

| Topic | Documentation |
|---|---|
| Conditional Access for agents | [Conditional Access for agents](https://learn.microsoft.com/entra/identity/conditional-access/agent-id) |
| Target agent identities in CA | [Target agent identities in Conditional Access](https://learn.microsoft.com/entra/identity/conditional-access/howto-target-agent-identities) |
| Recommended policies for autonomous agents | [Recommended policies for autonomous agents](https://learn.microsoft.com/entra/identity/conditional-access/policy-autonomous-agents) |
| Entitlement management | [What is entitlement management?](https://learn.microsoft.com/entra/id-governance/entitlement-management-overview) |
| Lifecycle workflows | [Lifecycle Workflows overview](https://learn.microsoft.com/entra/id-governance/what-are-lifecycle-workflows) |
| Community walkthrough (risk + CSA, with verification script) | [Conditional Access for Agents: Blocking Agent Identities with Risk and Custom Security Attributes](https://derkvanderwoude.medium.com/conditional-access-for-agents-blocking-agent-identities-with-risk-and-custom-security-attributes-2ec3d6bf995b) by Derk van der Woude (Microsoft Security MVP) |

## Prerequisites

Complete [Chapter 0 - Prerequisites](../chapter-0-prerequisites/README.md), [UC1](../chapter-uc1-agent-discovery/README.md), and [UC2](../chapter-uc2-identity-ownership/README.md).

## How Conditional Access enforces on agents (token-exchange model)

A modern Entra Agent ID authenticates in two legs:

| Token leg | What it does | CA behavior |
|---|---|---|
| **T1** - blueprint request | The agent's **blueprint app** authenticates to Microsoft Entra and requests a token-exchange token, passing `fmi_path` pointing at the **agent identity's** object ID. | T1 is not evaluated by Conditional Access for agents. The blueprint can always obtain T1. |
| **T2** - agent-identity request | The agent identity presents T1 as a client assertion (`jwt-bearer`) and exchanges it for a resource token (for example a Microsoft Graph token). | **CA for agents evaluates and enforces here.** When a policy blocks, T2 fails with an AADSTS error. T1 still succeeds. |

Two consequences:

- A "block" shows up as a **T2 failure** - the T1 success in the log does not mean CA failed.
- The sign-in log evidence for UC3 (and any audit of agent CA) must come from the **service-principal sign-ins** view, filtered to the agent identity, looking at the T2 exchange.

For a vendor-neutral community walkthrough with a PowerShell test harness that exercises both legs, see [Blue161616/Agent-Identity/AgentID-AuthenticationFlow.ps1](https://github.com/Blue161616/Agent-Identity/blob/main/AgentID-AuthenticationFlow.ps1) referenced from the article in the Documentation table above.

## Setup - Conditional Access policy for agent identities (Report-only)

Performed by **Conditional Access Administrator**.

1. Open <https://entra.microsoft.com> > **Protection** > **Conditional Access** > **Policies** > **New policy**.
2. Name: `PoC - Agent access boundary (Report-only)`.
3. **Assignments** > **Users, agents or workload identities** > **What does this policy apply to?** > **Agents**.
   - **Select agent identities**: pick the PoC agents (their `-AgentIdentity` service principals).
   - Alternatively: select the agent blueprint principal(s) to cover every agent derived from those blueprints, including future ones.
4. **Target resources** > **Include** > **Select resources**: pick only the resources the PoC agents actually call (for example Microsoft Graph and any Foundry / Power Platform APIs). This scopes the boundary.
5. Optionally, **Conditions** > **Agent risk (Preview)** > `High` (and `Medium`) so the policy fires only on risky-agent signals.
6. **Access controls** > **Grant** > **Block**. Block is the only enforcement control available for agent identities (there is no interactive remediation for an agent).
7. **Enable policy** = **Report-only**.
8. **Create**.

Report-only lets the agent keep working while every token request is evaluated and written to the sign-in log as "would have been blocked / granted". Flip to **On** after the log looks correct.

## Scaling pattern 1 - risk-based blocking (dynamic)

Use when you want the whole agent fleet governed by one policy that reacts to risky-agent signals from Microsoft Entra ID Protection.

### Policy

Performed by **Conditional Access Administrator**.

1. In Entra, create a new CA policy named `Block high-risk agent identities`.
2. **Assignments** > **Users, agents or workload identities** > **Agents** > **All agent identities**.
3. **Target resources** > **All resources**. (The "All agent resources" scope does **not** cover a raw Microsoft Graph `.default` token exchange - see Common issues at the end of this chapter.)
4. **Conditions** > **Agent risk** > **High** (optionally also **Medium**).
5. **Access controls** > **Grant** > **Block access**.
6. **Enable policy** = **Report-only** first, then **On** after validation.

### Verify

To test without waiting for real risky behavior, synthesize risk against a lab agent with the Microsoft Graph Identity Protection `confirmCompromised` action:

```http
POST https://graph.microsoft.com/beta/identityProtection/riskyAgents/confirmCompromised
Content-Type: application/json

{ "agentIds": [ "<agent-object-id>" ] }
```

A `204 No Content` confirms the agent is now in confirmed-compromised state. It appears under **Entra ID** > **Protection** > **ID Protection** > **Risky agents**.

Then exercise the agent (or run the T1/T2 verification script) and confirm the T2 leg is blocked with an AADSTS code in the sign-in log.

## Scaling pattern 2 - attribute-based blocking with custom security attributes (static)

Use when you want to differentiate agents by approval state, department, or environment without enumerating object IDs.

### Mental model - who vs what

A CA-for-agents policy has two independent filter sides:

| Side | What it selects | Example |
|---|---|---|
| **Agent side** (Users or agents > Select agent identities based on attributes) | **Which agents the policy applies to.** The *who*. | `AgentApprovalStatus Contains IT_Approved` |
| **Resource side** (Target resources > Edit filter) | **Which resources are protected.** The *what*. | `ResourceCategory eq HR` |

Common modelling error: putting the discriminator on the wrong side. "Block all agents except approved ones" is a statement about the *who*, so it belongs on the **agent side**. Putting an approval filter on the resource side would block **everyone** from those resources, approved agents included.

There is no join between the two sides. The filters evaluate independently and the grant applies to the **intersection**. "Only HR agents reach HR resources" is two static scopes, not a dynamic comparison.

### Prerequisites specific to CSA

- CSA definition type must be **String**. A Boolean attribute assigns successfully but silently never matches a CA filter - the filter builder will not even show it.
- Attribute roles are split by design and **Global Administrator does not grant them**:
  - **Attribute Definition Administrator** - create and manage attribute sets and definitions.
  - **Attribute Assignment Administrator** - write attribute values on an agent.
  - **Attribute Assignment Reader** - required by the Conditional Access Administrator who references the attribute inside a policy.

### Step 1 - define the classification

Reuse the `AgentGovernance` attribute set from [UC2](../chapter-uc2-identity-ownership/README.md#2-3-optional-setup---custom-security-attributes-for-governance), or create a dedicated one for approval status.

Example definition (predefined string, collection):

| Field | Value |
|---|---|
| Set | `AgentAttributes` |
| Name | `AgentApprovalStatus` |
| Type | **String** |
| Collection | true |
| Pre-defined values | `New`, `In_Review`, `IT_Approved`, `HR_Approved`, `Finance_Approved` |

Graph POST, if you need to script it:

```http
POST https://graph.microsoft.com/v1.0/directory/customSecurityAttributeDefinitions
Content-Type: application/json

{
  "attributeSet": "AgentAttributes",
  "name": "AgentApprovalStatus",
  "type": "String",
  "status": "Available",
  "isCollection": true,
  "usePreDefinedValuesOnly": true,
  "allowedValues": [
    { "id": "New",              "isActive": true },
    { "id": "In_Review",        "isActive": true },
    { "id": "IT_Approved",      "isActive": true },
    { "id": "HR_Approved",      "isActive": true },
    { "id": "Finance_Approved", "isActive": true }
  ]
}
```

### Step 2 - assign the label to the agent

In the portal: **Entra ID** > **Agents** > **Agent identities** > open the agent > **Custom security attributes** > assign `AgentAttributes/AgentApprovalStatus = IT_Approved`.

Via Graph (PATCH on the agent's service principal, requires Attribute Assignment Administrator):

```http
PATCH https://graph.microsoft.com/v1.0/servicePrincipals/<agent-object-id>
Content-Type: application/json

{
  "customSecurityAttributes": {
    "AgentAttributes": {
      "@odata.type": "#Microsoft.DirectoryServices.CustomSecurityAttributeValue",
      "AgentApprovalStatus@odata.type": "#Collection(String)",
      "AgentApprovalStatus": ["IT_Approved"]
    }
  }
}
```

### Step 3 - build the policy using the null-safe "exclude approved" pattern

Performed by **Conditional Access Administrator** who also holds **Attribute Assignment Reader**.

Read the policy as **"block everyone, then carve out the approved."**

| Setting | Value |
|---|---|
| Policy name | `Block unapproved agent identities` |
| Users or agents > Include | **All agent identities** |
| Users or agents > Exclude | Agents where `AgentAttributes_AgentApprovalStatus Contains IT_Approved` |
| Target resources | **All resources** |
| Grant | **Block access** |
| State | **Report-only** first, then **On** |

Why "exclude = Contains IT_Approved" is the safe pattern:

- An agent that has `IT_Approved` matches the exclusion, is removed from the include set, and passes.
- An agent with any other value (`New`, `In_Review`, missing attribute) does **not** match the exclusion, stays inside **All agent identities**, and is blocked.
- A missing attribute is treated as "not approved" without extra null handling.

Pair this baseline with one policy per classification that excludes only its own label and targets only its own resources. Never exclude one department's agents from another department's policy - that opens cross-department reach by design.

### Verify

Approved agent (CSA = `IT_Approved`): the T2 Graph token exchange succeeds, the sign-in log shows an allow entry.

Unapproved or unlabeled agent: the T2 Graph token exchange fails with an AADSTS code, the sign-in log shows a deny entry with the policy name attached.

The same verification script linked in Documentation (`AgentID-AuthenticationFlow.ps1`) runs both legs so you can observe T1 success + T2 block.

## Setup - just-in-time access via access package (optional)

Performed by **Identity Governance Administrator**.

1. Open <https://entra.microsoft.com> > **Identity Governance** > **Entitlement management** > **Access packages** > **New access package**.
2. Scope the package to the specific resource(s) the agent needs.
3. Set expiry (for example 8 hours) so grants are time-bounded.
4. Assign to the agent identity (or a group containing agent identities).

**Check result (Setup role)**

- Access package assignment appears on the agent.
- The agent can invoke the target resource only within the grant window.

## Setup - sponsor change via Lifecycle Workflows (optional)

Performed by **Lifecycle Workflows Administrator**.

1. Open <https://entra.microsoft.com> > **Identity Governance** > **Lifecycle Workflows**.
2. Create a new workflow from the template **"Agent sponsor job profile change"** (Mover / Agents category).
3. Configure the scope condition to match the attribute change you want to trigger on (for example `department -eq "Compliance"`).
4. Review the two default tasks:
   - Send email to manager about sponsorship changes.
   - Transfer agent identity sponsorships to manager.
5. Save.

## Test - CA block is provable in sign-in logs

Performed by anyone with **Global Reader**, **Reports Reader**, or **Security Reader**.

1. Have the PoC agent attempt an action outside the scoped resources (for example a Graph endpoint not on the allow list).
2. Open <https://entra.microsoft.com> > **Monitoring** > **Sign-in logs** > **Service principal sign-ins**.
3. Filter by the agent's `AppId` or Display name.
4. Confirm a **Failure** entry with **Conditional Access = Failure** and the policy name matching your PoC policy.

**Expected result**

- The out-of-scope call is logged as blocked with the policy name attached.
- A parallel in-scope call is logged as allowed.

## Test - JIT grant expires

Performed by anyone with **Global Reader**.

1. Confirm the agent can invoke the target resource inside the grant window.
2. After the grant window expires, retry and confirm the call fails and appears as denied in the sign-in log.

## Test - sponsor change workflow (if configured)

Performed by anyone with **Global Reader** on the workflow history.

1. Change the sponsor's attribute so they leave scope (for example department change).
2. Run the workflow on demand.
3. Confirm the sponsor is transferred to the manager and the notification email is sent.

## Evidence to capture

- Screenshot of the CA policy in **Report-only** and then in **On** state.
- Sign-in log export showing at least one Deny and one Allow for the same agent identity within a short window.
- Access package assignment record with expiry.
- Lifecycle workflow run history if used.

## Common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| CA policy has no effect | Left in Report-only, or the agent identity not selected in Assignments | Flip to On; confirm the correct `-AgentIdentity` service principal is selected. |
| Sign-in log shows no service principal entries | Wrong log view (interactive vs service principal) | Switch to the **Service principal sign-ins** tab. |
| Agent still calls a resource after grant expiry | Cached token still valid | Wait for token expiry, or force token refresh; grants become effective for new tokens. |
| Lifecycle workflow does not fire | Scope condition does not match, or user was not "in scope" at the time | Adjust the scope filter to match the value you change to; re-run on demand. |
| CSA-based policy builds in the portal but target field is missing | Attribute type is Boolean | Recreate the attribute as **String**. Boolean attributes silently never match a CA filter. |
| CSA-based policy builds but never fires | Resource scope is **All agent resources** | Change Target resources to **All resources** (or the specific resource the agent calls). "All agent resources" does not cover a Microsoft Graph `.default` token exchange. |
| CSA Conditional Access policy cannot see the attribute | CA Admin does not hold **Attribute Assignment Reader** | Add Attribute Assignment Reader to the CA Admin building the policy. |
| Risk-based policy does not fire for a known risky agent | Agent risk condition set to the wrong level, or the agent was not actually marked risky | Confirm **Entra ID > Protection > ID Protection > Risky agents** shows the expected risk level; synthesize a test risk via Graph `confirmCompromised` if needed. |
| T1 token succeeds but you expected a block | CA for agents enforces on the **T2** leg only | T1 success is normal; look at the T2 exchange (the Graph `.default` token request) in the sign-in log. |

---

Previous: [UC2 - Identity & Ownership](../chapter-uc2-identity-ownership/README.md) · Next: [UC4 - Sensitive Data Protection](../chapter-uc4-sensitive-data-protection/README.md)
