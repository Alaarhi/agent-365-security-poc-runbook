# Copilot instructions - Microsoft Agent 365 PoC runbook

Use these instructions when creating or editing this repository's customer-facing documentation and samples. Keep content self-contained, precise, and grounded in documented capabilities and verifiable evidence.

## 1. Purpose and writing style

This runbook helps a PoC coordinator, setup administrators, developers, and read-only reviewers validate Microsoft Agent 365 across **Observe**, **Govern**, and **Secure**.

- Write practical, concrete instructions for readers who understand administration but may be new to Agent 365.
- Use concise, professional language. Remove authoring commentary, internal framing, and references to unrelated projects.
- Explain what a control proves, why it matters, who performs the task, and how to verify the result.
- Use observable pass/fail criteria, not claims such as "the agent is secure" or "everything works."
- Keep setup, test execution, and independent review distinct.
- Preserve technical meaning during formatting edits. Do not silently change permissions, policy modes, commands, expected results, or feature scope.

---

## 2. Repository layout and scope

| Location | Purpose |
|---|---|
| Root `README.md` | Entry point, chapter index, reading order, least-privilege model, and portal overview |
| Chapter-local `prerequisites.md` | Applicable tenant checks, accounts, role assignments, test assets, and readiness verification |
| `chapter-01-*` and `chapter-02-*` | Observe: discovery, inventory, third-party platforms, and custom agents |
| `chapter-03-*` through `chapter-05-*` | Govern: identity, ownership, tools, MCP, lifecycle, and audit |
| `chapter-06-*` through `chapter-09-*` | Secure: access, data protection, threat protection, and Shadow AI |
| Chapter-local `samples/` folders | Scripts, queries, configuration, and agent examples used by that chapter |
| `Agent-365-Security-PoC-Runbook.pdf` | Combined reading copy of the runbook |

Keep the existing chapter folders and `README.md` entry points. Do not split chapters into separate step files or introduce a separate build-order page without a request.

Chapter 2 has two independent guides: `README.md` for connected platforms and `agent-365-sdk.md` for the SDK path. Keep their permissions, tests, evidence, and references path-specific, with shared preparation in `prerequisites.md`. Preserve the existing Chapter 2 topic numbers across both guides.

Place new screenshots in the relevant chapter's `screenshots/` folder with descriptive kebab-case filenames. Keep executable assets separate from screenshots and link to them from the task that uses them.

---

## 3. Root README structure

When revising the landing page, organize it in this order:

1. **Title and goal:** a short `> **Goal of this PoC:** ...` blockquote.
2. **Chapters:** retain the index table with `# | Pillar | Chapter | Prerequisites | What it proves`, linking directly to each chapter and its preparation page. This table is the outcome overview; do not repeat it in a separate generic outcomes list.
3. **Prerequisites and reading order:** keep shared scope, test-data, and evidence-storage guidance here, and link to chapter-specific preparation. Identify Chapters 1 and 3 as foundations where applicable, without requiring unrelated chapters. Do not add a generic requirements table.
4. **How to use this runbook:** briefly explain navigation, estimates, and evidence checks.
5. **Least-privilege model**, **Portals used**, and **Repository content:** keep the shared account and role-assignment model here, with the practical reference material and preview notice.
6. **Key references:** relevant, verified Microsoft Learn links.

Keep detailed timing on the chapter pages rather than adding a duration column to the root index. End the page after a separator with a clear start pointer:

> **Ready?** Start with [Chapter 1 - Agent discovery and inventory](../chapter-01-agent-discovery/README.md) →

The example above is relative to this instructions file. In the root README, use `chapter-01-agent-discovery/README.md` instead.

---

## 4. Chapter structure

Preserve the runbook's numbered chapter format and use this order for new or substantially revised chapters:

1. **Title:** `# Chapter N - <topic>`.
2. **Pillar**, **What it proves**, and **Success criteria:** state the pillar and purpose, then link to the outcome checklist. Keep the measurable outcomes in that checklist only, with optional outcomes labeled explicitly.
3. **Topics and time guide:** use one linked table for numbered topics and their estimated hands-on time. Mark optional topics and identify alternative paths. Link to the outcome checklist and references alongside it; do not repeat the topics in a separate table of contents.
4. **`## N.1 Required permissions`:** list tasks, least-privilege roles, and the sections that need them. Clearly distinguish setup roles from read-only / validation roles.
5. **Before you start:** link directly to chapter-local `prerequisites.md`. Keep detailed tenant checks, scenario accounts, groups, setup instructions, and dependencies there rather than repeating them in the chapter.
6. **Setup sections:** use `## N.2 <verb phrase>` and `### N.2.1 <task>`. Start each setup section with a **Documentation:** line linking to its authoritative sources.
7. **Test and validation:** identify the actor, test action, expected result, and control or negative case where relevant.
8. **Evidence** and **Troubleshooting:** retain numbered sections. Do not include post-PoC teardown sections or instructions to delete test agents and policies after completion. Preserve deletion, restoration, and policy changes when they are the control being tested.
9. **Outcome checklist:** use an unnumbered `## ✅ What you proved` section with `- [ ]` items. This is the canonical success-criteria list, not a copy of another list.
10. **References:** summarize the page's official documentation links in a deduplicated list at the bottom, while retaining section-level **Documentation:** links.
11. **Navigation:** link back to the root index and to the next chapter. The final chapter returns to the index. Navigation does not replace dependency guidance.

Prerequisite pages should have a goal, a table of contents, chapter-specific preparation steps with checks, consolidated references, and a link back to the chapter. Link to the root's shared scope and role-assignment guidance instead of copying it. List scenario-specific accounts; refer to the shared setup and reviewer accounts. Describe each test asset once and link to its build steps. Do not add a generic checklist that repeats the section checks. State which setup tasks must finish before testing; do not create circular chapter dependencies.

Chapter 8 keeps all enablement, setup permissions, connection steps, rule creation, and test-data preparation in `prerequisites.md`. Its chapter page contains test permissions, investigation, runtime validation, containment, and test evidence. Enabling or disabling a prepared test rule remains part of its audit/block comparison.

For each actionable task, use this pattern:

```markdown
### N.2.1 Configure the test control

Performed by **<least-privilege setup role>**.

1. Open the relevant portal and select **Area** > **Page**.
2. Apply the documented configuration to the PoC test object.

**Check result**
- State the exact configuration or observable outcome to confirm.
```

Keep **Check result** for immediate setup verification and **Expected result** for test outcomes. Name the read-only reviewer role when independent validation is required.

Time guides use approximate author estimates, not measured benchmarks or delivery guarantees. Estimate focused work on one agent or a small PoC test set after prerequisites are ready. Separate optional and alternative paths; do not add mutually exclusive platform examples into a single total. Exclude service propagation, ingestion, approval queues, and unattended installation or deployment waits, and point readers to the prerequisite timing guidance. Include permission review and evidence collection; show troubleshooting as "As needed" rather than assuming every reader will encounter problems. Keep the tone practical and reassuring without understating the work.

---

## 5. Formatting and callouts

- Use sentence case for new headings, preserving official product names and exact UI labels.
- Place a `---` separator before each `##` heading except the first on the page. Do not add separators inside code fences.
- Keep paragraphs short. Use numbered lists for actions, bullets for requirements, and tables for roles, comparisons, test cases, evidence, and troubleshooting.
- Bold UI labels and roles. Use backticks for commands, identifiers, filenames, and configuration values; use actual links when readers should open a file.
- Tag every code fence: `powershell`, `bash`, `json`, `yaml`, `python`, `typescript`, `csharp`, `kusto` / `kql`, or `text` as appropriate.
- Keep the root README focused on navigation and outcomes, without an overview diagram. Mermaid is appropriate for chapter-specific relationships. Do not repeat the same idea in multiple diagrams; align ASCII borders.
- Use relative Markdown links for repository content, encoding spaces and parentheses in link destinations.
- Keep tables of contents synchronized with headings and GitHub-generated anchors. Check punctuation, repeated headings, and leading emoji rather than guessing anchors.

Use these callouts sparingly and consistently:

| Callout | Use |
|---|---|
| `> 💡 **Why this matters:** ...` | Explain a design choice or the reason for a control |
| `> ⚠️ **Watch out:** ...` | Highlight a concrete pitfall, limitation, or propagation delay |
| `> 🔍 **Prove it to yourself:** ...` | Offer optional additional verification |
| `## ✅ What you proved` | Close a chapter with an outcome checklist |

Callouts supplement, rather than replace, **Documentation**, **Performed by**, **Check result**, and **Expected result**.

Apply the target style to new or substantially revised pages. For a small correction, keep the diff focused; do not reformat unrelated sections, renumber tasks, or break existing anchors.

Keep each instruction or outcome in one canonical location and use targeted links elsewhere. Preserve chapter-specific requirements, test actions, and immediate verification checks. Section-level documentation links and the consolidated reference list serve different purposes and should both remain.

---

## 6. Permissions, technical accuracy, and test evidence

- Preserve the split between the person making a change and the reviewer validating it. Request read-only roles first; do not give reviewers setup roles merely to simplify a test.
- Follow the existing PoC role model: time-bound Active assignments for the PoC window, with just-in-time activation for Global Administrator. Do not broaden privileges without a documented task-specific requirement.
- Keep each chapter's prerequisite page and permissions table consistent when requirements change.
- Distinguish agent identity blueprints, runtime agent identities, agent user accounts, and delegated user access. Do not treat their IDs, token subjects, grants, or policy targets as interchangeable.
- Prefer verified Microsoft Learn documentation. Validate new role requirements, portal paths, API versions, CLI syntax, licenses, and feature availability against authoritative sources. Do not invent URLs or results.
- Do not assume tenant readiness, permissions, licensing, feature availability, or test outcomes. State prerequisites explicitly and provide a verification step. If a required fact cannot be verified, identify the gap for review rather than presenting it as established.
- Label preview, optional, platform-specific, and tenant-dependent behavior. Document supported propagation or ingestion delays without inventing timing guarantees.
- Separate visibility, detection, blocking, and containment. A registry entry is not proof of enforcement; an alert is not proof that an action was blocked.
- For each test, identify the test object, actor, action, expected outcome, and evidence location. Add a comparison or negative case when needed to prove the control rather than merely show configuration.
- Evidence guidance should identify relevant timestamps, correlation identifiers, policy results, and log filters. Never claim a live test passed unless it was actually run.
- Troubleshooting should connect symptoms to specific checks or remedies.

---

## 7. Public content and samples

- Publish no credentials, access tokens, real tenant or customer identifiers, personal data, internal hostnames, or private authoring material.
- Exclude confidential information, internal-only programs or links, unpublished roadmaps, and customer-specific context. Every published instruction must be understandable using public documentation and the stated prerequisites.
- Use synthetic test content and clearly marked placeholders such as `<tenant-id>`, `<agent-identity-id>`, and `<your-handle>`. Keep blueprint and runtime identity placeholders distinct.
- Use reserved example domains such as `contoso.com` or `example.com` and documentation-only IP ranges when examples need network values.
- Keep screenshots sanitized. Document what evidence to collect, but do not commit real tenant evidence.
- Explain sample prerequisites, required permissions, configuration, invocation, and expected output. Reuse existing samples rather than duplicating them.
- Do not replace working samples, enable blocking policies, or change deployment defaults as a side effect of a formatting request.

---

## 8. Cross-links, validation, and local review

- When adding or re-scoping a chapter, update the root chapter index and affected chapter-local prerequisite pages.
- Keep prerequisite and next-step links consistent. Add reciprocal links where they help readers follow a real dependency; do not invent dependencies from chapter order.
- Preserve section numbers and anchors where possible. If a heading must change, update all affected inbound links.
- Treat Markdown as the editable source. Do not claim that the combined PDF reflects changes unless it has been regenerated and checked; report when it remains unchanged.
- Validate changed links, anchors, numbering, tables, code fences, diagram alignment, and referenced assets. Use existing checks if available; documentation-only edits do not require unrelated application builds.
- For changed executable samples, run the relevant existing build or tests where available. Distinguish local checks from tenant-dependent validation that was not performed.
- Keep changes local for review. Do not push to the public repository unless the user explicitly authorizes it.

Before handing off, confirm:

- [ ] The requested scope is complete without unrelated rewrites.
- [ ] Changed pages follow the applicable landing-page or chapter structure.
- [ ] Roles, prerequisites, setup checks, test outcomes, and evidence agree.
- [ ] Links and assets resolve, and existing navigation is preserved.
- [ ] No sensitive data or unsupported technical claims were introduced.
- [ ] Validation performed and any untested or stale artifacts are stated accurately.
- [ ] Nothing was pushed without explicit authorization.
