# Prerequisites - Chapter 7: Sensitive data protection (Purview)

> **Goal:** Prepare the accounts, access, and test assets needed for this chapter and its selected optional paths.

Apply the [shared PoC preparation guidance](../README.md#prerequisites-and-reading-order) and agree the [chapter outcomes](README.md#-what-you-proved). Finish dependent build steps before their tests.

## Table of contents

- [Tenant readiness](#tenant-readiness)
- [Prepare accounts and role assignments](#prepare-accounts-and-role-assignments)
- [Audit recording](#audit-recording)
- [Test assets and dependencies](#test-assets-and-dependencies)
- [Plan propagation and test timing](#plan-propagation-and-test-timing)
- [References](#references)

---

## Tenant readiness

**Documentation:** [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started) · [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview) · [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)

Use the task-specific roles in [7.1 Required permissions](README.md#71-required-permissions). Confirm availability rather than assuming the tenant is ready.

Follow the [shared tenant readiness check](../README.md#tenant-readiness) using the chapter permissions and feature prerequisites linked above.

---

## Prepare accounts and role assignments

Alongside the [shared setup and reviewer accounts](../README.md#least-privilege-model), prepare the following scenario accounts:

| Account | Purpose |
|---|---|
| Maker account | Creates the PoC SharePoint site and test agents; needs the permissions specified in the chapter. |
| Authorized and unauthorized test users | Chapter 7 acceptance tests: one user inside and one user outside the sharing scope of the PoC site and agents. No admin role. |
| Intended non-owner account | Discovers and installs the published Copilot Studio agent. Can be the authorized test user if it didn't create the agents. No admin role. |
| Controlled recipient mailbox | Receives the test email from the Copilot Studio email agent. Never use a real personal address. |

Assign the roles in [7.1 Required permissions](README.md#71-required-permissions) using the shared model. Verify each account can access the pages needed for its tasks.

---

## Audit recording

**Documentation:** [Turn auditing on or off](https://learn.microsoft.com/purview/audit-log-enable-disable) · [Audit logs for Copilot and AI applications](https://learn.microsoft.com/purview/audit-copilot)

Performed by a member of **Audit Manager**. Follow the [shared audit recording check](../chapter-05-lifecycle-audit/prerequisites.md#audit-recording) before the activity to be reviewed.

---

## Test assets and dependencies

**Documentation:** [Manage site creation in SharePoint](https://learn.microsoft.com/sharepoint/manage-site-creation) · [Manage sensitivity labels in Office apps](https://learn.microsoft.com/purview/sensitivity-labels-office-apps) · [Enable sensitivity labels for Office files in SharePoint and OneDrive](https://learn.microsoft.com/purview/sensitivity-labels-sharepoint-onedrive-files) · [Build agents in Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/copilot-studio-agent-builder-build) · [Add knowledge sources to an agent in Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/agent-builder-add-knowledge) · [Share and manage agents built in Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/agent-builder-share-manage-agents)

- Make sure a **Confidential** sensitivity label exists and is published to the PoC maker account and test users. If you plan to keep the Excel workbook in 7.4.4 as a comparison source, make sure a **General** label is published as well.
- Prepare the test accounts: an authorized test user, an intended non-owner account (it can be the authorized test user, as long as it didn't create the agents), an unauthorized test user who is outside the sharing scope you choose in 7.4.6 and 7.5.3, and one controlled email recipient.
- Review who has permission to enable blocking and organization-wide sharing before turning anything on.
- Build the sections in order: the two DLP policies (7.2, 7.3), the SharePoint site and files (7.4), the two agents (7.5, 7.6), then the supervision policies (7.7, 7.8), and finally the acceptance checklist (7.9).

Build guidance: [7.4 SharePoint communication site and PoC files](README.md#74-sharepoint-communication-site-and-poc-files) · [7.5 Microsoft 365 Copilot knowledge agent](README.md#75-microsoft-365-copilot-knowledge-agent) · [7.6 Copilot Studio email agent and publication](README.md#76-copilot-studio-email-agent-and-publication)


**Check result**
- Each asset needed for the selected paths is prepared or has a named build task that will finish before its dependent tests.

---

## Plan propagation and test timing

**Documentation:** [Create and configure sensitivity labels and their policies](https://learn.microsoft.com/purview/create-sensitivity-labels) · [Learn about the Microsoft 365 Copilot and Copilot Chat DLP location](https://learn.microsoft.com/purview/dlp-microsoft365-copilot-location-learn-about)

| Configuration | Documented propagation window |
|---|---|
| Sensitivity label and label policy changes | Up to 24 hours |
| DLP policy changes for the Microsoft 365 Copilot and Copilot Chat location | Up to 4 hours |

> ⚠️ **Watch out:** Allow for the documented propagation window and verify the actual configuration or signal before testing. Elapsed time alone is not proof that a change has applied.

---

## References

- [Get started with Microsoft Agent 365](https://learn.microsoft.com/microsoft-agent-365/get-started)
- [Agent management in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview)
- [Frontier program](https://learn.microsoft.com/microsoft-agent-365/frontier)
- [Turn auditing on or off](https://learn.microsoft.com/purview/audit-log-enable-disable)
- [Audit logs for Copilot and AI applications](https://learn.microsoft.com/purview/audit-copilot)
- [Manage site creation in SharePoint](https://learn.microsoft.com/sharepoint/manage-site-creation)
- [Manage sensitivity labels in Office apps](https://learn.microsoft.com/purview/sensitivity-labels-office-apps)
- [Enable sensitivity labels for Office files in SharePoint and OneDrive](https://learn.microsoft.com/purview/sensitivity-labels-sharepoint-onedrive-files)
- [Build agents in Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/copilot-studio-agent-builder-build)
- [Add knowledge sources to an agent in Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/agent-builder-add-knowledge)
- [Share and manage agents built in Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/agent-builder-share-manage-agents)
- [Create and configure sensitivity labels and their policies](https://learn.microsoft.com/purview/create-sensitivity-labels)
- [Learn about the Microsoft 365 Copilot and Copilot Chat DLP location](https://learn.microsoft.com/purview/dlp-microsoft365-copilot-location-learn-about)

---

> **Ready?** Continue to the [chapter](README.md). →
