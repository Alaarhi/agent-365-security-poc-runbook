# Chapter 7 – Sensitive Data Protection (Purview)

**Pillar:** Secure
**What it proves:** Microsoft Purview and Microsoft 365 Copilot work together to protect sensitive data that an agent can access or generate: sensitivity labels and DLP stop Copilot from processing or emailing regulated content, two agents built on a labeled SharePoint knowledge source respect those controls, and Communication Compliance and Insider Risk Management supervise what agents do.

**Success criteria**
- A DLP policy scoped to Microsoft 365 Copilot and Copilot Chat restricts Copilot from processing content that carries the **Confidential** sensitivity label.
- A separate DLP policy scoped to Exchange email blocks delivery of email that contains credit card or ABA routing numbers.
- A Microsoft 365 Copilot agent and a Copilot Studio agent use the PoC SharePoint site as their knowledge source; an authorized user retrieves a harmless fact from an approved comparison source.
- A synthetic fact unique to a **Confidential**-labeled file is not returned by either agent in any intended channel, and the response and available policy evidence are recorded.
- Email that the Copilot Studio agent's email tool sends with approved synthetic payment data to a controlled recipient isn't delivered, while a benign control message is delivered.
- The Copilot Studio agent is approved and published to the store by an administrator, and an intended non-owner account can discover and install it.
- A Communication Compliance policy for AI agents is created and the authorized reviewer can access it and review test evidence.
- The **Default policy for agents** in Insider Risk Management is confirmed enabled, and its actual status and coverage are recorded.

## 7.1 Required permissions

Grant the read-only role first; give setup roles only to the person who makes each change, and assign them as Active for the PoC window.

| Task | Least-privilege role | Section |
|---|---|---|
| Create the DLP policy for Microsoft 365 Copilot and Copilot Chat | **Data Security AI Admins** (Purview role group) or **AI Administrator** (Microsoft Entra) | 7.2 |
| Create the DLP policy for Exchange email | **Information Protection Admins** (Purview role group) | 7.3 |
| Create the communication site, add and label the PoC files, share the site | PoC maker account allowed to create SharePoint sites (becomes the site owner), with the PoC sensitivity labels published to it | 7.4 |
| Build and share the Microsoft 365 Copilot knowledge agent | PoC maker account | 7.5 |
| Build and publish the Copilot Studio email agent | PoC maker account with permissions to create and access a Copilot Studio environment | 7.6.1–7.6.8 |
| Review, approve, and publish the agent to the store | **AI Administrator** (Microsoft Entra) | 7.6.9 |
| Create the Communication Compliance policy; review its configuration | **Communication Compliance Administrators** (Purview role group) | 7.7, 7.9.1 |
| Review Communication Compliance policy matches | **Communication Compliance Investigators** or **Communication Compliance Analysts** (Purview role groups), and named as reviewer in the policy | 7.7, 7.9.8 |
| Verify the Insider Risk Management agent policy | **Insider Risk Management Admins** (Purview role group) | 7.8, 7.9.1, 7.9.9 |
| Run the agent, email, availability, and permission tests | Test accounts without admin roles: an authorized test user, an intended non-owner account, and an unauthorized test user | 7.9.2–7.9.7 |
| Validation / read-only review of the DLP policies | **Global Reader** (Microsoft Entra) + **Information Protection Analysts** (Purview role group, view-only access to DLP policies and sensitivity labels) | 7.9.1 |

**Before you start:**
- Complete [Chapter 0 – Prerequisites and PoC preparation](../chapter-00-prerequisites/README.md). Use an approved PoC environment, synthetic data, and controlled test accounts throughout.
- Make sure a **Confidential** sensitivity label exists and is published to the PoC maker account and test users. If you plan to keep the Excel workbook in 7.4.4 as a comparison source, make sure a **General** label is published as well.
- Prepare the test accounts: an authorized test user, an intended non-owner account (it can be the authorized test user, as long as it didn't create the agents), an unauthorized test user who is outside the sharing scope you choose in 7.4.6 and 7.5.3, and one controlled email recipient.
- Review who has permission to enable blocking and organization-wide sharing before turning anything on.
- Build the sections in order: the two DLP policies (7.2, 7.3), the SharePoint site and files (7.4), the two agents (7.5, 7.6), then the supervision policies (7.7, 7.8), and finally the acceptance checklist (7.9).

## 7.2 DLP policy for Copilot content protection
**Documentation:** [Microsoft Purview DLP for Microsoft 365 Copilot and Cowork](https://learn.microsoft.com/purview/dlp-microsoft365-copilot-location-learn-about) · [Create and deploy a DLP policy](https://learn.microsoft.com/purview/dlp-create-deploy-policy)

Agents and Copilot can surface confidential content in a chat response unless sensitive data is explicitly protected at the point Copilot processes it. This section builds a Purview DLP policy aimed at the Copilot location itself – not at a file share or a mailbox – that stops Microsoft 365 Copilot and Copilot Chat from processing content carrying the **Confidential** sensitivity label. It controls what an AI surface is allowed to read and act on, not only where a document is allowed to live.

### 7.2.1 Create the DLP policy
Performed by **Data Security AI Admins**.
1. In Microsoft Purview (`https://purview.microsoft.com`), open **Solutions** > **Data Loss Prevention** > **Policies** and select **Create policy**.
2. Create a separate policy for this PoC rather than editing an existing one, so the Copilot restriction stays isolated and easy to remove afterward.
3. On the category screen, select **Enterprise applications and devices**.
4. Select **Custom** under **Categories** and **Custom** under **Regulations**, then select **Next**.
5. Name the policy `PoC - Copilot Confidential Content`, so it is clearly distinguished from the email policy in 7.3. Add a description so that anyone who picks up the tenant later understands its purpose. Select **Next**.

### 7.2.2 Scope the policy to Copilot
Performed by **Data Security AI Admins**.
1. On **Assign admin units**, keep **Full directory** – the **Microsoft 365 Copilot and Copilot Chat** location doesn't support admin units – then select **Next**.
2. On the locations screen, turn on only **Microsoft 365 Copilot and Copilot Chat**. Selecting this location disables all other locations for the policy, so the restriction applies only to what this PoC is meant to show.
3. Select **Next**.

### 7.2.3 Build the advanced rule
Performed by **Data Security AI Admins**.
1. On the policy-settings screen, select **Create or customize advanced DLP rules**, then **Create rule**.
2. Name the rule (the wizard labels this field as a policy name, but it names the rule inside the policy). Record the rule name.
3. Select **Add condition** > **Content contains** > **Sensitivity labels**, and add the **Confidential** label.
4. Check the condition in the live rule and make sure that only the intended label or sublabels are present.
5. Complete and save the rule before advancing in the wizard. Do not continue with an empty rules list.

### 7.2.4 Add the Copilot restriction action
Performed by **Data Security AI Admins**.
1. Under **Actions**, select **Add an action** > **Restrict Copilot from processing content**.
2. Within that action, select **Accessing knowledge sources**.
3. Treat this as the specific restriction this PoC configures. It does not automatically cover every Copilot operation or every agent channel; if the PoC needs a broader restriction, configure it explicitly.

### 7.2.5 Review, enable, and submit
Performed by **Data Security AI Admins**.
1. Save the rule, confirm it shows as enabled in the rules list, and select **Next**.
2. If an administrator-alert action is shown in the summary, review its recipients.
3. Select **Turn on policy immediately**. Use immediate enforcement only within an approved test scope.
4. Select **Next**, review the final summary, and select **Submit**.

**Check result**
- The policy name and status are recorded.
- The policy has one enabled rule with the **Confidential** label condition and the **Restrict Copilot from processing content** > **Accessing knowledge sources** action.
- Policy updates can take up to four hours to reach Microsoft 365 Copilot and Copilot Chat. The restriction is validated with controlled content-access tests in 7.9.3, not assumed from the configuration alone.

## 7.3 DLP policy for sensitive email content
**Documentation:** [Create and deploy a DLP policy](https://learn.microsoft.com/purview/dlp-create-deploy-policy) · [DLP policy reference](https://learn.microsoft.com/purview/dlp-policy-reference) · [Credit card number entity definition](https://learn.microsoft.com/purview/sit-defn-credit-card-number) · [ABA routing number entity definition](https://learn.microsoft.com/purview/sit-defn-aba-routing)

Separate from what Copilot can read, organizations need to stop regulated payment data from leaving the tenant by email. This section builds a second, independent DLP policy scoped to Exchange email. Where 7.2 stops Copilot from processing labeled content, this policy prevents delivery of email that contains matching sensitive information – it detects content by pattern (sensitive information types) rather than by label.

### 7.3.1 Create the email DLP policy
Performed by **Information Protection Admins**.
1. Return to **Data Loss Prevention** > **Policies** and select **Create policy**. Keep this configuration entirely separate from the Copilot policy so the two can be tested and removed independently.
2. Select **Enterprise applications and devices**, then **Custom** under both **Categories** and **Regulations**, and select **Next**.
3. Name the policy `PoC - Email Payment Data`. Select **Next**.

### 7.3.2 Scope the policy to Exchange email
Performed by **Information Protection Admins**.
1. On **Assign admin units**, retain the displayed settings after confirming that the scope matches your approved test environment, then select **Next**.
2. On the locations screen, deselect every other location and keep only **Exchange email** selected.
3. Review the included and excluded users and groups. A stray exclusion can make a PoC test message silently skip the policy.
4. Select **Next**.

### 7.3.3 Build the rule to detect payment data
Performed by **Information Protection Admins**.
1. On the policy-settings screen, select **Create or customize advanced DLP rules**, then **Create rule**.
2. Name the rule and record the name.
3. Select **Add condition** > **Content contains** > **Sensitive info types**.
4. Select **Credit Card Number** and **ABA Routing Number**, then select **Add**.
5. Record the AND/OR grouping, confidence level, and instance count that the rule uses for the two detectors. These settings determine how the detectors combine and are tested separately and together in 7.9.4.

### 7.3.4 Add the blocking action
Performed by **Information Protection Admins**.
1. Under **Actions**, select **Add an action** > **Restrict access or encrypt the content in Microsoft 365 locations**. Selecting this action does not by itself enable encryption; the next selection defines the restriction.
2. Select **Block users from receiving email, or accessing shared SharePoint, OneDrive, Teams files, and Power BI items**, then **Block everyone**. This blocks delivery regardless of whether the recipient is internal or external.
3. Get explicit approval for the **Block everyone** scope, and test only with controlled recipients.

### 7.3.5 Review, enable, and submit
Performed by **Information Protection Admins**.
1. Save the rule, verify its condition and blocking action, and confirm it is enabled.
2. Check that no unintended exception changes the test, then select **Next**.
3. Select **Turn on policy immediately**, then **Next**.
4. Review the final summary and select **Submit**.

**Check result**
- The policy name, location (**Exchange email** only), included and excluded users, detectors and their settings, action, and mode are recorded.
- The policy is validated in 7.9.4 with a benign control message and approved synthetic matching content before blocking is treated as proven. Test within a limited scope before any production rollout.

## 7.4 SharePoint communication site and PoC files
**Documentation:** [Manage site creation in SharePoint](https://learn.microsoft.com/sharepoint/manage-site-creation) · [Manage sensitivity labels in Office apps](https://learn.microsoft.com/purview/sensitivity-labels-office-apps) · [Enable sensitivity labels for Office files in SharePoint and OneDrive](https://learn.microsoft.com/purview/sensitivity-labels-sharepoint-onedrive-files)

Both agents need a realistic, properly labeled knowledge source to answer questions from and to trigger the DLP policies above. This section creates a communication site with synthetic invoice data in Word and Excel, labels it, and shares the site for the agents. Use synthetic PoC content only – nothing in this section should touch real invoices, payment details, or customer names.

### 7.4.1 Start a new communication site
Performed by the **PoC maker account**.
1. Open your approved SharePoint tenant's home page and confirm you are authorized to create a site there.
2. Select **Create site**, then **Communication site** (not **Team site**). A communication site is built to share information broadly rather than to collaborate privately.
3. Select **Standard communication site** as the template, then **Use template**.

### 7.4.2 Name and create the site
Performed by the **PoC maker account**.
1. On **Give your site a name**, enter a site name and address that follow your organization's naming standards, then select **Next**.
2. Record the resulting site URL. You paste it into both agents' knowledge sources in 7.5 and 7.6.
3. On **Set language and other options**, review the language and other displayed options, then select **Create site**.

**Check result**
- The new site and its **Documents** library open successfully.

### 7.4.3 Add the Word sample and label it
Performed by the **PoC maker account**.
1. In **Documents**, select **New** > **Word document**.
2. Paste synthetic invoice content into the document. Keep the `TEST – Not Real` wording so no one mistakes it for a live record. Use this entry for one company:

   ```text
   Contoso Ltd.
   Invoice ID: CT-INV-1001
   Amount Due: $12,450.00
   Payment Information (TEST – Not Real)
   Credit Card Number: 4111 1111 1111 1111
   ABA Routing Number: 021000021
   Bank Account Number: 000123456789
   ```

3. On the **Home** ribbon, select **Sensitivity** > **Confidential**. This aligns the document with the label condition of the Copilot DLP policy in 7.2.
4. Close the document, open the saved document again, and check that the applied label shows **Confidential**. Rely on the saved document, not on the instruction text.

**Check result**
- The saved Word document shows the **Confidential** label.

### 7.4.4 Add the Excel sample and resolve its label
Performed by the **PoC maker account**.
1. In **Documents**, select **New** > **Excel workbook**.
2. Add the columns `Company`, `InvoiceID`, `CreditCard`, `Routing`, `Account`, and `Amount`.
3. Format the **Routing** and **Account** columns as **Text** before entering values. With Excel's default **General** format, numeric routing and account numbers can lose a leading zero or be rewritten in scientific notation.
4. Populate one or two rows with synthetic values in the same shape as the Word sample, for example:

   | Company | InvoiceID | CreditCard | Routing | Account | Amount |
   |---|---|---|---|---|---|
   | Contoso Ltd. | CT-INV-1001 | 4111 1111 1111 1111 | 021000021 | 000123456789 | $12,450.00 |

5. Decide whether this workbook is a comparison source (labeled **General**) or another **Confidential**-labeled test source, and apply the label you chose. The knowledge baseline in 7.9.2 needs an approved comparison source on the site; if you label the workbook **Confidential**, add another approved **General**-labeled file with a harmless fact for that test.
6. Record the label the workbook carries and use that decision consistently in the tests in 7.9.

**Check result**
- The workbook shows the label you chose, and the **Routing** and **Account** values keep their leading zeros.

### 7.4.5 Verify the files and open Site access
Performed by the **PoC maker account**.
1. In the **Documents** library, confirm that the files appear with the labels you intended.
2. Optionally create a PDF copy of the Word document for later use. If you do, check its content and protection separately rather than assuming they match the Word source.
3. Select **Site access** to move to the sharing step.

### 7.4.6 Share the site
Performed by the **PoC maker account**.
1. In the sharing search box, type `Everyone` and select **Everyone except external users**. This grants broad internal access across the tenant, which keeps both agents' knowledge-source setup simple.
2. Review the permission level before confirming. Use a limited test group instead of tenant-wide sharing unless broad internal access has explicit approval.
3. Select **Share**.

**Check result**
- The site URL, the file names, each file's label, and the sharing scope and permission level are recorded.

## 7.5 Microsoft 365 Copilot knowledge agent
**Documentation:** [Build agents in Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/copilot-studio-agent-builder-build) · [Add knowledge sources to an agent in Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/agent-builder-add-knowledge) · [Share and manage agents built in Agent Builder](https://learn.microsoft.com/microsoft-365-copilot/extensibility/agent-builder-share-manage-agents)

This section shows how quickly a business user – not only IT – can build a knowledge agent in Microsoft 365 Copilot's agent builder, scoped to the SharePoint site from 7.4. It is a separate authoring path from the Copilot Studio agent in 7.6.

### 7.5.1 Create the agent and its details
Performed by the **PoC maker account**.
1. Open Microsoft 365 Copilot (`https://m365.cloud.microsoft`) and confirm you are signed in to the intended PoC tenant.
2. Select **New agent**, then open the **Configure** tab.
3. Enter a **Name**, **Description**, and **Instructions** for the agent.
4. Record the exact wording you use. The instructions are a deliberate decision for the PoC, not a setting to copy.

**Check result**
- The **Configure** tab shows the name, description, and instructions you recorded.

### 7.5.2 Add the SharePoint knowledge source
Performed by the **PoC maker account**.
1. Under **Knowledge**, paste the SharePoint site URL recorded in 7.4.2.
2. Turn on **Only use specified sources**. The agent then prioritizes the knowledge source shown in the **Knowledge** panel; this setting doesn't block the agent's general AI knowledge.
3. Treat this toggle as a scoping control, not as an access control: it controls what the agent searches, not who is allowed to see the results. Source citations and permissions are tested separately in 7.9.2, 7.9.3, and 7.9.7.

### 7.5.3 Share and publish the agent
Performed by the **PoC maker account**.
1. Select **Share** and verify the agent's name before changing access.
2. Select **Anyone in your organization** > **Apply**. Use a restricted pilot audience instead unless organization-wide sharing has explicit approval.
3. Select **Update** and confirm the success message.

**Check result**
- The agent name, instructions, knowledge source, **Only use specified sources** setting, and sharing audience are recorded.
- An account other than the one that created the agent can open and use it (tested in 7.9.6).

## 7.6 Copilot Studio email agent and publication
**Documentation:** [Add SharePoint as a knowledge source](https://learn.microsoft.com/microsoft-copilot-studio/knowledge-add-sharepoint) · [Add tools to custom agents](https://learn.microsoft.com/microsoft-copilot-studio/add-tools-custom-agent) · [Office 365 Outlook connector](https://learn.microsoft.com/connectors/office365/) · [Key concepts – Publish and deploy your agent](https://learn.microsoft.com/microsoft-copilot-studio/publication-fundamentals-publish-channels) · [Connect and configure an agent for Teams and Microsoft 365](https://learn.microsoft.com/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams) · [Manage agent requests in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-requests) · [Agent overview in Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/agent-365-overview)

A more capable, IT-governed agent needs an action – not just knowledge retrieval – and a controlled path to publication. This section builds a second agent in Copilot Studio with the same SharePoint knowledge source plus an Outlook email tool, then takes it through the full publish lifecycle: add a tool, connect an identity, publish, enable a channel, submit to the org catalog, and have an administrator approve and publish it to the store. Track this agent's configuration independently from the agent in 7.5.

### 7.6.1 Create a blank agent and set its details
Performed by the **PoC maker account**.
1. Open Copilot Studio (`https://copilotstudio.microsoft.com`), select **Agents**, and confirm the intended tenant and environment before making changes.
2. Select **Create blank agent**.
3. Select **Edit details** and enter a **Name** and **Description** that clearly distinguish this email-capable agent from the knowledge-only agent in 7.5.
4. Select **Edit instructions** and define the agent's behavior, including how it handles recipients and whether it confirms before sending. Record the instructions; the behavior is verified in 7.9.5 once the email tool is wired up.

### 7.6.2 Add the SharePoint knowledge source
Performed by the **PoC maker account**.
1. Select **Add knowledge source** > **SharePoint**.
2. Paste the SharePoint site URL recorded in 7.4.2 and select **Add**, then **Add to agent**.
3. Confirm the source appears without an error before moving on to the tool.

### 7.6.3 Add the Outlook email tool
Performed by the **PoC maker account**.
1. Select **Add tool** and choose the **Office 365 Outlook** connector.
2. Select the operation **Send an email (V2)**. Check the operation name carefully – Outlook exposes more than one similarly named email action.

### 7.6.4 Create the connection and configure the tool
Performed by the **PoC maker account**.
1. Under **Connect**, select **Create new connection**.
2. Decide which approved test identity authenticates the connection, then select **Create** in the Outlook connection dialog to start the authentication flow.
3. Select the approved account and review the requested permissions.
4. Select **Add and configure** to attach the operation.
5. On the tool's configuration page, review and record:
   - The **Authentication** setting: **End user** (the default – the tool uses the credentials of the user chatting with the agent) or **Maker-provided** (the tool uses the maker's credentials, so email is sent from the connection account).
   - The **Ask the end user before running** setting, which controls whether the agent asks for confirmation before sending.
   - How the recipient (**To**), **Subject**, and **Body** inputs are filled.

   Don't assume email is always sent as the person chatting with the agent; the sending identity is verified in 7.9.5.

**Check result**
- **Send an email (V2)** is listed on the agent's **Tools** page with the settings you recorded.

### 7.6.5 Publish the agent
Performed by the **PoC maker account**.
1. Select **Publish**.
2. Before continuing to channel configuration, run a controlled test of both knowledge retrieval and the email action, sending only to the controlled recipient.
3. When prompted, read the dialog's explanation, select **Force newest version**, and complete publication.

**Check result**
- Publication completes, and the controlled test returns an answer from the knowledge source and delivers a benign email to the controlled recipient.

### 7.6.6 Enable the Microsoft 365 Copilot and Teams channel
Performed by the **PoC maker account**.
1. Go to **Channels** for the published agent.
2. Under **Microsoft channels**, select **Microsoft 365 Copilot and Teams**.
3. Select the **Microsoft 365 Copilot** option and choose **Add channel**.
4. Confirm the channel is added successfully. Channel creation alone does not establish administrator approval or guarantee end-user access; both are checked later in this section and in 7.9.6.

**Check result**
- **Microsoft 365 Copilot and Teams** shows as added on the **Channels** page.

### 7.6.7 Make the agent available and submit for review
Performed by the **PoC maker account**.
1. Select **Availability options** > **Show to everyone in my org**. Obtain approval before making a test agent widely available in a real tenant.
2. Select **Submit to org catalog for review**.
3. Read the confirmation dialog text and select **Yes**.
4. Record the submission status. Submission and administrator approval are separate stages; approval is in 7.6.9.

**Check result**
- Copilot Studio shows the submission status for the agent, and the status is recorded.

### 7.6.8 Republish after the channel change
Performed by the **PoC maker account**.
1. Select **Publish** again so that the channel and availability changes take effect.
2. Select **Force newest version**, then **Publish**.
3. Confirm success and record the version or timestamp if one is shown.

### 7.6.9 Administrator review and publish to store
Performed by **AI Administrator**.
1. In the Microsoft 365 admin center (`https://admin.cloud.microsoft`), go to **Agents** > **All agents** > **Requests**.
2. Select the submitted agent. Confirm it is the agent that was actually reviewed and tested.
3. Select **Publish to store**.
4. Select **All users can install the agent**, then **Next**. Review installation eligibility separately from the document permissions and email-tool access configured earlier – they are independent controls.
5. At **Apply security template**, review the displayed settings and select **Next**. Record the actual template selection and obtain the security owner's sign-off on it.
6. Review the permissions screen and select **Next** only after that approval. Treat this as an actual consent review.
7. Review the final summary and select **Publish**.

**Check result**
- The submission status, the security template applied, and the security owner's sign-off are recorded.
- Discovery and installation are tested with an intended, non-owner account in 7.9.6, followed by separate source-access and email tests.

## 7.7 Communication Compliance policy
**Documentation:** [Configure a Communication Compliance policy to detect generative AI interactions](https://learn.microsoft.com/purview/communication-compliance-copilot) · [Create and manage Communication Compliance policies](https://learn.microsoft.com/purview/communication-compliance-policies) · [Get started with Communication Compliance](https://learn.microsoft.com/purview/communication-compliance-configure)

Once agents can send email and chat with users, someone needs to review what they actually say. A Communication Compliance policy does not block anything by itself – it supervises agent interactions and routes matches to a human reviewer, a complementary control to the DLP policies in 7.2 and 7.3.

### 7.7.1 Open Communication Compliance and start the policy
Performed by **Communication Compliance Administrators**.
1. In Microsoft Purview, select **Solutions** > **Communication Compliance**. Confirm the operator account has approved access to this workflow.
2. Under **Policies**, check for existing policies to avoid creating an unnecessary duplicate.
3. Select **Create policy**.

### 7.7.2 Choose the template and set sources and reviewer
Performed by **Communication Compliance Administrators**.
1. Select the template **Detect unethical interactions for AI agents**. Check that the template is available in your environment before continuing.
2. Under the agents to supervise, select **Copilot Studio** and **Azure AI Foundry**.
3. Add yourself or the approved reviewer as reviewer.
4. Select **Create policy**.

**Check result**
- The saved scope (Copilot Studio and Azure AI Foundry) and the authorized reviewer are recorded.
- Policy creation alone does not demonstrate event ingestion or review; that is checked in 7.9.8 once agent traffic exists.

## 7.8 Insider Risk Management verification
**Documentation:** [Monitoring agents with Insider Risk Management](https://learn.microsoft.com/purview/insider-risk-management-monitoring-agents) · [Create and manage Insider Risk Management policies](https://learn.microsoft.com/purview/insider-risk-management-policies)

Agent risk detection only works if the underlying policy is actually turned on – a step that is easy to assume rather than confirm. This section verifies an existing policy rather than configuring a new one.

### 7.8.1 Confirm the default agent policy is enabled
Performed by **Insider Risk Management Admins**.
1. In Microsoft Purview, select **Solutions** > **Insider Risk Management**.
2. Under **Policies**, switch to the **Agent policies** tab. Agent policies are listed separately from the standard user-risk policies, so check you are on the correct tab before searching.
3. Find **Default policy for agents** and open it or inspect its status.
4. Confirm it is enabled with the scope you expect. Seeing the policy name in the list does not prove it is enabled – open it and check.
5. If the policy is absent or inactive, escalate it and do not mark this configuration complete.

**Check result**
- The actual status and coverage of **Default policy for agents** are recorded.

## 7.9 Acceptance checklist (tests)

The sections above configure the PoC; they do not by themselves prove that it works. Run every check below before calling the environment validated, and record the result of each. Policy updates can take up to four hours to reach Microsoft 365 Copilot and Copilot Chat, so run 7.9.3 only after that time has passed since 7.2.5. Start a new conversation with the agent for each test prompt.

### 7.9.1 Policy configuration
Performed by the **read-only reviewer** for the DLP policies (7.2, 7.3), **Communication Compliance Administrators** for 7.7, and **Insider Risk Management Admins** for 7.8.
1. For each policy (7.2, 7.3, 7.7, 7.8), record its name, scope, mode, conditions, and exceptions.

**Expected result**
- Each recorded configuration matches what was set up in its section.

### 7.9.2 Knowledge baseline
Performed by an **authorized test user**.
1. In each agent (7.5 and 7.6), ask for a harmless fact from the approved comparison source (see 7.4.4).
2. Record the response and its citation.

**Expected result**
- The authorized user retrieves the harmless fact from both agents.

### 7.9.3 Label restriction
Performed by an **authorized test user**.
1. In each intended agent (7.5 and 7.6) and channel, ask for a synthetic fact that is unique to a **Confidential**-labeled file – for example, the bank account number for invoice `CT-INV-1001`.
2. Record the response and any available policy evidence for each agent and channel.

**Expected result**
- The fact from the **Confidential**-labeled file is not returned in the response. The file can still appear in the response's citations, but its content isn't used.

### 7.9.4 Email restriction
Performed by an **authorized test user** with the Copilot Studio agent from 7.6.
1. Ask the agent to send a benign control message to the controlled recipient.
2. Ask the agent to send approved synthetic matching messages to the controlled recipient, testing the detectors separately (only the credit card number from 7.4.3; only the ABA routing number) and together (both). Include the synthetic values in your request, because the agent can't use the content of the **Confidential**-labeled invoice.
3. Check the controlled recipient's mailbox and record, for each message, whether it was delivered.

**Expected result**
- The benign control message is delivered; messages with matching payment data are not delivered, according to the detector settings recorded in 7.3.3.

### 7.9.5 Tool identity
Performed by the **PoC maker account**.
1. Verify the actual sending account of the email tool, the recipient mapping, and the confirmation behavior, using the messages received in 7.9.4.
2. Compare them with the settings recorded in 7.6.4 and the instructions recorded in 7.6.1.

**Expected result**
- The sending account, recipient, and confirmation behavior match the recorded settings and instructions.

### 7.9.6 Agent availability
Performed by an **intended non-owner test account**.
1. Discover the Copilot Studio agent published in 7.6.9 and install it.
2. Open the agent built in 7.5 from the same account.

**Expected result**
- The non-owner account can discover, install, and use the agents.

### 7.9.7 Permissions
Performed by an **authorized test user** and an **unauthorized test user**.
1. As the authorized test user, confirm the intended access to the site, the files, and both agents.
2. As the unauthorized test user, try to open the site and both agents.

**Expected result**
- The authorized test user has the intended access; the unauthorized test user does not.

### 7.9.8 Compliance review
Performed by the **Communication Compliance reviewer**.
1. Open the Communication Compliance policy created in 7.7.
2. Review the approved test evidence generated by the agent tests above.

**Expected result**
- The reviewer can access the policy and review the test evidence.

### 7.9.9 Default policy
Performed by **Insider Risk Management Admins**.
1. Record the actual status and coverage of the **Default policy for agents** (7.8.1).

**Expected result**
- The policy is enabled, and its status and coverage are recorded.

## 7.10 Evidence
- Policy name, status, rule name, condition, action, and mode of `PoC - Copilot Confidential Content` (7.2).
- Policy name, location, included and excluded users, detector grouping, confidence level, instance count, action, and mode of `PoC - Email Payment Data` (7.3).
- Site URL, file names, the label of each file (including the decision for the Excel workbook), and the sharing scope and permission level (7.4).
- Agent names, descriptions, exact instructions, knowledge source, **Only use specified sources** setting, and sharing audience for the Microsoft 365 Copilot agent (7.5).
- For the Copilot Studio agent: email tool operation, connection identity, recipient, subject, body, authentication and confirmation settings, publish versions or timestamps, channel, availability option, submission status, security template applied, and the security owner's sign-off (7.6).
- Communication Compliance template, agents supervised, and reviewer (7.7).
- Status and coverage of **Default policy for agents** (7.8).
- The recorded result of every acceptance check in 7.9, including responses, delivery results, and available policy evidence.

## 7.11 Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| A PoC test email is delivered although it contains payment data | An included or excluded user or group setting makes the message skip the policy, or the detector grouping, confidence level, or instance count does not match the test content | Review the included and excluded users in 7.3.2 and the recorded detector settings in 7.3.3, then retest with controlled recipients. |
| Copilot still uses a file you expected to be restricted | The saved file carries a different label than intended, the rule's label condition contains other labels or sublabels, or the policy update hasn't reached Copilot yet | Reopen the saved file and check the applied label (7.4.3); check that only the intended label or sublabels are in the rule (7.2.3); allow up to four hours after 7.2.5 before retesting. |
| Restriction appears to work in one agent or channel but not another | The **Accessing knowledge sources** action does not automatically cover every Copilot operation or agent channel | Test each intended agent and channel (7.9.3) and configure any broader restriction explicitly. |
| Routing or account numbers look wrong in the workbook | Columns left in Excel's **General** format dropped a leading zero or switched to scientific notation | Format **Routing** and **Account** as **Text** before entering values (7.4.4). |
| Email tool sends as an unexpected account | The tool's **Authentication** is set to **Maker-provided**, so email is sent from the connection account instead of the user chatting with the agent | Check the **Authentication** setting recorded in 7.6.4 and verify the sending account in 7.9.5. |
| Several similarly named Outlook actions are listed | Outlook exposes more than one email action | Select **Send an email (V2)** (7.6.3). |
| Users can't find or install the Copilot Studio agent | Channel added but agent not yet approved and published to the store, or channel changes not republished | Complete 7.6.8 and 7.6.9, then test with a non-owner account (7.9.6). |
| Communication Compliance policy exists but shows nothing to review | Policy creation alone does not demonstrate ingestion; no agent traffic yet | Generate the agent tests in 7.9, then check again as the reviewer (7.9.8). |
| **Default policy for agents** appears in the list, but its status is unknown | The name in the list does not prove the policy is enabled | Open the policy and check its status; escalate if absent or inactive (7.8.1). |

## 7.12 Cleanup
Once the PoC is done, review the following with the change owner and remove what is no longer needed:
- Temporary sharing, for example **Everyone except external users** on the PoC site.
- Agent availability: org-wide sharing of the Microsoft 365 Copilot agent (7.5) and the store publication of the Copilot Studio agent (7.6.9).
- The two PoC agents themselves (7.5, 7.6).
- The Outlook connection created for the email tool (7.6.4).
- The policies `PoC - Copilot Confidential Content`, `PoC - Email Payment Data`, and the Communication Compliance policy (7.7).
- The synthetic Word, Excel, and optional PDF files, and the PoC communication site (7.4).

---
Previous: [Chapter 6 – Conditional Access and Least Privilege](../chapter-06-conditional-access/README.md) · Next: [Chapter 8 – Threat Detection and Runtime Protection (Defender)](../chapter-08-threat-detection/README.md)
