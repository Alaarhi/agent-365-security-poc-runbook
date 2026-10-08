/**
 * Minimal custom engine agent for the Agent 365 PoC (Node.js / TypeScript).
 *
 * Built on the Microsoft 365 Agents SDK hosting layer, following the
 * "Create and test a basic agent" quickstart:
 * https://learn.microsoft.com/microsoft-365/agents-sdk/quickstart?pivots=nodejs
 *
 * This file is the agent code only. It doesn't register the agent with
 * Agent 365. Registration (agent identity blueprint, agent identity,
 * permissions) is done with the Agent 365 CLI (`a365 setup all`) or the
 * Agent 365 Skills (`a365-setup` > `make-a365-agent`). See ../README.md.
 *
 * Install:
 *   npm install @microsoft/agents-hosting @microsoft/agents-hosting-express
 *
 * Compile with tsc (or use a TypeScript runner), run it locally in anonymous
 * mode (no credentials), and test it with Microsoft 365 Agents Playground.
 */

import { AgentApplication, MemoryStorage, TurnContext, TurnState } from "@microsoft/agents-hosting";
import { startServer } from "@microsoft/agents-hosting-express";

class PocAgent extends AgentApplication<TurnState> {
  constructor(storage: MemoryStorage) {
    super({ storage });
    this.onActivity("message", this.handleMessage);
  }

  private handleMessage = async (context: TurnContext, _state: TurnState): Promise<void> => {
    const prompt = context.activity.text ?? "";

    // Optional: Purview DLP guard before the model call.
    // The `purview-dlp-integration` skill adds a guard that calls the
    // Microsoft Graph processContent API and stops the turn when an
    // input-blocking DLP policy matches. See Chapter 2, section 2.11.2.

    const reply = await callYourModel(prompt);

    await context.sendActivity(reply);
  };
}

async function callYourModel(prompt: string): Promise<string> {
  // Replace with your model client (Azure OpenAI, Microsoft Foundry, or other).
  return `Echo: ${prompt}`;
}

// Listens on port 3978 by default; messaging endpoint is /api/messages.
startServer(new PocAgent(new MemoryStorage()));
