# Chapter UC2 - Identity & Ownership

**Pillar:** Govern
**What it proves:** anonymous agents become governable identities. Every agent gets a directory identity, a human sponsor, and a lifecycle state, so its access can be attributed and revoked like any other workload identity.

## Roles - least privilege

| Task | Role | Notes |
|---|---|---|
| Enable Entra Agent Identity at environment level | **Agent ID Developer** + Power Platform admin (env-level toggle) | One-time environment setup. |
| Assign / change owners and sponsors | **Agent Registry Administrator** | Required to change ownership. |
| Create and assign custom security attributes (CSA) | **Attribute Definition Administrator** (define set + keys) and **Attribute Assignment Administrator** (write values) | Split by design - definition and assignment are separate roles for governance. |
| Read-only / validation | **Directory Readers** (built-in) and **AI Reader** | Sufficient to view Agent IDs, owners, sponsors, and CSA values in Entra and the Agent Registry. |

The two custom-security-attribute roles are distinct from CA / directory admin roles by design. Grant them explicitly if the PoC uses CSA.

## Portals

- Microsoft Entra admin center - <https://entra.microsoft.com> > **Enterprise applications** and **Custom security attributes**.
- Microsoft 365 admin center - <https://admin.cloud.microsoft> > **Agents** (owner assignment).

## Documentation

| Topic | Documentation |
|---|---|
| Entra Agent ID overview | [Microsoft Entra Agent ID](https://learn.microsoft.com/entra/agent-id/overview) |
| Custom security attributes | [Custom security attributes in Microsoft Entra ID](https://learn.microsoft.com/entra/fundamentals/custom-security-attributes-overview) |
| Recreate Copilot Studio agents in Agent ID | [Recreate Copilot Studio agents in Microsoft Entra Agent ID](https://learn.microsoft.com/entra/agent-id/migrate-copilot-studio-agents-to-agent-id) |

## Prerequisites

Complete [Chapter 0 - Prerequisites](../chapter-0-prerequisites/README.md) and [UC1 - Agent Discovery](../chapter-uc1-agent-discovery/README.md). In addition:

1. Entra Agent Identity is enabled at the Copilot Studio environment level (Power Platform admin center).
2. Each in-scope agent has a nominated sponsor (a human accountable for the agent).

## Setup steps

### 2.1 Enable Entra Agent Identity at the environment level

Performed by an admin with **Agent ID Developer** plus Power Platform environment access.

1. Open <https://admin.powerplatform.microsoft.com>.
2. Go to **Environments** > select the environment used for PoC agents.
3. Enable **Entra Agent Identity** for the environment.

Once enabled, every new Copilot Studio agent created in that environment automatically receives an Entra Agent ID (a service principal with the "Agent" subtype), sponsored by the agent's owner. Legacy agents created before enablement continue using traditional app registrations and can be migrated (see the docs link above).

### 2.2 Assign / confirm sponsors

Performed by **Agent Registry Administrator**.

1. In Entra, go to **Enterprise applications** and open each agent's `-AgentIdentity` service principal.
2. Under **Owners / Sponsors**, confirm the correct human sponsor is listed.
3. If missing, add the sponsor.

### 2.3 (Optional) Create custom security attributes for governance

Performed by **Attribute Definition Administrator** (definition) then **Attribute Assignment Administrator** (values).

1. In Entra, go to **Custom security attributes** > **Add attribute set** and create `AgentGovernance`.
2. Define two attributes inside the set (recommended starter values):

   | Attribute | Type | Allowed values | Why |
   |---|---|---|---|
   | `Project` | String (predefined) | `Agent365PoC` | Groups everything in this PoC; one filter pulls every PoC agent. |
   | `Environment` | String (predefined) | `Pilot`, `Prod` | Prevents PoC agents from being mistaken for production. |

3. Switch to **Attribute Assignment Administrator** context. For each in-scope agent's `-AgentIdentity` service principal, add the assignments:

   | Attribute | Value |
   |---|---|
   | `Project` | `Agent365PoC` |
   | `Environment` | `Pilot` |

## Test - identity and ownership

Performed by anyone with **Directory Readers** + **AI Reader**.

1. In Entra > **Enterprise applications**, filter by the CSA `AgentGovernance/Project = Agent365PoC` (or by name if CSA not used).
2. Confirm every in-scope PoC agent has an **Entra Agent ID** service principal.
3. Confirm each service principal has a named **Owner / Sponsor**.
4. In the Agent Registry (M365 admin center), confirm the same agent shows the same owner.
5. Export the list as evidence.

**Expected result**

- Every in-scope agent has an Entra Agent ID with an assigned sponsor.
- Owner is consistent between Entra and the Agent Registry.
- CSA values (if used) let you filter and enumerate PoC agents in a single query.

## Evidence to capture

- Entra service-principal export for the PoC agents (Object ID, Display name, Owners, CSA values).
- Screenshot of the Agent Registry showing owner column populated.
- If applicable, a filter/query using CSA that returns all PoC agents.

## Common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| No Entra Agent ID for an agent | Entra Agent Identity not enabled at env level, or agent is a legacy pre-enablement Copilot Studio agent | Enable at env level; migrate legacy agents using the doc link above. |
| Owner column blank in Agent Registry but sponsor set in Entra | Sync delay or misconfigured owner mapping | Wait for sync; if persistent, re-assign in Entra and refresh registry. |
| CSA values not visible to reviewer | Reviewer missing Attribute Assignment Reader | Grant read equivalent, or use built-in Directory Readers if CSA reader is not separately provisioned. |

---

Previous: [UC1 - Agent Discovery](../chapter-uc1-agent-discovery/README.md) · Next: [UC3 - Least-Privilege Access](../chapter-uc3-least-privilege/README.md)
