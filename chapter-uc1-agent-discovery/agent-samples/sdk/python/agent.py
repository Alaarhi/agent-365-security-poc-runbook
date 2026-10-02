"""Minimal Agent 365 SDK agent skeleton for the PoC.

Shows the hosting-layer shape produced by ``make-ai-teammate`` from
microsoft/agent365-skills (Python variant). Replace the LLM call with your
actual model client. Run ``a365 setup all`` first to produce the Blueprint
and Entra Agent Identity so this agent is discoverable in Agent 365.

Install:
    pip install microsoft-agents-hosting aiohttp python-dotenv
"""

import os
from aiohttp import web
from microsoft.agents.hosting import CloudAdapter, ConfigurationBotFrameworkAuthentication


auth = ConfigurationBotFrameworkAuthentication({
    # Values written by `a365 setup all`
    "MicrosoftAppId": os.environ["AGENT_APP_ID"],
    "MicrosoftAppTenantId": os.environ["AGENT_TENANT_ID"],
    "MicrosoftAppType": "SingleTenant",
})

adapter = CloudAdapter(auth)


async def handle_turn(context):
    prompt = context.activity.text or ""

    # 1. (Optional, strongly recommended) Purview DLP guard goes here.
    #    See purview-dlp-integration skill - the guard calls Graph
    #    processContent and blocks sensitive prompts before the LLM.

    # 2. Call your LLM.
    reply = await call_your_model(prompt)

    # 3. (Optional) Purview output audit.

    await context.send_activity(reply)


async def call_your_model(prompt: str) -> str:
    # Replace with Azure OpenAI / Foundry / any model client.
    return f"Echo: {prompt}"


async def messages(request: web.Request) -> web.Response:
    return await adapter.process(request, handle_turn)


app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3978))
    web.run_app(app, port=port)
