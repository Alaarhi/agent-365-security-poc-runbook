/**
 * Minimal Agent 365 SDK agent skeleton for the PoC.
 *
 * Shows the hosting-layer shape produced by `make-ai-teammate` from
 * microsoft/agent365-skills (Node.js variant). Replace the LLM call with your
 * actual model client. Run `a365 setup all` first to produce the Blueprint and
 * Entra Agent Identity so this agent is discoverable in Agent 365.
 */

import {
  CloudAdapter,
  ConfigurationBotFrameworkAuthentication,
} from "@microsoft/agents-hosting";
import express from "express";

const auth = new ConfigurationBotFrameworkAuthentication({
  // Values written by `a365 setup all` into .env / configuration
  MicrosoftAppId: process.env.AGENT_APP_ID!,
  MicrosoftAppTenantId: process.env.AGENT_TENANT_ID!,
  MicrosoftAppType: "SingleTenant",
});

const adapter = new CloudAdapter(auth);

async function handleTurn(context: any) {
  const prompt = context.activity.text ?? "";

  // 1. (Optional, strongly recommended) Purview DLP guard goes here.
  //    The guard calls Graph processContent and blocks sensitive prompts
  //    before the LLM. See purview-dlp-integration skill.

  // 2. Call your LLM.
  const reply = await callYourModel(prompt);

  // 3. (Optional) Purview output audit.

  await context.sendActivity(reply);
}

async function callYourModel(prompt: string): Promise<string> {
  // Replace with Azure OpenAI / Foundry / any model client.
  return `Echo: ${prompt}`;
}

const app = express();
app.use(express.json());

app.post("/api/messages", async (req, res) => {
  await adapter.process(req, res, (context) => handleTurn(context));
});

const port = Number(process.env.PORT ?? 3978);
app.listen(port, () => {
  console.log(`Agent listening on http://localhost:${port}/api/messages`);
});
